# -*- coding: utf-8 -*-
"""Sirah timeline for My Personal Quran (Azli, 15 Oct 2026).
Each event: a short summary written for the app (EN/MS), Qur'an links that the hadith books or the classical tafsir
make themselves, hadith from the app's own books (gradings come from the data), reports from books outside the app
(named, with their status where it is known), and popular stories with their status shown plainly.
Story kinds: 'hist' = told by the sirah historians (Ibn Ishaq and others) without a checked chain;
'weak' = graded weak by hadith scholars; 'disputed' = scholars differ on the chain; 'none' = no authentic basis."""
E=[]
def ev(**k): E.append(k)

# ---------------- BEFORE PROPHETHOOD ----------------
ev(id='fil',era='pre',ce='c. 570',when={'en':'The Year of the Elephant','ms':'Tahun Gajah'},
 title={'en':'Abrahah and the Elephant','ms':'Abrahah dan tentera bergajah'},
 sum={'en':'Abrahah, the Abyssinian ruler of Yemen, marched on Makkah with an elephant to destroy the Ka\'bah. Allah destroyed his army with flocks of birds, as Surah al-Fil describes. The Prophet ﷺ was born in the same year, according to most historians.',
      'ms':'Abrahah, pemerintah Yaman dari Habsyah, mara ke Makkah dengan gajah untuk meruntuhkan Kaabah. Allah membinasakan tenteranya dengan kawanan burung, seperti yang diceritakan dalam Surah al-Fil. Menurut kebanyakan ahli sejarah, Nabi ﷺ lahir pada tahun yang sama.'},
 q=[[105,1,5,'The event itself','Peristiwa itu sendiri']],
 h=[['bukhari',2731,'At al-Hudaybiyah the Prophet ﷺ said of his camel: "She was stopped by the One who stopped the elephant."','Di Hudaibiyah, Nabi ﷺ berkata tentang untanya: "Dia ditahan oleh (Allah) yang menahan gajah."'],
    ['tirmidhi',3619,'"I and the Messenger of Allah ﷺ were born in the Year of the Elephant" (see its grading).','"Aku dan Rasulullah ﷺ dilahirkan pada Tahun Gajah" (lihat hukumnya).']])
ev(id='birth',era='pre',
 nasab={'chain':['Muhammad ﷺ','\'Abdullah','\'Abd al-Muttalib','Hashim','\'Abd Manaf','Qusayy','Kilab','Murrah','Ka\'b','Lu\'ayy','Ghalib','Fihr','Malik','an-Nadr','Kinanah','Khuzaymah','Mudrikah','Ilyas','Mudar','Nizar','Ma\'add','\'Adnan'],
  'ar':'محمد بن عبد الله بن عبد المطلب بن هاشم بن عبد مناف بن قصي بن كلاب بن مرة بن كعب بن لؤي بن غالب بن فهر بن مالك بن النضر بن كنانة بن خزيمة بن مدركة بن إلياس بن مضر بن نزار بن معد بن عدنان',
  'en':'Al-Bukhari gives this lineage as the heading of the chapter on the sending of the Prophet ﷺ (Sahih al-Bukhari, Kitab Manaqib al-Ansar, before hadith 3851). Ibn al-Qayyim: up to \'Adnan it is known to be correct and agreed by the genealogists; above \'Adnan they differ (Zad al-Ma\'ad 1/70-71). That \'Adnan descends from Isma\'il (Ishmael), son of Ibrahim, is supported by the hadith "Allah chose Kinanah from the children of Isma\'il" (Muslim 5938). His mother Aminah bint Wahb ibn \'Abd Manaf ibn Zuhrah ibn Kilab: her line meets his father\'s at Kilab ibn Murrah (Nadrat an-Na\'im 1/193).',
  'ms':'Al-Bukhari meletakkan nasab ini sebagai tajuk bab pengutusan Nabi ﷺ (Sahih al-Bukhari, Kitab Manaqib al-Ansar, sebelum hadis 3851). Ibn al-Qayyim: hingga \'Adnan ia diketahui sahih dan disepakati oleh ahli nasab; di atas \'Adnan mereka berselisih (Zad al-Ma\'ad 1/70-71). Bahawa \'Adnan daripada keturunan Ismail, anak Ibrahim, disokong oleh hadis "Allah memilih Kinanah daripada keturunan Ismail" (Muslim 5938). Ibunya Aminah binti Wahb bin \'Abd Manaf bin Zuhrah bin Kilab: nasabnya bertemu dengan nasab bapanya pada Kilab bin Murrah (Nadrat an-Na\'im 1/193).',
  'url':'https://shamela.ws/book/22798/290'},ce='c. 570',when={'en':'Monday, Rabi\' al-Awwal, Year of the Elephant','ms':'Isnin, Rabiulawal, Tahun Gajah'},
 title={'en':'Birth of the Prophet ﷺ','ms':'Kelahiran Nabi ﷺ'},
 sum={'en':'Muhammad ﷺ was born in Makkah to Aminah bint Wahb, into Banu Hashim of Quraysh. He himself said he was born on a Monday. His father \'Abdullah had died before his birth, according to the historians.',
      'ms':'Muhammad ﷺ dilahirkan di Makkah oleh Aminah binti Wahb, dalam Bani Hasyim dari Quraisy. Baginda sendiri bersabda bahawa baginda lahir pada hari Isnin. Menurut ahli sejarah, bapanya, Abdullah, telah wafat sebelum baginda lahir.'},
 h=[['muslim',2750,'"That is the day I was born, and the day revelation came to me" (about fasting on Monday).','"Itulah hari aku dilahirkan dan hari wahyu diturunkan kepadaku" (tentang puasa hari Isnin).'],['muslim',5938,'"Allah chose Kinanah from the children of Isma\'il, chose Quraysh from Kinanah, chose Banu Hashim from Quraysh, and chose me from Banu Hashim."','"Allah memilih Kinanah daripada keturunan Ismail, memilih Quraisy daripada Kinanah, memilih Bani Hasyim daripada Quraisy, dan memilih aku daripada Bani Hasyim."']],
 pop=[{'kind':'none','en':'The date 12 Rabi\' al-Awwal: the best-known date, but no authentic hadith fixes the day of the month; historians give 2, 8, 9, 10, 12 and others.','ms':'Tarikh 12 Rabiulawal: tarikh paling masyhur, tetapi tiada hadis sahih yang menetapkan harinya; ahli sejarah menyebut 2, 8, 9, 10, 12 dan lain-lain.'},
      {'kind':'hist','en':'His father \'Abdullah died in Madinah before he was born: told by the historians (Ibn Ishaq and others); not in an authenticated hadith.','ms':'Bapanya, Abdullah, wafat di Madinah sebelum baginda lahir: diriwayatkan oleh ahli sejarah (Ibn Ishaq dan lain-lain); tiada dalam hadis yang disahkan.'},
      {'kind':'none','en':'At his birth the palace of Chosroes shook, fourteen balconies fell and the fire of the Persians went out: reported by al-Bayhaqi and Abu Nu\'aym with a chain of unknown narrators; not established.','ms':'Ketika baginda lahir, istana Kisra bergegar, empat belas anjungnya runtuh dan api sembahan Parsi terpadam: diriwayatkan oleh al-Baihaqi dan Abu Nu\'aim dengan sanad yang perawinya tidak dikenali; tidak sabit.'}])
ev(id='halimah',era='pre',ce='c. 570–575',when={'en':'Infancy and early childhood','ms':'Zaman bayi dan kanak-kanak'},
 title={'en':'With Halimah among Banu Sa\'d; his chest opened','ms':'Bersama Halimah di Bani Sa\'d; dadanya dibelah'},
 sum={'en':'As was the custom of Makkah\'s nobles, he was nursed in the desert among Banu Sa\'d by Halimah as-Sa\'diyyah. While a boy playing with other children, Jibril opened his chest, took out a portion of it and washed his heart, as Sahih Muslim reports.',
      'ms':'Seperti adat bangsawan Makkah, baginda disusukan di padang pasir dalam Bani Sa\'d oleh Halimah as-Sa\'diyyah. Ketika masih kanak-kanak dan bermain dengan kanak-kanak lain, Jibril membelah dadanya, mengeluarkan sebahagian daripadanya dan membasuh hatinya, seperti yang diriwayatkan dalam Sahih Muslim.'},
 h=[['muslim',413,'Jibril opened his chest while he played with other boys.','Jibril membelah dadanya ketika baginda bermain dengan kanak-kanak lain.']],
 pop=[{'kind':'hist','en':'The blessings Halimah saw (her dry camel giving milk, her weak donkey outpacing others): told by Ibn Ishaq from Halimah; scholars differ on its chain.','ms':'Keberkatan yang dilihat Halimah (untanya yang kering kembali berair susu, keldainya yang lemah mendahului yang lain): diriwayatkan oleh Ibn Ishaq daripada Halimah; ulama berbeza pendapat tentang sanadnya.'}])
ev(id='aminah',era='pre',ce='c. 576–578',when={'en':'Age about 6 to 8','ms':'Usia kira-kira 6 hingga 8 tahun'},
 title={'en':'Death of his mother; care of \'Abd al-Muttalib, then Abu Talib','ms':'Kewafatan ibunya; dipelihara Abdul Muttalib, kemudian Abu Talib'},
 sum={'en':'His mother Aminah died when he was about six, at al-Abwa\' between Makkah and Madinah, according to the historians. His grandfather \'Abd al-Muttalib cared for him until he died two years later, then his uncle Abu Talib. Years later the Prophet ﷺ visited his mother\'s grave and wept.',
      'ms':'Menurut ahli sejarah, ibunya, Aminah, wafat ketika baginda berusia kira-kira enam tahun, di al-Abwa\' antara Makkah dan Madinah. Datuknya, Abdul Muttalib, memeliharanya sehingga beliau meninggal dua tahun kemudian, kemudian bapa saudaranya, Abu Talib. Bertahun-tahun kemudian, Nabi ﷺ menziarahi kubur ibunya dan menangis.'},
 q=[[93,6,8,'"Did He not find you an orphan and give you shelter?"','"Bukankah Dia mendapatimu yatim lalu Dia melindungimu?"']],
 h=[['muslim',2259,'He visited his mother\'s grave and wept.','Baginda menziarahi kubur ibunya dan menangis.']],
 pop=[{'kind':'hist','en':'Her death at al-Abwa\' on the way back from Madinah, and his age at the time: told by the historians; not in an authenticated hadith.','ms':'Kewafatannya di al-Abwa\' dalam perjalanan pulang dari Madinah, dan usia baginda ketika itu: diriwayatkan oleh ahli sejarah; tiada dalam hadis yang disahkan.'}])
ev(id='bahira',era='pre',ce='c. 582',when={'en':'Age about 12','ms':'Usia kira-kira 12 tahun'},
 title={'en':'Journey to Syria with Abu Talib; the monk Bahira','ms':'Perjalanan ke Syam bersama Abu Talib; rahib Bahira'},
 sum={'en':'He travelled with Abu Talib in a trading caravan to Syria. A monk (named Bahira by the historians) is reported to have recognised signs of prophethood in him and urged Abu Talib to take him home. The hadith in at-Tirmidhi is graded differently by the scholars; see the gradings.',
      'ms':'Baginda mengikut Abu Talib dalam kafilah dagang ke Syam. Diriwayatkan bahawa seorang rahib (dinamakan Bahira oleh ahli sejarah) mengenali tanda-tanda kenabian padanya dan menasihati Abu Talib supaya membawanya pulang. Hadis dalam at-Tirmizi dinilai berbeza oleh ulama; lihat hukumnya.'},
 h=[['tirmidhi',3620,'The monk and the caravan of Quraysh (see the gradings: some scholars reject parts of it).','Rahib dan kafilah Quraisy (lihat hukumnya: sebahagian ulama menolak sebahagian isinya).']])
