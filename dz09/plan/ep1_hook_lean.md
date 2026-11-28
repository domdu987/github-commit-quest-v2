# EP.1 "ทางด่วนนรก" — opening hook, lean plan (Director C)

Scene 01 "สายที่ไม่ได้รับ" complete, plus the first beat of Scene 02 "คนที่กลับมา" (the driver lunges and bites). Vertical 720x1280, 24 fps, Thai dialogue with burned-in Thai captions. Every shot is rendered in 3D through the v3 pipeline (puppet cards in a Blender set). The only exception is the black title card at the end.

The approach: one expressway set seen from eight camera setups. Three new puppets. Five new props. Rain, splashes and screen droplets are done in post and use the render's depth pass. Nothing in this plan needs a second location, a crowd, or a back view of a puppet.

## Header

| Item | Value |
|---|---|
| Total duration | 54.50 s = 1308 frames at 24 fps (51.75 s of picture plus a 2.75 s black title card) |
| Shot count | 17 shots (16 rendered in 3D, 1 title card), 16 camera takes. Shots 09 and 10 are joined by a cut hidden inside a whip pan. |
| Average shot length | 3.21 s (median 3.0 s). With in-shot snaps, the framing changes every 1.3 s on average. |
| Transitions | 9 hard cuts, 1 punch-in, 1 hidden whip cut, 4 dissolves (9-13 frames), 1 smash to black |
| Sets | **1**: `expressway3d` (an elevated Bangkok expressway deck in the rain at night). It holds every shot, including the inserts on real props and the car interior. |
| Cast on screen | **3 new puppets**: ก้อง (Kong), เจ้าหน้าที่กู้ภัย (the rookie rescuer, `rookie`), คนขับ (the driver, `driver`, alive and then infected). |
| Voices off screen | เสียงวิทยุ (another unit's rescuer, radio only). น้ำเหนือ (phone only); her face appears only as a small contact photo drawn into the phone texture. |
| Props (new) | Cordless rescue spreader with a 3-bar battery LED. Crowbar (ชะแลง) on Kong's pack. Phone (3 screen states). Shoulder radio (costume detail, plus a 3D insert prop). Wristwatch with a red seconds hand (costume detail on Kong's left wrist). |
| Set dressing (in the set) | Crashed hero sedan (its driver door opens; simple interior; stuck wiper). A second crashed car. Kong's rescue pickup with a red light bar. 3 gridlock car models, instanced about 40 times. 2 light masts. Jersey barriers. Skyline backdrop card. |
| Effects | Rain streaks in 3 depth layers (post, occluded by the Z pass). Puddle splashes (post, projected onto the road). Raindrops on the phone and radio screens (post, registered to the prop corners). Puppet `drip` effect (wet hair and sleeves). Pulsing `tint` for the red light on the cards. Pocket glow. Radio static and LED. Handheld camera noise in 4 levels. |
| Palette | EP.1: deep blue (shade and ambient, hue 235-255), wet grey (concrete, asphalt), emergency red (light bar, LEDs, reflections). Warm colours appear only on Kong's orange suit and the phone screen. |
| Render estimate | 1242 rendered frames + about 46 dissolve handle frames = 1288 Cycles frames at an estimated 15-17 CPU s each, about 5.8 CPU hours (about 1.5 h wall on 4 cores). The budget is 18 CPU s per frame; see "Budget". |

### Handheld levels (camera noise added on top of the eased move, keys every 3 frames, Bezier, never linear)

| Level | Use | Amplitude |
|---|---|---|
| H0 | locked drift (dread, the call's silence) | 0 |
| H1 | breathing | 1.5 px sd, about 1 Hz |
| H2 | nervous, work in progress | 4 px sd, 2 Hz, roll ±0.6° |
| H3 | violence (the lunge only) | 12 px sd, 5 Hz, 86 px peak to peak, 1.0-1.5 s, then decays over 10 frames |

The handheld energy follows emotion: H2 for the rescue work, H1 for the call, H0 while the driver lifts his head, H3 only for the bite.

### Light model for the set (one key, as LOOK_SPEC)

- **Key:** a sun lamp motivated by the nearer of the two light masts. Cool white `#cfd8ff`, angular size 0.8°, elevation 42°, coming from screen-left in most setups. Actors are drawn with `head_flip = False`: the thick ink side and the crescent sit at the lower right, away from the key. Setups that look back along the lanes (2, 13) use `head_flip = True`.
- **Ambient:** blue-violet emission term, hue 240-250, with per-surface tints: asphalt toward slate-blue, concrete toward grey-blue, the orange suit left untinted. Shade must come out at 0.15-0.31 of lit luminance.
- **Emergency red:** the light bar on Kong's pickup is emissive geometry (bloom above 1.0) plus **one** red point light with shadows off. It runs a 2 Hz double flash, alternating left and right (L-L-R-R per 1 s).
  - Red on the road is an emissive "reflection smear" decal under and behind the truck that pulses in sync. This is not glossy ray tracing; it keeps direct-light-only rendering at 12 samples.
  - Red on the actors: cards are never lit, so each puppet's `tint` is driven per frame from the light bar phase (peak `#ffb0a8` on the side facing the truck, lerped over 2 frames) and `rim="#ff5a4a"` at 0.4 opacity on flash frames. Body and face must still read in shade.
- **Fog:** Blender mist pass. The post grade mixes a navy haze `#1b2440` by depth (0 at 15 D, 0.75 at 140 D), so the gridlock fades into the rain.
- **Night ink** on all puppets: `ink="#1e142e"`. The skin and head fill get a night tint `#dfe4ff` before the red pulse.

### Captions

Thai, burned in, bottom band. Use Noto Sans Thai Bold or Sarabun Bold from `@fontsource` (free, not yet installed; see Risks). White with a 6 px dark outline. Phrases are 4-14 Thai characters.

Off-screen voices (radio and phone) get a different caption colour, pale cyan `#bfe9ff`, and a small icon before the first phrase of each line:
- 📻 is drawn as an SVG glyph for the radio.
- A handset glyph is used for the phone.

On-screen speakers use white. Whole heads stay above the caption band (y < 880 px).

---

## Shot list

### Shot 01 — the radio in the dark (HOOK)

| Field | Plan |
|---|---|
| Time | 0.00-3.00 s, f0-71 (72 f), 3.00 s |
| Set / setup | expressway3d, `insert_radio`: a raking insert on Kong's shoulder radio (a 3D prop pinned each frame to Kong's `shoulder_l` anchor) |
| Framing / angle / lens | Extreme close-up. Slightly low (camera 0.3 D below the radio, pitched up 8°). 22 mm, 0.7 D from the grille. The radio fills the upper-middle frame. Out of focus behind it, a big orange-and-reflective slab of Kong's vest card. |
| Camera move | Already moving on frame 0. Slow push at 8 %/s with H1. At 2.15 s ("เดี๋ยว!") a snap push ×1.5 in 14 frames onto the red TX LED. On the static burst (2.75 s) a 4-frame jolt, H3-sized but only 4 frames. |
| Cast | Kong, only as the out-of-focus vest and strap (sprite rendered at `upper_k` crop). No face, no acting needed in this frame. A rain `drip` runs off the antenna. |
| Action | Near-black frame, read as "จอดำ" from the screenplay. The only lights are the radio's red TX LED, which flickers with the voice's loudness, and raindrops beading on the grille. At 1.3 s one red sweep from the off-screen light bar crosses the radio and is gone. At "เฮ้ย!" the LED stutters; at 2.75 s the signal dies (LED off, static burst). |
| Dialogue / caption | เสียงวิทยุ (another unit, male, radio filter): 0.25 "ศูนย์ครับ" / 1.00 "คนเจ็บ" / 1.35 "ไม่ตอบสนอง..." / 2.15 "เดี๋ยว!" / 2.50 "เฮ้ย!" |
| Sound | Rain on plastic: close, dry ticks. Radio carrier hiss from 0.0, with a squelch click at 0.15. Voice band-passed at 300-3000 Hz. A wet scuffle under "เฮ้ย!". 2.75 a harsh static burst, then the radio squelch closes. No music. Room ambience muted, so the cut to rain is a slam. |
| Light | Key off this face of the radio: it is in shade, deep navy. Emissive LED with bloom. One red sweep at 1.3 s. 8-15 % of pixels darker than V 0.25 is exceeded on purpose (about 70 %). |
| Transition out | Hard cut on the static burst (f71→72). The full rain roar arrives on the cut. |
| Sets up | The bite that is about to happen here has already happened to another unit (the outbreak is spreading). Kong's radio as a story device (Scene 04 kit, later calls). |

