import json
# Objective check of a generated score: loudness curve, section changes, percussion share, instrument/mood tags.
import sys, numpy as np, librosa, torch, subprocess
from transformers import ASTFeatureExtractor, ASTForAudioClassification
src = sys.argv[1]
y, sr = librosa.load(src, sr=44100, mono=True)
print(f'duration {len(y)/sr:.2f}s  peak {np.max(np.abs(y)):.3f}')
# loudness (RMS dBFS) per 1 s
hop = sr // 2
rms = [20*np.log10(np.sqrt(np.mean(y[i:i+sr]**2))+1e-9) for i in range(0, len(y)-sr//2, hop)]
print('RMS dB per 0.5s:')
for k in range(0, len(rms), 8): print(f'  {k*0.5:5.1f}s ' + ' '.join(f'{v:6.1f}' for v in rms[k:k+8]))
# percussive share
H, P = librosa.effects.hpss(y)
print(f'percussive energy share {np.sum(P**2)/np.sum(y**2):.3f}')
# spectral novelty peaks (section changes)
S = np.abs(librosa.stft(y, n_fft=4096, hop_length=2048))
chroma = librosa.feature.chroma_stft(S=S**2, sr=sr)
mf = librosa.feature.mfcc(S=librosa.power_to_db(librosa.feature.melspectrogram(S=S**2, sr=sr)), n_mfcc=13)
feat = np.vstack([chroma, mf / 50])
nov = np.r_[0, np.linalg.norm(np.diff(feat, axis=1), axis=0)]
nov = np.convolve(nov, np.ones(5) / 5, mode='same')
tt = librosa.frames_to_time(np.arange(len(nov)), sr=sr, hop_length=2048)
top = np.argsort(nov)[::-1]
picked = []
for i in top:
    if all(abs(tt[i] - tt[j]) > 3 for j in picked): picked.append(i)
    if len(picked) == 6: break
print('largest timbral changes at:', ' '.join(f'{tt[i]:.1f}s' for i in sorted(picked)))
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
print('tempo', np.round(tempo, 1))
key_prof = np.mean(chroma, axis=1)
names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
print('chroma strongest:', [names[i] for i in np.argsort(key_prof)[::-1][:5]])
# AST tags per section
y16 = librosa.resample(y, orig_sr=sr, target_sr=16000)
fe = ASTFeatureExtractor.from_pretrained('MIT/ast-finetuned-audioset-10-10-0.4593')
model = ASTForAudioClassification.from_pretrained('MIT/ast-finetuned-audioset-10-10-0.4593').eval()
labels = model.config.id2label; idx = {v: k for k, v in labels.items()}
want = ['Piano','Cello','Violin, fiddle','String section','Bowed string instrument','Orchestra','Harp','Synthesizer','Drum','Drum kit','Percussion','Singing','Choir','Vocal music','Tender music','Sad music','Happy music','Exciting music','Ambient music','Classical music','Soundtrack music','Music for children','Bell']
import os
secs = json.loads(os.environ['SECS']) if os.environ.get('SECS') else [(0, 14.6), (14.6, 28.0), (28.0, 34.7), (34.7, 42.6), (42.6, 46.0)]
for a, b in secs:
    seg = y16[int(a * 16000):int(b * 16000)]
    with torch.no_grad(): p = torch.sigmoid(model(**fe(seg, sampling_rate=16000, return_tensors='pt')).logits)[0]
    tags = sorted([(w, float(p[idx[w]])) for w in want if w in idx], key=lambda x: -x[1])
    print(f'{a:5.1f}-{b:5.1f}:', ', '.join(f'{w} {v:.2f}' for w, v in tags[:9]))
