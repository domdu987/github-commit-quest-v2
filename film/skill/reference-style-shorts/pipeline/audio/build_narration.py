"""Build a whole narration from a new script, with no dependency on an earlier recording.

usage:
  python3 build_narration.py <script.json> <voice_id> <out_dir> [--lang th] [--speed 1.2] [--target-s 65]
                             [--groups auto | "0|1,2,3|4,5"] [--max-chars 320] [--dry-run]

<script.json> has the format of pipeline/script_th_v2/script_th.json: {"sentences": [{"beat", "tts", "captions": [...]}, ...],
optional "caption_number_readings": {"1938": "<the number as spoken words>", ...}} (used to compare the speech-to-text check,
which writes digits, with the script, which spells numbers out).

Steps: speech in paragraph chunks through fal.ai (ElevenLabs v3, character timestamps; up to 3 takes per chunk, the best
speech-to-text match wins, a chunk is cached in <out_dir>/chunkNN.* and never paid for twice) -> tighten pauses (silences over
0.14 s cut to 0.10 s) -> loudness match -> join with 0.16 s gaps -> one atempo so the total lands on --target-s (pitch kept;
capped at 1.22, a warning above 1.15) -> limiter -> caption phrase timing.
Writes <out_dir>/narration.wav, narration.chars.json, narration_timing.json (the format the shots, assemble.py and the mix read).

--groups auto: the first sentence (the hook) alone, then paragraphs of 2 to 4 sentences that break where the beat changes and
stay under --max-chars characters. One request of about 1,000 characters failed with HTTP 502; sentence-by-sentence varies the
delivery. --dry-run prints the groups and the character count (the paid amount) and stops.

Paid: each chunk take is one text-to-speech request plus one speech-to-text request. Run it from the main conversation.
Film 1 used audio/th/build_narration_v2.py, which also reused the opening's chunk and tempo from an earlier build; this is
that script with the film-specific parts removed.
"""
import sys, json, os, wave, subprocess, re, difflib, shutil, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, 'th'))
import tts_fal

ap = argparse.ArgumentParser()
ap.add_argument('script'); ap.add_argument('voice'); ap.add_argument('out')
ap.add_argument('--lang', default='th'); ap.add_argument('--speed', type=float, default=1.2)
ap.add_argument('--target-s', type=float, default=None); ap.add_argument('--groups', default='auto')
ap.add_argument('--max-chars', type=int, default=320); ap.add_argument('--dry-run', action='store_true')
A = ap.parse_args()
SR = 48000; GAP = 0.16
os.makedirs(A.out, exist_ok=True)
sc = json.load(open(A.script, encoding='utf8')); sents = sc['sentences']
NUM = sc.get('caption_number_readings', {})
norm = lambda s: re.sub(r"[\s\.,!?\"“”‘’ๆ:;…\-–—()]", "", s)

def auto_groups():
    groups, cur = [[0]], []
    for i in range(1, len(sents)):
        n = sum(len(sents[k]['tts']) for k in cur) + len(sents[i]['tts'])
        new_beat = cur and sents[i]['beat'] != sents[cur[-1]]['beat'] and len(cur) >= 2
        if cur and (len(cur) >= 4 or n > A.max_chars or new_beat):
            groups.append(cur); cur = []
        cur.append(i)
    if cur: groups.append(cur)
    return groups

GROUPS = auto_groups() if A.groups == 'auto' else [[int(x) for x in g.split(',')] for g in A.groups.split('|')]
assert sorted(sum(GROUPS, [])) == list(range(len(sents))), 'groups must cover every sentence once'
total_chars = sum(len(s['tts']) for s in sents)
print('groups:', GROUPS, '| characters:', total_chars, '| chunk sizes:', [sum(len(sents[i]['tts']) for i in g) for g in GROUPS])
if A.dry_run: sys.exit(0)

def read_wav(path):
    w = wave.open(path); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768; return x, w.getframerate()

def write(path, x):
    w = wave.open(path, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def tighten(x, sr, t0, t1, max_gap=0.14, keep=0.10, thr=0.012):
    win = int(0.02 * sr); env = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, 'same')); sil = env < thr
    cuts, i, n = [], 0, len(x)
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if i == 0: cuts.append((0, max(0, j - int(0.03 * sr))))
            elif j == n: cuts.append((min(n, i + int(0.08 * sr)), n))
            elif (j - i) / sr > max_gap: cuts.append((i + int(keep * sr / 2), j - int(keep * sr / 2)))
            i = j
        else: i += 1
    km = np.ones(n, bool)
    for a, b in cuts: km[a:b] = False
    rb = np.cumsum(~km)
    rm = lambda t: (min(n - 1, max(0, int(t * sr))) - rb[min(n - 1, max(0, int(t * sr)))]) / sr
    return x[km], [rm(t) for t in t0], [rm(t) for t in t1]

