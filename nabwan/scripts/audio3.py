import sys, numpy as np, librosa, torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification
d = sys.argv[1]; sr = 16000
mix = librosa.load(f"{d}/../../../audio/audio16k.wav", sr=sr)[0]
fe = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593").eval()
labels = model.config.id2label
want = ["Meow","Cat","Hiss","Whoosh, swoosh, swish","Ding","Chime","Bell","Pop","Boing","Thump, thud","Explosion","Rumble","Sound effect","Zipper (clothing)","Scrape","Click","Jingle, tinkle","Glockenspiel","Piano","Strings","Violin, fiddle","Cello","Guitar","Ukulele","Harp","Synthesizer","Ambient music","Music of Asia","Tender music","Sad music","Happy music","Background music","Theme music"]
idx = {v:k for k,v in labels.items()}
def probs(y):
    inp = fe(y, sampling_rate=sr, return_tensors="pt")
    with torch.no_grad(): return torch.sigmoid(model(**inp).logits)[0]
for a in np.arange(60.0, 70.0, 0.5):
    p = probs(mix[int(a*sr):int((a+1.0)*sr)])
    s = {w: round(float(p[idx[w]]),2) for w in ["Meow","Cat","Whoosh, swoosh, swish","Ding","Chime","Sound effect"] if w in idx}
    print(f"{a:5.1f}", s)
p = probs(librosa.load(f"{d}/music_only.wav", sr=sr)[0][:sr*40])
print("music 0-40 mood/instr:", sorted([(w, round(float(p[idx[w]]),3)) for w in want if w in idx], key=lambda x:-x[1])[:14])
p = probs(librosa.load(f"{d}/music_only.wav", sr=sr)[0][sr*61:sr*70])
print("music 61-70 mood/instr:", sorted([(w, round(float(p[idx[w]]),3)) for w in want if w in idx], key=lambda x:-x[1])[:14])
