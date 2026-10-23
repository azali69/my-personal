# My Personal Qur'an

Version numbers: v&lt;major&gt;.&lt;minor&gt;.&lt;patch&gt;.&lt;build&gt; (e.g. v1.0.0.65). major.minor.patch is in `VERSION`; build is the APK build number.

A personal Madinah Mushaf reader and hafazan (memorisation) checker.

Open it at **https://azali69.github.io/my-personal/** in Chrome. On Android, use Chrome's menu → *Add to Home screen* to install it.

## Features

- 604-page Madinah Mushaf: the app's own text layout, or the printed KFGQPC pages (plain or tajweed colours)
- Translation in Bahasa Melayu or English, transliteration, word-by-word meaning and sound, tafsir
- Recitation by several reciters, word highlighting as it plays
- Hafazan: hidden text that appears as you recite, with wrong, skipped and unclear words marked, and a session history
- Search in Arabic (harakat ignored), Malay or English; ayat with similar wording; Kamus Al-Quran by root
- Hadith: the six books, Muwatta Malik and the Shama'il of at-Tirmidhi, with scholars' gradings, the same hadith in the other books, HadeethEnc explanations, and the hadith that quote each ayah
- Sirah timeline, Sifat Solat Nabi, Solat Jumaat with the latest MUIS khutbah, Hisnul Muslim (Doa & zikir)
- Scan & check: is a text an ayah or a hadith in the app's books, and its grading
- Singapore prayer times (MUIS) with azan alerts, Hijri dates, qibla, mosques and musollahs
- Bookmarks, notes and last-read places in every book; sync between devices through one file in Google Drive
- Works offline once each part has been opened

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
| Hadith books | Sahih al-Bukhari, Sahih Muslim, Sunan Abi Dawud, Jami' at-Tirmidhi, Sunan an-Nasa'i, Sunan Ibn Majah, Muwatta Malik: Arabic, English and Indonesian from [fawazahmed0/hadith-api](https://github.com/fawazahmed0/hadith-api) (public domain); gradings of al-Albani, Shu'ayb al-Arna'ut, Zubair 'Ali Za'i and at-Tirmidhi's own verdict. Built by `tools/build_kutub.py` into `kutub/` |
| Shama'il of at-Tirmidhi | Sunnah.com (Arabic, English, Zubair 'Ali Za'i's gradings) and al-Albani's *Mukhtasar ash-Shama'il* (his gradings). `tools/build_shamail.py` |
| Hadith explanations | [HadeethEnc.com](https://hadeethenc.com), shown unchanged and credited. `tools/build_hadeethenc.py` |
| Same hadith in other books; hadith that quote an ayah | Computed from the Arabic of the app's books (`tools/build_hadith_links.py`, `tools/build_ayah_hadith.py`); an aid for finding, not a takhrij |
| Sirah, Sifat Solat, Solat Jumaat | Written for this app from hadith in the app's books and named classical works (volume and page given where checked); weak and unproven reports are marked as such. `tools/sirah_events.py`, `tools/sifat_solat.py`, `tools/jumuah.py` |
| Kamus Al-Quran | Roots, lemmas and parts of speech: Quranic Arabic Corpus morphology v0.4 (Kais Dukes, University of Leeds, GNU GPL) as corrected in [mustafa0x/quran-morphology](https://github.com/mustafa0x/quran-morphology); meanings from Quran.com word by word. `tools/build_kamus.py` |
| Friday khutbah | MUIS, [muis.gov.sg](https://www.muis.gov.sg/resources/khutbah-and-religious-advice/khutbah/): title, date and links only, checked every Thursday and Friday by `tools/fetch_khutbah.py` |
| Hijri dates | MABIMS 2021 criteria, as used by MUIS; checked against Singapore's dates 2023-2026. `tools/hijri_mabims.py` |
| Mosques and musollahs | MUIS Mosque Directory, OneMap (Singapore Land Authority), OpenStreetMap (ODbL), Wikipedia. `tools/build_places.py` |
| Adhan sound | The user's own audio file (no freely licensed Makkah or Madinah recording found); built-in tones generated for this app |
| Word-judging logic | Adapted from [Tilawi quran-asr](https://github.com/Tilawi/quran-asr), MIT licence, © 2025-2026 Muhammed Durakovic |

The Qur'an text and translations are reproduced without modification. The app checks its own copy against the verified build (Settings → Sources & verification).

## Limits

- Voice checking uses the browser's speech recognition. In Chrome this is Google's online service, so it needs internet and sends audio to Google.
- It checks words only. It does not judge tajwid, makhraj, or where you stop and start.
- Speech recognition can mishear. Check flagged words against the text.

## Repository

- `src/app.html`: the app's code. `python3 src/build.py <build>` fills in the data, fonts, art and manuals and writes `index.html` (the whole app in one file) and names the offline cache in `sw.js` after the version.
- `index.html`: what GitHub Pages serves and what the APK carries. Pushing a change to it (or to `android/`) builds the APK (`.github/workflows/android.yml`) and publishes it as a release.
- `android/`: the Android app around `index.html` (speech, prayer alerts, scanning, sync).
- Data the app downloads when first used: `kutub/`, `hadith/`, `tafsir/`, `wbw/`, `translit/`, `dua/`, `sirah/`, `solat/`, `kamus/`, `quran/`, `khutbah/`, `mosque/`, `prayer/`.
- `tools/`: the scripts that made each data folder (named in the Sources table). `src/quran-data/`: how the Qur'an data in `src/data.json` was made.
- `tests/`: `smoke.py` (every Home tile opens), `features.py` (main flows), `data_cache.py` (downloads, offline use and updates). They need Playwright.
