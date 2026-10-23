"""Build the Kutub as-Sittah data for the app from fawazahmed0/hadith-api (public domain).

Usage: python3 build_kutub.py <path to a clone of fawazahmed0/hadith-api> <output dir> [<path to a clone of ShathaTm/LK-Hadith-Corpus>]

Per book: Arabic with harakat (ara-*), English (eng-*), Indonesian (ind-*), split by kitab.
Gradings kept (decided 10 Oct 2026 after checking the data):
  al-Albani, Shu'ayb al-Arna'ut, Zubair 'Ali Za'i, and at-Tirmidhi's own verdict taken from his text.
Left out: the columns named Abu Ghuddah, Fuad Abd al-Baqi, Muhyi al-Din Abdul Hamid and Ahmad Shakir
(95-97% identical to al-Albani: his rulings as printed in those editions), and "Bashar Awad Maarouf"
(91% identical to at-Tirmidhi's own wording).
"""
import hashlib
import json, os, re, subprocess, sys

SRC, OUT = sys.argv[1], sys.argv[2]
LKDIR = sys.argv[3] if len(sys.argv) > 3 else None
BOOKS = [
    ('bukhari', 'صحيح البخاري', 'Sahih al-Bukhari'),
    ('muslim', 'صحيح مسلم', 'Sahih Muslim'),
    ('abudawud', 'سنن أبي داود', 'Sunan Abi Dawud'),
    ('tirmidhi', 'جامع الترمذي', "Jami' at-Tirmidhi"),
    ('nasai', 'سنن النسائي', "Sunan an-Nasa'i"),
    ('ibnmajah', 'سنن ابن ماجه', 'Sunan Ibn Majah'),
    ('malik', 'موطأ الإمام مالك', 'Muwatta Malik'),   # added 11 Oct 2026 at Azli's request; one grader only (al-Hilali)
]
KEEP = {'Al-Albani': 'alb', 'Shuaib Al Arnaut': 'arn', 'Zubair Ali Zai': 'zub', 'Salim al-Hilali': 'hil'}
# Unreferenced hadith on a kitab boundary that open the next kitab (checked by content):
# Bukhari 521 Mawaqit as-Salat, 2711 ash-Shurut, 3156 al-Jizyah, 4978 Fada'il al-Qur'an; Muslim 5885-5886 ash-Shi'r.
OPENS_NEXT = {('bukhari', 521), ('bukhari', 2711), ('bukhari', 3156), ('bukhari', 4978), ('muslim', 5885), ('muslim', 5886)}
HARAKAT = re.compile('[ً-ْٰۡـ]')
TIR = re.compile(r'هذا حديث ((?:(?:حسن|صحيح|غريب|ضعيف|مرسل|منكر|مضطرب|مفسر|موقوف)\s*)+)')


