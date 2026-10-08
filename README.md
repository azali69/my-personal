# My Personal Quran v1.0

A personal Madinah Mushaf reader and hafazan (memorisation) checker.

Open it at **https://azali69.github.io/my-personal/** in Chrome. On Android, use Chrome's menu → *Add to Home screen* to install it.

## Features

- 604-page Madinah Mushaf layout with waqf signs
- Translation on or off, in Bahasa Melayu or English
- Search in Arabic (harakat ignored), Malay or English, or jump by reference (18:10, p296)
- Six background colours and adjustable Arabic size
- Waqaf and ibtida' blocks: ruku' (ع) sections, or your own blocks
- Hafazan: hidden text that appears as you recite, with wrong, skipped and unclear words marked, and a session history
- Works offline after the first visit

## Sources

| Content | Source |
|---|---|
| Qur'an text, waqf signs, pages, juz | King Fahd Glorious Qur'an Printing Complex (KFGQPC), Uthmanic Hafs data v2.0 (Hafs 'an 'Asim) |
| Cross-check of the text | Tanzil Project Uthmani text: no letter differences across 6,236 ayat |
| Ruku' sections | Tanzil metadata, cross-checked against a second compilation (556 of 556 match) |
| Bahasa Melayu | Abdullah Muhammad Basmeih, via [QuranEnc.com](https://quranenc.com/en/browse/malay_basumayyah) (malay_basumayyah v1.0.0) |
| English | Saheeh International, via [QuranEnc.com](https://quranenc.com/en/browse/english_saheeh) (english_saheeh v1.1.2) |
| Arabic fonts | KFGQPC HAFS Uthmanic Script 1.001 (2021) for the text; KFGQPC Uthmanic Script HAFS 0.09 for ayah markers. © King Fahd Glorious Qur'an Printing Complex, included unmodified |
| Surah header frames | KFGQPC surah header font (QCF_SurahHeader, v1.000, Sept 2025), via [QUL / Tarteel](https://qul.tarteel.ai/resources/font/458). © King Fahd Complex, included unmodified |
| Printed pages | KFGQPC V4 (1441H) page fonts, plain and tajweed, via [QUL / Tarteel](https://qul.tarteel.ai), downloaded when a page is first opened |
| Recitation audio (ayah by ayah) | Mishary Rashid Alafasy, Maher al-Muaiqly, Yasser ad-Dussary, streamed from [EveryAyah.com](https://everyayah.com/recitations_ayat.html) (128 kbps) |
| Word timings (karaoke) | Alafasy, as-Sudais, Yasser ad-Dussary: Quran.com (api.qurancdn.com), corrected per surah where they ran ahead of the voice; measured with `tools/drift_check.py`, results in `tools/timing-corrections.json` |
| Recitation audio (as-Sudais, Maher whole surah) | Quran.com / QuranicAudio; MP3Quran.net (Maher al-Muaiqly, all 114 surahs) |
| Recitation audio (whole surahs) | Hazza al-Balushi, streamed from [MP3Quran.net](https://www.mp3quran.net/eng/hazza): 91 of 114 surahs are published |
| Transliteration | Quran.com ayah transliteration (resource 57, the Tanzil-style scheme), shown only under the Arabic. Fetched by `tools/fetch_translit.py` into `translit/` |
| Tafsir | Al-Mukhtasar fi Tafsir al-Qur'an (Tafsir Center for Quranic Studies), English, Indonesian and Arabic; Tafsir As-Sa'di (Taysir al-Karim ar-Rahman), Indonesian and Arabic. All from [QuranEnc.com](https://quranenc.com), shown without changes (QuranEnc gives no version number for these, so `tafsir/index.json` records the retrieval date and a hash). Refreshed monthly by `tools/fetch_tafsir.py`. As-Sa'di is not in QuranEnc's API, so it is read from their pages, with only the HTML markup removed |
| Word-judging logic | Adapted from [Tilawi quran-asr](https://github.com/Tilawi/quran-asr), MIT licence, © 2025-2026 Muhammed Durakovic |

The Qur'an text and translations are reproduced without modification. The app checks its own copy against the verified build (Settings → Sources & verification).

## Limits

- Voice checking uses the browser's speech recognition. In Chrome this is Google's online service, so it needs internet and sends audio to Google.
- It checks words only. It does not judge tajwid, makhraj, or where you stop and start.
- Speech recognition can mishear. Check flagged words against the text.