### Shot 02 — the gridlock

| Field | Plan |
|---|---|
| Time | 3.00-6.50 s, f72-155 (84 f), 3.50 s |
| Set / setup | expressway3d, `wide_high`. The camera hangs above the shoulder, beside the near light mast, looking along the lanes toward the city. |
| Framing / angle / lens | Extreme wide. HIGH: 9 D above the deck, pitched down 18°. 22 mm. Kong and the rookie are about 40 px heads at lower third. The pileup is in the middle ground; the stopped traffic runs to the vanishing point in the haze; the skyline card is beyond. |
| Camera move | Crane down and push: an eased descent of 9 D → 6.5 D plus a forward dolly of 3 D (about 9 %/s) with H1. It decelerates to near-still by f143. |
| Cast | Kong (yaw +0.4, `wide` legs, spreader held in both hands, `determined`) walks the last 2 steps to the crashed sedan. The rookie (`worried`) tugs at the jammed driver door, with a small `lean` cycle every 20 frames. Both are small but acting. |
| Action | Establishes the pileup: the crashed sedan nosed into a second car, glass in the lane, Kong's rescue pickup angled behind with the light bar flashing. Three lanes of stopped cars with hazards blinking. The gridlock goes past the haze. |
| Dialogue / caption | None. |
| Sound | Full rain roar (wide, stereo). Distant horns, one long. Two distant sirens from different directions, at different pitches. The light bar relay tick-tock (close, panned to the truck side). Hazards on the near cars. |
| Light | Mast key from screen-left; actor shadows fall long toward screen-right and down. Red flash smears on wet asphalt. Hazard lights are small emissive orange blinks; they are the only warm points apart from Kong. |
| Transition out | Dissolve 9 frames; both shots keep moving. |
| Sets up | The scale of the gridlock: "nowhere to go" (Scene 03 truck blocked). The rescue pickup and its light bar: Scene 03 "รถกู้ภัยคันสุดท้าย"; the siren that draws the horde. |

### Shot 03 — Kong and the spreader, 3 bars

| Field | Plan |
|---|---|
| Time | 6.50-9.50 s, f156-227 (72 f), 3.00 s |
| Set / setup | expressway3d, `low_medium_K`: road level by the sedan's front wheel |
| Framing / angle / lens | Medium (head 200 px, centre at 0.42 of frame height). LOW: 1.2 D above the deck, pitched up 15°. 22 mm. Kong frame-right with the crashed sedan's crumpled hood behind him. The light bar is far frame-left, blurred red. |
| Camera move | Eased truck left 0.5 D with a slight orbit, H2. At 8.10 s a snap push ×2.2 in 16 frames down onto the spreader's battery pack, ending as a raking insert on the LED: **3 bars, green-white**. |
| Cast | Kong: yaw -0.3, `determined`, `legs: wide`. Both hands on the spreader (`arm_r`/`arm_l` hand targets on the grips). He thumbs the test trigger: the jaws open 15% and close, with a 0.03 D squash on the press. Blink at 7.2 s. Crowbar visible strapped to the right side of his backpack. Watch on the left wrist. `drip` fx on hair tips and the sleeve. |
| Action | He checks the tool before he cuts the door. This is the one gesture of the shot. |
| Dialogue / caption | None. |
| Sound | Rain on his jacket (close), the hydraulic whine of the test trigger at 7.6 s, a battery-pack beep ×3 when the bars light (8.4 s), the light bar tick. |
| Light | Key from screen-left; Kong in hard light on his left half. Red pulse in his `tint`. The LED is emissive (bloom). |
| Transition out | Hard cut on the first phone buzz (f227→228). |
| Sets up | **Battery 3 bars** (the drain countdown in later episodes; Scene 04 "เลือกเครื่องตัด"). **The crowbar on the pack** (Scene 02: "ก้องใช้ชะแลงผลักผู้ติดเชื้อ"). |

### Shot 04 — the buzz in his pocket

| Field | Plan |
|---|---|
| Time | 9.50-12.00 s, f228-287 (60 f), 2.50 s |
| Set / setup | expressway3d, `eye_two`: the sedan's driver side |
| Framing / angle / lens | Medium two-shot. EYE level. 22 mm. Kong frame-right (head 230 px); the rookie frame-left at the driver door (head 170 px; near/far ratio about 1.4). |
| Camera move | Opens on a snap push from Kong's chest pocket glow (first 14 frames) that tilts up to his face. Then a slow eased drift right at 30 px/s, H2. |
| Cast | Kong: the `pocket_glow` fx pulses with the buzz. He glances down (pitch +0.6, `gaze` down). He sees the time on his watch, a hint of guilt, and swaps to `worried` behind a blink at 10.3 s. He holds the spreader out to the rookie (arm `forward`). The rookie steps in 2 frames late, takes it (`excited` → `determined` behind a blink: eager, the youngest), and turns to the door. Kong pulls the phone from the pocket (arm_r to the chest, prop `phone`). |
| Action | Kong hands the job to the rookie so he can take the call. The wordless trade explains why the rookie, not Kong, opens the door. |
| Dialogue / caption | None. |
| Sound | Phone vibration (close, dry buzz in 2 pulses of 0.4 s, repeating). Rain. Spreader handled (a plastic knock). The rookie's boots in a puddle. |
| Light | As shot 03. The phone glow lights nothing on the card (it is emissive in the sprite only). |
| Transition out | Punch-in cut (f287→288) to the phone screen. |
| Sets up | Why Kong is not at the door when it opens (the rookie is bitten, not Kong). The spreader dropped at the bite (shot 15). |

