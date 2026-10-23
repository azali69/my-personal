"""Sahih Muslim standard numbers (23 Oct 2026 audit).

fawazahmed0/hadith-api numbers Sahih Muslim 1..7563 in its own order, but Muslim is cited by Muhammad Fu'ad 'Abd al-Baqi's
number, with a, b, c for further chains as sunnah.com writes it (the Jibril hadith is Muslim 8a; in the source list it is 93).
This maps each entry of the app's list to that number, from the source's arabicnumber field (8.01 -> "8a").
Usage: python3 build_muslim_std.py <ara-muslim.min.json from fawazahmed0/hadith-api> <kutub dir>
"""
import glob, json, sys
H = json.load(open(sys.argv[1]))['hadiths']
ours = {h[0] for f in glob.glob(sys.argv[2] + '/muslim/[0-9]*.json') for h in json.load(open(f))['h']}
def conv(a):
    a = str(a)
    if '.' in a:
        i, d = a.split('.'); return i + chr(96 + int(d))
    return a
m = {str(h['hadithnumber']): conv(h['arabicnumber']) for h in H if h.get('arabicnumber') not in (None, '') and h['hadithnumber'] in ours}
json.dump({'about': "Sahih Muslim: the standard number (Muhammad Fu'ad 'Abd al-Baqi's numbering, with a, b, c for further chains, as on sunnah.com) for each entry of this app's list, from the arabicnumber field of fawazahmed0/hadith-api ara-muslim. Entries without one are left out.", 'n': m},
          open(sys.argv[2] + '/muslim/std.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(m), 'of', len(ours))