ev(id='shepherd',era='pre',ce='c. 580s',when={'en':'Youth','ms':'Zaman remaja'},
 title={'en':'Shepherd in Makkah','ms':'Menggembala kambing di Makkah'},
 sum={'en':'He tended sheep for the people of Makkah for a few qirats. He said that every prophet Allah sent had been a shepherd.',
      'ms':'Baginda menggembala kambing penduduk Makkah dengan upah beberapa qirat. Baginda bersabda bahawa setiap nabi yang diutus Allah pernah menjadi gembala.'},
 h=[['bukhari',2262,'"Every prophet shepherded sheep... I used to shepherd the sheep of the people of Makkah for a few qirats."','"Setiap nabi pernah menggembala kambing... Aku dahulu menggembala kambing penduduk Makkah dengan upah beberapa qirat."']])
ev(id='fudul',era='pre',ce='c. 590',when={'en':'Age about 20','ms':'Usia kira-kira 20 tahun'},
 title={'en':'The War of Fijar and the Pact of al-Fudul','ms':'Perang Fijar dan Perjanjian al-Fudul'},
 sum={'en':'Quraysh fought the War of Fijar, and afterwards several clans made the Pact of al-Fudul (Hilf al-Fudul) at the house of \'Abdullah ibn Jud\'an, pledging to defend anyone wronged in Makkah. The Prophet ﷺ was present and later praised it.',
      'ms':'Quraisy berperang dalam Perang Fijar, dan selepas itu beberapa kabilah membuat Perjanjian al-Fudul (Hilf al-Fudul) di rumah Abdullah bin Jud\'an, berikrar untuk membela sesiapa yang dizalimi di Makkah. Nabi ﷺ hadir dan kemudian memujinya.'},
 ext=[{'en':'"I witnessed with my uncles the Pact of the Mutayyabin as a boy..." Musnad Ahmad (not in this app\'s books).','ms':'"Aku menyaksikan Perjanjian al-Mutayyabin bersama bapa-bapa saudaraku ketika aku masih budak..." Musnad Ahmad (tiada dalam kitab aplikasi ini).'}],
 pop=[{'kind':'hist','en':'The details of the War of Fijar and of the Pact of al-Fudul, and his words "If I were called to it in Islam I would answer": told by Ibn Ishaq and al-Bayhaqi; not in the authenticated collections.','ms':'Butiran Perang Fijar dan Perjanjian al-Fudul, serta sabdanya "Jika aku diseru kepadanya dalam Islam, nescaya aku menyahutnya": diriwayatkan oleh Ibn Ishaq dan al-Baihaqi; tiada dalam himpunan hadis yang disahkan.'}])
ev(id='khadijah',era='pre',ce='c. 595',when={'en':'Age 25 (according to most historians)','ms':'Usia 25 tahun (menurut kebanyakan ahli sejarah)'},
 title={'en':'Marriage to Khadijah','ms':'Perkahwinan dengan Khadijah'},
 sum={'en':'He married Khadijah bint Khuwaylid, a noble and wealthy woman of Quraysh; the historians say this followed his leading her trade caravan to Syria. She bore him all his children except Ibrahim, his son by Mariyah al-Qibtiyyah, born in Madinah in Dhu al-Hijjah 8 AH (Ibn al-Athir, Usd al-Ghabah 1/49), who died as an infant (al-Bukhari 1303). He said she was the best of the women of her time.',
      'ms':'Baginda berkahwin dengan Khadijah binti Khuwailid, wanita Quraisy yang mulia dan berharta; menurut ahli sejarah, ini berlaku selepas baginda membawa kafilah dagangnya ke Syam. Beliau melahirkan semua anak baginda kecuali Ibrahim, anak baginda dengan Mariyah al-Qibtiyyah, yang lahir di Madinah pada Zulhijjah tahun 8 H (Ibn al-Athir, Usd al-Ghabah 1/49) dan wafat ketika masih bayi (al-Bukhari 1303). Baginda bersabda bahawa beliau sebaik-baik wanita pada zamannya.'},
 h=[['bukhari',3815,'"The best of the world\'s women is Mary, and the best of the world\'s women is Khadijah."','"Sebaik-baik wanita dunia ialah Maryam, dan sebaik-baik wanita dunia ialah Khadijah."'],['bukhari',1303,'Ibrahim, the son of the Prophet ﷺ, dies as an infant: "The eyes shed tears and the heart grieves..."','Ibrahim, anak Nabi ﷺ, wafat ketika bayi: "Mata menitiskan air mata dan hati bersedih..."']],
 pop=[{'kind':'hist','en':'His trade journey for Khadijah with her servant Maysarah: told by Ibn Ishaq (Ibn Hisham, as-Sirah an-Nabawiyyah) without a checked chain.','ms':'Perjalanan dagang untuk Khadijah bersama khadamnya Maisarah: diriwayatkan oleh Ibn Ishaq (Ibn Hisyam, as-Sirah an-Nabawiyyah) tanpa sanad yang disemak.'},
      {'kind':'weak','en':'Khadijah\'s age at the marriage: "40" (he was 25) is from al-Waqidi in Ibn Sa\'d, at-Tabaqat al-Kubra 1/132, and al-Waqidi is matruk (abandoned) as a narrator; Ibn Ishaq said 28 (al-Hakim, al-Mustadrak 3/200), without a chain. No authentic report fixes her age.','ms':'Usia Khadijah ketika berkahwin: "40" (baginda 25) datang daripada al-Waqidi dalam Ibn Sa\'d, at-Tabaqat al-Kubra 1/132, dan al-Waqidi seorang perawi yang matruk (ditinggalkan); Ibn Ishaq menyebut 28 (al-Hakim, al-Mustadrak 3/200), tanpa sanad. Tiada riwayat sahih yang menetapkan usianya.','src':"Muhammad al-'Awshan, Ma Sha'a wa Lam Yathbut fi as-Sirah an-Nabawiyyah, p. 18",'url':'https://shamela.ws/book/97932/17'}])
ev(id='kabah',era='pre',ce='c. 605',when={'en':'Age about 35','ms':'Usia kira-kira 35 tahun'},
 title={'en':'Rebuilding the Ka\'bah and the Black Stone','ms':'Pembinaan semula Kaabah dan Hajarul Aswad'},
 sum={'en':'Quraysh rebuilt the Ka\'bah and he carried stones with his uncle al-\'Abbas. According to Musnad Ahmad and the historians, when the clans disputed who would put the Black Stone back in place, they accepted his judgement: he placed it on a cloth, each clan lifted a corner, and he set it with his own hand.',
      'ms':'Quraisy membina semula Kaabah dan baginda mengangkat batu bersama bapa saudaranya, al-Abbas. Menurut Musnad Ahmad dan ahli sejarah, apabila kabilah-kabilah bertelagah siapa yang akan meletakkan semula Hajarul Aswad, mereka menerima keputusannya: baginda meletakkannya di atas kain, setiap kabilah mengangkat satu penjuru, dan baginda meletakkannya dengan tangannya sendiri.'},
 h=[['bukhari',1582,'He carried stones for the Ka\'bah with al-\'Abbas.','Baginda mengangkat batu untuk Kaabah bersama al-Abbas.'],['bukhari',3829,'','']],
 ext=[{'en':'The arbitration over the Black Stone: Musnad Ahmad and al-Hakim (not in this app\'s books), and Ibn Ishaq.','ms':'Penyelesaian pertikaian Hajarul Aswad: Musnad Ahmad dan al-Hakim (tiada dalam kitab aplikasi ini), dan Ibn Ishaq.'}],
 pop=[{'kind':'hist','en':'That they called him "al-Amin" (the trustworthy) at the arbitration: told by Ibn Ishaq; the title itself is widely reported.','ms':'Bahawa mereka memanggilnya "al-Amin" (yang dipercayai) ketika itu: diriwayatkan oleh Ibn Ishaq; gelaran itu sendiri masyhur diriwayatkan.'}])
ev(id='hira',era='pre',ce='c. 605–610',when={'en':'Approaching 40','ms':'Menjelang usia 40'},
 title={'en':'Seclusion in the cave of Hira\'','ms':'Beruzlah di Gua Hira\''},
 sum={'en':'Before revelation, true dreams came to him like the light of dawn, and he came to love seclusion. He would go to the cave of Hira\' for nights of worship, taking provisions, then return to Khadijah.',
      'ms':'Sebelum wahyu, baginda mengalami mimpi benar yang jelas seperti cahaya subuh, dan baginda gemar bersendirian. Baginda pergi ke Gua Hira\' untuk beribadah beberapa malam dengan membawa bekalan, kemudian pulang kepada Khadijah.'},
 h=[['bukhari',3,'The beginning of revelation: true dreams, then seclusion in Hira\'.','Permulaan wahyu: mimpi benar, kemudian beruzlah di Hira\'.']])

# ---------------- MAKKAH ----------------
ev(id='iqra',era='mak',ce='610',when={'en':'Ramadan, 13 years before the Hijrah (age 40)','ms':'Ramadan, 13 tahun sebelum Hijrah (usia 40)'},
 title={'en':'The first revelation','ms':'Wahyu pertama'},
 sum={'en':'In the cave of Hira\', Jibril came and said "Read!", and the first verses of Surah al-\'Alaq were revealed. He returned trembling to Khadijah, who comforted him and took him to her cousin Waraqah ibn Nawfal, who said this was the angel sent to Musa.',
      'ms':'Di Gua Hira\', Jibril datang dan berkata "Bacalah!", lalu ayat-ayat pertama Surah al-\'Alaq diturunkan. Baginda pulang dalam keadaan gementar kepada Khadijah, yang menenangkannya dan membawanya kepada sepupunya, Waraqah bin Naufal, yang berkata inilah malaikat yang diutus kepada Musa.'},
 q=[[96,1,5,'The first verses revealed','Ayat pertama yang diturunkan'],[2,185,185,'The Qur\'an was sent down in Ramadan','Al-Quran diturunkan pada bulan Ramadan']],
 h=[['bukhari',3,'The full account of the first revelation, from \'Aishah.','Kisah penuh wahyu pertama, daripada Aisyah.'],['bukhari',3902,'He received revelation at forty.','Baginda menerima wahyu pada usia empat puluh.']],
 pop=[{'kind':'none','en':'17 Ramadan as the day of the first revelation: the date observed for Nuzul al-Quran in Malaysia and Singapore, but no authentic hadith fixes the day; scholars give several dates in Ramadan.','ms':'17 Ramadan sebagai hari wahyu pertama: tarikh sambutan Nuzul al-Quran di Malaysia dan Singapura, tetapi tiada hadis sahih yang menetapkan harinya; ulama menyebut beberapa tarikh dalam Ramadan.'}])
