// สร้างไทม์ไลน์จากความยาวเสียงจริง + ประกอบแทร็กเสียงบรรยาย (เร่งด้วย atempo)
// ใช้: node audio/timeline.js  -> audio/timeline.json, audio/voice.wav
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const TEMPO = parseFloat(process.env.TEMPO || '1.15');
const lines = JSON.parse(fs.readFileSync(path.join(__dirname, 'lines.json'), 'utf8'));
const durs = JSON.parse(fs.readFileSync(path.join(__dirname, 'durations.json'), 'utf8'));
// ช่องว่างก่อนแต่ละคลิป (วินาที) — จังหวะหายใจของผู้บรรยาย
const GAP_BEFORE = { '01': 0.5, '02': 0.35, '03': 0.35, '04a': 0.45, '04b': 0.55, '04c': 0.45, '05': 0.4, '06': 0.45, '07': 0.4, '08': 0.4, '09': 0.4, '10a': 0.6, '10b': 1.0 };
const END_CARD = 4.0; // การ์ด "ตอนที่ 2"
let t = 0; const clips = [];
for (const l of lines) {
  t += GAP_BEFORE[l.id] ?? 0.35;
  const d = durs[l.id] / TEMPO;
  clips.push({ id: l.id, beat: l.beat, start: +t.toFixed(3), end: +(t + d).toFixed(3), dur: +d.toFixed(3), text: l.tts });
  t += d;
}
const voiceEnd = t; const total = t + 0.5 + END_CARD;
const timeline = { fps: 30, tempo: TEMPO, voiceEnd: +voiceEnd.toFixed(3), endCardStart: +(voiceEnd + 0.5).toFixed(3), total: +total.toFixed(3), clips };
fs.writeFileSync(path.join(__dirname, 'timeline.json'), JSON.stringify(timeline, null, 1));
// ประกอบเสียง: แต่ละคลิป atempo แล้ว adelay ไปยังตำแหน่ง start
const inputs = []; const fc = []; const mixIn = [];
clips.forEach((c, i) => {
  inputs.push('-i', path.join(__dirname, 'clips', `${c.id}.mp3`));
  fc.push(`[${i}:a]atempo=${TEMPO},aresample=48000,adelay=${Math.round(c.start * 1000)}|${Math.round(c.start * 1000)}[a${i}]`);
  mixIn.push(`[a${i}]`);
});
fc.push(`${mixIn.join('')}amix=inputs=${clips.length}:normalize=0,apad=whole_dur=${total.toFixed(3)},loudnorm=I=-16:TP=-1.5:LRA=11[out]`);
execFileSync('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex', fc.join(';'), '-map', '[out]', '-ar', '48000', '-ac', '2', path.join(__dirname, 'voice.wav')]);
console.log(JSON.stringify(timeline, null, 1));
