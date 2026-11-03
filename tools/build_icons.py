"""Icone de Tonus : un chrono (anneau presque plein = 10 minutes) autour d'un haltere, sur fond corail.

Ecrit icons/icon.svg (source, aussi favicon) puis rend les PNG avec Chrome headless et PIL :
icon-192.png, icon-512.png et icon-maskable-512.png (fond plein bord a bord, dessin reduit a 80 %
pour rester dans la zone sure des icones adaptatives Android).
Usage : python tools/build_icons.py   (depuis le dossier tonus)
"""
import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
ICONS = Path(__file__).resolve().parent.parent / 'icons'


def svg(maskable):
    bg = '<rect width="512" height="512" fill="url(#bg)"/>' if maskable else '<rect width="512" height="512" rx="112" fill="url(#bg)"/>'
    scale = ' transform="translate(256 256) scale(.8) translate(-256 -256)"' if maskable else ''
    r = 160
    circ = 2 * math.pi * r
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a45"/><stop offset="1" stop-color="#e2336b"/></linearGradient>
  </defs>
  {bg}
  <g{scale}>
    <circle cx="256" cy="256" r="{r}" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="30"/>
    <circle cx="256" cy="256" r="{r}" fill="none" stroke="#fff" stroke-width="30" stroke-linecap="round"
      stroke-dasharray="{circ * 300 / 360:.1f} {circ:.1f}" transform="rotate(-90 256 256)"/>
    <g fill="#fff" transform="rotate(-30 256 256)">
      <rect x="168" y="245" width="176" height="22" rx="11"/>
      <rect x="196" y="196" width="32" height="120" rx="13"/>
      <rect x="284" y="196" width="32" height="120" rx="13"/>
      <rect x="168" y="218" width="24" height="76" rx="10"/>
      <rect x="320" y="218" width="24" height="76" rx="10"/>
    </g>
  </g>
</svg>
'''


def render(svg_text, out, sizes):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / 'i.svg').write_text(svg_text, encoding='utf-8')
        (tmp / 'i.html').write_text('<html><body style="margin:0;background:transparent">'
                                    '<img src="i.svg" style="display:block;width:1024px;height:1024px"></body></html>', encoding='utf-8')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--default-background-color=00000000',
                        '--window-size=1024,1024', f'--screenshot={tmp / "big.png"}', (tmp / 'i.html').as_uri()],
                       check=True, capture_output=True, timeout=60)
        big = Image.open(tmp / 'big.png').convert('RGBA')
        for size, name in sizes:
            big.resize((size, size), Image.LANCZOS).save(out / name, optimize=True)
            print(name, size)


if __name__ == '__main__':
    (ICONS / 'icon.svg').write_text(svg(False), encoding='utf-8')
    render(svg(False), ICONS, [(192, 'icon-192.png'), (512, 'icon-512.png')])
    render(svg(True), ICONS, [(512, 'icon-maskable-512.png')])
