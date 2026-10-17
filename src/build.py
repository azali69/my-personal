"""Builds index.html (the whole app in one file) from src/app.html.

Usage, from anywhere:  python3 src/build.py
Fills the %%...%% placeholders in app.html with: the Qur'an data (src/data.json), the fonts (src/fonts/),
the cover art (src/art/), the manuals (manual/), the MUIS timetable and Hijri dates (prayer/) and the
recitation timing corrections (tools/timing-corrections.json). Writes index.html at the repository root.
After building: bump the cache name in sw.js, then commit; pushing index.html builds the APK."""
import base64, json, os, re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repository root
S = os.path.join(R, 'src')
rd = lambda *p: open(os.path.join(*p), encoding='utf-8').read()
b64 = lambda *p: base64.b64encode(open(os.path.join(*p), 'rb').read()).decode()
js = lambda s: s.replace('</', '<\\/')                              # safe inside a <script> block

t = rd(S, 'app.html')
rep = {
    'FAVICON': b64(S, 'art', 'fav96.png'),
    'HIJRI': rd(R, 'prayer', 'hijri.json'),
    'MANUAL_EN': js(json.dumps(rd(R, 'manual', 'en.md'))),
    'MANUAL_MS': js(json.dumps(rd(R, 'manual', 'ms.md'))),
    'MUIS': rd(R, 'prayer', 'muis.json'),
    'TFIX': rd(R, 'tools', 'timing-corrections.json'),
    'FONT': b64(S, 'fonts', 'kfgqpc.otf'),                     # KFGQPC Uthmanic Script HAFS 0.09 (ayah markers)
    'FONT2': b64(S, 'fonts', 'kfgqpc-hafs-2021.woff2'),         # KFGQPC HAFS Uthmanic Script 1.001 (text)
    'FONT3': b64(S, 'fonts', 'qcf-surah-header.woff2'),         # QCF surah header frames
    'FONT4': b64(S, 'fonts', 'great-vibes.woff2'),              # cover name (OFL)
    'DATA': js(rd(S, 'data.json')),                             # made by src/quran-data/build_data.py
}
t = re.sub(r'%%ART:([\w.-]+)%%', lambda m: b64(S, 'art', 'cover', m.group(1)), t)
# one pass, so text inside an inserted file is never treated as a placeholder
t = re.sub(r'%%([A-Z0-9_]+)%%', lambda m: rep[m.group(1)], t)
left = re.findall(r'%%[A-Z0-9_:.a-z-]+%%', t)
assert not left, f'unfilled placeholders: {left}'
open(os.path.join(R, 'index.html'), 'w', encoding='utf-8').write(t)
print(f'index.html {len(t)/1e6:.2f} MB')
