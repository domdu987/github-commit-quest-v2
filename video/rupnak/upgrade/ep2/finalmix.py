"""Rule A5 finishing (owner 2 Nov: "เพลงเบาไม่ได้ยิน"): an audible score with a gentle duck, then ONE linear gain to -14 LUFS
(no loudnorm, so the stems stay exactly what is summed), a soft peak limit at -1.2 dBTP, and the stems written next to mix.wav."""
import os, re, subprocess
import numpy as np

SR = 48000


def duck_curve(vo, amount=0.5, att=0.08, rel=0.4, rate=200):
    """1 → (1-amount) while the voice speaks: a voice-activity envelope with an 80 ms attack and a 400 ms release (no gate)."""
    hop = SR // rate; n = len(vo) // hop + 1
    e = np.sqrt(np.add.reduceat(vo.astype(np.float64) ** 2, np.arange(0, len(vo), hop)) / hop)[:n]
    on = np.clip((20 * np.log10(e + 1e-9) + 50) / 12, 0, 1)   # -50 dBFS → 0 … -38 dBFS → 1 (speech is ~-20)
    a, r = np.exp(-1 / (att * rate)), np.exp(-1 / (rel * rate)); s = np.zeros(n); v = 0.0
    for i in range(n):
        k = a if on[i] > v else r
        v = k * v + (1 - k) * on[i]; s[i] = v
    g = 1 - amount * s
    return np.interp(np.arange(len(vo)) / hop, np.arange(n), g).astype(np.float32)


def _lufs(x):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", "ebur128=peak=true", "-f", "null", "-"],
                         input=np.repeat(x.astype(np.float32)[:, None], 2, 1).tobytes(), capture_output=True).stderr.decode()
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1]); P = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)[-1])
    return I, P


def _write(path, x):
    # duplicate the channel ourselves (ffmpeg's mono→stereo upmix drops each side 3 dB)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", path],
                   input=np.repeat(x.astype(np.float32)[:, None], 2, 1).tobytes(), check=True)


def finalize(here, mix, vo_part, mus_part, target=-14.0, tp=-1.8):
    """mix = vo_part + mus_part + effects (already summed); writes mix.wav, vo_stem.wav, music_stem.wav at the same gain."""
    for _ in range(3):
        I, P = _lufs(mix); g = 10 ** ((target - I) / 20)
        mix, vo_part, mus_part = mix * g, vo_part * g, mus_part * g
        I, P = _lufs(mix)
        if P <= tp: break
        lim = 10 ** ((tp - 0.3) / 20); pk = np.max(np.abs(mix))   # soft knee limiter on the mix only, then renormalise
        over = np.abs(mix) > lim * 0.8
        mix = np.where(over, np.sign(mix) * (lim * 0.8 + (lim * 0.2) * np.tanh((np.abs(mix) - lim * 0.8) / (lim * 0.2))), mix).astype(np.float32)
    I, P = _lufs(mix)
    _write(os.path.join(here, "mix.wav"), mix); _write(os.path.join(here, "vo_stem.wav"), vo_part); _write(os.path.join(here, "music_stem.wav"), mus_part)
    print(f"final: {I:.1f} LUFS, true peak {P:.1f} dBFS")
