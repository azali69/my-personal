# -*- coding: utf-8 -*-
"""Sifat Solat Nabi ﷺ: the Prophet's prayer, step by step, for My Personal Quran (Azli, 15 Oct 2026).
Written for this app. Every step cites hadith in the seven books in the app (the app shows each one's grading);
where scholars differ, the positions are given side by side with their evidence, without choosing between them.
Positions of the schools: al-Nawawi, al-Majmu' Sharh al-Muhadhdhab and Minhaj at-Talibin (Shafi'i, with his reports of
the other schools); Ibn Qudamah, al-Mughni (Hanbali, with the others); Ibn Rushd, Bidayat al-Mujtahid (comparative).
Al-Albani: Sifat Salat an-Nabi ﷺ (his conclusions). Hadith numbers are this app's numbering.
h entries: [book, number, note-or-None]; positions: who = shafii | hanafi | maliki | hanbali | albani | majority."""

E = [
 dict(id='asas', t=dict(en="The basis: pray as you saw him pray", ms="Asasnya: solatlah seperti kamu melihat Baginda solat"),
  s=dict(en="The Prophet ﷺ said: \"Pray as you have seen me praying\" (Bukhari 631). When a man prayed badly, he taught him the pillars: takbir, recite, bow until at rest, stand up straight, prostrate until at rest, sit until at rest, prostrate again, and do this in the whole prayer (the hadith of 'the man who prayed badly', Bukhari 757, Muslim 885). Being at rest (tuma'ninah) in each position is part of the prayer itself.",
         ms="Nabi ﷺ bersabda: \"Solatlah kamu sebagaimana kamu melihat aku solat\" (Bukhari 631). Apabila seorang lelaki solat dengan tidak sempurna, Baginda mengajarnya rukun-rukunnya: takbir, membaca, rukuk hingga tenang, bangun hingga lurus, sujud hingga tenang, duduk hingga tenang, sujud lagi, dan lakukan begitu dalam seluruh solat (hadis 'orang yang buruk solatnya', Bukhari 757, Muslim 885). Tenang (tuma'ninah) dalam setiap rukun ialah sebahagian daripada solat itu sendiri."),
  h=[['bukhari',631,None],['bukhari',757,None],['muslim',885,None],['abudawud',855,dict(en="The back must be at rest in bowing and prostration",ms="Belakang mesti tenang ketika rukuk dan sujud")]]),

 dict(id='niat', t=dict(en="Intention (niyyah)", ms="Niat"),
  s=dict(en="Every prayer needs an intention: which prayer you are praying. All scholars agree the intention is in the heart.",
         ms="Setiap solat memerlukan niat: solat apa yang sedang dilakukan. Semua ulama sepakat niat itu di dalam hati."),
  h=[['bukhari',1,dict(en="Actions are only by intentions",ms="Setiap amalan hanya dengan niat")]],
  d=[dict(topic=dict(en="Saying the intention aloud (e.g. 'usolli')", ms="Melafazkan niat (cth. 'usolli')"),
     p=[dict(w='shafii',en="Later Shafi'i scholars consider saying it with the tongue recommended, to help the heart; the intention itself stays in the heart.",ms="Ulama Syafi'i terkemudian menganggap melafazkannya sunat, untuk membantu hati; niat itu sendiri tetap di dalam hati."),
        dict(w='albani',en="Not reported from the Prophet ﷺ or the Companions; he held that it should not be done (also the view of Ibn Taymiyyah).",ms="Tidak diriwayatkan daripada Nabi ﷺ atau para Sahabat; beliau berpendapat ia tidak patut dilakukan (juga pendapat Ibn Taimiyyah)."),
        dict(w='ibnbaz',en="Not prescribed: saying it aloud is an innovation; the intention is in the heart.",ms="Tidak disyariatkan: melafazkannya adalah bid'ah; niat di dalam hati."),
        dict(w='uthaymin',en="Not prescribed; the intention is in the heart.",ms="Tidak disyariatkan; niat di dalam hati.")],
     note=dict(en="No hadith reports the Prophet ﷺ saying an intention for prayer aloud; the difference is whether doing so is a helpful practice.",ms="Tiada hadis yang meriwayatkan Nabi ﷺ melafazkan niat solat; perbezaannya ialah sama ada melakukannya amalan yang membantu."))]),

 dict(id='takbir', t=dict(en="Opening takbir and raising the hands", ms="Takbiratul ihram dan mengangkat tangan"),
  s=dict(en="He began the prayer with \"Allahu akbar\", raising his hands to the level of his shoulders, and in other reports to his ears.",
         ms="Baginda memulakan solat dengan \"Allahu akbar\" sambil mengangkat kedua tangan setentang bahu, dan dalam riwayat lain setentang telinga."),
  h=[['bukhari',735,dict(en="To the shoulders",ms="Setentang bahu")],['muslim',865,dict(en="Opposite the ears (Malik ibn al-Huwayrith)",ms="Setentang telinga (Malik bin al-Huwairith)")],['muslim',1110,dict(en="'Aishah: he began with the takbir",ms="'Aisyah: Baginda memulakan dengan takbir")]]),

 dict(id='qiyam', t=dict(en="Placing the right hand on the left", ms="Meletakkan tangan kanan di atas tangan kiri (bersedekap)"),
  s=dict(en="People were told to place the right hand on the left forearm in the prayer (Bukhari 740). Wa'il ibn Hujr saw him place his right hand on his left (Muslim 896). Where the hands are placed is where scholars differ.",
         ms="Orang ramai diperintah meletakkan tangan kanan di atas lengan kiri dalam solat (Bukhari 740). Wa'il bin Hujr melihat Baginda meletakkan tangan kanan di atas tangan kiri (Muslim 896). Di mana tangan diletakkan, di situlah ulama berbeza."),
  h=[['bukhari',740,None],['muslim',896,None],['abudawud',755,dict(en="He moved Ibn Mas'ud's right hand onto his left",ms="Baginda memindahkan tangan kanan Ibn Mas'ud ke atas tangan kirinya")]],
  d=[dict(topic=dict(en="Where the hands are placed",ms="Di mana tangan diletakkan"),
     p=[dict(w='shafii',en="Below the chest, above the navel.",ms="Di bawah dada, di atas pusat."),
        dict(w='hanafi',en="Below the navel (for men).",ms="Di bawah pusat (bagi lelaki)."),
        dict(w='hanbali',en="Below the navel, in the best-known report from Ahmad; he also allowed above it.",ms="Di bawah pusat, menurut riwayat yang masyhur daripada Ahmad; beliau juga membenarkan di atasnya."),
        dict(w='maliki',en="The best-known view in the school is to let the hands hang down in obligatory prayers; others in the school hold them as the majority do.",ms="Pendapat masyhur mazhab ialah melepaskan tangan di sisi dalam solat fardu; sebahagian ulama mazhab bersedekap seperti jumhur."),
        dict(w='albani',en="On the chest.",ms="Di atas dada."),
        dict(w='ibnbaz',en="On the chest.",ms="Di atas dada."),
        dict(w='uthaymin',en="On the chest.",ms="Di atas dada.")],
     h=[['abudawud',756,dict(en="'Ali: below the navel",ms="'Ali: di bawah pusat")],['abudawud',758,dict(en="Abu Hurairah: below the navel",ms="Abu Hurairah: di bawah pusat")],['abudawud',759,dict(en="Tawus (a Successor, mursal): on the chest",ms="Tawus (Tabi'in, mursal): di atas dada")]],
     note=dict(en="The reports naming a place are all disputed: see the gradings on each. 'On the chest' from Wa'il ibn Hujr is in Sahih Ibn Khuzaymah, and from Hulb at-Ta'i in Musnad Ahmad (not in this app's books).",ms="Riwayat yang menyebut tempatnya semuanya dipertikaikan: lihat penilaian setiap satu. 'Di atas dada' daripada Wa'il bin Hujr ada dalam Sahih Ibn Khuzaimah, dan daripada Hulb at-Ta'i dalam Musnad Ahmad (bukan dalam kitab aplikasi ini)."))]),

 dict(id='iftitah', dua=[[16,dict(en="Hisn al-Muslim: opening supplications",ms="Hisn al-Muslim: doa iftitah")]], t=dict(en="Opening supplication (du'a al-istiftah)", ms="Doa iftitah"),
  s=dict(en="He said a short supplication silently before reciting. Several wordings are authentic: 'Allahumma ba'id bayni wa bayna khatayaya…' (Bukhari 744), 'Wajjahtu wajhiya…' (Muslim, in the night prayer), and 'Subhanakallahumma wa bihamdika…' (Abu Dawud 776, and 'Umar said it aloud to teach it, Muslim 892).",
         ms="Baginda membaca doa pendek secara perlahan sebelum membaca Al-Fatihah. Beberapa lafaz adalah sahih: 'Allahumma ba'id baini wa baina khatayaya…' (Bukhari 744), 'Wajjahtu wajhiya…' (Muslim, dalam solat malam), dan 'Subhanakallahumma wa bihamdika…' (Abu Dawud 776, dan 'Umar menyaringkannya untuk mengajar, Muslim 892)."),
  h=[['bukhari',744,None],['muslim',1812,None],['abudawud',776,None],['muslim',892,None]],
  d=[dict(topic=dict(en="Which wording is preferred",ms="Lafaz mana yang diutamakan"),
     p=[dict(w='shafii',en="'Wajjahtu wajhiya…'.",ms="'Wajjahtu wajhiya…'."),
        dict(w='hanafi',en="'Subhanakallahumma…'.",ms="'Subhanakallahumma…'."),
        dict(w='hanbali',en="'Subhanakallahumma…'.",ms="'Subhanakallahumma…'."),
        dict(w='maliki',en="No opening supplication in obligatory prayers, in the best-known view.",ms="Tiada doa iftitah dalam solat fardu, menurut pendapat masyhur."),
        dict(w='albani',en="Any of the authentic wordings, varying between them.",ms="Mana-mana lafaz yang sahih, berselang-seli."),
        dict(w='uthaymin',en="Any of the authentic wordings, varying between them.",ms="Mana-mana lafaz yang sahih, berselang-seli.")])]),

 dict(id='basmalah', t=dict(en="Seeking refuge and the basmalah", ms="Ta'awwuz dan basmalah"),
  s=dict(en="He sought refuge in Allah before reciting (Abu Dawud 775). Anas said the Prophet ﷺ, Abu Bakr and 'Umar began the recitation with 'Al-hamdu lillahi Rabbil-'alamin' (Bukhari 743); in Muslim's wording they did not mention (aloud) 'Bismillah…' (Muslim 892). Whether it is said aloud is where scholars differ.",
         ms="Baginda memohon perlindungan Allah sebelum membaca (Abu Dawud 775). Anas berkata Nabi ﷺ, Abu Bakar dan 'Umar memulakan bacaan dengan 'Al-hamdu lillahi Rabbil-'alamin' (Bukhari 743); dalam lafaz Muslim mereka tidak menyebut (dengan kuat) 'Bismillah…' (Muslim 892). Sama ada ia dibaca kuat, di situlah ulama berbeza."),
  h=[['abudawud',775,None],['bukhari',743,None],['muslim',892,None]],
  d=[dict(topic=dict(en="Basmalah aloud in loud prayers",ms="Basmalah dibaca kuat dalam solat jahar"),
     p=[dict(w='shafii',en="It is a verse of al-Fatihah and is said aloud where the recitation is aloud.",ms="Ia satu ayat daripada Al-Fatihah dan dibaca kuat apabila bacaan dikuatkan."),
        dict(w='hanafi',en="Said quietly.",ms="Dibaca perlahan."),
        dict(w='hanbali',en="Said quietly.",ms="Dibaca perlahan."),
        dict(w='maliki',en="Not said in obligatory prayers, in the best-known view.",ms="Tidak dibaca dalam solat fardu, menurut pendapat masyhur."),
        dict(w='albani',en="Said quietly, as a rule.",ms="Dibaca perlahan, pada kebiasaannya."),
        dict(w='ibnbaz',en="Said quietly; saying it aloud sometimes is allowed.",ms="Dibaca perlahan; kadang-kadang menguatkannya dibolehkan."),
        dict(w='uthaymin',en="Said quietly.",ms="Dibaca perlahan.")],
     h=[['nasai',905,dict(en="Nu'aym al-Mujmir: Abu Hurairah recited it (aloud) and said his prayer was most like the Prophet's",ms="Nu'aim al-Mujmir: Abu Hurairah membacanya (kuat) dan berkata solatnya paling menyerupai solat Nabi")]])]),

 dict(id='fatihah', t=dict(en="Al-Fatihah and amin", ms="Al-Fatihah dan amin"),
  s=dict(en="\"There is no prayer for whoever does not recite al-Fatihah\" (Bukhari 756, Muslim 874). After it the imam and those behind him say 'Amin'; \"whoever's amin coincides with the angels' amin, his past sins are forgiven\" (Bukhari 780).",
         ms="\"Tiada solat bagi sesiapa yang tidak membaca Al-Fatihah\" (Bukhari 756, Muslim 874). Selepasnya imam dan makmum menyebut 'Amin'; \"sesiapa yang aminnya bersamaan dengan amin malaikat, diampunkan dosanya yang lalu\" (Bukhari 780)."),
  h=[['bukhari',756,None],['muslim',874,None],['bukhari',780,None],['muslim',915,None]],
  d=[dict(topic=dict(en="Al-Fatihah behind the imam",ms="Membaca Al-Fatihah di belakang imam"),
     p=[dict(w='shafii',en="Obligatory for everyone, including behind the imam in loud prayers.",ms="Wajib bagi setiap orang, termasuk makmum dalam solat jahar."),
        dict(w='hanafi',en="The follower does not recite; the imam's recitation counts for him.",ms="Makmum tidak membaca; bacaan imam memadai baginya."),
        dict(w='maliki',en="The follower recites in quiet prayers and listens in loud ones.",ms="Makmum membaca dalam solat sirr dan mendengar dalam solat jahar."),
        dict(w='hanbali',en="The follower recites in quiet prayers and listens in loud ones.",ms="Makmum membaca dalam solat sirr dan mendengar dalam solat jahar."),
        dict(w='albani',en="The follower listens in loud prayers and recites in quiet ones.",ms="Makmum mendengar dalam solat jahar dan membaca dalam solat sirr."),
        dict(w='ibnbaz',en="Obligatory for the follower too, in loud prayers as well (in the imam's pauses or quietly while he recites).",ms="Wajib juga bagi makmum, termasuk dalam solat jahar (ketika imam berhenti atau perlahan semasa imam membaca).",src='https://binbaz.org.sa/fatwas/12708'),
        dict(w='uthaymin',en="Obligatory for the follower too, in loud prayers as well.",ms="Wajib juga bagi makmum, termasuk dalam solat jahar.")],
     h=[['tirmidhi',312,dict(en="'Has any of you recited with me?' (after a loud prayer)",ms="'Adakah sesiapa antara kamu membaca bersamaku?' (selepas solat jahar)")],['tirmidhi',247,None]]),
     dict(topic=dict(en="Saying amin aloud",ms="Menyaringkan amin"),
     p=[dict(w='shafii',en="Aloud in loud prayers, by the imam and those behind him.",ms="Dikuatkan dalam solat jahar, oleh imam dan makmum."),
        dict(w='hanbali',en="Aloud in loud prayers.",ms="Dikuatkan dalam solat jahar."),
        dict(w='hanafi',en="Quietly.",ms="Perlahan."),
        dict(w='maliki',en="Quietly; the imam does not say it in loud prayers in the best-known view.",ms="Perlahan; imam tidak menyebutnya dalam solat jahar menurut pendapat masyhur."),
        dict(w='albani',en="Aloud, by the imam and those behind him.",ms="Dikuatkan, oleh imam dan makmum."),
        dict(w='ibnbaz',en="Aloud, by the imam and those behind him.",ms="Dikuatkan, oleh imam dan makmum."),
        dict(w='uthaymin',en="Aloud.",ms="Dikuatkan.")])]),

 dict(id='ruku', dua=[[17,dict(en="Hisn al-Muslim: what to say in ruku'",ms="Hisn al-Muslim: bacaan ketika rukuk")]], t=dict(en="Bowing (ruku')", ms="Rukuk"),
  s=dict(en="He said the takbir and bowed, with his back level, head neither raised nor lowered (Muslim 1110, Bukhari 828). In bowing he said 'Subhana Rabbiyal-'Azim' (Muslim 1814) and also 'Subhanakallahumma Rabbana wa bihamdika, Allahummaghfir li' (Muslim 1085).",
         ms="Baginda bertakbir dan rukuk dengan belakang rata, kepala tidak diangkat dan tidak direndahkan (Muslim 1110, Bukhari 828). Dalam rukuk Baginda membaca 'Subhana Rabbiyal-'Azim' (Muslim 1814) dan juga 'Subhanakallahumma Rabbana wa bihamdika, Allahummaghfir li' (Muslim 1085)."),
  h=[['muslim',868,dict(en="Takbir at every movement",ms="Takbir pada setiap perpindahan")],['muslim',1110,None],['bukhari',828,None],['muslim',1814,None],['muslim',1085,None]],
  d=[dict(topic=dict(en="Raising the hands when bowing, rising from it, and standing up after the first tashahhud",ms="Mengangkat tangan ketika rukuk, bangkit daripadanya, dan bangun selepas tasyahhud awal"),
     p=[dict(w='shafii',en="Recommended when bowing and rising; al-Nawawi held it is also recommended when standing up after the first tashahhud, following Bukhari 739.",ms="Sunat ketika rukuk dan bangkit; al-Nawawi berpendapat ia juga sunat ketika bangun selepas tasyahhud awal, berdasarkan Bukhari 739."),
        dict(w='hanbali',en="Recommended when bowing and rising from it.",ms="Sunat ketika rukuk dan bangkit daripadanya."),
        dict(w='hanafi',en="Only at the opening takbir.",ms="Hanya pada takbiratul ihram."),
        dict(w='maliki',en="Only at the opening takbir, in the best-known view.",ms="Hanya pada takbiratul ihram, menurut pendapat masyhur."),
        dict(w='albani',en="At all three, and sometimes when prostrating (Nasa'i 1085).",ms="Pada ketiga-tiganya, dan kadang-kadang ketika sujud (Nasa'i 1085)."),
        dict(w='ibnbaz',en="At the opening, bowing, rising, and standing from the first tashahhud.",ms="Pada takbiratul ihram, rukuk, bangkit, dan bangun daripada tasyahhud awal."),
        dict(w='uthaymin',en="At the opening, bowing, rising, and standing from the first tashahhud.",ms="Pada takbiratul ihram, rukuk, bangkit, dan bangun daripada tasyahhud awal.")],
     h=[['bukhari',735,None],['bukhari',739,None],['nasai',1085,None]])]),

 dict(id='itidal', t=dict(en="Rising from bowing (i'tidal)", ms="I'tidal"),
  s=dict(en="He rose saying 'Sami'allahu liman hamidah', then 'Rabbana wa lakal-hamd', standing straight until every bone returned to its place (Bukhari 734, Bukhari 828).",
         ms="Baginda bangkit sambil membaca 'Sami'allahu liman hamidah', kemudian 'Rabbana wa lakal-hamd', berdiri lurus hingga setiap tulang kembali ke tempatnya (Bukhari 734, Bukhari 828)."),
  h=[['bukhari',734,None],['bukhari',828,None]],
  d=[dict(topic=dict(en="The hands after rising from bowing",ms="Tangan selepas bangkit daripada rukuk"),
     p=[dict(w='shafii',en="Let them hang at the sides.",ms="Dilepaskan di sisi."),
        dict(w='hanbali',en="Either is allowed; some Hanbali scholars place the right on the left again.",ms="Kedua-duanya dibolehkan; sebahagian ulama Hanbali bersedekap semula."),
        dict(w='albani',en="Placing them again is not reported and should not be done.",ms="Bersedekap semula tidak diriwayatkan dan tidak patut dilakukan."),
        dict(w='ibnbaz',en="Place the right on the left again: that is the sunnah.",ms="Bersedekap semula: itulah sunnahnya.",src='https://binbaz.org.sa/fatwas/5128'),
        dict(w='uthaymin',en="Place the right on the left again.",ms="Bersedekap semula.")],
     note=dict(en="No hadith speaks of this directly; both sides argue from the general wording of the hadith on placing the hands.",ms="Tiada hadis yang menyebutnya secara langsung; kedua-dua pihak berhujah dengan lafaz umum hadis meletakkan tangan."))]),

 dict(id='sujud', t=dict(en="Prostration (sujud)", ms="Sujud"),
  s=dict(en="He prostrated on seven bones: the forehead with the nose, the two hands, the two knees and the ends of the two feet (Bukhari 812), keeping his arms away from his sides. In prostration he said 'Subhana Rabbiyal-A'la' (Muslim 1814).",
         ms="Baginda sujud di atas tujuh anggota: dahi bersama hidung, dua tapak tangan, dua lutut dan hujung dua kaki (Bukhari 812), dengan lengan direnggangkan dari rusuk. Dalam sujud Baginda membaca 'Subhana Rabbiyal-A'la' (Muslim 1814)."),
  h=[['bukhari',812,None],['muslim',1814,None],['muslim',1085,None]],
  d=[dict(topic=dict(en="Knees first or hands first when going down",ms="Lutut dahulu atau tangan dahulu ketika turun sujud"),
     p=[dict(w='shafii',en="Knees first.",ms="Lutut dahulu."),
        dict(w='hanafi',en="Knees first.",ms="Lutut dahulu."),
        dict(w='hanbali',en="Knees first, in the best-known report.",ms="Lutut dahulu, menurut riwayat yang masyhur."),
        dict(w='maliki',en="Hands first.",ms="Tangan dahulu."),
        dict(w='albani',en="Hands first.",ms="Tangan dahulu."),
        dict(w='ibnbaz',en="Knees first.",ms="Lutut dahulu.",src='https://binbaz.org.sa/fatwas/18683'),
        dict(w='uthaymin',en="Knees first.",ms="Lutut dahulu.")],
     h=[['abudawud',838,dict(en="Wa'il: knees before hands",ms="Wa'il: lutut sebelum tangan")],['abudawud',840,dict(en="Abu Hurairah: 'do not kneel as a camel kneels; put the hands before the knees'",ms="Abu Hurairah: 'jangan turun seperti unta turun; letakkan tangan sebelum lutut'")]],
     note=dict(en="Each side judges the other's hadith weak: see the gradings on each. Ibn al-Qayyim argued that the wording of Abu Hurairah's hadith was reversed by a narrator.",ms="Setiap pihak menilai hadis pihak lain lemah: lihat penilaian setiap satu. Ibn al-Qayyim berhujah lafaz hadis Abu Hurairah terbalik oleh seorang perawi."))]),

 dict(id='duduk', t=dict(en="Sitting between the two prostrations", ms="Duduk antara dua sujud"),
  s=dict(en="He sat on his left foot with the right foot upright (Bukhari 828) and stayed until at rest, saying 'Rabbighfir li, Rabbighfir li' (Nasa'i 1145, Abu Dawud 874) or 'Allahummaghfir li warhamni…' (Abu Dawud 850, Tirmidhi 284).",
         ms="Baginda duduk di atas kaki kiri dengan kaki kanan ditegakkan (Bukhari 828) dan kekal hingga tenang, sambil membaca 'Rabbighfir li, Rabbighfir li' (Nasa'i 1145, Abu Dawud 874) atau 'Allahummaghfir li warhamni…' (Abu Dawud 850, Tirmidhi 284)."),
  h=[['bukhari',828,None],['nasai',1145,None],['abudawud',874,None],['abudawud',850,None],['tirmidhi',284,None]]),

 dict(id='istirahah', t=dict(en="The short sitting before standing (jalsat al-istirahah)", ms="Duduk istirahat sebelum bangun"),
  s=dict(en="Malik ibn al-Huwayrith saw that in the odd rak'ahs (the first and third) he did not stand up until he had sat upright (Bukhari 823).",
         ms="Malik bin al-Huwairith melihat bahawa pada rakaat ganjil (pertama dan ketiga) Baginda tidak bangun sehingga duduk dengan sempurna (Bukhari 823)."),
  h=[['bukhari',823,None],['abudawud',844,None]],
  d=[dict(topic=dict(en="Is it a sunnah?",ms="Adakah ia sunat?"),
     p=[dict(w='shafii',en="Yes, a sunnah.",ms="Ya, sunat."),
        dict(w='albani',en="Yes, a sunnah.",ms="Ya, sunat."),
        dict(w='ibnbaz',en="Recommended.",ms="Sunat."),
        dict(w='uthaymin',en="Only for one who needs it (age, weakness).",ms="Hanya bagi yang memerlukannya (usia, lemah)."),
        dict(w='hanafi',en="Not a sunnah; he did it when he had grown heavy.",ms="Bukan sunat; Baginda melakukannya ketika badan sudah berat."),
        dict(w='maliki',en="Not a sunnah.",ms="Bukan sunat."),
        dict(w='hanbali',en="Not a sunnah in the best-known report, except for one who needs it; another report from Ahmad makes it a sunnah.",ms="Bukan sunat menurut riwayat yang masyhur, kecuali bagi yang memerlukannya; satu riwayat lain daripada Ahmad menjadikannya sunat.")])]),

 dict(id='tasyahhud1', t=dict(en="The first tashahhud", ms="Tasyahhud awal"),
  s=dict(en="After two rak'ahs he sat on his left foot with the right upright (Bukhari 828), placed his hands on his thighs, closed the fingers of the right hand and pointed with the index finger (Muslim 1311), and recited the tashahhud: 'At-tahiyyatu lillah, was-salawatu wat-tayyibat…' (Ibn Mas'ud, Bukhari 831; Ibn 'Abbas's wording, Muslim 902).",
         ms="Selepas dua rakaat Baginda duduk di atas kaki kiri dengan kaki kanan ditegakkan (Bukhari 828), meletakkan tangan di atas paha, menggenggam jari tangan kanan dan menunjuk dengan jari telunjuk (Muslim 1311), dan membaca tasyahhud: 'At-tahiyyatu lillah, was-salawatu wat-tayyibat…' (Ibn Mas'ud, Bukhari 831; lafaz Ibn 'Abbas, Muslim 902)."),
  h=[['bukhari',828,None],['muslim',1311,None],['muslim',1310,None],['bukhari',831,None],['muslim',902,None]],
  d=[dict(topic=dict(en="The index finger: raised, moved, or still",ms="Jari telunjuk: diangkat, digerakkan, atau diam"),
     p=[dict(w='shafii',en="Raised at 'illallah' and kept raised, without moving it.",ms="Diangkat pada 'illallah' dan kekal diangkat, tanpa digerakkan."),
        dict(w='hanafi',en="Raised at 'la ilaha' and lowered at 'illallah'.",ms="Diangkat pada 'la ilaha' dan diturunkan pada 'illallah'."),
        dict(w='maliki',en="Moved to and fro throughout the tashahhud.",ms="Digerakkan sepanjang tasyahhud."),
        dict(w='hanbali',en="Pointed each time Allah is mentioned, without moving it.",ms="Ditunjukkan setiap kali nama Allah disebut, tanpa digerakkan."),
        dict(w='albani',en="Pointed and moved throughout the tashahhud.",ms="Ditunjukkan dan digerakkan sepanjang tasyahhud."),
        dict(w='uthaymin',en="Pointed, and moved each time one supplicates in the tashahhud.",ms="Ditunjukkan, dan digerakkan setiap kali berdoa dalam tasyahhud.")],
     h=[['nasai',889,dict(en="Wa'il: 'I saw him moving it, supplicating with it'",ms="Wa'il: 'Aku melihat Baginda menggerakkannya, berdoa dengannya'")],['abudawud',989,dict(en="Ibn az-Zubayr: 'and he did not move it'",ms="Ibn az-Zubair: 'dan Baginda tidak menggerakkannya'")]],
     note=dict(en="Many scholars consider the word 'moving it' in Wa'il's hadith a wording only one narrator added (shadhdh); al-Albani accepted it. 'And he did not move it' is graded weak.",ms="Ramai ulama menganggap perkataan 'menggerakkannya' dalam hadis Wa'il sebagai tambahan seorang perawi sahaja (syaz); al-Albani menerimanya. 'Dan tidak menggerakkannya' dinilai lemah."))]),

 dict(id='tasyahhud2', dua=[[24,dict(en="Hisn al-Muslim: supplications after the last tashahhud, before the salam",ms="Hisn al-Muslim: doa selepas tasyahhud akhir, sebelum salam")]], t=dict(en="The final tashahhud, salawat and supplication", ms="Tasyahhud akhir, selawat dan doa"),
  s=dict(en="In the last sitting he put his left foot forward, kept the right upright and sat on his seat (tawarruk) (Bukhari 828). After the tashahhud comes the salawat on the Prophet ﷺ ('Allahumma salli 'ala Muhammad…', Bukhari 6357), then seeking refuge from four things: the punishment of Hell, the punishment of the grave, the trial of life and death, and the trial of the Dajjal (Muslim 1326), and any supplication, such as the one he taught Abu Bakr (Bukhari 834).",
         ms="Pada duduk terakhir Baginda mengeluarkan kaki kiri ke hadapan, menegakkan kaki kanan dan duduk di atas punggung (tawarruk) (Bukhari 828). Selepas tasyahhud ialah selawat ke atas Nabi ﷺ ('Allahumma salli 'ala Muhammad…', Bukhari 6357), kemudian memohon perlindungan daripada empat perkara: azab neraka, azab kubur, fitnah hidup dan mati, dan fitnah Dajjal (Muslim 1326), dan apa-apa doa, seperti doa yang Baginda ajarkan kepada Abu Bakar (Bukhari 834)."),
  h=[['bukhari',828,None],['bukhari',6357,None],['bukhari',3369,None],['muslim',1326,None],['bukhari',834,None]],
  d=[dict(topic=dict(en="Which sittings are tawarruk",ms="Duduk mana yang tawarruk"),
     p=[dict(w='shafii',en="The final sitting of every prayer, including two-rak'ah prayers such as Subuh.",ms="Duduk terakhir setiap solat, termasuk solat dua rakaat seperti Subuh."),
        dict(w='hanbali',en="Only the final sitting of a prayer that has two tashahhuds.",ms="Hanya duduk terakhir solat yang mempunyai dua tasyahhud."),
        dict(w='hanafi',en="Neither: both sittings on the left foot (for men).",ms="Tidak: kedua-dua duduk di atas kaki kiri (bagi lelaki)."),
        dict(w='maliki',en="Both sittings.",ms="Kedua-dua duduk.")])]),

 dict(id='salam', t=dict(en="Ending with salam", ms="Salam"),
  s=dict(en="He ended the prayer with 'As-salamu 'alaykum wa rahmatullah' to the right and to the left, turning until the whiteness of his cheek was seen (Muslim 1315, Tirmidhi 295).",
         ms="Baginda mengakhiri solat dengan 'As-salamu 'alaikum wa rahmatullah' ke kanan dan ke kiri, berpaling hingga kelihatan putih pipinya (Muslim 1315, Tirmidhi 295)."),
  h=[['muslim',1315,None],['tirmidhi',295,None]],
  d=[dict(topic=dict(en="One salam or two",ms="Satu salam atau dua"),
     p=[dict(w='shafii',en="Two; the first is a pillar, the second a sunnah.",ms="Dua; yang pertama rukun, yang kedua sunat."),
        dict(w='hanbali',en="Two, both required in obligatory prayers.",ms="Dua, kedua-duanya wajib dalam solat fardu."),
        dict(w='hanafi',en="Two.",ms="Dua."),
        dict(w='maliki',en="One, for the imam and one praying alone.",ms="Satu, bagi imam dan orang yang solat bersendirian.")])]),

 dict(id='selepas', dua=[[25,dict(en="Hisn al-Muslim: what to say after completing the prayer",ms="Hisn al-Muslim: bacaan selepas selesai solat")]], t=dict(en="Dhikr and du'a after the prayer", ms="Zikir dan doa selepas solat"),
  s=dict(en="After the salam he said 'Astaghfirullah' three times and 'Allahumma antas-salam wa minkas-salam, tabarakta ya dhal-jalali wal-ikram' (Muslim 1334), 'La ilaha illallahu wahdahu la sharika lah…' (Bukhari 844), and taught 'Subhanallah', 'Al-hamdulillah' and 'Allahu akbar' 33 times each (Muslim 1352), and told Mu'adh never to leave 'Allahumma a'inni 'ala dhikrika wa shukrika wa husni 'ibadatik' at the end of every prayer (Abu Dawud 1522). Ibn 'Abbas said that raising the voice with dhikr when people finished the obligatory prayer was done in the Prophet's time (Bukhari 841). Whether dhikr is said aloud together, and whether the imam makes du'a aloud with the people saying amin, is where scholars differ.",
         ms="Selepas salam Baginda membaca 'Astaghfirullah' tiga kali dan 'Allahumma antas-salam wa minkas-salam, tabarakta ya dzal-jalali wal-ikram' (Muslim 1334), 'La ilaha illallahu wahdahu la syarika lah…' (Bukhari 844), dan mengajar 'Subhanallah', 'Al-hamdulillah' dan 'Allahu akbar' 33 kali setiap satu (Muslim 1352), dan berpesan kepada Mu'adz agar tidak meninggalkan 'Allahumma a'inni 'ala dzikrika wa syukrika wa husni 'ibadatik' pada akhir setiap solat (Abu Dawud 1522). Ibn 'Abbas berkata menguatkan suara dengan zikir apabila orang selesai solat fardu dilakukan pada zaman Nabi (Bukhari 841). Sama ada zikir dibaca kuat beramai-ramai, dan sama ada imam berdoa dengan kuat sementara makmum mengaminkan, di situlah ulama berbeza."),
  h=[['muslim',1334,None],['bukhari',844,None],['muslim',1352,None],['abudawud',1522,None],['tirmidhi',3499,dict(en="Du'a most likely heard: in the last part of the night and after the obligatory prayers",ms="Doa paling didengar: pada akhir malam dan selepas solat fardu")]],
  d=[dict(topic=dict(en="Dhikr after the prayer: aloud together, or quietly each person",ms="Zikir selepas solat: kuat beramai-ramai, atau perlahan seorang-seorang"),
     p=[dict(w='shafii',en="Quietly, for the imam and the follower; the imam may say it aloud for a time to teach it, then lower his voice. Al-Shafi'i read Ibn 'Abbas's report as such teaching.",ms="Perlahan, bagi imam dan makmum; imam boleh menguatkannya untuk satu tempoh bagi mengajar, kemudian memperlahankan suara. Asy-Syafi'i memahami riwayat Ibn 'Abbas sebagai pengajaran seperti itu.",ref="al-Shafi'i, al-Umm 1/150; al-Nawawi, al-Majmu' 3/487",src="https://dorar.net/feqhia/1068"),
        dict(w='maliki',en="Quietly.",ms="Perlahan.",ref="al-Nafrawi, al-Fawakih ad-Dawani 1/492",src="https://dorar.net/feqhia/1068"),
        dict(w='hanafi',en="Views differ in the school: al-Kasani said raising the voice with takbir is in principle an innovation, as the sunnah in dhikr is to say it quietly; Ibn 'Abidin and al-Tahtawi report that saying dhikr aloud after the prayer is recommended.",ms="Pendapat berbeza dalam mazhab: al-Kasani berkata menguatkan suara dengan takbir pada asalnya bid'ah, kerana sunnah dalam zikir ialah perlahan; Ibn 'Abidin dan at-Tahtawi menukilkan bahawa menguatkan zikir selepas solat adalah sunat.",ref="al-Kasani, Bada'i' as-Sana'i' 1/196; Ibn 'Abidin, Hashiyah 1/666; al-Tahtawi, Hashiyah p. 214",src="https://dorar.net/feqhia/1068"),
        dict(w='hanbali',en="Views differ in the school: Ibn Muflih lists it with the Shafi'i view (aloud only to teach) and al-Mardawi held saying it quietly is correct; al-Bahuti held saying it aloud is recommended.",ms="Pendapat berbeza dalam mazhab: Ibn Muflih menyenaraikannya bersama pendapat Syafi'i (kuat hanya untuk mengajar) dan al-Mardawi berpendapat perlahan itulah yang betul; al-Buhuti berpendapat menguatkannya sunat.",ref="Ibn Muflih, al-Furu' 2/231; al-Mardawi, Tashih al-Furu' 2/231; al-Bahuti, Kashshaf al-Qina' 1/366",src="https://dorar.net/feqhia/1068"),
        dict(w='nawawi',en="Reports that al-Shafi'i and others agree that raising the voice with dhikr and takbir is not recommended.",ms="Menukilkan bahawa asy-Syafi'i dan yang lain sepakat menguatkan suara dengan zikir dan takbir tidak disunatkan.",ref="al-Nawawi, Sharh Sahih Muslim 5/84",src="https://dorar.net/feqhia/1068"),
        dict(w='taymiyyah',en="Recommended to say the tasbih and tahmid aloud.",ms="Disunatkan menguatkan tasbih dan tahmid.",ref="Ibn Taymiyyah, al-Fatawa al-Kubra 5/336",src="https://dorar.net/feqhia/1068"),
        dict(w='albani',en="What is established in the sunnah is that the voice is not raised with dhikr.",ms="Yang sabit dalam sunnah ialah suara tidak dikuatkan dengan zikir.",ref="al-Albani, Silsilat al-Huda wan-Nur, recording 428",src="https://dorar.net/feqhia/1068"),
        dict(w='ibnbaz',en="Saying the dhikr aloud after the five prayers is the sunnah.",ms="Menguatkan zikir selepas solat lima waktu ialah sunnah.",ref="Ibn Baz, Majmu' Fatawa 11/191",src="https://dorar.net/feqhia/1068"),
        dict(w='uthaymin',en="Saying the dhikr aloud after the obligatory prayers is a sunnah.",ms="Menguatkan zikir selepas solat fardu ialah sunnah.",ref="Ibn 'Uthaymin, Majmu' Fatawa wa Rasa'il 13/247-248",src="https://dorar.net/feqhia/1068"),
        dict(w='iftamisr',en="The matter is broad and the difference is minor: whoever wishes says it aloud and whoever wishes says it quietly; quoting al-Tahtawi, which is better depends on the person, the situation and the time. It must not become a cause of division.",ms="Perkara ini luas dan perbezaannya kecil: sesiapa mahu, bacalah dengan kuat, dan sesiapa mahu, bacalah perlahan; menukil at-Tahtawi, mana yang lebih baik bergantung pada orang, keadaan dan masa. Ia tidak boleh dijadikan punca perpecahan.",ref="Dar al-Ifta al-Misriyyah, fatwa 2315 ('Ali Jum'ah, 3 June 2012), citing al-Tahtawi, Hashiyah 'ala Maraqi al-Falah p. 318",src="https://www.dar-alifta.org/ar/fatwa/details/13441"),
        dict(w='perlis',en="Imams are not to hold congregational wirid at set times such as after the obligatory prayers, except to teach for a limited time; no one may recite wirid in a way that disturbs others.",ms="Imam tidak mengadakan wirid secara jamaie pada masa tertentu seperti selepas solat fardu, kecuali untuk mengajar dalam waktu yang terbatas; para jemaah tidak boleh mengadakan wirid atau bacaan yang mengganggu jemaah lain.",ref="Garis Panduan Pengurusan Masjid dan Surau Negeri Perlis (Pindaan 2020): Imam, klausa 3; Jemaah, klausa 4 (Jawatankuasa Fatwa Perlis, mesyuarat ke-50, 14 Dis 2020; diperakui MAIPs 26 Jan 2021)",src="https://muftiperlis.gov.my/index.php/fatwa-insights/waqf-mosque-dan-funeral-management/1564-guidelines-for-the-management-of-mosques-and-prayer-halls-throughout-the-state-of-perlis-amendment-year-2020")],
     h=[['bukhari',841,dict(en="Ibn 'Abbas: raising the voice with dhikr after the obligatory prayer was done in the Prophet's time",ms="Ibn 'Abbas: menguatkan suara dengan zikir selepas solat fardu dilakukan pada zaman Nabi")],['muslim',1318,None],['bukhari',842,dict(en="Ibn 'Abbas: 'I knew the prayer had ended by the takbir'",ms="Ibn 'Abbas: 'Aku tahu solat telah selesai dengan takbir'")]]),
   dict(topic=dict(en="Du'a together after the prayer: the imam supplicates aloud and the people say amin",ms="Doa berjemaah selepas solat: imam berdoa dengan kuat dan makmum mengaminkan"),
     p=[dict(w='shafii',en="Du'a after the prayer is recommended for the imam and the follower, said quietly, unless the imam says it aloud to teach.",ms="Doa selepas solat disunatkan bagi imam dan makmum, dibaca perlahan, kecuali imam menguatkannya untuk mengajar.",ref="al-Shafi'i, al-Umm 1/150; al-Nawawi, al-Majmu' 3/487",src="https://dorar.net/feqhia/1068"),
        dict(w='maliki',en="Malik and a group of scholars disliked imams making du'a aloud after the obligatory prayers for those present.",ms="Malik dan sekumpulan ulama tidak menyukai imam berdoa dengan kuat untuk para hadirin selepas solat fardu.",ref="Mayyarah, ad-Durr ath-Thamin pp. 173, 212 (via Mawsu'at al-Firaq 7/202)",src="https://shamela.ws/book/32150/3203"),
        dict(w='hanbali',en="Asked about people who gather regularly for du'a, Imam Ahmad said 'this is newly begun (muhdath)'; he did not dislike it for brothers who met without arranging it, unless they did it often.",ms="Ditanya tentang orang yang berkumpul secara tetap untuk berdoa, Imam Ahmad berkata 'ini perkara baharu (muhdath)'; beliau tidak membencinya bagi saudara yang bertemu tanpa dirancang, kecuali jika dilakukan dengan kerap.",ref="Ibn Muflih, al-Adab ash-Shar'iyyah 2/75, 2/102 (via islamqa 93757)",src="https://islamqa.info/ar/answers/93757"),
        dict(w='taymiyyah',en="It is not reported that the Prophet ﷺ and those behind him made du'a together after the salam; what is reported is dhikr.",ms="Tidak diriwayatkan bahawa Nabi ﷺ dan makmum berdoa bersama selepas salam; yang diriwayatkan ialah zikir.",ref="Ibn Taymiyyah, as quoted in ad-Durar as-Saniyyah (via Mawsu'at al-Firaq 7/204)",src="https://shamela.ws/book/32150/3205"),
        dict(w='shatibi',en="Du'a after the prayers in the form of a gathering (the imam supplicating and the people together) is an innovation.",ms="Doa selepas solat dalam bentuk berhimpun (imam berdoa dan makmum bersama) ialah bid'ah.",ref="al-Shatibi, al-I'tisam (via Mawsu'at al-Firaq 7/204)",src="https://shamela.ws/book/32150/3205"),
        dict(w='ibnbaz',en="Collective du'a after the obligatory prayer is an innovation with no basis.",ms="Doa berjemaah selepas solat fardu ialah bid'ah yang tiada asal.",ref="Ibn Baz, Nur 'ala ad-Darb (binbaz.org.sa fatwa 13394)",src="https://binbaz.org.sa/fatwas/13394"),
        dict(w='uthaymin',en="Du'a together in one voice after the imam's salam has no known basis.",ms="Doa beramai-ramai dengan satu suara selepas salam imam tiada asal yang diketahui.",ref="Ibn 'Uthaymin, in al-Fatawa al-Islamiyyah (via Mawsu'at al-Firaq 7/204)",src="https://shamela.ws/book/32150/3205"),
        dict(w='iftamisr',en="Collective dhikr and du'a with the people saying amin is permissible in the mosque and elsewhere, done in an orderly way that does not disturb others praying or reciting, following the mosque's rules; it must not cause division.",ms="Zikir dan doa berjemaah dengan makmum mengaminkan dibolehkan di masjid dan di tempat lain, dilakukan dengan tertib tanpa mengganggu orang yang solat atau membaca al-Quran, mengikut peraturan masjid; ia tidak boleh menimbulkan perpecahan.",ref="Dar al-Ifta al-Misriyyah, fatwa 4319 (Shawqi 'Allam, 15 March 2018)",src="https://www.dar-alifta.org/ar/fatwa/details/14377")],
     h=[['abudawud',1522,None],['tirmidhi',3499,None]],
     note=dict(en="No hadith in the eight books in this app describes the Prophet ﷺ making du'a aloud after the salam with the people saying amin. Those who allow it cite the general merit of du'a after prayer, and the hadith narrated by Habib ibn Maslamah al-Fihri that he heard the Prophet ﷺ say: \"No group gathers, some of them supplicating and the rest saying amin, but Allah answers them\" (al-Tabarani, al-Mu'jam al-Kabir 4/21-22, no. 3536; also al-Hakim). It is general, not about after the prayer. Al-Haythami (Majma' az-Zawa'id 10/170) said its narrators are those of the Sahih except Ibn Lahi'ah, whom he held to be hasan in hadith; others hold Ibn Lahi'ah weak, so its grading is disputed. Habib ibn Maslamah al-Fihri was of Quraysh, about 12 when the Prophet ﷺ died, so his being a Companion was questioned (Ibn Sa'd); he became a commander in Syria and Armenia and died in 42 AH. Many mosques in Singapore and Malaysia follow the practice; ask your teacher.",
          ms="Tiada hadis dalam lapan kitab dalam aplikasi ini yang menyebut Nabi ﷺ berdoa dengan kuat selepas salam sementara makmum mengaminkan. Yang membolehkannya berhujah dengan kelebihan doa selepas solat secara umum, dan hadis riwayat Habib bin Maslamah al-Fihri bahawa beliau mendengar Nabi ﷺ bersabda: \"Tidaklah berkumpul satu kumpulan, lalu sebahagian mereka berdoa dan yang lain mengaminkan, melainkan Allah memperkenankan mereka\" (at-Tabarani, al-Mu'jam al-Kabir 4/21-22, no. 3536; juga al-Hakim). Hadis ini umum, bukan khusus selepas solat. Al-Haithami (Majma' az-Zawa'id 10/170) berkata perawinya ialah perawi kitab Sahih kecuali Ibn Lahi'ah, yang menurut beliau hasan hadisnya; ulama lain melemahkan Ibn Lahi'ah, maka darjatnya diperselisihkan. Habib bin Maslamah al-Fihri berketurunan Quraisy, berusia kira-kira 12 tahun ketika Nabi ﷺ wafat, maka status sahabatnya dipersoalkan (Ibn Sa'd); beliau menjadi panglima di Syam dan Armenia dan wafat pada tahun 42 H. Banyak masjid di Singapura dan Malaysia mengamalkannya; tanya guru anda."),
     src="https://shamela.ws/book/61/3232")]),
 dict(id='qunut', t=dict(en="Qunut in Subuh", ms="Qunut Subuh"),
  s=dict(en="The Prophet ﷺ made qunut (a standing supplication after rising from bowing) in Subuh and other prayers at times of calamity, for a month (Muslim 1548, Bukhari 4090). Whether qunut is made in every Subuh is a well-known difference.",
         ms="Nabi ﷺ berqunut (doa ketika berdiri selepas bangkit daripada rukuk) dalam Subuh dan solat lain ketika musibah, selama sebulan (Muslim 1548, Bukhari 4090). Sama ada qunut dibaca dalam setiap Subuh ialah perbezaan yang terkenal."),
  h=[['muslim',1548,None],['bukhari',4090,None],['bukhari',1001,dict(en="Anas was asked: did he make qunut in Fajr? 'Yes', after bowing, for a short time",ms="Anas ditanya: adakah Baginda berqunut dalam Subuh? 'Ya', selepas rukuk, untuk tempoh yang singkat")],['tirmidhi',401,dict(en="Al-Bara': he made qunut in Subh and Maghrib",ms="Al-Bara': Baginda berqunut dalam Subuh dan Maghrib")]],
  d=[dict(topic=dict(en="Qunut in every Subuh",ms="Qunut dalam setiap Subuh"),
     p=[dict(w='shafii',en="A confirmed sunnah, after rising from the bowing of the second rak'ah.",ms="Sunat muakkad, selepas bangkit daripada rukuk rakaat kedua."),
        dict(w='maliki',en="Recommended, said quietly, before bowing.",ms="Sunat, dibaca perlahan, sebelum rukuk."),
        dict(w='hanafi',en="Not in Subuh, except at times of calamity in some views; qunut is in witr.",ms="Tidak dalam Subuh, kecuali ketika musibah menurut sebahagian pendapat; qunut dalam witir."),
        dict(w='hanbali',en="Not in Subuh, except at times of calamity.",ms="Tidak dalam Subuh, kecuali ketika musibah."),
        dict(w='albani',en="Only at times of calamity.",ms="Hanya ketika musibah."),
        dict(w='ibnbaz',en="Only at times of calamity.",ms="Hanya ketika musibah.",src='https://binbaz.org.sa/fatwas/15800'),
        dict(w='uthaymin',en="Only at times of calamity.",ms="Hanya ketika musibah.")],
     h=[['tirmidhi',402,dict(en="Abu Malik al-Ashja'i's father: 'My son, it is something newly begun'",ms="Bapa Abu Malik al-Asyja'i: 'Wahai anakku, ia perkara baharu'")]],
     note=dict(en="The Shafi'is also cite Anas: 'He kept making qunut in Fajr until he left this world' (Musnad Ahmad 12657; al-Hakim, al-Arba'in; al-Bayhaqi, as-Sunan al-Kubra 2/201; not in this app's books). Judged weak by Ibn al-Jawzi (al-'Ilal al-Mutanahiyah 1/444), Ibn Taymiyyah (Majmu' al-Fatawa 22/374), Ibn al-Qayyim (Zad al-Ma'ad 1/99), Ibn Hajar (at-Talkhis al-Habir 1/245), al-Albani (as-Silsilah ad-Da'ifah 1238) and Ibn Baz (Fatawa Nur 'ala ad-Darb 10/227), as listed by IslamQA 101015 and Dorar.net.",ms="Mazhab Syafi'i juga berhujah dengan riwayat Anas: 'Baginda sentiasa berqunut dalam Subuh hingga Baginda meninggalkan dunia' (Musnad Ahmad 12657; al-Hakim, al-Arba'in; al-Baihaqi, as-Sunan al-Kubra 2/201; bukan dalam kitab aplikasi ini). Dinilai lemah oleh Ibn al-Jauzi (al-'Ilal al-Mutanahiyah 1/444), Ibn Taimiyyah (Majmu' al-Fatawa 22/374), Ibn al-Qayyim (Zad al-Ma'ad 1/99), Ibn Hajar (at-Talkhis al-Habir 1/245), al-Albani (as-Silsilah adh-Dha'ifah 1238) dan Ibn Baz (Fatawa Nur 'ala ad-Darb 10/227), seperti yang disenaraikan oleh IslamQA 101015 dan Dorar.net."))]),
]