### Shot 05 — insert: 4 missed calls

| Field | Plan |
|---|---|
| Time | 12.00-15.00 s, f288-359 (72 f), 3.00 s |
| Set / setup | expressway3d, `insert_phone`: the phone is a 3D prop (0.30 × 0.62 D, thickness 0.03 D) pinned to Kong's `hand_r` world point. Kong's ink thumb and hand ball are on his card behind it. |
| Framing / angle / lens | Raking insert from slightly above (pitched down 12°). 22 mm at 0.9 D. The screen fills 60 % of the frame above the caption band. |
| Camera move | Eased orbit 6° plus push at 7 %/s, H1. The phone itself vibrates (±2 px, in the 0.4 s pulses). |
| Cast | Kong's hand. The thumb wipes a raindrop smear across the screen at 13.1 s, then taps the green accept at 14.2 s. |
| Action | Screen state A (incoming call): "น้ำเหนือ" with a round contact photo (her head drawn by the `namnuea` cast entry: ponytail, maroon hoodie collar, `happy`). Below it a red badge: **"4 สายที่ไม่ได้รับ"**. The accept/decline buttons. Raindrops land on the glass and bead (post droplets registered to the screen corners); one runs down through her name. At the tap the screen flips to state B (in-call 00:00). |
| Dialogue / caption | No caption. The screen text is the line and sits clear of the caption band. |
| Sound | Buzz (very close). Rain ticks on glass. The swipe squeak at 13.1. A tap click at 14.2, then the line connects (a soft digital click and the room tone of her side: a quiet indoor hum). |
| Light | Screen emissive (value about 1.2, slight bloom). The rest is navy shade and the red pulse on the hand card. |
| Transition out | Dissolve 9 frames to shot 06. |
| Sets up | **The broken promise** ("4 สาย", Kong always picks the job): payoff in Scene 05 "ครั้งนี้พ่ออย่าผิดสัญญานะ". Her face (the red hoodie) is planted, so viewers recognise her in Scene 05. |

### Shot 06 — "พ่อสัญญา"

