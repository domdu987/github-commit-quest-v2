// ผสมเสียงบรรยาย + SFX/แอมเบียนต์ตามไทม์ไลน์ -> audio/mix.wav
// ใช้: node audio/mix.js
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const tl = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json'), 'utf8'));
const cues = JSON.parse(fs.readFileSync(path.join(__dirname, 'cues.json'), 'utf8'));
const T = id => tl.clips.find(c => c.id === id); const C = (id, i) => cues.find(c => c.id === id && c.i === i).start;
const clockStart = C('05', 0) + 0.3;
// [ชื่อไฟล์, เวลาเริ่ม, ความดัง, ความยาว(ตัด), fadeIn, fadeOut]
const place = [];
const put = (name, at, vol = 0.5, len = 0, fi = 0.05, fo = 0.3) => place.push([name, at, vol, len, fi, fo]);
// ดนตรีพื้น + แอมเบียนต์
put('drone', 0, 0.28, 46, 2.5, 1.5); put('drone', 44.5, 0.32, 33, 1.5, 2.0);
put('amb_dusk', 0, 0.45, 20, 1.0, 3.0); put('amb_dusk', 18, 0.35, 8, 2.0, 3.0);
put('amb_night', 24, 0.35, 30, 3.0, 2.0); put('amb_night', 52, 0.35, 30, 2.0, 3.0);
// เหตุการณ์
put('throttle', T('02').start - 0.3, 0.55, 3, 0.05, 0.6);
put('boom', C('02', 0) + 0.05, 0.7, 2); put('boom', T('04b').start, 1.0, 2); put('boom', tl.endCardStart, 0.75, 2);
put('walk', T('04a').start, 0.45, 4, 0.2, 0.8);
put('cars', T('04c').start, 0.4, 5, 0.3, 1.0);
put('fuel', C('06', 6), 0.45, 4, 0.2, 0.8);
put('generator', C('07', 1) + 0.1, 0.6, 7, 0.05, 2.0);
put('bark', C('08', 3) + 0.3, 0.7, 3, 0.02, 0.4);
put('freezer', C('08', 5), 0.35, 6, 0.3, 1.0);
put('lightsoff', T('09').start + 0.25, 0.6, 1.2, 0.01, 0.5); put('lightsoff', T('09').start + 0.47, 0.5, 1.2, 0.01, 0.5); put('lightsoff', T('09').start + 0.69, 0.5, 1.6, 0.01, 0.8);
put('truck', C('09', 3), 0.5, 4, 0.2, 0.8);
put('pencil', C('09', 4), 0.45, 5.5, 0.2, 1.0);
put('doorknob', C('10b', 1), 0.6, 2, 0.02, 0.5);
put('riser', C('10b', 2) - 0.3, 0.55, 4, 0.5, 0.05);
// เสียง pop ของ HUD การ์ด
for (const at of [C('04c', 1), clockStart, C('06', 7) + 0.1, C('07', 3), C('07', 4), C('08', 1), C('08', 2), C('08', 3) + 0.2, C('08', 5), C('08', 6), T('09').start, C('09', 2), C('09', 3) + 0.2, C('09', 5), C('09', 6), C('09', 7) + 0.1, C('04a', 0) + 0.3, C('03', 1)]) put('pop', at, 0.4, 1, 0.01, 0.3);
const inputs = ['-i', path.join(__dirname, 'voice.wav')]; const fc = []; const mix = ['[0:a]'];
place.forEach(([name, at, vol, len, fi, fo], i) => {
  inputs.push('-i', path.join(__dirname, 'sfx', `${name}.mp3`));
  const trim = len ? `atrim=0:${len},` : '';
  const dur = len || 60;
  fc.push(`[${i + 1}:a]${trim}aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,afade=t=in:st=0:d=${fi},afade=t=out:st=${Math.max(0, dur - fo)}:d=${fo},volume=${vol},adelay=${Math.round(at * 1000)}|${Math.round(at * 1000)}[s${i}]`);
  mix.push(`[s${i}]`);
});
fc.push(`${mix.join('')}amix=inputs=${mix.length}:normalize=0:dropout_transition=0,atrim=0:${tl.total},apad=whole_dur=${tl.total},loudnorm=I=-14:TP=-1.0:LRA=11[out]`);
execFileSync('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex', fc.join(';'), '-map', '[out]', '-ar', '48000', '-ac', '2', path.join(__dirname, 'mix.wav')]);
console.log('mix.wav', place.length, 'placements');