WHO = dict(shafii=dict(en="Shafi'i", ms="Syafi'i"), hanafi=dict(en="Hanafi", ms="Hanafi"), maliki=dict(en="Maliki", ms="Maliki"),
           hanbali=dict(en="Hanbali", ms="Hanbali"), albani=dict(en="Al-Albani", ms="Al-Albani"),
           ibnbaz=dict(en="Ibn Baz", ms="Ibn Baz"), uthaymin=dict(en="Ibn 'Uthaymin", ms="Ibn 'Uthaimin"),
           nawawi=dict(en="Imam al-Nawawi", ms="Imam al-Nawawi"), arnaut=dict(en="Shu'ayb al-Arna'ut", ms="Syu'aib al-Arna'ut"),
           taymiyyah=dict(en="Ibn Taymiyyah", ms="Ibn Taimiyyah"), shatibi=dict(en="Al-Shatibi", ms="Asy-Syatibi"),
           iftamisr=dict(en="Dar al-Ifta al-Misriyyah", ms="Dar al-Ifta' Mesir"),
           perlis=dict(en="Perlis State Fatwa Committee", ms="Jawatankuasa Fatwa Negeri Perlis"))
# Commentators, shown apart from the four schools in their own box: al-Albani (Sifat Salat an-Nabi), 'Abd al-'Aziz ibn Baz
# (Majmu' Fatawa), Muhammad ibn Salih al-'Uthaymin (al-Sharh al-Mumti').
COMMENTATORS = ['nawawi', 'taymiyyah', 'shatibi', 'albani', 'ibnbaz', 'uthaymin', 'arnaut', 'iftamisr', 'perlis']

