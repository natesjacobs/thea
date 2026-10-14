"""Build Earth frames: 0.25 deg land/ocean x frozen/temperate/hot maps.

Geography: Cao et al. 2024 plate model (0-1800 Ma), coastlines via pyGPlates.
Climate: earth.csv. Each row holds until the next older-to-younger row.
  ice_n, ice_s: frozen poleward of this |latitude| (90 = no ice, 0 = snowball).
  hot: very hot (mean annual > ~30 C) equatorward of this |latitude| (0 = none).
Frames: every 5 Myr to 1000 Ma, every 25 Myr to 1800 Ma. Indexed PNG, named by Ma.
Pixel values: 0 ocean, 1 sea ice, 2 hot ocean, 3 land, 4 ice, 5 hot land.

Run: pip install pygplates plate-model-manager pillow numpy
     python build.py out/   (then zip out/ and attach to a GitHub release)
"""
import csv, os, sys
import numpy as np
import pygplates
from PIL import Image, ImageDraw
from plate_model_manager import PlateModelManager

S = 4  # pixels per degree
HERE = os.path.dirname(os.path.abspath(__file__))
PALETTE = [40, 70, 120,  200, 225, 240,  70, 120, 150,
           150, 160, 110,  250, 250, 250,  200, 120, 60]

def climate_rows():
    with open(os.path.join(HERE, 'earth.csv')) as f:
        rows = [r for r in csv.DictReader(f)]
    return sorted(rows, key=lambda r: -float(r['time_Ma']))

def climate_at(rows, t):
    cur = None
    for r in rows:
        if float(r['time_Ma']) >= t:
            cur = r
    return cur

def main(out):
    os.makedirs(out, exist_ok=True)
    m = PlateModelManager().get_model('cao2024', data_dir=os.path.join(out, '.model'))
    rot = pygplates.RotationModel(m.get_rotation_model())
    coast = pygplates.FeatureCollection()
    for f in m.get_layer('Coastlines'):
        coast.add(pygplates.FeatureCollection(f))
    wrap = pygplates.DateLineWrapper()
    rows = climate_rows()
    lat = 90 - (np.arange(180 * S) + 0.5) / S
    alat = np.abs(lat)[:, None]
    north = (lat > 0)[:, None]
    times = list(range(0, 1000, 5)) + list(range(1000, 1801, 25))
    for t in times:
        recon = []
        pygplates.reconstruct(coast, rot, recon, float(t))
        img = Image.new('L', (360 * S, 180 * S), 0)
        d = ImageDraw.Draw(img)
        for r in recon:
            g = r.get_reconstructed_geometry()
            if not isinstance(g, pygplates.PolygonOnSphere):
                continue
            for p in wrap.wrap(g):
                pts = [((q.get_longitude() + 180) * S, (90 - q.get_latitude()) * S)
                       for q in p.get_exterior_points()]
                if len(pts) > 2:
                    d.polygon(pts, fill=1)
        land = np.array(img, dtype=np.uint8)
        c = climate_at(rows, t)
        ice = np.where(north, alat >= float(c['ice_n']), alat >= float(c['ice_s']))
        hot = alat < float(c['hot'])
        zone = np.where(ice, 1, np.where(hot, 2, 0))
        zone = np.broadcast_to(zone, land.shape)
        px = Image.fromarray((land * 3 + zone).astype(np.uint8), 'P')
        px.putpalette(PALETTE)
        px.save(os.path.join(out, f'{t:04d}.png'), optimize=True)
        print(t, c['state'])

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'out')
