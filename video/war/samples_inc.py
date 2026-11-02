# ---- recorded-style effects (ElevenLabs sound effects in scratchpad/sfxlib) laid over the synth stem ----
SFXLIB = "/home/user/github-commit-quest-v2/video/war/sfxlib"
_cache = {}


def smp(name, maxlen=None):
    if name not in _cache:
        _cache[name] = load(os.path.join(SFXLIB, name + ".mp3"))
    x = _cache[name].copy()
    if maxlen:
        x = x[: int(maxlen * SR)]
    x = x * (0.12 / (np.sqrt(np.mean(x ** 2)) + 1e-9))   # every sample to the same loudness, then the cue's gain
    n = len(x)
    fi, fo = min(n, int(0.01 * SR)), min(n, int((0.4 if n > 4 * SR else 0.12) * SR))
    x[:fi] *= np.linspace(0, 1, fi)
    x[n - fo:] *= np.linspace(1, 0, fo)
    return x


REPLACED = {"crickets", "engine", "click", "beep", "screech", "thud", "splash", "roar", "motor", "bubbles", "glitch", "powerdown", "buzz", "knock"}
