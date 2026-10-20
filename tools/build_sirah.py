"""Builds sirah/sirah.json from tools/sirah_events.py, adding the kitab number of each hadith (from kutub/)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sirah_events as S
from kitab_index import where, with_kitab, write
W = where()
out = [dict(e, h=with_kitab(e.get('h', []), W)) for e in S.E]
write('sirah/sirah.json', {'v': 1, 'built': '2026-10-15', 'events': out, 'family': S.FAMILY, 'familyNote': S.FAMILY_NOTE})
print(len(out), 'events')
