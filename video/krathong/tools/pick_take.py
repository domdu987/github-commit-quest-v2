import sys, glob, os, re, json
sys.path.insert(0, "tools"); os.environ.setdefault("WHISPER_DIR", "/tmp/claude-0/-home-user-github-commit-quest-v2/dadc119d-850b-549d-82c6-f1e8a1f13306/scratchpad/whisper")
import voice_qa as Q
from faster_whisper import WhisperModel
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", download_root=Q.MODEL_DIR)
L = {l["id"]: l for l in json.load(open("lines.json"))}
for vid in sys.argv[1:]:
    for f in sorted(glob.glob(f"vo/{vid}.*.mp3")):
        heard, _ = Q.transcribe(m, f)
        print(vid, os.path.basename(f), round(Q.cer(L[vid]["text"], heard), 3), heard)