def edition(name):
    raw = subprocess.run(['git', '-C', SRC, 'show', f'HEAD:editions/{name}.min.json'], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


def tirmidhi_verdict(ar):
    t = HARAKAT.sub('', ar)
    i = t.find('قال أبو عيسى')
    m = TIR.search(t, i if i >= 0 else 0)
    return m.group(1).strip() if m else None


# ---- Narrators (isnad) vs text (matn), so the app can show the text only ----
# Arabic and English: the split of the LK Hadith Corpus (Leeds & King Saud Univ.): Bukhari checked by hand; the other five
# books split by their tool (about 92% accurate, by their account). A hadith is matched to ours by its whole Arabic text
# (ignoring harakat); the split is used only if the text after it matches the corpus's matn. Indonesian: the translation
# brackets every narrator, so the chain is the opening run of [names]. Anything not confirmed is shown in full.
import csv, glob
csv.field_size_limit(10 ** 9)
DIAC = re.compile('[\u064B-\u065F\u0670\u06D6-\u06ED\u0640\u200f\u200e]')
def sk(s):
    s = re.sub(r'[^\u0621-\u064A]', '', DIAC.sub('', s or ''))
    return s.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ى', 'ي').replace('ة', 'ه')
LKBOOK = {'bukhari': 'Bukhari', 'muslim': 'Muslim', 'abudawud': 'AbuDaud', 'tirmidhi': 'Tirmizi', 'nasai': 'Nesai', 'ibnmajah': 'IbnMaja'}
def lk_rows(bid):
    if not LKDIR or bid not in LKBOOK: return {}   # the corpus has no Muwatta: shown in full
    out = {}
    for f in glob.glob(os.path.join(LKDIR, LKBOOK[bid], '*.csv')):
        for r in csv.DictReader(open(f, encoding='utf-8-sig')):
            k = sk(r.get('Arabic_Hadith'))
            if k: out.setdefault(k, []).append(r)
    return out
def ar_cut(ar, isnad_sk, matn_sk):
    """offset in our Arabic text where the matn starts, or None"""
    if not isnad_sk or not matn_sk or len(matn_sk) < 6: return None
    n = 0
    for i, ch in enumerate(ar):
        if sk(ch): n += len(sk(ch))
        if n == len(isnad_sk):
            j = i + 1
            while j < len(ar) and not sk(ar[j]): j += 1   # skip harakat, spaces and punctuation after the chain
            return j if sk(ar[j:]).startswith(matn_sk[:40]) and sk(ar[:j]) == isnad_sk else None
    return None
# Checks on a narrator/text split, so that no word of the hadith itself is hidden (the corpus's tool is ~92% right):
# the hidden chain must end at a natural boundary, only a short name may follow the last "haddathana/'an/...",
# and no typical narrative verb may be hidden.
def _w(s): return re.sub(r'[^\u0621-\u064A\s]', ' ', DIAC.sub('', s)).split()
LINKS = {'حدثنا','حدثني','أخبرنا','أخبرني','اخبرنا','اخبرني','أنبأنا','انبأنا','عن','سمعت','سمع','حدثه','أخبره','اخبره','حدثهم','ثنا','نا'}
ENDS = {'قال','قالت','قالا','قالوا','أنه','انه','أنها','انها','أن','ان','يقول','تقول','عنه','عنها','عنهما','عنهم','يحدث','حدثه','يرفعه','يحدثه'}
NARR = {'جاء','جاءت','رأيت','رأى','رايت','راى','كان','كانت','كنا','كنت','سأل','سألت','سال','سالت','خرج','خرجنا','أتى','أتيت','اتى','اتيت','دخل','دخلت','قام','أمر','امر','نهى','بعث','أرسل','ارسل','لما','إذا','اذا','إن','لقد','قد'}
def ar_ok(hidden):
    w = _w(hidden)
    if len(w) < 3: return False
    if not (w[-1] in ENDS or hidden.rstrip().endswith(('،', ','))): return False
    k = max([i for i, x in enumerate(w) if x in LINKS] or [-1])
    if k < 0: return False
    tail = w[k + 1:]
    return len(tail) <= 9 and not any(x in NARR for x in tail)
def ar_tail_ok(hidden):
    # lighter check for Bukhari: after the last "haddathana/'an/..." no narrative word (kana, inna, jaa'a ...) may be hidden.
    # The corpus split is hand-checked there, but 174 of its boundaries still hide words of the story (e.g. 5443, 4824).
    w = _w(hidden); k = max([i for i, x in enumerate(w) if x in LINKS] or [-1])
    return k >= 0 and len(w) - k - 1 <= 14 and not any(x in NARR for x in w[k + 1:])
# ---- Start the text at the Prophet ﷺ (Azli, 11 Oct 2026) ----
# "سمعت رسول الله ﷺ يقول ..." -> "رسول الله ﷺ يقول ...": after the chain, only words of transmission (heard / said / that /
# from) may be dropped before "رسول الله" or "النبي", at most 3 of them; never a narrative word (كان، رأيت، جاء ...).
LEAD_AR = {'سمعت', 'سمعنا', 'سمع', 'قال', 'قالت', 'قالا', 'عن', 'ان', 'انه', 'انها', 'يقول', 'تقول', 'يحدث', 'حدثنا', 'اخبرنا'}
def ar_prophet(ar, a):
    """offset of "رسول الله" / "النبي" / "نبي الله" in ar[a:] if only transmission words come before it, else None"""
    words = [(m.start() + a, m.group()) for m in re.finditer(r'\S+', ar[a:])]
    lead = 0
    for k, (pos, w) in enumerate(words[:6]):
        x = sk(w)
        if not x: continue
        nxt = sk(words[k + 1][1]) if k + 1 < len(words) else ''
        if (x == 'رسول' and nxt == 'الله') or x == 'النبي' or (x == 'نبي' and nxt == 'الله'):
            return pos
        if x not in LEAD_AR: return None
        lead += 1
        if lead > 3: return None
    return None
EN_PROPHET = re.compile(r"Allah's (?:Messenger|Apostle)|[Tt]he Prophet|(?:the )?Messenger of Allah|Allah's Prophet")
def en_prophet(en, e):
    m = EN_PROPHET.search(en, e, e + 60)
    if not m: return None
    lead = en[e:m.start()]
    words = re.findall(r"[A-Za-z']+", lead)
    return m.start() if len(words) <= 4 and all(w.lower() in {'i', 'we', 'heard', 'that', 'said', 'say', 'he', 'she', 'narrated'} for w in words) and not re.search('["“(]', lead) else None
def id_prophet(t, i):
    m = re.compile(r"\b(?:Rasulullah|Nabi)\b").search(t, i, i + 120)
    if not m: return None
    lead = t[i:m.start()]
    # only words of transmission may go (never "ketika", "apabila", "isteri", ... which belong to the text itself)
    ws = [w for w in re.split(r"[\s,;:.\-–—']+", lead.lower()) if w]
    ok = all(w in ID_LEAD or w.startswith(('radl', 'radh', 'anhu', 'anha')) for w in ws)
    return m.start() if ok and len(ws) <= 10 and not re.search(r'["“\[]', lead) else None
ID_LEAD = set("""telah menceritakan mengabarkan memberitakan menuturkan mengatakan mengabarinya menceritakannya kepada kepadanya kami
kepadaku kepada mereka berdua aku saya dari dan berkata katanya keduanya ia dia beliau bahwa bahwasanya bahwasannya bawasanya
sesungguhnya mendengar mendengarnya pernah diatas atas di mimbar""".split())
def en_ok(hidden):
    h = hidden.strip()
    return len(h) <= 140 and h.endswith((':', 'that', 'said', 'that:', 'said:')) and not re.search(r'Messenger|Prophet|\bAllah\b|"|“', h)
def en_cut(en, lk_isnad, lk_matn):
    m = (lk_matn or '').strip()
    if len(m) < 12 or not (lk_isnad or '').strip(): return None
    i = en.find(m[:30])
    return i if 0 < i < len(en) * 0.8 else None
def by_name(lk_isnad):
    s = (lk_isnad or '').strip()
    for pat in [r"^Narrated\s+(.{2,70}?)\s*:?$", r"^It was narrated (?:from|that)\s+(.{2,70}?)\s+(?:said|that)\b.*$", r"^(.{2,70}?)\s+(?:reported|narrated)(?: that)?\s*:?$"]:
        m = re.match(pat, s)
        if m: return m.group(1).strip(" ,:")
    return None
BR = re.compile(r'\[[^\]]{1,80}\]')
CHAIN_WORDS = set("""telah menceritakan mengabarkan memberitakan menuturkan mengatakan kepada kami kepadaku aku saya dari dan
berkata katanya keduanya mereka semuanya yaitu yakni ia dia beliau bahwa bahwasanya mendengar pernah juga sama lafazh lafadz
haditsnya hadits ini dengan isnad sanad jalur lain lainnya yang menyebutkan riwayat meriwayatkan diriwayatkan ibnu bin binti
radliallahu radhiallahu radhiyallahu anhu anha anhuma ta'ala namanya adalah""".split())
def id_cut(t):
    """end of the opening chain of bracketed narrators in the Indonesian text (only chain words between the names), or None"""
    ms = list(BR.finditer(t))
    if len(ms) < 2 or ms[0].start() > 80: return None
    if any(w.strip(",.;:'-()").lower() not in CHAIN_WORDS for w in t[:ms[0].start()].split() if w.strip(",.;:'-()")): return None
    end = ms[0].end()
    for m in ms[1:]:
        gap = t[end:m.start()]
        words = [w.strip(",.;:'-()").lower() for w in gap.split()]
        if '"' in gap or '“' in gap or len(gap) > 120 or any(w and w not in CHAIN_WORDS for w in words): break
        end = m.end()
    rest = t[end:]
    # whole words only ("dia" must not take the start of "diatas")
    mm = re.match(r"^[\s,;:]*(?:(?:radliallahu|radhiyallahu)\s+'anh(?:u|uma|a)\b)?[\s,;:]*(?:(?:dia|ia|beliau)\b)?\s*(?:(?:berkata|mengatakan|menuturkan|bahwasanya|bahwa)\b)?[\s,;:]*", rest, re.I)
    j = end + (mm.end() if mm else 0)
    if 0 < j < len(t) and t[j - 1].isalnum() and t[j].isalnum(): return None   # never cut inside a word
    if '"' in t[:j] or '“' in t[:j]: return None
    return j if j < len(t) - 15 else None

info = json.load(open(os.path.join(SRC, 'info.json')))
# 75 Arabic texts have a damaged letter (U+FFFD) in the source. 59 were repaired word by word from the same hadith in
# the Sunnah.com copy (tools/fffd_repair.py -> tools/fffd_fix.json). The rest show "…" there and a note in the app.
FIX = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fffd_fix.json')))
_hm = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hadeethenc_map.json')
HEMAP = json.load(open(_hm)) if os.path.exists(_hm) else {}
index = []
for bid, ar_name, en_name in BOOKS:
    A, E, I = edition('ara-' + bid), edition('eng-' + bid), edition('ind-' + bid)
    grades = {h['hadithnumber']: h['grades'] for h in info[bid]['hadiths']}
    LK = lk_rows(bid); stats = {'ar': 0, 'en': 0, 'id': 0}
    ah, eh, ih = A['hadiths'], E['hadiths'], I['hadiths']
    if bid == 'malik':
        # Indonesian has one extra entry (774.5, no Arabic): pair by number. English: entries re-paired with the Arabic by
        # tools/malik_en_fix.py (Malik's rulings moved back to the entry they close; 5 unmatched left without English).
        byn = {x['hadithnumber']: x for x in ih}
        ih = [byn.get(a['hadithnumber'], {'hadithnumber': a['hadithnumber'], 'text': ''}) for a in ah]
        MEN = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'malik_en_fix.json')))['en']
        eh = [dict(x, text=MEN.get(str(x['hadithnumber']), x['text'])) for x in eh]
    assert len(ah) == len(eh) == len(ih), bid
    # kitab of each hadith: its own reference; 306 in Bukhari, 148 in Muslim and 266 in Ibn Majah have none (book 0)
    # hadith without a kitab reference: the kitab of the referenced hadith on both sides (they agree for all but 17)
    refbook = [((a.get('reference') or {}).get('book') or 0) for a in ah]
    prev_k, next_k, last = [0] * len(ah), [0] * len(ah), 0
    for k, rb in enumerate(refbook):
        if rb: last = rb
        prev_k[k] = last
    last = 0
    for k in range(len(ah) - 1, -1, -1):
        if refbook[k]: last = refbook[k]
        next_k[k] = last
    def kitab(k, n):
        if refbook[k]:
            return str(refbook[k])
        if prev_k[k] == next_k[k]:
            return str(prev_k[k])
        if (bid, n) in OPENS_NEXT:   # on a kitab boundary: the first hadith of the next kitab
            return str(next_k[k])
        return str(prev_k[k])        # otherwise it continues the previous one (e.g. "another chain" narrations)
    secs = {}
    for k, (a, e, i) in enumerate(zip(ah, eh, ih)):
        n = a['hadithnumber']
        assert e['hadithnumber'] == n and i['hadithnumber'] == n, (bid, n)
        if not (a['text'].strip() or e['text'].strip()):
            continue
        g = [[KEEP[x['name']], x['grade']] for x in grades.get(n, []) if x['name'] in KEEP]
        if bid == 'tirmidhi':
            v = tirmidhi_verdict(a['text'])
            if v:
                g.insert(0, ['tir', v])
        ref = a.get('reference') or e.get('reference') or {}
        sec = kitab(k, n)
        ar = FIX.get(f'{bid}:{n}', a['text']).strip()
        damaged = '\ufffd' in ar
        if damaged: ar = re.sub('\ufffd+', '…', ar)
        row = [n, ref.get('hadith') if ref.get('book') else None, ar, e['text'].strip().replace('\ufffd', ''), i['text'].strip().replace('\ufffd', ''), g]
        row.append(1 if damaged else 0)
        cut = {}
        cand = LK.get(sk(ar)) or []
        if len(cand) == 1:
            r = cand[0]; a_i = ar_cut(ar, sk(r['Arabic_Isnad']), sk(r['Arabic_Matn']))
            # never hide quoted words; the boundary must also pass the checks (a lighter one for Bukhari, hand-checked in the corpus)
            if a_i and ('"' in ar[:a_i] or not (ar_tail_ok if bid == 'bukhari' else ar_ok)(ar[:a_i])): a_i = None
            if a_i: cut['a'] = a_i; stats['ar'] += 1
            e_i = en_cut(row[3], r.get('English_Isnad'), r.get('English_Matn'))
            if e_i and not en_ok(row[3][:e_i]): e_i = None
            if e_i: cut['e'] = e_i; stats['en'] += 1
            nm = by_name(r.get('English_Isnad'))
            if nm and (a_i or e_i): cut['by'] = nm
        if row[4] and bid in LKBOOK:   # Muwatta: no split in Arabic or English, so none in Indonesian either (same view)
            i_i = id_cut(row[4])
            if i_i: cut['i'] = i_i; stats['id'] += 1
        # the shown Arabic starts with the Prophet ﷺ after transmission words only: start there, and the translations too
        if cut.get('a'):
            p_a = ar_prophet(ar, cut['a'])
            if p_a is not None:
                cut['a'] = p_a; stats['pa'] = stats.get('pa', 0) + 1
                if cut.get('e'):
                    p_e = en_prophet(row[3], cut['e'])
                    if p_e: cut['e'] = p_e; stats['pe'] = stats.get('pe', 0) + 1
                if cut.get('i'):
                    p_i = id_prophet(row[4], cut['i'])
                    if p_i: cut['i'] = p_i; stats['pi'] = stats.get('pi', 0) + 1
        row.append(cut or 0)
        if HEMAP.get(f'{bid}:{n}'): row.append(HEMAP[f'{bid}:{n}'])   # HadeethEnc explanation(s) for this hadith (tools/build_hadeethenc.py)
        secs.setdefault(sec, []).append(row)
    names = E['metadata']['sections']
    os.makedirs(os.path.join(OUT, bid), exist_ok=True)
    sl = []
    for sec in sorted(secs, key=int):
        hs = secs[sec]
        body = json.dumps({'h': hs}, ensure_ascii=False, separators=(',', ':'))
        with open(os.path.join(OUT, bid, f'{sec}.json'), 'w', encoding='utf8') as f:
            f.write(body)
        nm = (names.get(sec) or ('Introduction' if sec == '0' else f'Book {sec}')).strip()
        if nm.count('(') > nm.count(')'): nm += ')'
        sl.append({'n': int(sec), 'en': nm,
                   'first': hs[0][0], 'last': hs[-1][0], 'count': len(hs),
                   'v': hashlib.sha1(body.encode('utf8')).hexdigest()[:8]})  # the app re-downloads a kept kitab when this changes
    total = sum(s['count'] for s in sl)
    index.append({'id': bid, 'ar': ar_name, 'en': en_name, 'count': total, 'sections': sl})
    print(bid, total, 'hadith in', len(sl), 'kitab; text-only split: Arabic', stats['ar'], 'English', stats['en'], 'Indonesian', stats['id'], '| starts at the Prophet:', stats.get('pa', 0), stats.get('pe', 0), stats.get('pi', 0))
with open(os.path.join(OUT, 'books.json'), 'w', encoding='utf8') as f:
    # versions of the HadeethEnc files (kutub/he/<k>.json), so a kept copy is replaced when they change
    hev = {}
    for fn in sorted(glob.glob(os.path.join(OUT, 'he', '*.json'))):
        hev[os.path.basename(fn)[:-5]] = hashlib.sha1(open(fn, 'rb').read()).hexdigest()[:8]
    json.dump({'source': 'fawazahmed0/hadith-api (public domain)', 'books': index, 'he': hev}, f, ensure_ascii=False, separators=(',', ':'))

