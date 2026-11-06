"""หนวดใส ฉบับเต็ม · bookends sound (16 s: title 0–3, credits 3–8, card 8–16): the title lands on a low hit over the sea; the sea holds
under the credits for 5 s and fades to silence (bible §7); the end card is silent but for the two boxes popping in. No beds, no hiss."""
import json, os, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000; N = 16 * SR
AMB = "/home/user/github-commit-quest-v2/video/jelly-ep1/production/ambience"
def load(p): return np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]), np.float32).copy()
def filt(x, af):
    y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32).copy()
    return np.pad(y, (0, max(0, len(x) - len(y))))[: len(x)]
def level(x, t): xs = x[np.abs(x) > 1e-4]; return x * 10 ** ((t - 20 * np.log10(np.sqrt(np.mean(xs ** 2)) + 1e-9)) / 20)
waves = filt(load(os.path.join(AMB, "waves.mp3")), "lowpass=f=2000,lowpass=f=2000,lowpass=f=2000,highpass=f=60")
while len(waves) < N: waves = np.concatenate([waves, waves])
amb = level(waves[:N], -34); t = np.arange(N) / SR
env = np.clip(t / 0.6, 0, 1) * np.clip((8.0 - t) / 0.6, 0, 1); amb *= env.astype(np.float32)   # 0 → 8 s: the sea, gone before the card
cues = {"duration": 16, "sections": [{"start": 0, "end": 16, "mood": "silence"}], "sfx": [{"t": 0.12, "type": "thud", "gain": 0.3}, {"t": 0.7, "type": "swell", "gain": 0.14}, {"t": 8.5, "type": "pop", "gain": 0.2}, {"t": 8.7, "type": "pop", "gain": 0.2}]}
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"))
subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"), os.path.join(HERE, "sfx_cues.json"), os.path.join(HERE, "sfx.wav")], check=True, env={**os.environ, "STEMS": "1"})
sfx = load(os.path.join(HERE, "sfx_sfx.wav"))[:N]; sfx = np.pad(sfx, (0, N - len(sfx)))
sfx = filt(level(sfx, -27), "lowpass=f=3000,highpass=f=40")
mix = amb + sfx
mix *= 10 ** (-2 / 20)   # sits under the long's -14 (the long mix applies one static gain over everything)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", "pcm_s16le", os.path.join(HERE, "mix.wav")], input=mix.astype(np.float32).tobytes(), check=True)
print("bookends mix 16.0")
