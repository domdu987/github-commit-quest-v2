// สร้างเสียงประกอบ/แอมเบียนต์ด้วย fal.ai (stable-audio-25 text-to-audio) — เรียกครั้งเดียว แคชไว้ใน audio/sfx/
// ใช้: node audio/sfx.js
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const dir = path.join(__dirname, 'sfx'); fs.mkdirSync(dir, { recursive: true });
const SFX = {
  amb_dusk: ['evening ambience at a rural roadside gas station in Thailand, cicadas and crickets, distant highway traffic, light wind, field recording', 20],
  amb_night: ['quiet rural night ambience, crickets, soft wind, distant dog, eerie stillness, field recording', 30],
  drone: ['dark tense cinematic ambient drone, low sub bass, slow pulse, suspense, horror underscore, no melody', 47],
  throttle: ['motorcycle engine idling then sharp throttle rev, close microphone', 3],
  boom: ['deep cinematic impact boom with sub bass, trailer hit, short tail', 2],
  generator: ['portable gasoline generator pull start, engine sputters then runs steady, outdoor', 7],
  bark: ['medium dog barking aggressively several times, outdoor night, close', 3],
  lightsoff: ['heavy industrial light switch clunk then electrical hum powering down', 2],
  pencil: ['pencil writing quickly on paper, close microphone, quiet room', 6],
  doorknob: ['door knob rattling, locked metal door, quiet night, close', 2],
  riser: ['horror tension riser, rising string and noise swell, ends abruptly', 4],
  truck: ['pickup truck engine driving slowly on gravel then stops, handbrake click', 4],
  fuel: ['gasoline pouring from pump nozzle into plastic jerry can, outdoor', 4],
  pop: ['soft UI pop notification click, short, clean', 1],
  cars: ['distant traffic jam, many car horns, far away, night', 5],
  freezer: ['humming refrigerator compressor, fluorescent buzz, convenience store interior', 6],
  walk: ['footsteps on concrete, sneakers, walking steadily, outdoor', 4],
};
for (const [k, [prompt, sec]] of Object.entries(SFX)) {
  const out = path.join(dir, `${k}.mp3`); if (fs.existsSync(out)) continue;
  const res = execFileSync('curl', ['-sS', '-m', '240', '-X', 'POST', 'https://fal.run/fal-ai/stable-audio-25/text-to-audio', '-H', 'Content-Type: application/json', '-H', 'Authorization: Key dummy',
    '-d', JSON.stringify({ prompt, seconds_total: sec, steps: 8 })]).toString();
  let j; try { j = JSON.parse(res); } catch { console.error(k, res.slice(0, 200)); continue; }
  if (!j.audio) { console.error(k, res.slice(0, 300)); continue; }
  const wav = out.replace(/\.mp3$/, '.wav'); execFileSync('curl', ['-sS', '-o', wav, j.audio.url]); execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', out]); fs.unlinkSync(wav); console.log('ok', k, sec + 's');
}