ev(id='fatrah',era='mak',ce='610',when={'en':'Soon after the first revelation','ms':'Tidak lama selepas wahyu pertama'},
 title={'en':'The pause, then "O you wrapped in your cloak"','ms':'Wahyu terhenti, kemudian "Wahai orang yang berselimut"'},
 sum={'en':'Revelation paused for a time. Then he saw the same angel between the sky and the earth, hurried home asking to be covered, and the opening verses of Surah al-Muddaththir were revealed, commanding him to rise and warn.',
      'ms':'Wahyu terhenti buat seketika. Kemudian baginda melihat malaikat yang sama di antara langit dan bumi, bergegas pulang meminta diselimutkan, lalu ayat-ayat awal Surah al-Muddaththir diturunkan, memerintahkannya bangun dan memberi peringatan.'},
 q=[[74,1,5,'Revealed after the pause','Diturunkan selepas wahyu terhenti']],
 h=[['bukhari',4,'Jabir\'s account of the pause and al-Muddaththir.','Riwayat Jabir tentang wahyu terhenti dan al-Muddaththir.']])
ev(id='first',era='mak',ce='610–613',when={'en':'The first three years (approx.)','ms':'Tiga tahun pertama (anggaran)'},
 title={'en':'The first believers and the quiet call','ms':'Golongan pertama beriman dan dakwah secara senyap'},
 sum={'en':'The first to believe were Khadijah, Abu Bakr, \'Ali (a boy in his house) and Zayd ibn Harithah. For about three years the call was made quietly, person to person. \'Ammar said that at one time the only Muslims with the Prophet ﷺ were five slaves, two women and Abu Bakr.',
      'ms':'Yang terawal beriman ialah Khadijah, Abu Bakar, Ali (seorang budak di rumah baginda) dan Zaid bin Harithah. Selama kira-kira tiga tahun, dakwah dibuat secara senyap, dari seorang ke seorang. Ammar berkata pada suatu ketika, yang bersama Nabi ﷺ hanyalah lima hamba, dua wanita dan Abu Bakar.'},
 h=[['bukhari',3660,'"There was none with him but five slaves, two women and Abu Bakr."','"Tiada bersamanya kecuali lima hamba, dua wanita dan Abu Bakar."'],['ibnmajah',150,'The first seven to declare their Islam openly.','Tujuh orang pertama yang mengisytiharkan Islam secara terbuka.']],
 pop=[{'kind':'hist','en':'That the quiet call lasted three years: told by the historians (Ibn Ishaq); the length is not fixed by a hadith.','ms':'Bahawa dakwah secara senyap berlangsung tiga tahun: diriwayatkan oleh ahli sejarah (Ibn Ishaq); tempohnya tidak ditetapkan oleh hadis.'}])
ev(id='safa',era='mak',ce='c. 613',when={'en':'About the 4th year of prophethood','ms':'Kira-kira tahun ke-4 kenabian'},
 title={'en':'The open call from as-Safa','ms':'Dakwah terbuka dari Bukit Safa'},
 sum={'en':'When "And warn your nearest kinsmen" was revealed, he climbed as-Safa and called the clans of Quraysh. When they gathered he warned them of a severe punishment; Abu Lahab cursed him, and Surah al-Masad was revealed.',
      'ms':'Apabila ayat "Dan berilah peringatan kepada kaum kerabatmu yang terdekat" diturunkan, baginda naik ke Bukit Safa dan menyeru kabilah-kabilah Quraisy. Apabila mereka berkumpul, baginda memberi amaran tentang azab yang pedih; Abu Lahab mencelanya, lalu Surah al-Masad diturunkan.'},
 q=[[26,214,214,'"And warn your nearest kinsmen"','"Dan berilah peringatan kepada kaum kerabatmu yang terdekat"'],[111,1,5,'Revealed about Abu Lahab that day','Diturunkan tentang Abu Lahab pada hari itu']],
 h=[['bukhari',4770,'The call from as-Safa and Abu Lahab\'s reply.','Seruan dari Safa dan jawapan Abu Lahab.'],['bukhari',2753,'"O people of Quraysh, save yourselves... O Fatimah..."','"Wahai kaum Quraisy, selamatkanlah diri kamu... Wahai Fatimah..."']])
ev(id='persecution',era='mak',ce='613–619',when={'en':'Years 4 to 10 of prophethood','ms':'Tahun ke-4 hingga ke-10 kenabian'},
 title={'en':'Persecution of the believers','ms':'Penindasan terhadap orang beriman'},
 sum={'en':'Quraysh tortured the weak Muslims, among them Bilal, \'Ammar and his parents, and Khabbab; Sumayyah, \'Ammar\'s mother, was killed, according to the historians. The Prophet ﷺ himself was harmed: camel entrails were thrown on him while he prostrated at the Ka\'bah, and \'Uqbah ibn Abi Mu\'ayt tried to strangle him.',
      'ms':'Quraisy menyeksa orang Islam yang lemah, antaranya Bilal, Ammar dan ibu bapanya, serta Khabbab; menurut ahli sejarah, Sumayyah, ibu Ammar, dibunuh. Nabi ﷺ sendiri disakiti: perut unta dilemparkan ke atasnya ketika baginda sujud di Kaabah, dan Uqbah bin Abi Mu\'ait cuba mencekiknya.'},
 h=[['ibnmajah',150,'The first to declare Islam, and how they were made to suffer.','Golongan pertama yang mengisytiharkan Islam, dan bagaimana mereka diseksa.'],['bukhari',240,'Camel entrails thrown on him while he prostrated.','Perut unta dilemparkan ke atasnya ketika baginda sujud.'],['bukhari',3856,'\'Uqbah tried to strangle him; Abu Bakr defended him.','Uqbah cuba mencekiknya; Abu Bakar membelanya.']],
 pop=[{'kind':'hist','en':'Bilal under a rock in the midday sun, and Sumayyah as the first martyr of Islam: told by Ibn Ishaq and others, not in the authenticated collections in this form. That Bilal kept saying "Ahad, Ahad" under torture is in Ibn Majah 150 (in this app).','ms':'Bilal ditindih batu di tengah panas, dan Sumayyah sebagai syahid pertama Islam: diriwayatkan oleh Ibn Ishaq dan lain-lain, tiada dalam himpunan hadis yang disahkan dalam bentuk ini. Bahawa Bilal terus menyebut "Ahad, Ahad" ketika diseksa ada dalam Ibn Majah 150 (dalam aplikasi ini).'}])
ev(id='habasyah',era='mak',ce='615',when={'en':'5th year of prophethood','ms':'Tahun ke-5 kenabian'},
 title={'en':'Emigration to Abyssinia','ms':'Hijrah ke Habsyah'},
 sum={'en':'To escape persecution, a group of Muslims emigrated to Abyssinia, whose Christian king, the Negus (an-Najashi), protected them. Ja\'far ibn Abi Talib explained Islam to him. The Negus later accepted Islam, and when he died the Prophet ﷺ prayed the funeral prayer for him in absence.',
      'ms':'Untuk mengelak penindasan, sekumpulan orang Islam berhijrah ke Habsyah, yang rajanya beragama Kristian, an-Najasyi, melindungi mereka. Ja\'far bin Abi Talib menerangkan Islam kepadanya. An-Najasyi kemudian memeluk Islam, dan apabila beliau wafat, Nabi ﷺ menunaikan solat jenazah ghaib untuknya.'},
 h=[['bukhari',3876,'Abu Musa\'s ship reached the Negus, where Ja\'far and his companions were.','Kapal Abu Musa sampai kepada an-Najasyi, tempat Ja\'far dan sahabat-sahabatnya berada.'],['bukhari',1327,'The funeral prayer for the Negus.','Solat jenazah untuk an-Najasyi.']],
 ext=[{'en':'Ja\'far\'s speech before the Negus: Musnad Ahmad, from Umm Salamah (not in this app\'s books); also Ibn Ishaq.','ms':'Ucapan Ja\'far di hadapan an-Najasyi: Musnad Ahmad, daripada Ummu Salamah (tiada dalam kitab aplikasi ini); juga Ibn Ishaq.'}])
ev(id='umar',era='mak',ce='616',when={'en':'About the 6th year of prophethood','ms':'Kira-kira tahun ke-6 kenabian'},
 title={'en':'Hamzah and \'Umar accept Islam','ms':'Hamzah dan Umar memeluk Islam'},
 sum={'en':'Hamzah, the Prophet\'s uncle, and then \'Umar ibn al-Khattab accepted Islam, which greatly strengthened the Muslims. The Prophet ﷺ had prayed: "O Allah, strengthen Islam with whichever of these two men is dearer to You: Abu Jahl or \'Umar."',
      'ms':'Hamzah, bapa saudara Nabi, kemudian Umar bin al-Khattab memeluk Islam, dan ini sangat menguatkan orang Islam. Nabi ﷺ pernah berdoa: "Ya Allah, muliakanlah Islam dengan salah seorang daripada dua lelaki ini yang lebih Engkau cintai: Abu Jahal atau Umar."'},
 h=[['tirmidhi',3681,'The Prophet\'s du\'a for \'Umar.','Doa Nabi untuk Umar.'],['bukhari',3864,'Quraysh gathered at \'Umar\'s house when he became Muslim.','Quraisy berkumpul di rumah Umar apabila beliau memeluk Islam.'],['bukhari',3863,'"We have been strong since \'Umar accepted Islam."','"Kami menjadi kuat sejak Umar memeluk Islam."']],
 pop=[{'kind':'weak','en':'\'Umar setting out to kill the Prophet ﷺ, striking his sister and reading Surah Taha in her house: in Ibn Sa\'d and ad-Daraqutni with a weak chain; adh-Dhahabi called it munkar.','ms':'Umar keluar untuk membunuh Nabi ﷺ, memukul adiknya dan membaca Surah Taha di rumahnya: dalam Ibn Sa\'d dan ad-Daraqutni dengan sanad yang lemah; adz-Dzahabi menyatakannya munkar.'},
      {'kind':'hist','en':'How Hamzah accepted Islam (striking Abu Jahl with his bow after Abu Jahl insulted the Prophet ﷺ): told by Ibn Ishaq; not in the authenticated collections.','ms':'Cara Hamzah memeluk Islam (memukul Abu Jahal dengan busurnya selepas Abu Jahal menghina Nabi ﷺ): diriwayatkan oleh Ibn Ishaq; tiada dalam himpunan hadis yang disahkan.'}])
ev(id='boycott',era='mak',ce='616–619',when={'en':'Years 7 to 10 of prophethood','ms':'Tahun ke-7 hingga ke-10 kenabian'},
 title={'en':'The boycott of Banu Hashim','ms':'Pemulauan Bani Hasyim'},
 sum={'en':'Quraysh swore at Khayf Bani Kinanah to boycott Banu Hashim and Banu al-Muttalib, refusing to trade or intermarry with them until they handed over the Prophet ﷺ. They were confined to the valley of Abu Talib for about three years of hardship.',
      'ms':'Quraisy bersumpah di Khaif Bani Kinanah untuk memulaukan Bani Hasyim dan Bani al-Muttalib, enggan berjual beli dan berkahwin dengan mereka sehingga mereka menyerahkan Nabi ﷺ. Mereka terkurung di lembah Abu Talib selama kira-kira tiga tahun dalam kesusahan.'},
 h=[['bukhari',1590,'The Prophet ﷺ named Khayf Bani Kinanah, "where Quraysh swore on disbelief" against Banu Hashim.','Nabi ﷺ menyebut Khaif Bani Kinanah, "tempat Quraisy bersumpah di atas kekufuran" terhadap Bani Hasyim.']],
 pop=[{'kind':'hist','en':'Termites eating the boycott document except "In Your name, O Allah": told by Ibn Ishaq and others; not in the authenticated collections.','ms':'Anai-anai memakan surat pemulauan kecuali "Dengan nama-Mu, ya Allah": diriwayatkan oleh Ibn Ishaq dan lain-lain; tiada dalam himpunan hadis yang disahkan.'}])
