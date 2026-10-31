// จัดเวลาซับไตเติลให้ตรงกับเสียงจริง ด้วย Whisper (fal.ai) ระดับตัวอักษร
// ใช้: node audio/align.js -> audio/cues.json  (+ scenes/timeline.data.js)
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const tl = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json'), 'utf8'));
const subs = JSON.parse(fs.readFileSync(path.join(__dirname, 'subs.json'), 'utf8'));
const wdir = path.join(__dirname, 'whisper'); fs.mkdirSync(wdir, { recursive: true });
const strip = s => s.replace(/[\[\]{}\s]/g, '');
const tmp = '/tmp/claude-0/-home-user-github-commit-quest-v2/4c534666-d471-5527-8195-0a313cf890cc/scratchpad';
function whisper(id) {
  const out = path.join(wdir, `${id}.json`);
  if (fs.existsSync(out)) return JSON.parse(fs.readFileSync(out, 'utf8'));
  const b64 = fs.readFileSync(path.join(__dirname, 'clips', `${id}.mp3`)).toString('base64');
  const req = path.join(tmp, `w_${id}.json`);
  fs.writeFileSync(req, JSON.stringify({ audio_url: 'data:audio/mpeg;base64,' + b64, language: 'th', task: 'transcribe', chunk_level: 'word' }));
  const res = execFileSync('curl', ['-sS', '-m', '240', '-X', 'POST', 'https://fal.run/fal-ai/whisper', '-H', 'Content-Type: application/json', '-H', 'Authorization: Key dummy', '-d', '@' + req]).toString();
  const j = JSON.parse(res); if (!j.chunks) throw new Error(id + ': ' + res.slice(0, 200));
  fs.writeFileSync(out, JSON.stringify(j)); return j;
}
const cues = [];
for (const c of tl.clips) {
  const w = whisper(c.id);
  // แผนที่ตัวอักษร -> เวลา (ในหน่วยเวลาเดิมของคลิป ก่อน tempo)
  let chars = '', times = [];
  for (const ch of w.chunks) { const s = ch.text.replace(/\s/g, ''); for (let i = 0; i < s.length; i++) { chars += s[i]; times.push(ch.timestamp[0] + (ch.timestamp[1] - ch.timestamp[0]) * (i / Math.max(1, s.length))); } }
  const chunks = subs[c.id]; const n = chunks.length; const plain = chunks.map(strip); const totalChars = plain.join('').length;
  let pos = 0, cumChars = 0; const starts = [];
  chunks.forEach((raw, i) => {
    let found = -1;
    if (i === 0) found = 0;
    else {
      for (const len of [5, 4, 3, 2]) { const key = plain[i].slice(0, len); const k = chars.indexOf(key, pos); if (k >= 0 && k - pos < 40) { found = k; break; } }
    }
    let tLocal;
    if (found >= 0) { tLocal = times[found] ?? 0; pos = found + Math.max(1, plain[i].length - 2); }
    else { tLocal = (c.dur * tl.tempo) * (cumChars / totalChars); pos = Math.min(chars.length - 1, pos + plain[i].length); console.error('fallback', c.id, i, plain[i]); }
    cumChars += plain[i].length;
    starts.push(tLocal / tl.tempo);
  });
  chunks.forEach((raw, i) => {
    const s = c.start + (i === 0 ? 0 : Math.max(starts[i], starts[i - 1] + 0.35));
    const e = i < n - 1 ? c.start + Math.max(starts[i + 1], starts[i] + 0.35) : c.end + 0.15;
    cues.push({ id: c.id, i, beat: c.beat, start: +s.toFixed(3), end: +Math.max(e, s + 0.4).toFixed(3), text: raw });
  });
}
// ซ่อมให้ลำดับไม่ซ้อน
for (let i = 1; i < cues.length; i++) if (cues[i].start < cues[i - 1].end && cues[i].id === cues[i - 1].id) cues[i - 1].end = cues[i].start;
fs.writeFileSync(path.join(__dirname, 'cues.json'), JSON.stringify(cues, null, 1));
fs.writeFileSync(path.join(__dirname, '..', 'scenes', 'timeline.data.js'), 'window.TIMELINE=' + JSON.stringify(tl) + ';\nwindow.CUES=' + JSON.stringify(cues) + ';\n');
for (const q of cues) console.log(q.id, q.i, q.start, q.end, q.text);