# ---- Sources for the commentators (Azli, 15 Oct 2026: include other scholars' views only with a reliable source) ----
# Each line: (step id, topic number, scholar) -> (reference, link or None[, new English, new Malay]).
# References as cited in al-Mawsu'ah al-Fiqhiyyah of Dorar.net (dorar.net/feqhia) or on the scholar's own site / IslamQA,
# checked 15 Oct 2026. Lines with no source found were removed rather than shown unsourced.
A_ASL = "al-Albani, Asl Sifat Salat an-Nabi"
BZ_MF, BZ_NUR = "Ibn Baz, Majmu' Fatawa", "Ibn Baz, Fatawa Nur 'ala ad-Darb"
UT_MF, UT_SM = "Ibn 'Uthaymin, Majmu' Fatawa wa Rasa'il", "Ibn 'Uthaymin, al-Sharh al-Mumti'"
REFS = {
 ('niat',0,'ibnbaz'): (BZ_NUR+" 5/79", "https://binbaz.org.sa/fatwas/6205"),
 ('niat',0,'uthaymin'): (UT_SM+" 1/195", "https://dorar.net/feqhia/247"),
 ('qiyam',0,'albani'): (A_ASL+" 1/215", "https://dorar.net/feqhia/914"),
 ('qiyam',0,'ibnbaz'): (BZ_NUR+" 8/148", "https://binbaz.org.sa/fatwas/16879"),
 ('qiyam',0,'uthaymin'): (UT_MF+" 13/392", "https://dorar.net/feqhia/914"),
 ('iftitah',0,'albani'): ("al-Albani, Sifat Salat an-Nabi p. 91", "https://dorar.net/feqhia/919"),
 ('iftitah',0,'ibnbaz'): (BZ_MF+" 11/9", "https://dorar.net/feqhia/919", "Any authentic wording; best to alternate between them.", "Mana-mana lafaz yang sahih; lebih baik berselang-seli."),
 ('iftitah',0,'uthaymin'): (UT_SM+" 3/48", "https://dorar.net/feqhia/919"),
 ('basmalah',0,'ibnbaz'): (BZ_MF+" 29/244", "https://binbaz.org.sa/fatwas/6110"),
 ('basmalah',0,'uthaymin'): (UT_MF+" 13/109", "https://dorar.net/feqhia/925", "Said quietly; saying it aloud now and then is no blame.", "Dibaca perlahan; sesekali menguatkannya tidak mengapa."),
 ('fatihah',0,'albani'): ("al-Albani, Sifat Salat an-Nabi p. 97 (loud prayers); "+A_ASL+" 3/1055 (quiet prayers)", "https://islamqa.info/ar/answers/231217"),
 ('fatihah',0,'ibnbaz'): (BZ_NUR+" 8/72-73", "https://binbaz.org.sa/fatwas/12708"),
 ('fatihah',0,'uthaymin'): ("Ibn 'Uthaymin, Fath Dhi al-Jalal wa al-Ikram 2/70", "https://dorar.net/feqhia/923", "Obligatory on the imam, the follower and one praying alone in quiet prayers, except a latecomer who catches the bowing.", "Wajib bagi imam, makmum dan orang yang solat bersendirian dalam solat sirr, kecuali makmum masbuq yang sempat rukuk."),
 ('fatihah',1,'albani'): ("al-Albani, Silsilat al-Ahadith ad-Da'ifah 2/369", "https://islamqa.info/ar/answers/234769", "Aloud, by the imam and those behind him (his later view).", "Dikuatkan, oleh imam dan makmum (pendapat terakhirnya)."),
 ('fatihah',1,'ibnbaz'): ("Ibn Baz, fatwa", "https://binbaz.org.sa/fatwas/15815"),
 ('fatihah',1,'uthaymin'): (UT_MF+" 13/140", "https://islamqa.info/ar/answers/234769"),
 ('ruku',0,'albani'): ("al-Albani graded the hadith sahih (Sahih an-Nasa'i 1084)", "https://dorar.net/hadith/sharh/32554", "Graded sahih the hadith of raising the hands at prostration and rising from it (Nasa'i 1085 in this app).", "Menilai sahih hadis mengangkat tangan ketika sujud dan bangkit daripadanya (Nasa'i 1085 dalam aplikasi ini)."),
 ('ruku',0,'ibnbaz'): (BZ_MF+" 11/156", "https://binbaz.org.sa/fatwas/12609"),
 ('ruku',0,'uthaymin'): (UT_MF+" 13/66, 13/70", "https://dorar.net/feqhia/907", "At the opening, bowing, rising, and standing from the first tashahhud; not at prostration, as no authentic report establishes it.", "Pada takbiratul ihram, rukuk, bangkit, dan bangun daripada tasyahhud awal; tidak ketika sujud, kerana tiada riwayat sahih."),
 ('itidal',0,'albani'): (A_ASL+" 2/701", "https://dorar.net/feqhia/958"),
 ('itidal',0,'ibnbaz'): (BZ_MF+" 11/30", "https://binbaz.org.sa/fatwas/5128"),
 ('itidal',0,'uthaymin'): (UT_MF+" 13/160-161", "https://dorar.net/feqhia/958"),
 ('sujud',0,'albani'): (A_ASL+" 2/719", "https://dorar.net/feqhia/969"),
 ('sujud',0,'ibnbaz'): (BZ_MF+" 11/61-62", "https://binbaz.org.sa/fatwas/18683"),
 ('sujud',0,'uthaymin'): (UT_MF+" 13/173-174", "https://dorar.net/feqhia/969"),
 ('istirahah',0,'albani'): (A_ASL+" 3/816", "https://dorar.net/feqhia/989"),
 ('istirahah',0,'ibnbaz'): (BZ_MF+" 11/38-39", "https://binbaz.org.sa/fatwas/10375"),
 ('istirahah',0,'uthaymin'): (UT_MF+" 13/218", "https://dorar.net/feqhia/989", "Not a sunnah except for one who needs it (his later view).", "Bukan sunat kecuali bagi yang memerlukannya (pendapat terakhirnya)."),
 ('tasyahhud1',0,'albani'): ("al-Albani graded Wa'il's hadith ('moving it') sahih (Sahih an-Nasa'i)", "https://islamqa.info/ar/answers/11527", "Graded sahih Wa'il's hadith with the words 'moving it, supplicating with it' (Nasa'i 889).", "Menilai sahih hadis Wa'il dengan lafaz 'menggerakkannya, berdoa dengannya' (Nasa'i 889)."),
 ('tasyahhud1',0,'uthaymin'): (UT_SM+" 3/202", "https://islamqa.info/ar/answers/11527"),
 ('qunut',0,'ibnbaz'): (BZ_NUR+" 10/225", "https://binbaz.org.sa/fatwas/15800"),
 ('qunut',0,'uthaymin'): (UT_MF+" 14/131", "https://dorar.net/feqhia/936"),
}
NW = "al-Nawawi, al-Majmu' Sharh al-Muhadhdhab"
AR = "Shu'ayb al-Arna'ut"
REFS.update({
 ('qiyam',0,'nawawi'): (NW+" 3/313", "https://dorar.net/feqhia/914", "Our school: below the chest, above the navel. He also quotes Ibn al-Mundhir: nothing is established from the Prophet ﷺ on the exact place, so one may choose.", "Mazhab kami: di bawah dada, di atas pusat. Beliau juga memetik Ibn al-Mundzir: tiada yang sabit daripada Nabi ﷺ tentang tempatnya yang tepat, jadi seseorang boleh memilih."),
 ('qiyam',0,'arnaut'): (AR+", Takhrij al-Musnad 21967", "https://dorar.net/h/GB5LZpJM", "Hulb at-Ta'i's hadith (Musnad Ahmad): sahih li-ghayrihi, except the words 'he placed this on his chest'.", "Hadis Hulb at-Ta'i (Musnad Ahmad): sahih li-ghairihi, kecuali lafaz 'Baginda meletakkan ini di atas dadanya'."),
 ('basmalah',0,'nawawi'): (NW+" 3/208, as cited by Ibn Sarkand, al-Ahkam al-Fiqhiyyah allati qila fiha bin-naskh 2/832", "https://shamela.ws/book/787/792", "Saying it aloud is the view of most scholars from the Companions onward.", "Menguatkannya ialah pendapat kebanyakan ulama sejak para Sahabat."),
 ('fatihah',0,'nawawi'): (NW+" 3/327, 3/364", "https://dorar.net/feqhia/923", "Al-Fatihah is required: the prayer of anyone able to recite it is not valid without it. (3/364 records the school's old view that the follower does not recite in loud prayers.)", "Al-Fatihah wajib: solat orang yang mampu membacanya tidak sah tanpanya. (3/364 mencatat pendapat lama mazhab bahawa makmum tidak membaca dalam solat jahar.)"),
 ('fatihah',1,'nawawi'): (NW+" 3/368-373; Sharh Muslim 4/130", "https://dorar.net/feqhia/933", "Amin is a confirmed sunnah, aloud in loud prayers by the imam and those behind him.", "Amin sunat muakkad, dikuatkan dalam solat jahar oleh imam dan makmum."),
 ('ruku',0,'nawawi'): (NW+" 3/425-426", "https://islamqa.info/ar/answers/128038", "Raising the hands when standing up from the first tashahhud is recommended: 'this is what is correct' (وهذا هو الصواب).", "Mengangkat tangan ketika bangun daripada tasyahhud awal adalah sunat: 'inilah yang betul' (وهذا هو الصواب)."),
 ('sujud',0,'nawawi'): (NW+" 3/421", "https://dorar.net/feqhia/969", "Knees first (the Shafi'i school).", "Lutut dahulu (mazhab Syafi'i)."),
 ('istirahah',0,'nawawi'): (NW+" 3/442", "https://dorar.net/feqhia/989", "Recommended (the Shafi'i school).", "Sunat (mazhab Syafi'i)."),
 ('istirahah',0,'arnaut'): (AR+", Takhrij al-Musnad 16892", "https://dorar.net/feqhia/989", "Mu'awiyah's hadith 'Do not race me in bowing and prostrating, for I have grown heavy' (cited by those who say he sat only from need): sahih li-ghayrihi.", "Hadis Mu'awiyah 'Jangan mendahuluiku dalam rukuk dan sujud, kerana badanku sudah berat' (dalil mereka yang berkata Baginda duduk kerana keperluan): sahih li-ghairihi."),
 ('tasyahhud1',0,'nawawi'): (NW+" 3/454", "https://dorar.net/feqhia/1012", "Moving the finger is not prescribed in the tashahhud (the Shafi'i school).", "Menggerakkan jari tidak disyariatkan dalam tasyahhud (mazhab Syafi'i)."),
 ('qunut',0,'arnaut'): (AR+", Takhrij Zad al-Ma'ad 1/263", "https://dorar.net/feqhia/936", "Abu Mijlaz's report that he prayed Fajr behind Ibn 'Umar and Ibn 'Umar did not make qunut: hasan.", "Riwayat Abu Mijlaz bahawa beliau solat Subuh di belakang Ibn 'Umar dan Ibn 'Umar tidak berqunut: hasan."),
})
ADD = {('iftitah',0): ['ibnbaz'], ('qiyam',0): ['nawawi','arnaut'], ('basmalah',0): ['nawawi'], ('fatihah',0): ['nawawi'], ('fatihah',1): ['nawawi'],
       ('ruku',0): ['nawawi'], ('sujud',0): ['nawawi'], ('istirahah',0): ['nawawi','arnaut'], ('tasyahhud1',0): ['nawawi'], ('qunut',0): ['arnaut']}
