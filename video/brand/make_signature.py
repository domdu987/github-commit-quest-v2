"""Build brand/signature.wav, the channel's closing line "ถูกหมดทุกข้อ… ผิดแค่… ข้อเดียว".

s01-v3.mp3 is one uninterrupted Gemini take (Puck, slow, low, suspenseful; picked by the user as "slow 1").
It is trimmed like every other line and lowered by about a semitone with the formants kept, so it sounds
deeper but still like the same narrator. No splicing (the old "ทุกอย่าง… ถูกทาง" splice sounded choppy).
Usage: python3 make_signature.py   (then copy signature.wav to each episode's production/vo/s01.wav)
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
AF = ("silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB:stop_silence=0.22,"
      "areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,"
      "rubberband=pitch=0.944:formant=preserved,apad=pad_dur=0.04")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(HERE, "s01-v3.mp3"), "-af", AF, "-ar", "44100", "-ac", "2",
                os.path.join(HERE, "signature.wav")], check=True)
print("wrote signature.wav")