ev(id='qamar',era='mak',ce='c. 617',when={'en':'Makkah period (year differs)','ms':'Zaman Makkah (tahunnya berbeza)'},
 title={'en':'The splitting of the moon','ms':'Bulan terbelah'},
 sum={'en':'The people of Makkah asked for a sign, and the moon split into two parts, with Mount Hira\' between them. The Prophet ﷺ said: "Bear witness." Surah al-Qamar opens with this sign.',
      'ms':'Penduduk Makkah meminta satu tanda, lalu bulan terbelah dua, dengan Bukit Hira\' di antaranya. Nabi ﷺ bersabda: "Saksikanlah." Surah al-Qamar dimulakan dengan tanda ini.'},
 q=[[54,1,2,'"The Hour has drawn near and the moon has split"','"Telah hampir hari kiamat dan bulan telah terbelah"']],
 h=[['bukhari',3868,'They asked for a sign and saw the moon split.','Mereka meminta tanda dan melihat bulan terbelah.'],['bukhari',3869,'"Bear witness."','"Saksikanlah."']])
ev(id='huzn',era='mak',ce='619',when={'en':'10th year of prophethood','ms':'Tahun ke-10 kenabian'},
 title={'en':'Death of Abu Talib and Khadijah','ms':'Kewafatan Abu Talib dan Khadijah'},
 sum={'en':'Abu Talib, who had protected him, died without accepting Islam despite the Prophet\'s pleading at his deathbed. Khadijah died in the same period, three years before the Hijrah.',
      'ms':'Abu Talib, yang melindunginya, meninggal dunia tanpa memeluk Islam walaupun Nabi merayu ketika beliau nazak. Khadijah wafat dalam tempoh yang sama, tiga tahun sebelum Hijrah.'},
 q=[[28,56,56,'"You cannot guide whom you love": revealed about Abu Talib','"Engkau tidak dapat memberi hidayah kepada orang yang engkau kasihi": diturunkan tentang Abu Talib'],[9,113,113,'Revealed after Abu Talib\'s death','Diturunkan selepas kematian Abu Talib']],
 h=[['bukhari',3884,'The Prophet ﷺ at Abu Talib\'s deathbed.','Nabi ﷺ di sisi Abu Talib ketika nazak.'],['bukhari',3896,'Khadijah died three years before the Hijrah.','Khadijah wafat tiga tahun sebelum Hijrah.']],
 pop=[{'kind':'none','en':'The name "\'Am al-Huzn" (the Year of Sorrow): used by later writers; it does not come from a hadith.','ms':'Nama "Amul Huzni" (Tahun Kesedihan): digunakan oleh penulis kemudian; ia tidak datang daripada hadis.'}])
ev(id='taif',era='mak',ce='619',when={'en':'10th year of prophethood','ms':'Tahun ke-10 kenabian'},
 title={'en':'The journey to at-Ta\'if','ms':'Perjalanan ke Taif'},
 sum={'en':'He went to the leaders of Thaqif at at-Ta\'if, who rejected him harshly. He told \'Aishah it was harder for him than Uhud. On the way back the angel of the mountains offered to crush the people between two mountains, and he said: "I hope Allah will bring from their descendants people who worship Allah alone."',
      'ms':'Baginda pergi kepada pemimpin Thaqif di Taif, yang menolaknya dengan kasar. Baginda memberitahu Aisyah bahawa hari itu lebih berat daripada Uhud. Dalam perjalanan pulang, malaikat penjaga gunung menawarkan untuk menghimpit mereka di antara dua gunung, lalu baginda bersabda: "Aku berharap Allah akan mengeluarkan dari keturunan mereka orang yang menyembah Allah semata-mata."'},
 h=[['bukhari',3231,'"The worst I suffered from them was on the day of al-\'Aqabah..." and the angel of the mountains.','"Yang paling berat aku alami daripada mereka ialah pada hari al-\'Aqabah..." dan malaikat penjaga gunung.']],
 pop=[{'kind':'hist','en':'Children and slaves stoning him until his feet bled, and the Christian slave \'Addas: told by Ibn Ishaq and Musa ibn \'Uqbah; not in the authenticated collections.','ms':'Kanak-kanak dan hamba melontarnya dengan batu sehingga kakinya berdarah, dan kisah hamba Kristian, Addas: diriwayatkan oleh Ibn Ishaq dan Musa bin Uqbah; tiada dalam himpunan hadis yang disahkan.'},
      {'kind':'hist','en':'The du\'a "O Allah, to You I complain of my weakness...": reported by at-Tabarani and Ibn Ishaq; scholars consider its chain weak.','ms':'Doa "Ya Allah, kepada-Mu aku mengadu kelemahanku...": diriwayatkan oleh at-Tabarani dan Ibn Ishaq; ulama menilai sanadnya lemah.'}])
ev(id='jinn',era='mak',ce='619',when={'en':'Makkah period','ms':'Zaman Makkah'},
 title={'en':'The jinn listen to the Qur\'an','ms':'Jin mendengar al-Quran'},
 sum={'en':'While the Prophet ﷺ led his companions in the dawn prayer at Nakhlah on the way to \'Ukaz, a group of jinn heard the Qur\'an, believed, and returned to warn their people. Surah al-Jinn was revealed about it.',
      'ms':'Ketika Nabi ﷺ mengimamkan sahabat-sahabatnya solat subuh di Nakhlah dalam perjalanan ke \'Ukaz, sekumpulan jin mendengar al-Quran, lalu beriman dan kembali memberi peringatan kepada kaum mereka. Surah al-Jinn diturunkan tentangnya.'},
 q=[[72,1,2,'"A group of the jinn listened..."','"Sekumpulan jin telah mendengar..."'],[46,29,31,'The jinn who listened and warned their people','Jin yang mendengar dan memberi peringatan kepada kaum mereka']],
 h=[['bukhari',4921,'The jinn heard him recite in the dawn prayer.','Jin mendengar baginda membaca dalam solat subuh.'],['muslim',1006,'','']])
ev(id='isra',era='mak',ce='c. 620–621',when={'en':'A year or more before the Hijrah (date differs)','ms':'Setahun atau lebih sebelum Hijrah (tarikhnya berbeza)'},
 title={'en':'al-Isra\' and al-Mi\'raj','ms':'Israk dan Mikraj'},
 sum={'en':'He was taken by night on al-Buraq from al-Masjid al-Haram to al-Masjid al-Aqsa, then raised through the heavens, where he met the prophets. The five daily prayers were made obligatory, reduced from fifty.',
      'ms':'Baginda dibawa pada waktu malam dengan Buraq dari Masjidil Haram ke Masjidil Aqsa, kemudian diangkat melalui lapisan langit dan bertemu para nabi. Solat lima waktu difardukan, dikurangkan daripada lima puluh.'},
 q=[[17,1,1,'The Night Journey','Perjalanan malam'],[53,13,18,'What he saw at the Lote Tree','Apa yang baginda lihat di Sidratul Muntaha']],
 h=[['bukhari',3887,'The full account from Malik ibn Sa\'sa\'ah.','Riwayat penuh daripada Malik bin Sa\'sa\'ah.'],['bukhari',349,'His chest opened and washed with Zamzam; the prayers made obligatory.','Dadanya dibelah dan dibasuh dengan air zamzam; solat difardukan.'],['muslim',411,'al-Buraq and al-Aqsa.','Buraq dan al-Aqsa.']],
 pop=[{'kind':'none','en':'27 Rajab as the date: widely observed, but no authentic report fixes it; scholars differ even on the month and the year.','ms':'27 Rejab sebagai tarikhnya: disambut secara meluas, tetapi tiada riwayat sahih yang menetapkannya; ulama berbeza pendapat walaupun tentang bulan dan tahunnya.'}])
ev(id='aqabah',era='mak',ce='621–622',when={'en':'The last two Hajj seasons before the Hijrah','ms':'Dua musim haji terakhir sebelum Hijrah'},
 title={'en':'The pledges of al-\'Aqabah','ms':'Baiah al-Aqabah'},
 sum={'en':'He offered Islam to the tribes at the pilgrimage. Men of the Aws and Khazraj from Yathrib accepted, and at al-\'Aqabah in Mina pledged themselves to him, first twelve, then seventy-three men and two women. He sent Mus\'ab ibn \'Umayr with them to teach the Qur\'an.',
      'ms':'Baginda menawarkan Islam kepada kabilah-kabilah pada musim haji. Lelaki-lelaki Aus dan Khazraj dari Yathrib menerimanya dan berbaiah kepadanya di al-Aqabah, Mina, mula-mula dua belas orang, kemudian tujuh puluh tiga lelaki dan dua wanita. Baginda mengutus Mus\'ab bin Umair bersama mereka untuk mengajar al-Quran.'},
 h=[['bukhari',18,'The terms of the pledge, from \'Ubadah ibn as-Samit, a leader at al-\'Aqabah.','Syarat-syarat baiah, daripada Ubadah bin as-Samit, seorang naqib di al-Aqabah.'],['bukhari',3892,'',''],['bukhari',3925,'The first to come to Madinah: Mus\'ab ibn \'Umayr and Ibn Umm Maktum.','Yang terawal sampai ke Madinah: Mus\'ab bin Umair dan Ibn Ummi Maktum.']],
 pop=[{'kind':'hist','en':'The numbers (12, then 73 men and 2 women): from Ibn Ishaq and other historians.','ms':'Bilangannya (12, kemudian 73 lelaki dan 2 wanita): daripada Ibn Ishaq dan ahli sejarah lain.'}])
ev(id='hijrah',era='mak',ce='622',when={'en':'Rabi\' al-Awwal, 1 AH','ms':'Rabiulawal, tahun 1 Hijrah'},
 title={'en':'The Hijrah to Madinah','ms':'Hijrah ke Madinah'},
 sum={'en':'Quraysh plotted to kill him. He left with Abu Bakr, and they hid three nights in the cave of Thawr while searchers stood above them; he said: "What do you think of two whose third is Allah?" Suraqah ibn Malik chased them, but his horse sank into the ground and he turned back.',
      'ms':'Quraisy merancang untuk membunuhnya. Baginda keluar bersama Abu Bakar, dan mereka bersembunyi tiga malam di Gua Thur sementara pemburu berdiri di atas mereka; baginda bersabda: "Apa sangkaanmu terhadap dua orang yang ketiganya ialah Allah?" Suraqah bin Malik mengejar mereka, tetapi kaki kudanya terbenam ke dalam tanah dan beliau berpatah balik.'},
 q=[[9,40,40,'"The second of two, when they were in the cave"','"Salah seorang daripada dua orang ketika mereka berada dalam gua"'],[8,30,30,'Quraysh\'s plot','Rancangan jahat Quraisy']],
 h=[['bukhari',3905,'\'Aishah\'s full account of the Hijrah.','Kisah penuh Hijrah daripada Aisyah.'],['bukhari',3653,'"What do you think of two whose third is Allah?"','"Apa sangkaanmu terhadap dua orang yang ketiganya ialah Allah?"'],['bukhari',3906,'Suraqah\'s pursuit, in his own words.','Pengejaran Suraqah, dalam kata-katanya sendiri.']],
 pop=[{'kind':'disputed','en':'The spider\'s web over the mouth of the cave: Musnad Ahmad; Ibn Hajar and Ibn Kathir called its chain hasan, al-Albani graded it weak.','ms':'Sarang labah-labah di pintu gua: Musnad Ahmad; Ibn Hajar dan Ibn Kathir menilai sanadnya hasan, al-Albani menilainya lemah.'},
      {'kind':'none','en':'The two doves nesting at the cave: Ibn Kathir called it "very strange" (gharib jiddan); al-Albani said there is no authentic hadith about the spider and the doves.','ms':'Sepasang merpati bersarang di gua: Ibn Kathir menyatakannya "sangat gharib"; al-Albani berkata tiada hadis sahih tentang labah-labah dan merpati.'},
      {'kind':'hist','en':'\'Ali sleeping in the Prophet\'s bed on the night he left, and the tent of Umm Ma\'bad: told by the historians and in collections outside this app; scholars differ on their chains.','ms':'Ali tidur di tempat tidur Nabi pada malam baginda keluar, dan kisah khemah Ummu Ma\'bad: diriwayatkan oleh ahli sejarah dan dalam kitab di luar aplikasi ini; ulama berbeza tentang sanadnya.'}])

