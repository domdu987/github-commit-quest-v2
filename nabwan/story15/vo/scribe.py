# scribe.py OUT KEY... : one combined file of takes (1.2 s gaps) through ElevenLabs Scribe on fal; prints text per take
import sys, json, base64, subprocess, numpy as np, soundfile as sf
out, keys = sys.argv[1], sys.argv[2:]
sr = 44100; parts = []; marks = []; t = 0
for k in keys:
    a, _ = sf.read(f'{k}44.wav'); marks.append((k, t)); parts += [a, np.zeros(int(sr * 1.2))]; t += len(a) / sr + 1.2
sf.write(out + '.wav', np.concatenate(parts), sr)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', out + '.wav', '-ac', '1', '-b:a', '96k', out + '.mp3'], check=True)
b = base64.b64encode(open(out + '.mp3', 'rb').read()).decode()
json.dump({'audio_url': 'data:audio/mpeg;base64,' + b, 'language_code': 'tha', 'tag_audio_events': False, 'diarize': False}, open(out + '_req.json', 'w'))
r = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', 'https://fal.run/fal-ai/elevenlabs/speech-to-text', '-H', 'Content-Type: application/json', '-d', '@' + out + '_req.json'], capture_output=True, text=True).stdout
r = json.loads(r); marks.append(('end', 1e9))
for i, (k, t0) in enumerate(marks[:-1]):
    print(f'{k:14s}', ''.join(w['text'] for w in r['words'] if t0 - 0.3 <= w['start'] < marks[i + 1][1] - 0.3).strip())