for _e in E:
    for _ti, _d in enumerate(_e.get('d', [])):
        for _w in ADD.get((_e['id'], _ti), []):
            if not any(p['w'] == _w for p in _d['p']): _d['p'].append(dict(w=_w, en='', ms=''))
        _keep = []
        for _p in _d['p']:
            if _p['w'] not in COMMENTATORS: _keep.append(_p); continue
            r = REFS.get((_e['id'], _ti, _p['w']))
            if not r and _p.get('ref'): _keep.append(_p); continue
            if not r: continue                       # no reliable source found: not shown
            _p['ref'] = r[0]
            if r[1]: _p['src'] = r[1]
            if len(r) > 2: _p['en'], _p['ms'] = r[2], r[3]
            _keep.append(_p)
        _d['p'] = [x for x in _keep if x['w'] not in COMMENTATORS] + sorted([x for x in _keep if x['w'] in COMMENTATORS], key=lambda x: COMMENTATORS.index(x['w']))
for _e in E:
    for _d in _e.get('d', []):
        if _d.get('note') and 'al-Albani, judged it weak' in _d['note']['en']:
            _d['note'] = dict(en=_d['note']['en'].replace("others, including Ibn al-Qayyim and al-Albani, judged it weak", "others, including Ibn al-Qayyim (Zad al-Ma'ad), judged it weak"),
                              ms=_d['note']['ms'].replace("yang lain, termasuk Ibn al-Qayyim dan al-Albani, menilainya lemah", "yang lain, termasuk Ibn al-Qayyim (Zad al-Ma'ad), menilainya lemah"))
