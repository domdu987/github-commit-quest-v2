import sys, json, os
import numpy as np, librosa, soundfile as sf, torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification

stems_dir, mix_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
res = {}

def load(p, sr=None):
    y, s = librosa.load(p, sr=sr, mono=True)
    return y, s

# --- music stem = drums + bass + other
parts = [load(os.path.join(stems_dir, f"{n}.wav"), 44100)[0] for n in ("drums", "bass", "other")]
music = np.sum(parts, axis=0)
vocals, sr = load(os.path.join(stems_dir, "vocals.wav"), 44100)
sf.write(os.path.join(stems_dir, "music_only.wav"), music, sr)

# tempo / beats on music
tempo, beats = librosa.beat.beat_track(y=music, sr=sr)
res["tempo_bpm"] = float(np.atleast_1d(tempo)[0])
res["beat_times"] = [round(float(t), 2) for t in librosa.frames_to_time(beats, sr=sr)][:200]

# key estimate (Krumhansl-Schmuckler)
chroma = librosa.feature.chroma_cqt(y=music, sr=sr).mean(axis=1)
major = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
minor = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
scores = []
for i in range(12):
    scores.append((np.corrcoef(np.roll(major, i), chroma)[0,1], names[i]+' major'))
    scores.append((np.corrcoef(np.roll(minor, i), chroma)[0,1], names[i]+' minor'))
scores.sort(reverse=True)
res["key_candidates"] = [(round(float(s),3), k) for s, k in scores[:4]]

# loudness envelopes (dBFS, 0.5 s windows)
def env(y, hop=0.5):
    n = int(sr*hop)
    return [round(float(20*np.log10(np.sqrt(np.mean(y[i:i+n]**2))+1e-9)),1) for i in range(0, len(y), n)]
res["music_db_0p5s"] = env(music)
res["vocal_db_0p5s"] = env(vocals)

# voice pitch
v16 = librosa.resample(vocals, orig_sr=sr, target_sr=16000)
f0, vflag, _ = librosa.pyin(v16, fmin=60, fmax=500, sr=16000)
f0v = f0[~np.isnan(f0)]
res["voice_f0_median_hz"] = round(float(np.median(f0v)),1) if len(f0v) else None
res["voice_f0_p10_p90"] = [round(float(np.percentile(f0v,10)),1), round(float(np.percentile(f0v,90)),1)] if len(f0v) else None

# onsets in "other" + "drums" (sfx/pops) with strength
oth = parts[0] + parts[2]
oenv = librosa.onset.onset_strength(y=oth, sr=sr)
onsets = librosa.onset.onset_detect(onset_envelope=oenv, sr=sr, units='frames', backtrack=False)
times = librosa.frames_to_time(onsets, sr=sr)
strengths = oenv[onsets]
thr = np.percentile(strengths, 75) if len(strengths) else 0
res["strong_onsets"] = [round(float(t),2) for t, s in zip(times, strengths) if s >= thr]

# AST audio tagging on mix and music stem, 2 s windows / 1 s hop
fe = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593").eval()
def tag(y, win=2.0, hop=1.0, k=6):
    y16 = librosa.resample(y, orig_sr=sr, target_sr=16000)
    out = []
    for st in np.arange(0, len(y16)/16000 - 0.5, hop):
        seg = y16[int(st*16000):int((st+win)*16000)]
        inp = fe(seg, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            p = torch.sigmoid(model(**inp).logits)[0]
        top = torch.topk(p, k)
        out.append({"t": float(st), "labels": [(model.config.id2label[int(i)], round(float(s),2)) for s, i in zip(top.values, top.indices)]})
    return out
mix, _ = load(mix_path, 44100)
res["ast_music"] = tag(music)
# whole-clip tags for music
y16 = librosa.resample(music, orig_sr=sr, target_sr=16000)
agg = None
for st in range(0, int(len(y16)/16000)-9, 5):
    inp = fe(y16[st*16000:(st+10)*16000], sampling_rate=16000, return_tensors="pt")
    with torch.no_grad():
        p = torch.sigmoid(model(**inp).logits)[0]
    agg = p if agg is None else agg + p
top = torch.topk(agg, 15)
res["ast_music_overall"] = [(model.config.id2label[int(i)], round(float(s),2)) for s, i in zip(top.values, top.indices)]
json.dump(res, open(out_path, "w"), ensure_ascii=False, indent=1)
print("done")