# ---------------- MADINAH ----------------
ev(id='madinah',era='mad',ce='622',when={'en':'Rabi\' al-Awwal, 1 AH','ms':'Rabiulawal, tahun 1 Hijrah'},
 title={'en':'Arrival: Quba\' and the Prophet\'s Mosque','ms':'Ketibaan: Quba\' dan Masjid Nabawi'},
 sum={'en':'He stayed some days at Quba\' among Banu \'Amr ibn \'Awf and founded its mosque, then rode into Madinah. Where his camel knelt, he bought the land from two orphans of Banu an-Najjar and built his mosque, carrying bricks with his companions.',
      'ms':'Baginda tinggal beberapa hari di Quba\' dalam Bani Amr bin Auf dan mengasaskan masjidnya, kemudian menunggang masuk ke Madinah. Di tempat untanya berhenti, baginda membeli tanah daripada dua anak yatim Bani an-Najjar dan membina masjidnya, mengangkat bata bersama sahabat-sahabatnya.'},
 q=[[9,108,108,'"A mosque founded on piety from the first day": al-Bukhari\'s report says this of Quba\'; a hadith in Sahih Muslim applies it to the Prophet\'s Mosque','"Masjid yang diasaskan atas takwa sejak hari pertama": riwayat al-Bukhari menyebutnya tentang Quba\'; satu hadis dalam Sahih Muslim mengaitkannya dengan Masjid Nabawi']],
 h=[['bukhari',3906,'His stay at Quba\' and entry into Madinah (end of the hadith).','Baginda tinggal di Quba\' dan masuk ke Madinah (hujung hadis).'],['bukhari',428,'Building the mosque on the land of Banu an-Najjar.','Membina masjid di atas tanah Bani an-Najjar.']],
 pop=[{'kind':'weak','en':'"Tala\'a al-badru \'alayna" sung on his arrival: al-\'Iraqi and Ibn Hajar called it problematic, al-Albani graded its chain weak (several narrators missing).','ms':'"Tala\'al badru \'alaina" dinyanyikan ketika baginda tiba: al-\'Iraqi dan Ibn Hajar menyatakannya bermasalah, al-Albani menilai sanadnya lemah (beberapa perawi tercicir).'}])
ev(id='ukhuwwah',era='mad',ce='622',when={'en':'1 AH','ms':'Tahun 1 Hijrah'},
 title={'en':'Brotherhood of the Muhajirin and Ansar','ms':'Persaudaraan Muhajirin dan Ansar'},
 sum={'en':'He joined each emigrant from Makkah with a man of the Ansar as brothers. Sa\'d ibn ar-Rabi\' offered \'Abd ar-Rahman ibn \'Awf half his wealth; \'Abd ar-Rahman asked only to be shown the market.',
      'ms':'Baginda mempersaudarakan setiap Muhajirin dari Makkah dengan seorang lelaki Ansar. Sa\'d bin ar-Rabi\' menawarkan separuh hartanya kepada Abdul Rahman bin Auf; Abdul Rahman hanya meminta ditunjukkan pasar.'},
 q=[[59,9,9,'The Ansar "prefer them over themselves"','Ansar "mengutamakan mereka atas diri mereka sendiri"']],
 h=[['bukhari',3780,'Sa\'d ibn ar-Rabi\' and \'Abd ar-Rahman ibn \'Awf.','Sa\'d bin ar-Rabi\' dan Abdul Rahman bin Auf.'],['bukhari',2049,'','']],
 pop=[{'kind':'hist','en':'The "Constitution of Madinah" (Sahifat al-Madinah) between Muslims and Jews: its text comes from Ibn Ishaq without a chain and from Abu \'Ubayd; parts are supported by hadith, the full document is not authenticated.','ms':'"Piagam Madinah" (Sahifah al-Madinah) antara orang Islam dan Yahudi: teksnya daripada Ibn Ishaq tanpa sanad dan daripada Abu \'Ubaid; sebahagiannya disokong hadis, dokumen penuhnya tidak disahkan.'}])
ev(id='adhan',era='mad',ce='622–623',when={'en':'1 AH','ms':'Tahun 1 Hijrah'},
 title={'en':'The adhan','ms':'Azan disyariatkan'},
 sum={'en':'The Muslims discussed how to call people to prayer. \'Abdullah ibn Zayd saw the words of the adhan in a dream; the Prophet ﷺ confirmed it and had Bilal call it. \'Umar had seen the same.',
      'ms':'Orang Islam berbincang bagaimana memanggil orang untuk solat. Abdullah bin Zaid melihat lafaz azan dalam mimpi; Nabi ﷺ mengesahkannya dan menyuruh Bilal melaungkannya. Umar juga telah melihat perkara yang sama.'},
 h=[['bukhari',604,'The discussion, and Bilal called to prayer.','Perbincangan itu, dan Bilal melaungkan seruan solat.'],['abudawud',499,'\'Abdullah ibn Zayd\'s dream of the adhan.','Mimpi Abdullah bin Zaid tentang azan.']])
ev(id='qiblah',era='mad',ce='624',when={'en':'Rajab or Sha\'ban, 2 AH (16 or 17 months after the Hijrah)','ms':'Rejab atau Syaaban, tahun 2 Hijrah (16 atau 17 bulan selepas Hijrah)'},
 title={'en':'The qiblah turned to the Ka\'bah','ms':'Kiblat bertukar ke Kaabah'},
 sum={'en':'For sixteen or seventeen months in Madinah he prayed towards Jerusalem, wishing to face the Ka\'bah. Then Allah revealed "Turn your face towards al-Masjid al-Haram".',
      'ms':'Selama enam belas atau tujuh belas bulan di Madinah, baginda solat menghadap Baitulmaqdis sambil berharap untuk menghadap Kaabah. Kemudian Allah menurunkan "Palingkanlah wajahmu ke arah Masjidil Haram".'},
 q=[[2,142,150,'The change of qiblah','Perubahan kiblat']],
 h=[['bukhari',40,'Sixteen or seventeen months facing Jerusalem.','Enam belas atau tujuh belas bulan menghadap Baitulmaqdis.'],['bukhari',4486,'','']])
ev(id='badr',era='mad',ce='624',when={'en':'17 Ramadan, 2 AH','ms':'17 Ramadan, tahun 2 Hijrah'},
 title={'en':'The Battle of Badr','ms':'Perang Badar'},
 sum={'en':'About 313 Muslims met an army of about a thousand from Quraysh at Badr. The Prophet ﷺ prayed earnestly through the night for Allah\'s promised help; Allah sent angels, and Quraysh were defeated, with Abu Jahl among the dead. Allah calls it "the Day of the Criterion".',
      'ms':'Kira-kira 313 orang Islam berhadapan dengan tentera Quraisy seramai kira-kira seribu orang di Badar. Nabi ﷺ berdoa bersungguh-sungguh sepanjang malam memohon pertolongan yang dijanjikan Allah; Allah mengutus malaikat, dan Quraisy tewas, termasuk Abu Jahal yang terbunuh. Allah menamakannya "Hari al-Furqan".'},
 q=[[8,5,19,'The battle and its lessons','Peperangan dan pengajarannya'],[8,41,41,'"The Day of the Criterion, the day the two armies met"','"Hari al-Furqan, hari bertemunya dua pasukan"'],[3,123,127,'"Allah gave you victory at Badr when you were weak"','"Allah telah menolong kamu di Badar sedang kamu lemah"']],
 h=[['muslim',4588,'His du\'a before the battle and the help of the angels.','Doa baginda sebelum peperangan dan bantuan malaikat.'],['bukhari',3957,'Their number was that of Talut\'s companions who crossed the river: three hundred and ten-odd.','Bilangan mereka sama dengan sahabat Talut yang menyeberangi sungai: tiga ratus sepuluh lebih.'],['bukhari',3963,'The death of Abu Jahl.','Kematian Abu Jahal.']],
 pop=[{'kind':'none','en':'17 Ramadan is the date most historians give, though 19 Ramadan is also reported; the day is not fixed by a hadith in this app\'s books.','ms':'17 Ramadan ialah tarikh yang disebut oleh kebanyakan ahli sejarah, walaupun 19 Ramadan juga diriwayatkan; harinya tidak ditetapkan oleh hadis dalam kitab aplikasi ini.'}])
ev(id='qaynuqa',era='mad',ce='624',when={'en':'Shawwal, 2 AH (according to the historians)','ms':'Syawal, tahun 2 Hijrah (menurut ahli sejarah)'},
 title={'en':'Banu Qaynuqa\' expelled','ms':'Bani Qainuqa\' diusir'},
 sum={'en':'The Jewish tribe of Banu Qaynuqa\' broke their covenant after Badr; they were besieged and then expelled from Madinah.',
      'ms':'Kabilah Yahudi Bani Qainuqa\' melanggar perjanjian selepas Badar; mereka dikepung dan kemudian diusir dari Madinah.'},
 h=[['abudawud',3001,'He gathered them in their market after Badr (see the gradings: weak).','Baginda mengumpulkan mereka di pasar mereka selepas Badar (lihat hukumnya: lemah).'],['bukhari',4028,'The Jews of Madinah and their expulsion.','Yahudi Madinah dan pengusiran mereka.']],
 pop=[{'kind':'hist','en':'The cause (a Muslim woman humiliated in their market): told by the historians; not authenticated.','ms':'Puncanya (seorang wanita Islam dimalukan di pasar mereka): diriwayatkan oleh ahli sejarah; tidak disahkan.'}])