def asr_ratio(base, text):
    url = json.load(open(base + '.json', encoding='utf8'))['audio']['url']
    lang3 = {'th': 'tha', 'en': 'eng'}.get(A.lang, A.lang)
    r = subprocess.run(['curl', '-sS', '-m', '180', '-X', 'POST', 'https://fal.run/fal-ai/elevenlabs/speech-to-text', '-H', 'Content-Type: application/json',
                        '-d', json.dumps({'audio_url': url, 'language_code': lang3, 'tag_audio_events': False, 'diarize': False}), '-w', '\n%{http_code}'],
                       capture_output=True, text=True)
    txt, code = r.stdout.rsplit('\n', 1)
    if code != '200': return None
    t = json.loads(txt)['text']; open(base + '.asr.txt', 'w', encoding='utf8').write(t)
    for k, v in NUM.items(): t = t.replace(k, v)
    return difflib.SequenceMatcher(None, norm(text), norm(t), autojunk=False).ratio()

def synth(text, base):
    if A.lang != 'th' and '"language_code": "th"' in open(tts_fal.__file__, encoding='utf8').read():
        raise SystemExit('th/tts_fal.py sends language_code "th": change it before using --lang ' + A.lang)
    tts_fal.synth(text, base, A.voice, A.speed)

chunks = []
for gi, g in enumerate(GROUPS):
    base = f'{A.out}/chunk{gi:02d}'
    text = '\n'.join(sents[i]['tts'] for i in g)
    cached = os.path.exists(base + '.chars.json') and json.load(open(base + '.chars.json', encoding='utf8')).get('src_text') in (None, text)
    if not cached:
        best = None
        for take in range(1, 4):
            tb = f'{base}_take{take}'
            synth(text, tb)
            ratio = asr_ratio(tb, text)
            print(f'  chunk {gi} take {take}: speech-to-text match {ratio}')
            if best is None or (ratio or 0) > best[0]: best = (ratio or 0, tb)
            if ratio is not None and ratio >= 0.985: break
        for ext in ('.json', '.mp3', '.wav', '.chars.json'): shutil.copy(best[1] + ext, base + ext)
        c = json.load(open(base + '.chars.json', encoding='utf8')); c['src_text'] = text; c['asr_match'] = best[0]
        json.dump(c, open(base + '.chars.json', 'w', encoding='utf8'), ensure_ascii=False)
    c = json.load(open(base + '.chars.json', encoding='utf8'))
    x, sr = read_wav(base + '.wav'); assert sr == SR
    y, t0, t1 = tighten(x, sr, c['t0'], c['t1'])
    act = y[np.abs(y) > 0.02]; rms = float(np.sqrt((act ** 2).mean()))
    chunks.append({'chars': c['chars'], 't0': t0, 't1': t1, 'y': y, 'rms': rms})
    print(f"chunk {gi} sentences {g}: {len(x)/sr:.2f}s -> {len(y)/sr:.2f}s, match {c.get('asr_match')}")

target = float(np.median([c['rms'] for c in chunks]))
parts, chars, T0, T1, off = [], [], [], [], 0.0
for ci, c in enumerate(chunks):
    y = c['y'] * (target / c['rms'])
    if ci > 0:
        parts.append(np.zeros(int(GAP * SR))); chars.append('\n'); T0.append(off); T1.append(off + GAP); off += GAP
    parts.append(y); chars += c['chars']; T0 += [t + off for t in c['t0']]; T1 += [t + off for t in c['t1']]; off += len(y) / SR
y = np.concatenate(parts)
raw = len(y) / SR
tempo = 1.0 if not A.target_s else max(0.9, min(1.22, raw / A.target_s))
if tempo > 1.15: print(f'WARNING: tempo {tempo:.3f} is fast; shorten the script or offer the user the natural-speed version')
y = y * min(1.0, 0.89 / np.abs(y).max())
write(A.out + '/narration_raw.wav', y)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A.out + '/narration_raw.wav', '-af', f'atempo={tempo:.5f},alimiter=limit=0.9', '-ar', str(SR), A.out + '/narration.wav'], check=True)
x, _ = read_wav(A.out + '/narration.wav'); total = len(x) / SR
T0 = [t / tempo for t in T0]; T1 = [t / tempo for t in T1]
json.dump({'text': ''.join(chars), 'chars': chars, 't0': T0, 't1': T1, 'duration': total, 'voice': A.voice, 'speed': A.speed, 'tempo': tempo},
          open(A.out + '/narration.chars.json', 'w', encoding='utf8'), ensure_ascii=False)
caps = [{'text': t, 'sentence': si, 'beat': s['beat'], 'k': k} for si, s in enumerate(sents) for k, t in enumerate(s['captions'])]
timed, ratio, _ = tts_fal.align(A.out + '/narration', caps)
json.dump({'duration': total, 'audio': A.out + '/narration.wav', 'match_ratio': ratio, 'tempo': tempo, 'phrases': timed},
          open(A.out + '/narration_timing.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
d = [q['t1'] - q['t0'] for q in timed]
print(f'TOTAL {total:.2f}s (raw {raw:.2f}s, tempo {tempo:.4f}); captions {len(timed)} match {ratio:.3f}; phrase min {min(d):.2f} median {np.median(d):.2f} max {max(d):.2f}')
