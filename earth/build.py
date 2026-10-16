"""Build earth.nc: one best-guess map of Earth every 5 Myr (0-1000 Ma), 25 Myr (1000-1800 Ma).

Grid 0.25 deg. Per frame: land, elevation, annual/coldest/warmest-month surface temperature, class.
  0-540 Ma: Scotese & Wright 2018 PaleoDEMs (land, elevation). Temperature is the equal-weight
            mean of three climate models, each interpolated in time between its runs:
            CESM (Li 2022, 10 Myr), FOAM (Pohl 2022, 20 Myr), HadCM3L (Valdes 2021, by stage).
            CESM and FOAM are lapse-rate corrected to PaleoDEM elevation.
  >540 Ma:  Cao et al. 2024 plate model (land only). Climate unknown except Snowball
            intervals in sources/climate-notes.csv, which are fully frozen.
Class: 0 ocean, 1 frozen ocean, 2 hot ocean, 3 land, 4 frozen land, 5 hot land,
       6 ocean (climate unknown), 7 land (climate unknown).
  Frozen = warmest month < 10 C (Koppen polar). Very hot = annual mean >= 30 C.
Sources: sources/sources.md. Run: python build.py  (downloads ~2 GB into work/)
"""
import csv, functools, glob, os, re, sys, urllib.request, zipfile
import numpy as np, xarray as xr, netCDF4, pygplates
from PIL import Image, ImageDraw
from scipy.interpolate import RegularGridInterpolator
from plate_model_manager import PlateModelManager

HERE = os.path.dirname(os.path.abspath(__file__))
CESM_URL = 'https://ndownloader.figshare.com/files/35396138'
DEM_URL = 'https://earthbyte.org/webdav/ftp/Data_Collections/Scotese_Wright_2018_PaleoDEM/paleoDEM_0.2Deg_grids.zip'
FOAM_URL = 'https://zenodo.org/records/7220854/files/{a}ebP2_solCgough1981_EccN_pCO2FosterKr_atmos_slab.nc?download=1'
HAD_URL = 'https://zenodo.org/records/8237751/files/scotese_02_tas.zip?download=1'
S = 4
LAT = 90 - (np.arange(180 * S) + 0.5) / S
LON = -180 + (np.arange(360 * S) + 0.5) / S
GLAT, GLON = np.meshgrid(LAT, LON, indexing='ij')
PALETTE = [40, 70, 120, 200, 225, 240, 70, 120, 150, 150, 160, 110, 250, 250, 250, 200, 120, 60,
           90, 95, 105, 165, 165, 160]
LAPSE = 0.0065  # K/m, standard atmosphere

def fetch(url, path):
    if not os.path.exists(path):
        print('downloading', url)
        urllib.request.urlretrieve(url, path)
    return path

def regrid(lat, lon, z, method='linear'):
    """Regrid a global field (lon in 0..360 or -180..180) onto the 0.25 deg grid."""
    lon = np.asarray(lon) % 360
    lon, u = np.unique(lon, return_index=True); z = z[:, u]
    lon = np.concatenate([lon[-1:] - 360, lon, lon[:1] + 360])
    z = np.concatenate([z[:, -1:], z, z[:, :1]], axis=1)
    f = RegularGridInterpolator((lat, lon), z, method=method, bounds_error=False, fill_value=None)
    return f((GLAT, GLON % 360))

def snowball(t):
    with open(os.path.join(HERE, 'sources', 'climate-notes.csv')) as f:
        return any(r['state'] == 'Snowball' and float(r['end_Ma']) <= t <= float(r['start_Ma'])
                   for r in csv.DictReader(f))