ev(id='uhud',era='mad',ce='625',when={'en':'Shawwal, 3 AH','ms':'Syawal, tahun 3 Hijrah'},
 title={'en':'The Battle of Uhud','ms':'Perang Uhud'},
 sum={'en':'Quraysh came for revenge. The Prophet ﷺ placed fifty archers on a hill under \'Abdullah ibn Jubayr and told them not to leave it. When most left it to gather booty, Khalid ibn al-Walid\'s cavalry attacked from behind. About seventy Muslims were killed, among them Hamzah, and the Prophet ﷺ was wounded.',
      'ms':'Quraisy datang untuk membalas dendam. Nabi ﷺ menempatkan lima puluh pemanah di atas bukit di bawah Abdullah bin Jubair dan melarang mereka meninggalkannya. Apabila kebanyakan mereka meninggalkannya untuk mengutip harta rampasan, pasukan berkuda Khalid bin al-Walid menyerang dari belakang. Kira-kira tujuh puluh orang Islam gugur, termasuk Hamzah, dan Nabi ﷺ cedera.'},
 q=[[3,121,175,'Uhud, its causes and lessons','Uhud, sebab dan pengajarannya'],[33,23,23,'"Among the believers are men true to their covenant": about Anas ibn an-Nadr and those killed at Uhud','"Di antara orang beriman ada lelaki yang menepati janji mereka": tentang Anas bin an-Nadr dan yang gugur di Uhud'],[3,152,152,'"...until you lost courage and disputed about the order"','"...sehingga kamu menjadi lemah dan berbantah-bantahan tentang perintah itu"']],
 h=[['bukhari',3039,'Fifty archers under \'Abdullah ibn Jubayr, and how the battle turned.','Lima puluh pemanah di bawah Abdullah bin Jubair, dan bagaimana peperangan berubah.'],['bukhari',4043,'',''],['bukhari',4072,'How Hamzah was killed, told by Wahshi himself.','Bagaimana Hamzah dibunuh, diceritakan oleh Wahsyi sendiri.'],['bukhari',4051,'"When two of your parties almost lost heart" (3:122).','"Ketika dua golongan daripada kamu hampir hilang semangat" (3:122).'],['bukhari',2805,'Anas ibn an-Nadr at Uhud, and 33:23 revealed about him and those like him.','Anas bin an-Nadr di Uhud, dan 33:23 diturunkan tentangnya dan orang sepertinya.']],
 pop=[{'kind':'hist','en':'Hind bint \'Utbah chewing Hamzah\'s liver: told by Ibn Ishaq and later biographers; the mutilation of his body is reported in authentic narrations, the liver detail is not.','ms':'Hindun binti Utbah mengunyah hati Hamzah: diriwayatkan oleh Ibn Ishaq dan penulis sirah kemudian; pencincangan jasadnya diriwayatkan dalam riwayat sahih, butiran tentang hati tidak.'}])
ev(id='maunah',era='mad',ce='625',when={'en':'Safar, 4 AH','ms':'Safar, tahun 4 Hijrah'},
 title={'en':'Ar-Raji\' and Bi\'r Ma\'unah','ms':'Peristiwa ar-Raji\' dan Bi\'r Ma\'unah'},
 sum={'en':'Two groups of Muslims sent to teach were betrayed. At ar-Raji\' ten were attacked and Khubayb was later executed in Makkah; at Bi\'r Ma\'unah about seventy reciters of the Qur\'an were killed. The Prophet ﷺ supplicated against their killers for a month.',
      'ms':'Dua kumpulan orang Islam yang diutus untuk mengajar dikhianati. Di ar-Raji\', sepuluh orang diserang dan Khubaib kemudian dibunuh di Makkah; di Bi\'r Ma\'unah, kira-kira tujuh puluh qari al-Quran dibunuh. Nabi ﷺ berdoa ke atas pembunuh mereka selama sebulan.'},
 h=[['bukhari',3989,'Ar-Raji\' and Khubayb.','Ar-Raji\' dan Khubaib.'],['bukhari',4088,'The seventy reciters at Bi\'r Ma\'unah.','Tujuh puluh qari di Bi\'r Ma\'unah.'],['bukhari',4092,'"By the Lord of the Ka\'bah, I have succeeded!"','"Demi Tuhan Kaabah, aku telah berjaya!"']])
ev(id='nadir',era='mad',ce='625',when={'en':'Rabi\' al-Awwal, 4 AH','ms':'Rabiulawal, tahun 4 Hijrah'},
 title={'en':'Banu an-Nadir expelled','ms':'Bani an-Nadhir diusir'},
 sum={'en':'The Jewish tribe of Banu an-Nadir broke their covenant and plotted against the Prophet ﷺ. They were besieged and left Madinah, mostly for Khaybar. Surah al-Hashr was revealed about them.',
      'ms':'Kabilah Yahudi Bani an-Nadhir melanggar perjanjian dan berkomplot terhadap Nabi ﷺ. Mereka dikepung dan meninggalkan Madinah, kebanyakannya ke Khaibar. Surah al-Hasyr diturunkan tentang mereka.'},
 q=[[59,2,6,'Revealed about Banu an-Nadir','Diturunkan tentang Bani an-Nadhir']],
 h=[['bukhari',4029,'"Call it Surat an-Nadir."','"Namakanlah ia Surah an-Nadhir."'],['bukhari',4031,'The palm trees, and 59:5.','Pohon-pohon kurma, dan 59:5.']],
 pop=[{'kind':'hist','en':'Their plot to drop a stone on him from a roof: told by Ibn Ishaq and others; reported with differing chains.','ms':'Komplot mereka untuk menjatuhkan batu ke atasnya dari bumbung: diriwayatkan oleh Ibn Ishaq dan lain-lain; diriwayatkan dengan sanad yang berbeza-beza.'}])
ev(id='ifk',era='mad',ce='627',when={'en':'Sha\'ban, 5 or 6 AH','ms':'Syaaban, tahun 5 atau 6 Hijrah'},
 title={'en':'Banu al-Mustaliq and the slander against \'Aishah','ms':'Bani al-Mustaliq dan fitnah terhadap Aisyah'},
 sum={'en':'On the return from the campaign against Banu al-Mustaliq, \'Aishah was left behind looking for her necklace and was brought back by Safwan ibn al-Mu\'attal. The hypocrites spread a slander. After a month of distress, Allah declared her innocence in Surah an-Nur.',
      'ms':'Dalam perjalanan pulang dari ekspedisi menentang Bani al-Mustaliq, Aisyah tertinggal kerana mencari kalungnya dan dibawa pulang oleh Safwan bin al-Mu\'attal. Golongan munafik menyebarkan fitnah. Selepas sebulan dalam kesedihan, Allah mengisytiharkan kesuciannya dalam Surah an-Nur.'},
 q=[[24,11,26,'Her innocence declared','Kesuciannya diisytiharkan'],[63,8,8,'"If we return to Madinah..." said by the chief hypocrite on that campaign','"Jika kita kembali ke Madinah..." kata ketua munafik dalam ekspedisi itu']],
 h=[['bukhari',4141,'\'Aishah\'s own full account.','Kisah penuh oleh Aisyah sendiri.'],['bukhari',4900,'Zayd ibn Arqam and \'Abdullah ibn Ubayy.','Zaid bin Arqam dan Abdullah bin Ubai.']])
ev(id='khandaq',era='mad',ce='627',when={'en':'Shawwal, 5 AH','ms':'Syawal, tahun 5 Hijrah'},
 title={'en':'The Trench (al-Ahzab)','ms':'Perang Khandak (al-Ahzab)'},
 sum={'en':'A confederate army of about ten thousand besieged Madinah. The Muslims dug a trench, the Prophet ﷺ digging with them in hunger and cold. After weeks, Allah sent a wind and unseen forces, and the confederates withdrew.',
      'ms':'Tentera bersekutu seramai kira-kira sepuluh ribu orang mengepung Madinah. Orang Islam menggali parit, dan Nabi ﷺ menggali bersama mereka dalam keadaan lapar dan sejuk. Selepas beberapa minggu, Allah menghantar angin dan tentera yang tidak kelihatan, lalu tentera bersekutu berundur.'},
 q=[[33,9,25,'The siege and its end','Pengepungan dan pengakhirannya']],
 h=[['bukhari',4099,'Digging the trench and the verses they chanted.','Menggali parit dan syair yang mereka lantunkan.'],['bukhari',4101,'The great rock, and the Prophet\'s hunger.','Batu besar, dan kelaparan Nabi.'],['bukhari',4103,'\'Aishah on 33:10.','Aisyah tentang 33:10.']],
 pop=[{'kind':'hist','en':'That Salman al-Farisi suggested the trench: told by the historians (al-Waqidi and others); not in the authenticated collections.','ms':'Bahawa Salman al-Farisi mencadangkan parit: diriwayatkan oleh ahli sejarah (al-Waqidi dan lain-lain); tiada dalam himpunan hadis yang disahkan.'}])
ev(id='qurayzah',era='mad',ce='627',when={'en':'Dhu al-Qa\'dah, 5 AH','ms':'Zulkaedah, tahun 5 Hijrah'},
 title={'en':'Banu Qurayzah','ms':'Bani Quraizah'},
 sum={'en':'Banu Qurayzah had betrayed their treaty during the siege. After the confederates left, Jibril told the Prophet ﷺ to go to them; they were besieged and agreed to accept the judgement of Sa\'d ibn Mu\'adh, their former ally.',
      'ms':'Bani Quraizah telah mengkhianati perjanjian mereka semasa pengepungan. Selepas tentera bersekutu pergi, Jibril menyuruh Nabi ﷺ pergi kepada mereka; mereka dikepung dan bersetuju menerima keputusan Sa\'d bin Mu\'adz, bekas sekutu mereka.'},
 q=[[33,26,27,'Revealed about them','Diturunkan tentang mereka']],
 h=[['bukhari',4117,'Jibril came as he laid down his arms.','Jibril datang ketika baginda meletakkan senjata.'],['bukhari',4119,'"None of you should pray \'Asr except at Banu Qurayzah."','"Jangan seorang pun daripada kamu solat Asar kecuali di Bani Quraizah."'],['bukhari',4121,'The judgement of Sa\'d ibn Mu\'adh.','Keputusan Sa\'d bin Mu\'adz.']])
ev(id='hudaybiyah',era='mad',ce='628',when={'en':'Dhu al-Qa\'dah, 6 AH','ms':'Zulkaedah, tahun 6 Hijrah'},
 title={'en':'The Treaty of al-Hudaybiyah','ms':'Perjanjian Hudaibiyah'},
 sum={'en':'He set out with about 1,400 Companions for \'umrah and was stopped by Quraysh at al-Hudaybiyah. The Companions pledged themselves under the tree (Bay\'at ar-Ridwan). A ten-year truce was agreed on terms that seemed harsh, and on the way back Surah al-Fath called it "a clear victory".',
      'ms':'Baginda keluar bersama kira-kira 1,400 sahabat untuk umrah dan dihalang oleh Quraisy di Hudaibiyah. Para sahabat berbaiah di bawah pokok (Baiah ar-Ridwan). Gencatan senjata sepuluh tahun dipersetujui dengan syarat yang kelihatan berat, dan dalam perjalanan pulang Surah al-Fath menamakannya "kemenangan yang nyata".'},
 q=[[48,1,1,'"We have given you a clear victory"','"Sesungguhnya Kami telah memberikan kemenangan yang nyata"'],[48,18,18,'The pledge under the tree','Baiah di bawah pokok']],
 h=[['bukhari',2731,'The full account of al-Hudaybiyah and the treaty.','Kisah penuh Hudaibiyah dan perjanjiannya.'],['bukhari',4154,'"We were 1,400 on the day of al-Hudaybiyah" (Jabir).','"Kami seramai 1,400 orang pada hari Hudaibiyah" (Jabir).'],['bukhari',4155,'Ibn Abi Awfa: those under the tree numbered 1,300.','Ibn Abi Aufa: yang berbaiah di bawah pokok berjumlah 1,300.'],['bukhari',4177,'Surah al-Fath revealed on the way back.','Surah al-Fath diturunkan dalam perjalanan pulang.']])
