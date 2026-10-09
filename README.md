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
| Word-by-word meanings | Quran.com word-by-word translation (English, Indonesian), unchanged; fetched by `tools/fetch_wbw.py` into `wbw/`. Word sound: cut from the chosen reciter's recording using Quran.com word timings, or Quran.com's single-word audio (audio.qurancdn.com) |
| Hadith on an ayah | Sahih al-Bukhari, Book 65 (Kitab at-Tafsir): ayah taken from al-Bukhari's chapter heading (Sunnah.com reference) and checked against the Qur'an words quoted in the Arabic heading. Sahih Muslim, Book 56: the ayah quoted in the narration. Arabic and English from Sunnah.com (Bukhari via [freococo/sunnah_dataset](https://huggingface.co/datasets/freococo/sunnah_dataset), CC BY-NC-SA 4.0; Muslim via [fawazahmed0/hadith-api](https://github.com/fawazahmed0/hadith-api)); Indonesian from tafsirq.com via fawazahmed0/hadith-api (translator not named). Built by `tools/build_hadith.py`; unconfirmed links are listed in `hadith/review.txt` |
| Prayer times (Singapore) | MUIS, Muslim Prayer Timetable, [data.gov.sg](https://data.gov.sg/collections/2312/view) (Open Data Licence); fetched monthly by `tools/fetch_dua_prayer.py` into `prayer/muis.json` and built into the app |
| Prayer times (elsewhere) | Calculated: Fajr 20°, Isha 18°, Shafi'i Asr, Zohor +1 min, rounded up; fitted to and checked against MUIS 2026 (within 1 minute on 99% of days in Singapore) |
| Qibla | Great-circle bearing to the Ka'bah (21.4225° N, 39.8262° E); phone rotation sensor corrected to true north with Android's magnetic declination |
| Hisnul Muslim | Sa'id ibn Wahf al-Qahtani, *Hisn al-Muslim*: Arabic, English, transliteration, repeat counts and Arabic audio from [hisnmuslim.com](https://www.hisnmuslim.com) (chapter 126 not served by the source) |
| Adhan sound | The user's own audio file (no freely licensed Makkah or Madinah recording found); built-in tone generated for this app |
| Word-judging logic | Adapted from [Tilawi quran-asr](https://github.com/Tilawi/quran-asr), MIT licence, © 2025-2026 Muhammed Durakovic |

The Qur'an text and translations are reproduced without modification. The app checks its own copy against the verified build (Settings → Sources & verification).

## Limits

- Voice checking uses the browser's speech recognition. In Chrome this is Google's online service, so it needs internet and sends audio to Google.
- It checks words only. It does not judge tajwid, makhraj, or where you stop and start.
- Speech recognition can mishear. Check flagged words against the text.
