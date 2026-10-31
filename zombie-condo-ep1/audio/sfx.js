// สร้างเสียงประกอบ/แอมเบียนต์ด้วย fal.ai (stable-audio-25) — แคชเป็น mp3 ใน audio/sfx/
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const dir = path.join(__dirname, 'sfx'); fs.mkdirSync(dir, { recursive: true });
const SFX = {
  city_dusk: ['bangkok city ambience from a high balcony at dusk, distant traffic, car horns, faraway sirens, wind at height', 20],
  city_night: ['quiet city night ambience from high above, distant sirens, wind, eerie stillness, occasional far scream', 30],
  drone: ['dark tense cinematic ambient drone, low sub bass, slow pulse, suspense, horror underscore, no melody', 47],
  boom: ['deep cinematic impact boom with sub bass, trailer hit, short tail', 2],
  elev_ding: ['elevator arrival ding bell, single chime, indoor hall, clean', 2],
  elev_motor: ['elevator machinery humming and cables moving, metallic, distant, ominous', 8],
  elev_doors: ['elevator doors sliding open, metallic, indoor hall', 3],
  water_fill: ['bathtub filling with water from a tap, bathroom reverb, continuous', 10],
  drip: ['single water drops dripping into a sink, slow, bathroom echo', 5],
  meow: ['house cat meowing loudly twice, alert, indoor', 3],
  drag_metal: ['heavy steel cabinet being dragged across a concrete floor, scraping, then a thud against a door', 6],
  crowd: ['panicked crowd running in a lobby, shouting, footsteps, glass rattling', 6],
  beep: ['electrical panel warning beep, repeating, then power down hum', 4],
  pencil: ['pencil writing quickly on paper, close microphone, quiet room', 6],
  riser: ['horror tension riser, rising string and noise swell, ends abruptly', 4],
  pop: ['soft UI pop notification click, short, clean', 1],
  walk: ['footsteps on tile corridor, flat shoes, walking steadily, indoor', 4],
  flicker: ['fluorescent light buzzing and flickering, electrical', 4],
};
for (const [k, [prompt, sec]] of Object.entries(SFX)) {
  const out = path.join(dir, `${k}.mp3`); if (fs.existsSync(out)) continue;
  const res = execFileSync('curl', ['-sS', '-m', '240', '-X', 'POST', 'https://fal.run/fal-ai/stable-audio-25/text-to-audio', '-H', 'Content-Type: application/json', '-H', 'Authorization: Key dummy',
    '-d', JSON.stringify({ prompt, seconds_total: sec, steps: 8 })]).toString();
  let j; try { j = JSON.parse(res); } catch { console.error(k, res.slice(0, 200)); continue; }
  if (!j.audio) { console.error(k, res.slice(0, 300)); continue; }
  const wav = out.replace(/\.mp3$/, '.wav'); execFileSync('curl', ['-sS', '-o', wav, j.audio.url]); execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', out]); fs.unlinkSync(wav); console.log('ok', k, sec + 's');
}