ev(id='letters',era='mad',ce='628–629',when={'en':'6 to 7 AH','ms':'Tahun 6 hingga 7 Hijrah'},
 title={'en':'Letters to the kings','ms':'Surat kepada raja-raja'},
 sum={'en':'After al-Hudaybiyah he wrote to rulers inviting them to Islam: Heraclius of Rome, Chosroes of Persia, the Muqawqis of Egypt, the Negus and others. Heraclius questioned Abu Sufyan about him; Chosroes tore up the letter.',
      'ms':'Selepas Hudaibiyah, baginda menulis surat kepada pemerintah-pemerintah, menyeru mereka kepada Islam: Heraclius dari Rom, Kisra dari Parsi, al-Muqauqis dari Mesir, an-Najasyi dan lain-lain. Heraclius bertanya Abu Sufyan tentang baginda; Kisra mengoyakkan surat itu.'},
 q=[[3,64,64,'The verse quoted in the letter to Heraclius','Ayat yang dipetik dalam surat kepada Heraclius']],
 h=[['bukhari',7,'Heraclius and Abu Sufyan, with the text of the letter.','Heraclius dan Abu Sufyan, berserta teks surat itu.'],['bukhari',4424,'Chosroes tore up the letter.','Kisra mengoyakkan surat itu.']])
ev(id='khaybar',era='mad',ce='628',when={'en':'Muharram, 7 AH','ms':'Muharam, tahun 7 Hijrah'},
 title={'en':'Khaybar','ms':'Perang Khaibar'},
 sum={'en':'He marched on Khaybar, the fortified Jewish oasis from which the confederates had been rallied. The forts fell one by one; he gave the banner to \'Ali, "a man who loves Allah and His Messenger", and the last forts were taken.',
      'ms':'Baginda mara ke Khaibar, oasis Yahudi berkubu yang menjadi tempat penghimpunan tentera bersekutu. Kubu-kubunya jatuh satu demi satu; baginda menyerahkan panji kepada Ali, "seorang lelaki yang mencintai Allah dan Rasul-Nya", dan kubu-kubu terakhir ditawan.'},
 q=[[48,20,20,'"Allah has promised you much booty" (explained by the mufassirun as Khaybar and what followed)','"Allah menjanjikan kepada kamu harta rampasan yang banyak" (ditafsirkan oleh ahli tafsir sebagai Khaibar dan selepasnya)']],
 h=[['bukhari',4197,'Arriving at Khaybar in the morning.','Tiba di Khaibar pada waktu pagi.'],['bukhari',4210,'The banner given to \'Ali.','Panji diserahkan kepada Ali.']])
ev(id='qada',era='mad',ce='629',when={'en':'Dhu al-Qa\'dah, 7 AH','ms':'Zulkaedah, tahun 7 Hijrah'},
 title={'en':'The \'Umrah of Fulfilment (al-Qada\')','ms':'Umrah al-Qada\''},
 sum={'en':'As the treaty allowed, he performed \'umrah with his Companions a year after al-Hudaybiyah and stayed three days in Makkah.',
      'ms':'Seperti yang dibenarkan oleh perjanjian, baginda menunaikan umrah bersama sahabat-sahabatnya setahun selepas Hudaibiyah dan tinggal tiga hari di Makkah.'},
 q=[[48,27,27,'"You will surely enter al-Masjid al-Haram..."','"Sesungguhnya kamu pasti akan memasuki Masjidil Haram..."']],
 h=[['bukhari',4251,'The terms, and the three days in Makkah.','Syarat-syaratnya, dan tiga hari di Makkah.']])
ev(id='mutah',era='mad',ce='629',when={'en':'Jumada al-Ula, 8 AH','ms':'Jamadilawal, tahun 8 Hijrah'},
 title={'en':'The Battle of Mu\'tah','ms':'Perang Mu\'tah'},
 sum={'en':'An army of three thousand faced the Byzantines and their allies at Mu\'tah. The commanders Zayd ibn Harithah, Ja\'far ibn Abi Talib and \'Abdullah ibn Rawahah were killed one after another; Khalid ibn al-Walid took the banner and withdrew the army. The Prophet ﷺ told the people in Madinah of their deaths before the news came.',
      'ms':'Tentera seramai tiga ribu orang berhadapan dengan Rom dan sekutunya di Mu\'tah. Panglima-panglima Zaid bin Harithah, Ja\'far bin Abi Talib dan Abdullah bin Rawahah gugur seorang demi seorang; Khalid bin al-Walid mengambil panji dan menarik balik tentera. Nabi ﷺ memberitahu penduduk Madinah tentang kematian mereka sebelum berita itu sampai.'},
 h=[['bukhari',4261,'The three commanders appointed in order.','Tiga panglima yang dilantik mengikut giliran.'],['bukhari',4262,'He told of their deaths while his eyes shed tears.','Baginda memberitahu kematian mereka dengan air mata berlinang.']])
ev(id='fath',era='mad',ce='630',when={'en':'Ramadan, 8 AH','ms':'Ramadan, tahun 8 Hijrah'},
 title={'en':'The Conquest of Makkah','ms':'Pembukaan Kota Makkah'},
 sum={'en':'Quraysh\'s allies broke the truce. He marched with about ten thousand and entered Makkah almost without fighting. He destroyed the 360 idols around the Ka\'bah, reciting "Truth has come and falsehood has vanished", and pardoned its people.',
      'ms':'Sekutu Quraisy melanggar perjanjian damai. Baginda mara bersama kira-kira sepuluh ribu orang dan memasuki Makkah hampir tanpa pertempuran. Baginda memusnahkan 360 berhala di sekeliling Kaabah sambil membaca "Kebenaran telah datang dan kebatilan telah lenyap", dan memaafkan penduduknya.'},
 q=[[17,81,81,'Recited as he struck the idols','Dibaca ketika baginda memukul berhala'],[110,1,3,'Surah an-Nasr: the sign of his approaching death, as Ibn \'Abbas explained','Surah an-Nasr: tanda hampirnya ajal baginda, seperti yang dijelaskan Ibn Abbas']],
 h=[['bukhari',4280,'The march, Abu Sufyan, and the entry into Makkah.','Perjalanan, Abu Sufyan, dan kemasukan ke Makkah.'],['bukhari',4287,'The 360 idols and 17:81.','360 berhala dan 17:81.'],['bukhari',4294,'Ibn \'Abbas on Surah an-Nasr.','Ibn Abbas tentang Surah an-Nasr.']],
 pop=[{'kind':'weak','en':'"Go, for you are free (at-tulaqa\')": reported by Ibn Ishaq and al-Bayhaqi with an incomplete chain; the general pardon itself is established.','ms':'"Pergilah, kamu semua bebas (at-tulaqa\')": diriwayatkan oleh Ibn Ishaq dan al-Baihaqi dengan sanad yang tidak bersambung; pengampunan umum itu sendiri sabit.'}])
ev(id='hunayn',era='mad',ce='630',when={'en':'Shawwal, 8 AH','ms':'Syawal, tahun 8 Hijrah'},
 title={'en':'Hunayn and at-Ta\'if','ms':'Perang Hunain dan Taif'},
 sum={'en':'At Hunayn the large Muslim army was ambushed by Hawazin and many fled; the Prophet ﷺ held his ground, saying "I am the Prophet, no lie", and the Muslims rallied and won. He then besieged at-Ta\'if without taking it. He gave much of the booty to new Muslims of Quraysh and comforted the Ansar.',
      'ms':'Di Hunain, tentera Islam yang besar diserang hendap oleh Hawazin dan ramai yang lari; Nabi ﷺ tetap teguh sambil bersabda "Akulah Nabi, bukan dusta", lalu orang Islam berkumpul semula dan menang. Baginda kemudian mengepung Taif tanpa menawannya. Baginda memberikan banyak harta rampasan kepada Quraisy yang baru memeluk Islam dan menenangkan hati golongan Ansar.'},
 q=[[9,25,26,'"On the day of Hunayn when your great numbers pleased you"','"Pada hari Hunain ketika bilangan kamu yang ramai menyebabkan kamu bangga"']],
 h=[['bukhari',4315,'"I am the Prophet, no lie; I am the son of \'Abd al-Muttalib."','"Akulah Nabi, bukan dusta; akulah anak Abdul Muttalib."'],['bukhari',4325,'The siege of at-Ta\'if.','Pengepungan Taif.'],['bukhari',4330,'His words to the Ansar about the booty.','Sabdanya kepada Ansar tentang harta rampasan.']])
ev(id='tabuk',era='mad',ce='630',when={'en':'Rajab, 9 AH','ms':'Rejab, tahun 9 Hijrah'},
 title={'en':'The expedition of Tabuk','ms':'Ekspedisi Tabuk'},
 sum={'en':'In extreme heat and hardship he led about thirty thousand towards the Byzantine frontier at Tabuk; no battle took place. Three sincere believers, among them Ka\'b ibn Malik, stayed behind without excuse; they were boycotted for fifty days until Allah accepted their repentance.',
      'ms':'Dalam panas terik dan kesusahan, baginda memimpin kira-kira tiga puluh ribu orang ke sempadan Rom di Tabuk; tiada peperangan berlaku. Tiga orang mukmin yang ikhlas, antaranya Ka\'b bin Malik, tertinggal tanpa uzur; mereka dipulaukan selama lima puluh hari sehingga Allah menerima taubat mereka.'},
 q=[[9,38,42,'The call to march','Seruan untuk berangkat'],[9,117,118,'The repentance of the three','Taubat tiga orang itu']],
 h=[['bukhari',4418,'Ka\'b ibn Malik\'s own full account.','Kisah penuh Ka\'b bin Malik sendiri.'],['bukhari',4416,'\'Ali left in charge of Madinah: "like Harun to Musa".','Ali ditinggalkan menjaga Madinah: "seperti Harun kepada Musa".']])
ev(id='baraah',era='mad',ce='631',when={'en':'Dhu al-Hijjah, 9 AH','ms':'Zulhijah, tahun 9 Hijrah'},
 title={'en':'Abu Bakr leads the Hajj; Bara\'ah proclaimed','ms':'Abu Bakar memimpin haji; Bara\'ah diisytiharkan'},
 sum={'en':'Abu Bakr led the pilgrimage, and the opening of Surah at-Tawbah (Bara\'ah) was proclaimed at Mina: after that year no idolater would perform Hajj and no one would circle the Ka\'bah naked.',
      'ms':'Abu Bakar memimpin ibadah haji, dan awal Surah at-Taubah (Bara\'ah) diisytiharkan di Mina: selepas tahun itu tiada musyrik boleh menunaikan haji dan tiada sesiapa boleh bertawaf di Kaabah dalam keadaan bertelanjang.'},
 q=[[9,1,3,'The proclamation at the Hajj','Pengisytiharan pada musim haji']],
 h=[['bukhari',369,'The announcement at Mina.','Pengumuman di Mina.'],['bukhari',4655,'','']])
ev(id='wufud',era='mad',ce='630–631',when={'en':'9 to 10 AH','ms':'Tahun 9 hingga 10 Hijrah'},
 title={'en':'The Year of Delegations','ms':'Tahun Perutusan (\'Amul Wufud)'},
 sum={'en':'Delegations from tribes across Arabia came to Madinah to accept Islam or make terms, among them Banu Tamim and \'Abd al-Qays.',
      'ms':'Perutusan daripada kabilah-kabilah di seluruh Semenanjung Arab datang ke Madinah untuk memeluk Islam atau membuat perjanjian, antaranya Bani Tamim dan Abdul Qais.'},
 q=[[110,2,2,'"You see people entering Allah\'s religion in crowds"','"Engkau melihat manusia masuk agama Allah beramai-ramai"']],
 h=[['bukhari',4365,'The delegation of Banu Tamim.','Perutusan Bani Tamim.'],['bukhari',4369,'The delegation of \'Abd al-Qays.','Perutusan Abdul Qais.']])
