// ผสมเสียงบรรยาย + SFX/แอมเบียนต์ตามไทม์ไลน์ -> audio/mix.wav   (เรื่อง "คอนโดชั้น 23")
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const tl = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json'), 'utf8'));
const cues = JSON.parse(fs.readFileSync(path.join(__dirname, 'cues.json'), 'utf8'));
const T = id => tl.clips.find(c => c.id === id); const C = (id, i) => cues.find(c => c.id === id && c.i === i).start;
const clockStart = C('05', 0) + 0.3;
const place = []; const put = (name, at, vol = 0.5, len = 0, fi = 0.05, fo = 0.3) => place.push([name, at, vol, len, fi, fo]);
// พื้นเสียง
put('drone', 0, 0.26, 46, 2.5, 1.5); put('drone', 44.5, 0.32, 40, 1.5, 2.0);
put('city_dusk', 0, 0.5, 20, 1.0, 3.0); put('city_dusk', 18, 0.35, 10, 2.0, 3.0);
put('city_night', 26, 0.3, 30, 3.0, 2.0); put('city_night', 54, 0.3, 30, 2.0, 3.0);
// เหตุการณ์
put('elev_ding', T('02').start - 0.1, 0.5, 2);
put('boom', C('02', 0) + 0.1, 0.7, 2); put('boom', T('04b').start, 1.0, 2); put('boom', tl.endCardStart, 0.75, 2);
put('walk', T('04a').start, 0.4, 4, 0.2, 0.8);
put('crowd', T('04c').start, 0.45, 5, 0.3, 1.0);
put('beep', T('05').start + 0.3, 0.45, 4, 0.1, 0.8); put('flicker', T('05').start + 2, 0.3, 3, 0.3, 0.8);
put('water_fill', C('06', 6), 0.45, T('07').start - C('06', 6), 0.3, 0.8);
put('drip', C('07', 3), 0.5, 4, 0.2, 0.8);
put('meow', C('08', 4) + 0.3, 0.7, 3, 0.02, 0.4);
put('drag_metal', T('09').start + 0.2, 0.6, 6, 0.1, 0.6);
put('elev_doors', C('09', 2) + 0.3, 0.5, 3, 0.05, 0.5); put('elev_doors', C('09', 2) + 0.9, 0.4, 3, 0.05, 0.5);
put('pencil', C('09', 4), 0.4, 5.5, 0.2, 1.0);
put('elev_ding', C('10b', 1), 0.55, 2); put('elev_motor', C('10b', 1) + 0.2, 0.6, 8, 0.1, 0.05);
put('riser', C('10b', 2) - 0.2, 0.5, 4, 0.5, 0.05);
for (const at of [C('03', 1), C('04a', 0) + 0.3, C('04c', 0) + 0.4, clockStart, C('06', 6) + 0.2, C('07', 1), C('07', 2), C('07', 4), C('08', 1), C('08', 2), C('08', 3), C('08', 4) + 0.2, C('09', 1), C('09', 2) + 0.9, C('09', 5), C('09', 6), C('09', 7)]) put('pop', at, 0.4, 1, 0.01, 0.3);
const inputs = ['-i', path.join(__dirname, 'voice.wav')]; const fc = []; const mix = ['[0:a]'];
place.forEach(([name, at, vol, len, fi, fo], i) => {
  const f = path.join(__dirname, 'sfx', `${name}.mp3`); if (!fs.existsSync(f)) { console.error('missing sfx', name); return; }
  inputs.push('-i', f); const k = inputs.length / 2 - 1; const dur = len || 60;
  fc.push(`[${k}:a]${len ? `atrim=0:${len},` : ''}aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,afade=t=in:st=0:d=${fi},afade=t=out:st=${Math.max(0, dur - fo)}:d=${fo},volume=${vol},adelay=${Math.round(at * 1000)}|${Math.round(at * 1000)}[s${k}]`);
  mix.push(`[s${k}]`);
});
fc.push(`${mix.join('')}amix=inputs=${mix.length}:normalize=0:dropout_transition=0,atrim=0:${tl.total},apad=whole_dur=${tl.total},loudnorm=I=-14:TP=-1.0:LRA=11[out]`);
execFileSync('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex', fc.join(';'), '-map', '[out]', '-ar', '48000', '-ac', '2', path.join(__dirname, 'mix.wav')]);
console.log('mix.wav', mix.length - 1, 'placements');
