"""Builds solat/jumuah.json (Solat Jumaat) from tools/jumuah.py, adding the kitab number of each hadith (from kutub/)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jumuah as S
from kitab_index import where, with_kitab, write
W = where()
out = [dict(e, h=with_kitab(e.get('h', []), W), d=[dict(x, h=with_kitab(x.get('h', []), W)) for x in e.get('d', [])]) for e in S.E]
write('solat/jumuah.json', {'v': 1, 'built': '2026-10-17', 'who': S.WHO, 'com': S.COMMENTATORS, 'steps': out})
print(len(out), 'steps')