ev(id='ibrahim',era='mad',ce='632',when={'en':'10 AH','ms':'Tahun 10 Hijrah'},
 title={'en':'Death of his son Ibrahim','ms':'Kewafatan puteranya, Ibrahim'},
 sum={'en':'His infant son Ibrahim, born to Mariyah, died. The sun was eclipsed that day and people said it was for Ibrahim; he told them the sun and moon are not eclipsed for anyone\'s death or life.',
      'ms':'Puteranya yang masih bayi, Ibrahim, anak Mariah, wafat. Gerhana matahari berlaku pada hari itu dan orang ramai berkata ia kerana Ibrahim; baginda memberitahu mereka bahawa matahari dan bulan tidak gerhana kerana kematian atau kehidupan sesiapa.'},
 h=[['bukhari',1043,'The eclipse on the day Ibrahim died.','Gerhana pada hari Ibrahim wafat.']])
ev(id='wada',era='mad',ce='632',when={'en':'Dhu al-Hijjah, 10 AH','ms':'Zulhijah, tahun 10 Hijrah'},
 title={'en':'The Farewell Pilgrimage','ms':'Haji Wada\''},
 sum={'en':'He performed his only Hajj with a vast number of Muslims, teaching its rites. In his sermons at \'Arafah and Mina he declared the sanctity of life, wealth and honour, abolished the blood feuds and usury of the Jahiliyyah, and urged kindness to women. At \'Arafah was revealed: "This day I have perfected your religion for you."',
      'ms':'Baginda menunaikan satu-satunya haji baginda bersama jumlah orang Islam yang sangat ramai, sambil mengajar manasiknya. Dalam khutbahnya di Arafah dan Mina, baginda mengisytiharkan kehormatan nyawa, harta dan maruah, menghapuskan dendam darah dan riba Jahiliah, dan berpesan supaya berbuat baik kepada wanita. Di Arafah diturunkan: "Pada hari ini telah Aku sempurnakan bagi kamu agama kamu."'},
 q=[[5,3,3,'Revealed at \'Arafah','Diturunkan di Arafah']],
 h=[['muslim',2951,'Jabir\'s full description of the Hajj and the sermon at \'Arafah.','Huraian penuh Jabir tentang haji dan khutbah di Arafah.'],['bukhari',4406,'The sermon at Mina: "Your blood and your wealth are sacred..."','Khutbah di Mina: "Darah dan harta kamu adalah haram..."'],['bukhari',4407,'5:3 revealed on the Day of \'Arafah.','5:3 diturunkan pada Hari Arafah.']],
 pop=[{'kind':'hist','en':'The long "Farewell Sermon" text that circulates widely: it mixes the authentic parts (in Sahih Muslim and al-Bukhari) with wording from weaker reports and later additions; check a line against the hadith before quoting it.','ms':'Teks panjang "Khutbah Wida\'" yang tersebar luas: ia mencampurkan bahagian yang sahih (dalam Sahih Muslim dan al-Bukhari) dengan lafaz daripada riwayat yang lebih lemah dan tambahan kemudian; semak sesuatu ayat dengan hadis sebelum memetiknya.'}])
ev(id='wafat',era='mad',ce='632',when={'en':'Monday, Rabi\' al-Awwal, 11 AH (age 63)','ms':'Isnin, Rabiulawal, tahun 11 Hijrah (usia 63)'},
 title={'en':'His illness and death ﷺ','ms':'Sakit dan kewafatan baginda ﷺ'},
 sum={'en':'He fell ill and asked to be nursed in \'Aishah\'s house; Abu Bakr led the prayers. He died at the age of sixty-three, saying "With the Highest Companion". Abu Bakr told the people: "Whoever worshipped Muhammad, Muhammad has died; whoever worships Allah, Allah is Living and does not die," and recited 3:144.',
      'ms':'Baginda jatuh sakit dan meminta dirawat di rumah Aisyah; Abu Bakar mengimamkan solat. Baginda wafat pada usia enam puluh tiga tahun sambil menyebut "Bersama teman yang Maha Tinggi". Abu Bakar berkata kepada orang ramai: "Sesiapa yang menyembah Muhammad, maka Muhammad telah wafat; sesiapa yang menyembah Allah, maka Allah Maha Hidup dan tidak mati," lalu membaca 3:144.'},
 q=[[3,144,144,'Recited by Abu Bakr that day','Dibaca oleh Abu Bakar pada hari itu'],[39,30,30,'"Indeed you will die, and they will die"','"Sesungguhnya engkau akan mati dan mereka juga akan mati"']],
 h=[['bukhari',4463,'"With the Highest Companion."','"Bersama teman yang Maha Tinggi."'],['bukhari',3667,'Abu Bakr\'s words and 3:144.','Kata-kata Abu Bakar dan 3:144.'],['bukhari',4466,'He died at sixty-three.','Baginda wafat pada usia enam puluh tiga.']],
 pop=[{'kind':'none','en':'12 Rabi\' al-Awwal as the day of his death: the best-known date, but scholars give other days (1st, 2nd, 12th); that it was a Monday in Rabi\' al-Awwal is established.','ms':'12 Rabiulawal sebagai hari kewafatan: tarikh paling masyhur, tetapi ulama menyebut hari-hari lain (1, 2, 12); bahawa ia hari Isnin dalam bulan Rabiulawal adalah sabit.'}])

# ---- Sources for "reports in other books" and the popular stories (Azli, 17 Oct 2026: name the book) ----
IH='Ibn Hisham, as-Sirah an-Nabawiyyah (from Ibn Ishaq)'
AW='https://shamela.ws/book/97932/'
AWB="Muhammad al-'Awshan, Ma Sha'a wa Lam Yathbut fi as-Sirah an-Nabawiyyah"
SRC={
 ('birth','pop',1):(IH+"; Ibn Sa'd, at-Tabaqat al-Kubra",None),
 ('birth','pop',2):("al-Bayhaqi, Dala'il an-Nubuwwah; Abu Nu'aym, Dala'il an-Nubuwwah",None),
 ('halimah','pop',0):(IH+", from Halimah",None),
 ('aminah','pop',0):(IH+"; Ibn Sa'd, at-Tabaqat al-Kubra",None),
 ('fudul','ext',0):("Musnad Ahmad (3/193); al-Bukhari, al-Adab al-Mufrad 567. Al-Haythami (Majma' az-Zawa'id 8/172): its narrators are those of the Sahih; the Musnad's editors: isnad sahih. The 'Mutayyabin' here is taken to mean the Pact of al-Fudul, whose members came from it",'https://islamqa.info/ar/answers/469391'),
 ('fudul','pop',0):(IH+"; the words \"If I were called to it in Islam I would answer\": Ibn Kathir, al-Bidayah wa an-Nihayah 3/456, from al-Humaydi",'https://islamqa.info/ar/answers/469391'),
 ('kabah','ext',0):("Musnad Ahmad, from the mawla of Mujahid (as-Sa'ib); al-Haythami, Majma' az-Zawa'id 3/294: \"Hilal ibn Khabbab is in it; he is trustworthy but has been criticised; the rest are narrators of the Sahih\"; also "+IH,'https://dorar.net/h/y1SBgEZQ'),
 ('kabah','pop',0):(IH,None),
 ('first','pop',0):(IH,None),
 ('persecution','pop',0):("\"Ahad, Ahad\": Ibn Majah 150 (in this app; al-Albani hasan sahih). The rock on his chest: "+IH+". Sumayyah as the first martyr: Ibn Sa'd, at-Tabaqat al-Kubra",None),
 ('habasyah','ext',0):("Musnad Ahmad, from Umm Salamah; Shu'ayb al-Arna'ut: sahih (Takhrij Siyar A'lam an-Nubala' 1/216); also "+IH,'https://dorar.net/h/fwdzGYyg'),
 ('umar','pop',0):(AWB+", p. 54 (Ibn Ishaq's account: ar-Rawd al-Unuf 3/265)",AW+'53'),
 ('umar','pop',1):(AWB+", p. 52: Ibn Ishaq from an unnamed man of Aslam (ar-Rawd al-Unuf 3/118); al-Hakim, al-Mustadrak 3/212-213, which adh-Dhahabi called mu'dal (two or more narrators missing)",AW+'51'),
 ('boycott','pop',0):(IH+"; Ibn Sa'd, at-Tabaqat al-Kubra",None),
 ('huzn','pop',0):(AWB+", p. 67: the only report is in al-Qastallani, al-Mawahib al-Ladunniyyah, from \"Sa'id\" without a chain",AW+'66'),
 ('taif','pop',0):(IH+", from Muhammad ibn Ka'b al-Qurazi (mursal: no Companion named); Ibn Hajar, Fath al-Bari 6/315, from Musa ibn 'Uqbah",AW+'64'),
 ('taif','pop',1):("al-Albani, Silsilat al-Ahadith ad-Da'ifah 6/486 and Fiqh as-Sirah p. 126: weak; Ibn Ishaq gives it with no chain",AW+'64'),
 ('aqabah','pop',0):(IH,None),
 ('hijrah','pop',0):("Musnad Ahmad, from Ibn 'Abbas; Ibn Kathir, al-Bidayah wa an-Nihayah 3/181: hasan; Ibn Hajar, Fath al-Bari 7/236: hasan, yet in Taqrib at-Tahdhib he called its narrator 'Uthman al-Jazari weak ("+AWB+", p. 80)",AW+'79'),
 ('hijrah','pop',1):("Ibn Kathir, al-Fusul fi Sirat ar-Rasul p. 52, with \"it is said\" ("+AWB+", p. 80)",AW+'79'),
 ('hijrah','pop',2):("'Ali in the bed: Musnad Ahmad, from Ibn 'Abbas (the same report as the spider). Umm Ma'bad: al-Hakim, al-Mustadrak; al-Bayhaqi, Dala'il an-Nubuwwah",None),
 ('madinah','pop',0):("al-Bayhaqi, Dala'il an-Nubuwwah, from 'Ubaydullah ibn 'A'ishah (d. 228 AH); al-'Iraqi, Takhrij Ahadith al-Ihya' 3/1327: mu'dal; Ibn Hajar, Fath al-Bari 7/261-262: broken chain, and it may belong to the return from Tabuk",AW+'86'),
 ('ukhuwwah','pop',0):(IH+"; Abu 'Ubayd, al-Amwal",None),
 ('badr','pop',0):(IH,None),
 ('qaynuqa','pop',0):("Ibn Hisham, as-Sirah an-Nabawiyyah, from Abu 'Awn",None),
 ('uhud','pop',0):(IH,None),
 ('nadir','pop',0):(IH+"; Musa ibn 'Uqbah, al-Maghazi",None),
 ('khandaq','pop',0):("al-Waqidi, al-Maghazi; Ibn Sa'd, at-Tabaqat al-Kubra; Ibn Hisham, as-Sirah an-Nabawiyyah (\"it is said\")",None),
 ('fath','pop',0):(IH+"; al-Bayhaqi, as-Sunan al-Kubra",None),
 ('wafat','pop',0):(IH+" gives 12 Rabi' al-Awwal",None),
}
EXTBOOK={'fudul':'Musnad Ahmad, al-Adab al-Mufrad','kabah':'Musnad Ahmad','habasyah':'Musnad Ahmad'}
for _e in E:
    for kind in ('ext','pop'):
        for i,x in enumerate(_e.get(kind,[])):
            r=SRC.get((_e['id'],kind,i))
            if r:
                x['src']=r[0]
                if r[1]: x['url']=r[1]
    if _e['id'] in EXTBOOK: _e['extb']=EXTBOOK[_e['id']]