def main(work):
    os.makedirs(work, exist_ok=True)
    cesm = xr.open_dataset(fetch(CESM_URL, os.path.join(work, 'cesm.nc')))
    cesm_age = np.array([540 - 10 * i for i in range(54)] + [0])  # last run is preindustrial
    zp = fetch(DEM_URL, os.path.join(work, 'dem.zip'))
    with zipfile.ZipFile(zp) as z:
        z.extractall(os.path.join(work, 'dem'))
    dems = {float(re.search(r'_([\d.]+)Ma', f).group(1)): f
            for f in glob.glob(os.path.join(work, 'dem', 'paleoDEM_0.2Deg_grids', '*.nc'))}
    m = PlateModelManager().get_model('cao2024', data_dir=os.path.join(work, 'model'))
    rot = pygplates.RotationModel(m.get_rotation_model())
    coast = pygplates.FeatureCollection()
    for f in m.get_layer('Coastlines'):
        coast.add(pygplates.FeatureCollection(f))
    wrap = pygplates.DateLineWrapper()

    # Each model: ages, and load(i) -> monthly surface temperature (12, lat, lon) in K,
    # plus model surface height in m (None if not available) on its own grid.
    def cesm_load(i):
        return cesm.lat.values, cesm.lon.values, cesm.T.isel(simulation=i).values + 273.15, \
            np.maximum(cesm.PHIS.isel(simulation=i).values / 9.81, 0)
    foam_dir = os.path.join(work, 'foam'); os.makedirs(foam_dir, exist_ok=True)
    foam_age = np.arange(0, 541, 20)
    def foam_load(i):
        a = foam_age[i]
        f = xr.open_dataset(fetch(FOAM_URL.format(a=a), os.path.join(
            foam_dir, f'{a}ebP2_solCgough1981_EccN_pCO2FosterKr_atmos_slab.nc')), decode_times=False)
        return f.lat.values, f.lon.values, f.TS1.values, np.maximum(f.PHIS.values.mean(0) / 9.81, 0)
    hz = fetch(HAD_URL, os.path.join(work, 'scotese_02_tas.zip'))
    if not glob.glob(os.path.join(work, 'hadcm3l', '*.nc')):
        with zipfile.ZipFile(hz) as z:
            z.extractall(os.path.join(work, 'hadcm3l'))
    had = {}
    for f in glob.glob(os.path.join(work, 'hadcm3l', '**', '*_tas.nc'), recursive=True):
        had.setdefault(float(re.search(r'_([\d.]+)Ma_', f).group(1)), []).append(f)
    had_age = np.array(sorted(had))
    def had_load(i):
        T = np.mean([xr.open_dataset(f, decode_times=False).temp_mm_1_5m.values[:, 0]
                     for f in had[had_age[i]]], axis=0)
        lat = xr.open_dataset(had[had_age[i]][0], decode_times=False).latitude.values
        o = np.argsort(lat)
        lon = xr.open_dataset(had[had_age[i]][0], decode_times=False).longitude.values
        return lat[o], lon, T[:, o], None
    models = [(cesm_age, cesm_load), (foam_age, foam_load), (had_age, had_load)]

    def fields(age, load):
        @functools.lru_cache(maxsize=3)
        def slice_(i):
            lat, lon, T, z = load(i)
            T = T - 273.15
            return [regrid(lat, lon, x) for x in (T.mean(0), T.min(0), T.max(0))] + \
                   [None if z is None else regrid(lat, lon, z)]
        def at(t, elev):
            i = np.argsort(np.abs(age - t))[:2]
            a0, a1 = age[i]
            w = 1.0 if a0 == a1 else abs(t - a1) / abs(a1 - a0)
            out = 0
            for j, ww in ((i[0], w), (i[1], 1 - w)):
                tm, tc, tw, z = slice_(j)
                corr = 0 if z is None else LAPSE * (np.maximum(elev, 0) - z)
                out = out + ww * np.stack([tm - corr, tc - corr, tw - corr])
            return out
        return at
    climate = [fields(a, l) for a, l in models]

    def cao_land(t):
        recon = []
        pygplates.reconstruct(coast, rot, recon, float(t))
        img = Image.new('L', (360 * S, 180 * S), 0)
        d = ImageDraw.Draw(img)
        for r in recon:
            g = r.get_reconstructed_geometry()
            if isinstance(g, pygplates.PolygonOnSphere):
                for p in wrap.wrap(g):
                    pts = [((q.get_longitude() + 180) * S, (90 - q.get_latitude()) * S)
                           for q in p.get_exterior_points()]
                    if len(pts) > 2:
                        d.polygon(pts, fill=1)
        return np.array(img, dtype=bool)

    times = list(range(0, 1000, 5)) + list(range(1000, 1801, 25))
    nc = netCDF4.Dataset(os.path.join(work, 'earth.nc'), 'w')
    nc.title = 'Thea Earth frames'
    nc.createDimension('time', len(times)); nc.createDimension('lat', len(LAT)); nc.createDimension('lon', len(LON))
    v = nc.createVariable('time', 'f4', ('time',)); v.units = 'Ma'; v[:] = times
    nc.createVariable('lat', 'f4', ('lat',))[:] = LAT
    nc.createVariable('lon', 'f4', ('lon',))[:] = LON
    kw = dict(zlib=True, complevel=6, chunksizes=(1, len(LAT), len(LON)))
    V = {'class': nc.createVariable('class', 'u1', ('time', 'lat', 'lon'), **kw)}
    for name, units in (('elev', 'm'), ('t_mean', 'degC'), ('t_cold', 'degC'), ('t_warm', 'degC')):
        V[name] = nc.createVariable(name, 'i2', ('time', 'lat', 'lon'), fill_value=-32768, **kw)
        V[name].units = units
        if name != 'elev':
            V[name].scale_factor = 0.1
    nc.createVariable('source', str, ('time',))
    os.makedirs(os.path.join(work, 'png'), exist_ok=True)

    for k, t in enumerate(times):
        if t <= 540:
            age = min(dems, key=lambda a: abs(a - t))
            dz = xr.open_dataset(dems[age])
            elev = regrid(dz.lat.values, dz.lon.values, dz.z.values)
            land = elev > 0
            tm, tc, tw = np.mean([c(t, elev) for c in climate], axis=0)
            zone = np.where(tw < 10, 1, np.where(tm >= 30, 2, 0))
            V['elev'][k] = np.round(elev)
            V['t_mean'][k], V['t_cold'][k], V['t_warm'][k] = tm, tc, tw
            nc['source'][k] = 'Scotese PaleoDEM; CESM + FOAM + HadCM3L'
        else:
            land = cao_land(t)
            if snowball(t):
                zone = 1
                nc['source'][k] = 'Cao 2024; Snowball Earth'
            else:
                zone = None
                nc['source'][k] = 'Cao 2024; climate unknown'
        cls = (land * 3 + zone if zone is not None else 6 + land).astype(np.uint8)
        V['class'][k] = cls
        im = Image.fromarray(cls, 'P'); im.putpalette(PALETTE)
        im.save(os.path.join(work, 'png', f'{t:04d}.png'), optimize=True)
        print(t, nc['source'][k])
    nc.close()

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'work'))
