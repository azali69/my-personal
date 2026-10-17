How `src/data.json` (the Qur'an text, pages, translations, ruku' and mushaf layout built into the app) was made, 3–4 Oct 2026. Kept as a record; the inputs are not in this repository.

- `build_map.py`: word map between the KFGQPC Uthmani and imla'i text → `wordmap.json`
- `build_layout.py`: 15-line page layout from the `quran-qcf4` npm package → `layout.json`
- `build_glyph2.py`: KFGQPC V4 page-font glyph codes from the QUL exports (`qul-data` branch) → `glyph.json`
- `build_data.py`: joins KFGQPC Hafs v2.0, Basmeih (QuranEnc malay_basumayyah), Saheeh International (QuranEnc english_saheeh), Tanzil ruku' and the files above → `data.json`, and checks every ayah against the official KFGQPC text
- `crosscheck.py`, `verify_kfgqpc.py`: compare the KFGQPC text with Tanzil's Uthmani text (no letter differences)

The scripts were run from the folder holding the inputs and still have the paths used then.
