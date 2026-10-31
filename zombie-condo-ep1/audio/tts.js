// สร้างเสียงบรรยายทีละบีตผ่าน fal.ai (MiniMax speech-02-hd, language_boost=Thai) แล้ววัดความยาวจริง
// หมายเหตุ: ทดสอบแล้ว ElevenLabs multilingual-v2 ออกเสียงไทยเพี้ยน (Whisper ถอดความไม่ได้) ส่วน MiniMax ถอดความได้ตรงทุกคำ
// ใช้: node audio/tts.js   (ต้องมี FAL_KEY หรือ proxy ที่แทรก key ให้ fal.run)
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const dir = path.join(__dirname, 'clips');
const lines = JSON.parse(fs.readFileSync(path.join(__dirname, 'lines.json'), 'utf8'));
const VOICE = process.env.VOICE || 'Deep_Voice_Man';
async function gen(line) {
  const out = path.join(dir, `${line.id}.mp3`);
  if (fs.existsSync(out) && !process.env.FORCE) return;
  // ใช้ curl เพื่อให้วิ่งผ่าน HTTPS_PROXY ของ environment ได้
  const body = JSON.stringify({ text: line.tts, voice_setting: { voice_id: VOICE, speed: parseFloat(process.env.SPEED || '1.08'), vol: 1, pitch: 0 }, language_boost: 'Thai', output_format: 'url' });
  const res = execFileSync('curl', ['-sS', '-m', '180', '-X', 'POST', 'https://fal.run/fal-ai/minimax/speech-02-hd',
    '-H', 'Content-Type: application/json', '-H', `Authorization: Key ${process.env.FAL_KEY || 'dummy'}`, '-d', body]).toString();
  let j; try { j = JSON.parse(res); } catch { throw new Error(`${line.id}: ${res}`); }
  if (!j.audio) throw new Error(`${line.id}: ${res}`);
  execFileSync('curl', ['-sS', '-o', out, j.audio.url]);
  console.log('ok', line.id);
}
(async () => {
  fs.mkdirSync(dir, { recursive: true });
  await Promise.all(lines.map(gen));
  const durs = {};
  for (const l of lines) {
    const p = path.join(dir, `${l.id}.mp3`);
    durs[l.id] = parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).toString());
  }
  fs.writeFileSync(path.join(__dirname, 'durations.json'), JSON.stringify(durs, null, 1));
  console.log(durs);
})();