| Field | Plan |
|---|---|
| Time | 15.00-21.00 s, f360-503 (144 f), 6.00 s |
| Set / setup | expressway3d, `mcu_K_orbit`: Kong at mark K2, 2.5 D from the sedan's rear quarter, with the rookie at the driver door deep behind him |
| Framing / angle / lens | Medium close (head 290 px, centre at 0.40). EYE level. 22 mm. The rookie is out of focus frame-left behind Kong's shoulder, working the spreader into the door seam. |
| Camera move | Slow true-3D orbit of 14° to the right around Kong (the background slides about 120 px/s), with a push at 6 %/s, H1. One snap reframe ×1.3 at 18.45 s as Kong turns away from the car toward the lens. |
| Cast | **Kong** (listening, phone at the left ear, watch face toward the lens): `worried`, pitch +0.5. He blinks at 16.2 s and on "สัญญา" at 17.1 s with a tiny flinch (squash 0.97 over 2 frames). He answers with `talking` and a mouth cycle driven by his line's loudness. He turns away from the car (yaw -0.2 → +0.35 over 10 frames) and lowers his voice; head roll 10° toward the phone. **The rookie** (background): the spreader opens the door seam in 3 pulses (15.8, 17.5, 19.6 s), leaning back on each pulse. |
| Action | The daughter's complaint and Kong's stock answer, while a dangerous job goes on behind him. |
| Dialogue / caption | น้ำเหนือ (V.O., phone filter): 15.50 "พ่อ" / 15.85 "วันนี้พ่อสัญญา" / 16.90 "ว่าจะมารับหนูไง". Kong: 18.60 "พ่อมีเคสด่วนลูก" / 19.70 "รออีกแป๊บเดียว". |
| Sound | Her voice is thin, phone-band, close in the left channel. Rain ducks 3 dB under dialogue only, never to silence. Metal groan and hydraulic whine on each pulse, at a distance and frame-left. The light bar tick. |
| Light | Key from screen-left on Kong's face; the crescent is on the right. The red tint pulses through the whole line, a little stronger on his right side (truck side). |
| Transition out | Hard cut (f503→504) on her intake of breath. |
| Sets up | **The watch** (red seconds hand clearly ticking in the orbit's last second): the Scene 02 INSERT and the 60-second rule. The rookie is alone at the door. |

### Shot 07 — "ทุกครั้งเลย..."

| Field | Plan |
|---|---|
| Time | 21.00-24.00 s, f504-575 (72 f), 3.00 s |
| Set / setup | expressway3d, `cu_K_low` (same marks as shot 06, camera swung to the other side) |
| Framing / angle / lens | Close-up (head 380 px, centre at 0.45). Slightly LOW: 1.6 D, pitched up 8°. 22 mm. Behind him: the dark underside of the gantry and the rain lit by the mast. |
| Camera move | Nearly still, H0. An eased push at 5 %/s that dies by f563. This is the quietest frame in the film. |
| Cast | Kong: on "ทุกครั้งเลย" he swaps to `sad` behind a blink (pitch +0.9). His eyes close and hold closed for 10 frames (`blink`=2, held). His head sinks 0.08 D. His free hand comes up and wipes the rain off his face (arm_l `chin`, 10 frames), the one gesture. A `drip` falls from his hair across his cheek. |
| Action | He has no answer. |
| Dialogue / caption | น้ำเหนือ (V.O.): 21.40 "ทุกครั้งเลย..." |
| Sound | Rain sinks under the voice (subjective, −6 dB, the dip easing in over 12 frames). One far siren passing. Her small exhale. No music. |
| Light | Key on his near cheek. Red pulses are reduced in this shot (tint amplitude ×0.5), letting the blue night hold. |
| Transition out | Dissolve 11 frames. |
| Sets up | The emotional debt that drives Kong through all six episodes (the film's theme of who comes first). |

### Shot 08 — "เดี๋ยวพ่อโทรกลับนะ" / silence / hang-up

| Field | Plan |
|---|---|
| Time | 24.00-27.25 s, f576-653 (78 f), 3.25 s |
| Set / setup | expressway3d, `eye_34_K`: three-quarter from the car side, with the rookie at the door in frame-left middle ground (sharp this time) |
| Framing / angle / lens | Medium (Kong's head 240 px frame-right; the rookie's 150 px). EYE level. 22 mm. |
| Camera move | Eased slide left at 40 px/s with H1. It stops at 26.0 s (near-still, H0) for the silence. |
| Cast | Kong: `talking` on his line, then `worried` and frozen, listening to nothing (the listener freezes; one blink at 26.1 s). He takes the phone from his ear and looks at it (arm_r hand target moves down to the chest over 10 frames, pitch +0.6). The rookie in the background: the door seam gives and he braces his foot on the sill (`legs` `lift_r` 0.6). |
| Action | Kong promises to call back. The line is silent, then she hangs up. |
| Dialogue / caption | Kong: 24.30 "เดี๋ยวพ่อ" / 24.95 "โทรกลับนะ". (25.6-26.7 silence: no caption) |
| Sound | Kong's voice is dry, close. Then 1.1 s of line silence: only rain and the far groan of the door. At 26.70 the three-note call-ended tone, very small. |
| Light | As shot 06. |
| Transition out | Hard cut (f653→654). |
| Sets up | The promise "โทรกลับ": Scene 04 "ก้องมองโทรศัพท์ ยังไม่มีสายจากลูก" and Scene 05. |

### Shot 09 — insert: call ended

| Field | Plan |
|---|---|
| Time | 27.25-29.50 s, f654-707 (54 f), 2.25 s |
| Set / setup | expressway3d, `insert_phone` (the same build as shot 05; camera from the other side so it is not a repeat) |
| Framing / angle / lens | Raking insert, slightly low (the screen tilted up toward Kong). 22 mm. |
| Camera move | Eased push at 8 %/s. In the last 4 frames, an accelerating pan right that becomes the whip-off into shot 10 (the cut is hidden in the blur). |
| Cast | Kong's hand. The thumb hovers over "โทรกลับ" for a beat, then does not press. The hand turns to pocket the phone. |
| Action | Screen state C: "สิ้นสุดการโทร 00:21" under "น้ำเหนือ". A raindrop lands on her photo. |
| Dialogue / caption | None. |
| Sound | Rain on glass. Silence on the line. Then the metal of the door gives way with a deep crunch at 29.4 s, felt before it is seen. The whoosh of the whip starts at 29.35. |
| Light | Screen emissive, dimming at 28.8 s (screen timeout, step 1). |
| Transition out | Hidden cut in a whip pan (f707→708): 4 frames off, 5 frames on, streaked plate, actors sharp (`post.py`). |
| Sets up | Kong chose not to call back right away: the guilt engine of the season. |

### Shot 10 — "พี่ก้อง! เปิดได้แล้วครับ!"

| Field | Plan |
|---|---|
| Time | 29.50-31.75 s, f708-761 (54 f), 2.25 s |
| Set / setup | expressway3d, `door_low`: low by the sedan's front fender, looking along the car toward the opened driver door |
| Framing / angle / lens | Medium (the rookie's head 260 px). LOW: 1.2 D, pitched up 15°. 22 mm. Inside the car, dark and out of focus, the slumped driver's shoulder is just visible behind the door frame. |
| Camera move | Whip-on braking over 5 frames, then a snap push ×1.4 in 14 frames on "เปิดได้แล้ว", H2. |
| Cast | Rookie: the door swings open (door hinge keyed 0→55° over 8 frames; he staggers back with it, squash and stretch). He turns to Kong (yaw +0.6), `excited` with a wide grin, waves the spreader (arm_r `raised`). He sets the spreader on the road (arm down, prop released at 31.4 s and left lying by the front tyre). His mouth cycle follows his line. |
| Action | The door is open. The rookie is proud: the youngest one did it. |
| Dialogue / caption | Rookie: 30.00 "พี่ก้อง!" / 30.55 "เปิดได้แล้วครับ!" |
| Sound | Metal tearing, the door's final pop. A hinge squeal. His shout is bright and near. The spreader set down on asphalt with a metal clunk. The stuck wiper inside the car starts squeaking (once every 1.2 s) as the jolt frees it. |
| Light | Key from screen-left. The car interior is dark except for the dome light (warm-dim emissive `#ffdca8` at 0.3, flickering). |
| Transition out | Hard cut (f761→762). |
| Sets up | The open door: the bite. The squeaking wiper: the metronome of dread in shot 12. |

### Shot 11 — Kong pockets the phone and goes

| Field | Plan |
|---|---|
| Time | 31.75-34.50 s, f762-827 (66 f), 2.75 s |
| Set / setup | expressway3d, `track_K`: alongside the sedan |
| Framing / angle / lens | Medium-wide (head 200 px). EYE level. 22 mm. |
| Camera move | Tracks left with Kong (a truck of 2.4 D, eased in and out) with H2. It lets him walk out of frame-left at the end while the camera settles on the open door. |
| Cast | Kong: pushes the phone into the chest pocket (arm_r to the chest, prop removed on contact). Behind a blink he swaps from `worried` to `determined` (job face back on). He walks 2 steps (walk cycle, near-profile yaw -0.9, head bob 0.47 D, period 20 frames at 24 fps). His right hand touches the crowbar strap as he goes (a habit, not yet drawing it). |
| Action | Back to work. |
| Dialogue / caption | None. |
| Sound | Boots in standing water ×4. Pocket zip. Rain. The wiper squeak continues from inside the car, closer now. |
| Light | As shot 08; the red pulses build back to full amplitude. |
| Transition out | Dissolve 13 frames (time compresses; the dread begins). |
| Sets up | The crowbar is within reach of his right hand (shot 16 and Scene 02). |

### Shot 12 — the rookie leans into the car

| Field | Plan |
|---|---|
| Time | 34.50-40.00 s, f828-959 (132 f), 5.50 s |
| Set / setup | expressway3d, `interior_pass`: the camera at the passenger-side window, looking across the dashboard toward the open driver door. The windshield is to the left of frame with rain sheeting down it. |
| Framing / angle / lens | Medium (the rookie's head 240 px, entering the door gap). The driver is in the foreground right, slumped, head on the wheel, seen from his left side (no back view). EYE level, inside the car (2.0 D above the deck). 22 mm. |
| Camera move | A creeping eased push of 6 %/s toward the gap between the two heads, with H0 (no handheld: the dread is in the stillness). There is a constant-speed share in the keys so it never stops. |
| Cast | **Rookie**: crouches into the door frame (`legs` `crouch` 0.3, hidden by the sill), yaw -0.6. Expression `worried` (a professional checking a patient). His hand reaches for the driver's shoulder (arm_l hand target on the driver's `shoulder_r` world point, eased over 18 frames) and touches it at 37.8 s. Blinks at 36.1 and 38.6 s. **Driver**: slumped forward over the wheel (`head_dy` +0.45, pitch +1.5, `head_roll` 25°). Expression `infected_slump` (closed lines, mouth slack). Seatbelt drawn across the shirt. Small breaths are absent: he does not move. |
| Action | The rookie checks the unresponsive driver. Kong is out of focus through the windshield, approaching from the left, 5 D away. |
| Dialogue / caption | None. (No dialogue is added; the screenplay gives none.) |
| Sound | Rain on the car roof, close, drumming and muffled. Inside acoustics. The wiper squeak every 1.2 s, the metronome. The hazard relay tick in the dash. Distant sirens bleed in through the open door. A low sub-drone rises from 37.0 s (sound design, not music). |
| Light | The interior is lit only by the dome light (dim, flickering) and the red flashes through the rear window, sweeping across both cards (tint pulse). The key light reaches only the rookie's arm in the door gap. |
| Transition out | Hard cut (f959→960). |
| Sets up | The touch on the shoulder is what wakes him (Rule 3: reaction to touch and moving light is consistent with sound and light). |

### Shot 13 — the driver lifts his head

| Field | Plan |
|---|---|
| Time | 40.00-43.75 s, f960-1049 (90 f), 3.75 s |
| Set / setup | expressway3d, `windshield_cu`: from outside the windshield on the hood, looking in |
| Framing / angle / lens | Close-up on the driver (head 340 px, centre at 0.46). Slightly LOW, rising to EYE level as he rises. 22 mm. The windshield cracks and rain sheets are between us and him (cracks are a texture on the glass plane; the rain sheet is post, masked to the glass by an object-ID pass). |
| Camera move | A very slow push at 5 %/s that rises 0.3 D with his head, H0. A held stillness of 8 frames before the cut (one of the film's three holds). |
| Cast | **Driver**: the head rises slowly over 2.6 s (`head_dy` +0.45 → 0, pitch +1.5 → -0.2, `head_roll` 25° → 4°, eased in and out; the torso follows at half amplitude). The eyes stay closed (`infected_slump`); the mouth hangs. A wet `drip` from his chin. In the background, out of focus, the rookie's hand withdraws from his shoulder. |
| Action | "คนขับค่อยๆ เงยหน้าขึ้น" — exactly the screenplay's last image of Scene 01, slow and unbroken. |
| Dialogue / caption | None. |
| Sound | The rain flattens to a hiss through glass. The wiper squeaks once, then stops (stuck), and the silence is felt. The sub-drone holds. A wet creak of the seat as he rises. |
| Light | Red flashes only from behind the camera on the R beats; the face goes navy between flashes. The dome light flickers off at 43.2 s. |
| Transition out | Hard cut (f1049→1050). |
| Sets up | The face we will see transformed. |

### Shot 14 — Kong senses it

| Field | Plan |
|---|---|
| Time | 43.75-45.25 s, f1050-1085 (36 f), 1.50 s |
| Set / setup | expressway3d, `cu_K_eye`: by the sedan's rear door, 3 D behind the rookie |
| Framing / angle / lens | Close-up (head 330 px). EYE level. 22 mm. The rookie's back and shoulder are out of focus in the frame-left foreground (side view, not a back view). |
| Camera move | An eased push at 9 %/s, H1 rising to H2. |
| Cast | Kong: slows mid-step. His expression swaps `determined` → `worried` → `stunned` behind 2 blinks in 1.5 s. His head tilts (roll 12°). His right hand closes on the crowbar strap (arm_r hand target at the pack's crowbar point). |
| Action | Something is wrong: the driver moved. Kong's instinct is faster than his thought. |
| Dialogue / caption | None. |
| Sound | The drone holds. The rain is back to full volume. The crowbar's metal clink against the pack buckle. |
| Light | Key from screen-left. Full red pulse. |
| Transition out | Hard cut (f1085→1086). |
| Sets up | Kong already has his hand on the crowbar (shot 16 and Scene 02 push-off are not luck: "ห้ามความบังเอิญช่วยพระเอก"). |

### Shot 15 — eyes open, the lunge, the bite

| Field | Plan |
|---|---|
| Time | 45.25-48.75 s, f1086-1169 (84 f), 3.50 s |
| Set / setup | expressway3d, `door_low` (the shot 10 camera family, reused) |
| Framing / angle / lens | It starts as an extreme close-up on the driver's eyes (a punch-in, head 520 px). A crash zoom-out ×0.35 in 16 frames lands on a medium (driver plus rookie in the door gap). LOW: 1.2 D, pitched up 15°. 22 mm. |
| Camera move | f1086-1093: still on the closed eyes, H0, 8 frames. f1094: the eyes snap open. f1096-1111: crash zoom-out with H3. f1112-1169: H3 with a recoil tilt as the rookie stumbles back into the lens, decaying to H2 by f1160. |
| Cast | **Driver**: the eyes open with no blink in between (a hard swap to `infected`: pupil-less ring eyes, dark lids, open bite mouth with teeth). Jump-scare grammar: squash 2 frames, leap 2, hang 2, land 2. He launches from the seat at the rookie (the card slides 0.8 D out of the door gap; arms `forward` hands to the rookie's shoulders). **Rookie**: `shocked` (one frame), then `shouting` with `mouth=("open",0.30,0.20)`, eyes squeezed. He is dragged half into the door gap; the spreader falls from the sill. **The bite** is on the rookie's shoulder, hidden by the door frame pillar and the driver's own head (no gore; a dark smear `#3a0d14` appears on the orange shoulder on the landing frame). |
| Action | "คนขับพุ่งเข้ากัดเจ้าหน้าที่กู้ภัย. เสียงร้องท่ามกลางสายฝน" |
| Dialogue / caption | None. The scream is not captioned. |
| Sound | On f1094 a wet click as the eyes open, then 1 frame of silence (all sound cut). f1096: a lunge impact, a car-body thud and a glass crack. The rookie's scream (raw, unfiltered, close). The spreader hitting asphalt and splashing. The rain slams back. One car alarm starts nearby. |
| Light | The light bar's double flash lands exactly on f1096 (frames re-timed so the R-R hit is on the lunge). Two frames are pushed to red (a red flash, not a white one: the transition grammar's one "flash", in EP.1 colours). |
| Transition out | Hard cut (f1169→1170) in the middle of the scream. |
| Sets up | The infection rules (bitten → turns within 60 s: the watch). The spreader on the road (it must be recovered before Scene 04). |

### Shot 16 — Kong (final image)

| Field | Plan |
|---|---|
| Time | 48.75-51.75 s, f1170-1241 (72 f), 3.00 s |
| Set / setup | expressway3d, `cu_K_low` (the shot 07 setup, reused: the same face, now in horror, which echoes the call) |
| Framing / angle / lens | Close-up to extreme close-up. LOW: 1.4 D, pitched up 16°. 22 mm. The rain against the lit mast above him. |
| Camera move | Handheld H3 for the first 14 frames, decaying to H2. A snap push ×1.6 in 18 frames onto his eyes from f1200. It is still moving on the last frame. |
| Cast | Kong: `shocked` (ring eyes, 0.033 pupils, sweat plus rain `drip`), a 2-frame squash on the scream's first frame. He rips the crowbar from the pack strap (arm_r from the shoulder to the side, the prop `crowbar` appears in his hand at f1206, raised across his chest by f1230). Pitch -0.3; the eyes go `determined` on the last blink at f1228 (angry brows, `pitch` -0.6) and hold that way to the cut. |
| Action | The scream still going; Kong in the flashing red. He has the crowbar; we do not see him use it. |
| Dialogue / caption | None. |
| Sound | The rookie's scream continues from frame-left (directional), with the rain and the car alarm. Kong's breath. The crowbar scraping free. At f1241 everything cuts at once. |
| Light | Full red pulse on the card (`tint` peak plus red `rim`), alternating with the cool key. Bloom on the light bar in the background. |
| Transition out | Smash to black on the scream's peak (f1241→1242). |
| Sets up | Scene 02 continues directly: "ก้องใช้ชะแลงผลักผู้ติดเชื้อออก". This is the cliffhanger. |

### Shot 17 — black, title

| Field | Plan |
|---|---|
| Time | 51.75-54.50 s, f1242-1307 (66 f), 2.75 s |
| Set / setup | None (2D title card, Chromium) |
| Framing | f1242-1253: pure black, 12 frames. f1254: the title "เขตปิดตาย 09" with "DEAD ZONE 09" under it, red `#c8202a` "09" as in the character-sheet logo, a 6-frame flicker-in like a failing light bar. Then the line "EP.1 ทางด่วนนรก" in small grey. |
| Camera move | The logo itself drifts 3 %/s (it is not a held still) with a 2-frame red flicker twice. |
| Action | Title. |
| Dialogue / caption | None. |
| Sound | In black: 12 frames of total silence. Then the radio squelch from shot 01 opens on its own, the carrier hiss, and a faint unintelligible voice under static, cut off on the last frame. This is a wordless callback that bookends the hook; no new event is added. |
| Light | — |
| Transition out | End. |
| Sets up | The next episode. Rendering note: the screenplay places the TITLE CARD at the end of Scene 02. For this hook cut it is moved here, and the full episode keeps it where the screenplay puts it. |

---

## Compact timing table

| # | Start-end (s) | Frames | Dur | Setup | Angle | Move | Line | Out |
|---|---|---|---|---|---|---|---|---|
| 01 | 0.00-3.00 | 0-71 | 3.00 | insert_radio | low macro | push + snap, H1 | วิทยุ: ศูนย์ครับ...เฮ้ย! | hard cut |
| 02 | 3.00-6.50 | 72-155 | 3.50 | wide_high | high | crane down + push, H1 | — | dissolve 9 |
| 03 | 6.50-9.50 | 156-227 | 3.00 | low_medium_K | low | truck + snap to LED, H2 | — | hard cut |
| 04 | 9.50-12.00 | 228-287 | 2.50 | eye_two | eye | snap tilt + drift, H2 | — | punch-in |
| 05 | 12.00-15.00 | 288-359 | 3.00 | insert_phone | high insert | orbit + push, H1 | (screen) | dissolve 9 |
| 06 | 15.00-21.00 | 360-503 | 6.00 | mcu_K_orbit | eye | orbit 14° + snap, H1 | น้ำเหนือ / ก้อง | hard cut |
| 07 | 21.00-24.00 | 504-575 | 3.00 | cu_K_low | low | slow push, H0 | น้ำเหนือ: ทุกครั้งเลย... | dissolve 11 |
| 08 | 24.00-27.25 | 576-653 | 3.25 | eye_34_K | eye | slide then still, H1→H0 | ก้อง: เดี๋ยวพ่อโทรกลับนะ | hard cut |
| 09 | 27.25-29.50 | 654-707 | 2.25 | insert_phone | low insert | push, whip off | (screen) | hidden whip |
| 10 | 29.50-31.75 | 708-761 | 2.25 | door_low | low | whip-on + snap, H2 | กู้ภัย: พี่ก้อง! เปิดได้แล้วครับ! | hard cut |
| 11 | 31.75-34.50 | 762-827 | 2.75 | track_K | eye | track left, H2 | — | dissolve 13 |
| 12 | 34.50-40.00 | 828-959 | 5.50 | interior_pass | eye (in car) | creep push, H0 | — | hard cut |
| 13 | 40.00-43.75 | 960-1049 | 3.75 | windshield_cu | low→eye | slow push + hold, H0 | — | hard cut |
| 14 | 43.75-45.25 | 1050-1085 | 1.50 | cu_K_eye | eye | push, H1→H2 | — | hard cut |
| 15 | 45.25-48.75 | 1086-1169 | 3.50 | door_low | low | ECU, crash out, H3 | (scream) | hard cut |
| 16 | 48.75-51.75 | 1170-1241 | 3.00 | cu_K_low | low | H3→H2 + snap push | (scream) | smash to black |
| 17 | 51.75-54.50 | 1242-1307 | 2.75 | title (2D) | — | logo drift | — | end |

The camera setups are anchors on the one set, and four of them are used twice: `insert_phone` (05, 09), `door_low` (10, 15), `cu_K_low` (07, 16), and the K marks.

### Screenplay faithfulness check

| Screenplay beat | Shot |
|---|---|
| จอดำ, radio: "ศูนย์ครับ คนเจ็บไม่ตอบสนอง... เดี๋ยว! เฮ้ย!", signal cuts out | 01 (near-black instead of pure black; see Risks) |
| Red emergency lights on the road, multi-car crash, gridlock out of sight | 02 |
| Kong beside the damaged car with the cordless rescue cutter, battery full 3 bars | 03 |
| Phone vibrates, screen "น้ำเหนือ — 4 สายที่ไม่ได้รับ", Kong answers | 04, 05 |
| The four lines of the call, verbatim | 06, 07, 08 |
| น้ำเหนือ goes silent before hanging up | 08, 09 |
| "พี่ก้อง! เปิดได้แล้วครับ!" | 10 |
| Kong puts the phone away; the rescuer approaches the driver who sits motionless | 11, 12 |
| The driver slowly raises his head | 13 |
| (Scene 02) the driver lunges and bites the rescuer; screaming in the rain | 15, 16 |

Wordless additions, none contradicting the screenplay:
- Kong hands the spreader to the rookie (04).
- The watch with the red seconds hand (04, 06).
- The crowbar on the pack, and Kong's hand on it (03, 11, 14, 16).
- Rain on the phone (05, 09).
- Her contact photo (05).
- The stuck wiper (10-13).
- The radio squelch under the title (17).

---

## Assets to build

### Set (1)

`set3d/expressway3d.py`, built as an extension of the office3d pattern: real geometry, artwork as SVG textures from Python, anchors, setters. 1 D = one head diameter, about 0.58 m, so a car is 7.7 × 3.1 × 2.5 D and a lane is 6 D.

1. **Deck:** 3 lanes plus the shoulder, 26 D wide, 60 D of modelled deck. Beyond that a low-poly deck runs to 160 D and fades into the mist. The asphalt texture is wet: dark slate with lane markings, puddle patches and painted streak reflections.
2. **Barriers:** jersey barriers on both sides, plus a sound-wall railing on one side.
3. **Light masts:** 2 masts, with emissive heads (they bloom). They motivate the key.
4. **Hero sedan** (grey-blue): crumpled hood, cracked windshield texture, and these animatable parts:
   - driver door hinge (setter `door(angle)`)
   - wiper arm (setter `wiper(t, stuck)`)
   - dome light (setter `dome(level)`)

   Minimal interior: seat, steering wheel, dash plane with a hazard tell-tale, seatbelt as a ribbon on the driver card.
5. **Second crashed car** (a pickup, reusing a gridlock model with a crumple texture).
6. **Kong's rescue pickup:** orange-white livery with "กู้ภัย" text, closed equipment-compartment doors (Scene 03/04), and a light bar (2 emissive red pods plus 1 red point light, shadows off, setter `lightbar(t)` returning the phase for actor tints).
7. **Gridlock:** 3 low-poly car models (sedan, SUV, van), each with 4 colourways, linked-duplicate instanced about 40 times. Their windows are dark textures with faint head silhouettes. Hazard blinkers come from an emissive orange texture swap.
8. **Skyline backdrop card:** Bangkok towers in navy, sparse windows, red aircraft beacons.
9. **Road reflection decals:** emissive red smear decals under and behind the truck, pulsing with the light bar, plus soft white smears under the masts.
10. **Anchors:** marks K1, K2, K3, R1 (the rookie at the door), DRV (the driver seat, card plane), and the spreader rest point. Cameras: `wide_high`, `low_medium_K`, `eye_two`, `mcu_K_orbit`, `cu_K_low`, `cu_K_eye`, `eye_34_K`, `track_K`, `door_low`, `interior_pass`, `windshield_cu`, `insert_phone`, `insert_radio`.

### Puppets (3, plus 1 head-only)

`cast/cast_dz09.py`, in the cast_ext pattern (registers on import; `puppet.py` is not edited):

1. **`kong`**
   - Build: regular athletic, height about 3.1 D.
   - Hair: spiky black. Stubble beard (a new face extra `stubble`, dotted on the lower face).
   - Costume: orange rescue jacket with 2 reflective bands, "RESCUE" text on the chest, Thai flag patch on the near sleeve, black cargo trousers, boots.
   - Backpack straps, with the crowbar holder on the right strap.
   - Shoulder radio as a costume detail; anchor `radio` for the 3D insert prop.
   - `watch` costume key: a watch ball and strap on the left forearm, near the hand.
2. **`rookie`**
   - Build: slim, height about 2.95 D, visibly younger: no beard, rounder eyes in neutral, cowlick.
   - Costume: orange rescue vest (no jacket) over a dark long-sleeve shirt, white helmet with chin strap, gloves (the hand balls in a grey fill).
   - Different enough from Kong to read at 40 px heads: white helmet against black hair, and a vest silhouette.
3. **`driver`**
   - Build: stout-regular, middle-aged, height about 3.0 D.
   - Costume: rumpled pale-blue office shirt with sleeves rolled, loose tie, ID lanyard, seatbelt ribbon. No glasses and no suit, so he never reads as คุณทศ.
   - New expressions (registered in `EXPRESSIONS` by the extension):
     - `infected_slump`: closed lines, a slack open mouth.
     - `infected`: pupil-less ring eyes with dark grey lids, a wide bite mouth with teeth, no brows.
   - Both stay inside the stickman vocabulary (no gore, no texture).
4. **`namnuea`** (head and hoodie collar only, for the phone photo now; the full puppet comes in Scene 05): ponytail, maroon hoodie collar. Uses `happy`.

All three full puppets also need:
- the `drip` effect (wet hair and sleeves: 3 drops falling from hair tips and cuffs, `t` loop)
- a darker wet variant of the costume fills (×0.85 value, with 2-3 thin highlight streaks)
- canvas entries for `sprites.DEFAULT_CANVAS`
- a seated pose for the driver (legs hidden behind the door and dash; use `crouch` 0.6 with feet forward via `foot_r`/`foot_l`)

### Props (5)

1. **`spreader`** (puppet prop and loose 3D prop): yellow-black cordless rescue spreader with jaws (parameter `open` 0-1) and a battery LED (`led` 0-3 bars). The loose 3D version lies by the tyre in shots 10-16.
2. **`crowbar`** (puppet prop): dark red-black bar with a hooked end. It is also drawn as a costume element on the pack strap until it is drawn at f1206.
3. **`phone`** (puppet prop plus 3D insert prop): the screen is an SVG texture with Thai UI:
   - A: incoming call, "น้ำเหนือ", photo, badge "4 สายที่ไม่ได้รับ"
   - B: in call, timer
   - C: "สิ้นสุดการโทร 00:21"

   Plus a dimmed variant.
4. **Shoulder radio** (3D insert prop): black handset, grille, antenna, red TX LED driven by the audio envelope.
5. **Wristwatch**: costume detail on the puppet. In shots 04 and 06 it is legible enough that the red seconds hand ticks (one step per 24 frames).

### Effects and post (no new Blender features)

1. **Rain:** 3 streak layers in post: near (long, sparse, blurred), mid, far (fine, dense).
   - Slant 8° with the wind; speed scaled to the layer depth.
   - Each layer is occluded by the Z pass at its own depth, so rain falls behind the cars and in front of the actors correctly.
   - Brightness is modulated by the key and the light bar phase (red streaks on flash frames).
   - The camera motion of each frame is taken from `post.py`'s fitted camera, so streaks lengthen in moves.
2. **Splashes:** ring and crown sprites projected onto the road plane using the true camera (about 60 alive at a time in wide shots, 15 in close shots).
3. **Screen droplets** (05, 09) and the **radio grille droplets** (01): 2D droplets registered to the projected corners of the prop.
4. **Windshield rain sheet** (13): a post layer masked by the glass object-ID pass.
5. **Mist / haze:** the mist pass mixed toward `#1b2440`.
6. **Red flash** (15): 2 frames graded toward red. Black (01 near-black, 17).
7. **Handheld noise generator:** H0-H3, added to the camera keys before render (so parallax is true 3D).
8. **Title card:** a 2D SVG page in Chromium.
9. **Captions:** `proj/assemble.py` with the Thai phrases above and the two caption colours.

### Audio (free sources only, no paid API)

- Dialogue: 6 lines from 4 voices (radio man, น้ำเหนือ, Kong, rookie) plus the scream. These need human voice recordings or a free local Thai TTS; see Risks.
- Filters for the phone and radio voices.
- SFX from CC0 libraries: rain beds (wide, on car roof, on plastic), siren ×2, light bar relay, horn, hydraulic spreader, metal tear, door pop, hinge, wiper squeak, phone buzz, call tones, boots in water, body impact, glass crack, car alarm, radio squelch and static, sub-drone. Every cue in `sfx_cues.json` is placed by frame.

### Budget

| Part | Frames | Est. CPU s / frame | CPU s |
|---|---|---|---|
| 3D shots 01-16 | 1242 | 15-17 (12 samples, direct light, 1 shadowed sun + 1 shadowless red point) | about 19,900 |
| Dissolve handles (4 dissolves, both sides) | about 46 | 16 | about 740 |
| Plate and matte passes for streaked frames (whips, crash zoom, snaps: about 60 frames) | 60 | 8 | about 480 |
| Sprites (3 actors at most per frame, 0.06 s each) | — | — | about 220 |
| Post: rain, splashes, mist, grade (about 0.8 s/frame) | 1308 | 0.8 | about 1,050 |
| Title, captions, encode | — | — | about 120 |
| **Total** | | | **about 22,500 CPU s ≈ 6.3 CPU h ≈ 1.6 h wall on 4 cores** (17.2 CPU s per final frame against an 18 s budget) |

Gates before the full render:
1. Time 3 frames each of `wide_high` (02) and `interior_pass` (12): the most geometry, and the most transparency (glass).
2. If either is over 18 s, apply these fixes in order:
   1. Make the car glass a holdout with an opacity texture (no refraction).
   2. Turn the red point light off and keep the decals and tint only.
   3. Render shot 02 at 540x960 and upscale with Lanczos.
3. Retiming acting only costs sprites plus re-renders. There is no plate tier, because every shot has moving actors and a moving 3D camera (no still image with a camera move).

---

## Risks (honest)

1. **The pipeline is built for 30 fps.** `timing.py`, `film.py`, `post.py` and the QA tools hard-code `/30` (`g / 30`) and the reference grammar in frames at 30 fps. Every frame constant must become `round(seconds × FPS)`, and the QA thresholds (static runs of 6 frames, dissolves of 9-23 frames) must be converted to seconds. Until that is done, 24 fps output will drift. This is the first job, before any render.
2. **The first 3 seconds are near-black.** The screenplay says "จอดำ". A truly black frame for 3 s is the most common swipe trigger, so this plan keeps the spirit with a near-black macro (the radio LED, raindrops, one red sweep) and the caption carrying the words. A phone at low brightness may still show "nothing". Test on a real phone, and lift the radio's shade to about V 0.12 if needed.
3. **Cards are never lit.** The red emergency light cannot really fall on the puppets. The plan fakes it with a per-frame `tint` pulse and a red `rim`. It may read as a colour filter on the sprite rather than as light from a direction; the tint is uniform across the card. Check it against the set on a still sheet before the full render.
4. **No back views; seated and inside-car actors.** The driver sits behind a door and dashboard with the card close to surfaces (the stage limit "cards near a wall swing into it"). Use `yaw_fixed` for the driver, keep camera yaw under 30° off his card, and let the sill and dash hide the legs. The `interior_pass` camera is inside a modelled car; a clipping card or glass artefacts may appear.
5. **The bite is a contact between two cards.** The lunge moves the driver's card 0.8 D through the rookie's plane. A `depth_bias` order switch mid-move can pop. It is hidden behind the door pillar, the H3 shake and the 2 red flash frames, but a pop may still show on a frame-by-frame review.
6. **Rain in post.** The Z-pass occlusion handles cars and actors, but rain falling under the truck's overhang or inside the car will show. Mitigations: mask the car-interior shots with the object-ID pass (glass only), and keep the rain sparse in insert shots. Splash projection on the road assumes a flat deck.
7. **The colour targets do not fit.** The LOOK_SPEC hue band (red 30-41 %, orange 22-38 %, blue 14-30 %) and value 0.45-0.63 were measured on daylight interiors. This night exterior will run bluer and darker on purpose: value about 0.25-0.35, blue over 45 %, 25-40 % of pixels darker than V 0.25. `hue_report.py` will flag every frame. Judge with a sheet against the EP.1 grammar instead, and report the numbers with the reason.
8. **The infected faces may read as comic.** Two new face drawings inside a stickman vocabulary can look funny rather than frightening. The scare must come from timing (the 8-frame hold, the 1-frame silence, the flash) and sound, not from the drawing. Review the two drawings on their own before animating.
9. **Voices.** No paid API is allowed. The Thai lines need recorded voices (4 people plus a scream) or a free local Thai TTS. Free TTS will not deliver the guilt in "รออีกแป๊บเดียว" or the scream. Timing in this plan is estimated, not measured; re-time captions and acting to the real recordings before locking.
10. **Thai fonts.** Only Loma, FreeSerif and Unifont are installed with Thai coverage. Phone UI, captions and the title need a better Thai face (Noto Sans Thai / Sarabun via `@fontsource`, free). Check tone-mark stacking in Chromium.
11. **Continuity of the spreader.** It is handed to the rookie and dropped by the car, but Scene 04 takes the cutter from the truck's equipment compartment. Either show Kong grabbing it in Scene 02 when he drags the rookie back, or have the full-episode plan add a beat. Flag this to the screenplay owner rather than changing it here.
12. **The title card is moved.** The screenplay places TITLE CARD DEAD ZONE 09 after the aerial shot at the end of Scene 02. This hook ends on it instead. The full-episode edit should keep the screenplay's placement. The radio squelch under the title is a wordless callback, not a new event, but the owner should approve it.
13. **The render budget is estimated,** scaled from the office set (16 s with 2 cards, 4 threads). An exterior with about 40 instanced cars, glass and one extra light is untested. Gate it (see Budget). Shared CPU with other agents doubled wall time in the past.
14. **Wet-look rule.** Drips and darker fills may not read as "soaked" at 40-200 px heads. If the wide shots read dry, add a constant thin highlight streak to hair and shoulders.
