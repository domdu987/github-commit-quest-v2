# EP.1 "ทางด่วนนรก": opening hook, Director A (hook-first)

Scene 01 complete ("สายที่ไม่ได้รับ") plus the first beat of Scene 02 ("คนขับพุ่งเข้ากัดเจ้าหน้าที่กู้ภัย. เสียงร้องท่ามกลางสายฝน"). Vertical 720x1280, **24 fps**, Thai dialogue with burned-in Thai captions. Built with the existing pipeline: v2 puppets (extended by a new cast module, the same way `v3/cast/cast_ext.py` extends them) on emission-only cards in a code-built Blender set, one hard key, blue-violet ambient, 22 mm lens.

Clock: film time in seconds from frame 0; frame = round(t x 24). Every number the LOOK_SPEC gives in 30 fps frames is converted here (x 0.8): dissolve 11 f -> 9 f, snap 14-24 f -> 11-19 f, whip 7-20 f -> 6-16 f, shake 1-1.5 s unchanged in seconds. Blinks stay half/closed/half, one frame each.

## Header

| Item | Value |
|---|---|
| Total duration | 53.50 s (1284 frames at 24 fps): 51.50 s of picture + 2.00 s black tail |
| Shot count | 29 (27 picture shots, 1 near-black radio macro opening, 1 black tail) |
| Average shot length | 1.84 s over all 29; 1.83 s over shots 2-28; range 0.75-2.75 s |
| Joins (28) | 20 hard cuts, 3 punch-in cuts, 2 whip pans, 1 short dissolve (7 f), 1 static-burst cut, 1 smash cut to black |
| Sets | S1 `expressway3d` (elevated Bangkok expressway deck in rain at night: 3 lanes, concrete barriers, LED lamp posts, gridlock of 40+ instanced cars receding into rain haze, rescue truck with red light bar, hero wreck = crushed sedan with an openable driver door and a modelled interior). S2 `radio_macro` (Kong's shoulder radio in near-black, a 1 D-wide close-up set; can live as a corner of S1). Inserts (3D macro props in S1): phone in hand, cutter battery gauge, vest pocket |
| Cast | ก้อง Kong (38, rescue worker, hero); เจ้าหน้าที่กู้ภัย the rescue partner (unnamed in the screenplay; asset name `rescuer_b`); คนขับ the driver (becomes the first infected we see); น้ำเหนือ Namnuea (14, voice on the phone only; seen only as the contact photo on the phone screen); เสียงวิทยุ, a man's voice on the rescue radio (voice only) |
| Props | cordless rescue cutter with a 3-bar battery LED (Kong); smartphone with a Thai call UI (Kong); wristwatch (Kong, left wrist); shoulder radio (Kong; a second one on rescuer_b); crowbar strapped to Kong's backpack (visible, not used yet); spring-loaded glass punch (rescuer_b); crushed sedan door, steering wheel, seat belt; rescue truck light bar |
| Effects | rain (3 layers of streak cards + splash rings + window/phone-glass drops + drips drawn on the puppets); rotating red beacons as moving lights; red beacon pulse on the puppet tint; static burst; camera shake at the peaks only |
| Palette (EP.1 grammar) | dark blue, grey, emergency red. Orange exists only on Kong's vest and the cutter body; no sodium-orange lamps (cold white LED posts) |
| Captions | Thai, white fill, black 4 px stroke, centred at y = 900; phrases 4-14 Thai characters; voice-over lines (radio, phone) in pale grey-blue `#cfd8ee` so a viewer knows the speaker is not on screen. Font: a free Thai black weight (Kanit Black or Prompt Black, OFL), because Work Sans has no Thai glyphs |

## The hook in one paragraph

0-2.25 s: near-black. Only the red TX LED of a rescue radio flickers in time with a man's voice; the speaker grille catches it. "ศูนย์ครับ คนเจ็บไม่ตอบสนอง... เดี๋ยว! เฮ้ย!" On "เฮ้ย" the LED stutters, a static burst, the line dies. 2.25 s: hard cut on the static into a ground-level splash of red light on wet asphalt, rain rings in a puddle, and the camera snaps up to show tail lights stacked to the horizon. By 3.0 s the viewer has an unanswered question (what happened on that radio?) and a place full of danger (red-lit gridlock in rain). Everything after it is a fuse: the call from his daughter we know he will lose, then the driver who does not move.

---

## Shot list

Field key: **Set / framing** gives set, shot size, camera height class (low = 1.2 D up pitched +15 deg, eye, high = 3+ D up pitched -15 to -20 deg) and lens (22 mm everywhere; 22 mm close to the subject for inserts). Head sizes are px at 720x1280; main head centre 0.35-0.59 of frame height, whole head above y = 880 (caption band).

### 01. Radio in the dark (the hook image)
- **Time:** 0.00-2.25 (2.25 s, f0-53)
- **Set / framing:** S2 `radio_macro`. Extreme close-up of the shoulder radio's top: speaker grille, antenna root, TX LED. Eye level to the radio, 22 mm at 0.9 D. The frame is 90 percent black.
- **Camera move:** slow eased push 8 %/s from frame 0 (never static); at 1.70 a micro snap push x1.3 (11 f) onto the LED on "เดี๋ยว!". Tiny handheld drift (amplitude 4 px) only after "เฮ้ย!".
- **Cast:** none on screen (voice only).
- **Action:** the LED blinks red with the voice envelope (emission keyed to the dialogue loudness). Rain drops land on the grille and bead; one runs down. On "เฮ้ย!" the LED stutters 3 times, then goes dark on f53.
- **Dialogue / caption (V.O. colour):** เสียงวิทยุ: "ศูนย์ครับ / คนเจ็บ / ไม่ตอบสนอง... / เดี๋ยว! / เฮ้ย!"
- **Sound:** rain on fabric and plastic, close and muffled (0.00 in); radio squelch open (0.05); voice band-passed 300-3000 Hz with dropouts; on "เฮ้ย!" a scuffle thump through the radio, then a 6-frame static burst that ends the shot.
- **Light:** no key in frame; the LED is the only light (bloom above scene-linear 1.0). A faint blue ambient rim (value under 0.08) so the grille shape just reads.
- **Transition out:** hard cut on the static burst (the burst carries over the cut by 3 frames).
- **Sets up:** the radio call cut off by an attack elsewhere = the same thing is about to happen here (paid off in shot 24); the radio stays on Kong's shoulder for all of EP.1.

### 02. Red on wet asphalt
- **Time:** 2.25-3.50 (1.25 s, f54-83)
- **Set / framing:** S1, lane between two stopped cars. Camera 0.25 D above the road, pitched down 10 deg at frame 0 into a puddle.
- **Camera move:** frame 0 already moving: crane-up snap (16 f, sine in-out) from 0.25 D to 1.6 D, pitch -10 to +8 deg, revealing tail lights stacked into the rain. Settles into a slow drift.
- **Cast:** none.
- **Action:** a red beacon sweep crosses the puddle (rain rings break it into ripples); wipers of the nearest car swing once; rain streaks across lens depth.
- **Dialogue / caption:** none (on-screen text free). Optional small series bug "EP.1" top-left in grey, 1 s.
- **Sound:** full rain bed opens up (wide, loud); a car horn held far left; the beacon relay clicking; distant sirens (low).
- **Light:** key = cold white LED lamp post, hard (1 deg), from screen-left high; red beacons as rotating spot lights (practicals); blue-violet ambient. The road is the strongest reflector of red in the film.
- **Transition out:** hard cut.
- **Sets up:** red beacons and their sweep (the moving light of world rule 3; the siren choice in Scene 03).

### 03. The gridlock
- **Time:** 3.50-5.50 (2.00 s, f84-131)
- **Set / framing:** S1 wide from high (5 D up, pitch -20 deg) over the barrier: pile-up of 4-5 crashed cars in the foreground, rescue truck with light bar, gridlock to the vanishing point in haze. Kong is a tiny figure (head 22 px) beside the crushed sedan, rescuer_b at its door.
- **Camera move:** eased push 9 %/s plus 0.3 D truck right, so foreground cars slide against the background (true parallax, not a 2D zoom).
- **Cast:** Kong (standing, cutter held two-handed, `yaw` 0.3, held pose with breathing bob 0.02 D); rescuer_b (crouched at the driver door, working arm).
- **Action:** hazard lights blink on several cars in different phases; rain sheets visible against the lamp posts.
- **Dialogue / caption:** none.
- **Sound:** horns (2, far), rain, distant sirens, light bar relay; an engine idling nearby.
- **Light:** as 02; distance haze in blue-grey (depth mist in the compositor), tail lights in the haze bloom.
- **Transition out:** hard cut into the low angle (scale jump on the same axis).
- **Sets up:** scale of the gridlock (no way out by car: Scene 03 truck block).

### 04. Kong with the cutter
- **Time:** 5.50-7.50 (2.00 s, f132-179)
- **Set / framing:** S1 medium-full on Kong, low (1.2 D, +15 deg), head 190 px, centre at 0.42. Wreck to screen-right, rescue truck beacon behind him.
- **Camera move:** eased orbit 8 deg left plus push 7 %/s; at 6.80 a snap tilt-down (13 f) to the cutter in his hands, handing off to 05.
- **Cast:** Kong: `expr` determined, `pitch` -0.3, legs `wide`, both hands on the cutter (two-hand IK to the cutter grips), rain drips drawn on head and vest; blink at 6.2.
- **Action:** Kong shakes rain off his face with a head toss (head_roll -12 to 0 over 8 f), shifts his grip, looks toward the car door.
- **Dialogue / caption:** none.
- **Sound:** rain on his vest (closer, crisper); cutter handle creak; radio on his shoulder silent (just a faint hiss).
- **Light:** key from screen-left high (so the head's thick ink side and crescent go to the lower right: default `head_flip` False). Red beacon pulse on the puppet tint every 0.9 s (see Effects).
- **Transition out:** hard cut on the tilt, match on the cutter.
- **Sets up:** the cutter is Kong's equipment (ownership); the crowbar strapped on his backpack is visible in profile (used in Scene 02 beat 2).

### 05. Battery: 3 bars
- **Time:** 7.50-8.75 (1.25 s, f180-209)
- **Set / framing:** insert, raking macro on the cutter's battery pack, 0.7 D from the lens, eye level to the prop.
- **Camera move:** arrives inside the tilt (still moving down, braking over 6 f), then a 6 %/s drift along the gauge.
- **Cast:** Kong's ball hand and ink forearm only (on its own card) shifting on the grip.
- **Action:** rain beads run across the gauge; the 3 green-white bars glow steadily (3 of 3). The thumb wipes the gauge once.
- **Dialogue / caption:** none (the 3 bars read without words).
- **Sound:** drops ticking on plastic; faint electrical hum.
- **Light:** bars are emissive (bloom); key rakes the moulded plastic.
- **Transition out:** whip pan right (6 f out, 6 f in).
- **Sets up:** battery 3 bars full in EP.1, the screenplay's own countdown of the cutter's power in later episodes.

### 06. The door and the still driver
- **Time:** 8.75-10.75 (2.00 s, f210-257)
- **Set / framing:** S1 eye-level medium two-shot at the crushed sedan: rescuer_b in the foreground at the driver door (head 210 px), the driver visible through the rain-streaked side window behind him, slumped. Kong out of frame.
- **Camera move:** whip-on brake (6 f), then slow push 7 %/s toward the window.
- **Cast:** rescuer_b: yellow helmet, crouch 0.3, `expr` determined then worried behind a blink at 10.0; arm drives the glass punch into the corner of the window (gesture on 9.4), then both hands pull at the jammed door. Driver: seated, head down (`pitch` 1.3, `head_roll` 15), totally still, no blink (the stillness is the warning).
- **Action:** the glass punch clicks, the window crazes and drops in a sheet of rain; rescuer_b reaches in toward the door release.
- **Dialogue / caption:** none.
- **Sound:** glass punch snap and glass trickle; the car's hazard relay ticking (begins here; becomes the metronome to the bite); rain on the roof of the car.
- **Light:** key from screen-left; the car interior is dark except the dash cluster glow (cold blue) and the red beacon sweeping across the driver.
- **Transition out:** hard cut to the vibration.
- **Sets up:** the driver is planted 33 s before he moves; the hazard tick motif.

### 07. Pocket buzzing
- **Time:** 10.75-12.00 (1.25 s, f258-287)
- **Set / framing:** insert, close on Kong's chest: the reflective vest's chest pocket with the "RESCUE" strip; eye level, 0.8 D.
- **Camera move:** tiny vibration shake synced to the buzz (amplitude 3 px, only during the buzz), over a slow push.
- **Cast:** Kong (torso only, on card); his hand comes up into frame at 11.5.
- **Action:** the phone screen light glows through the wet fabric in pulses; rain beads on the reflective strip flash in the beacon.
- **Dialogue / caption:** none.
- **Sound:** phone vibration, 2 pulses (each 0.4 s), dry and close against the rain.
- **Light:** phone glow cold white-blue from inside the pocket; red beacon pulse on the strip.
- **Transition out:** hard cut on the pull.
- **Sets up:** where Kong keeps the phone (Scene 05 call).

### 08. Four missed calls
- **Time:** 12.00-14.00 (2.00 s, f288-335)
- **Set / framing:** insert, phone screen held in Kong's ball hand, slight high angle over his wrist (camera 0.6 D from the screen). The wristwatch on his left wrist sits at the lower edge.
- **Camera move:** eased rack in 6 %/s plus 2 deg roll drift; the phone tilts in his hand (hand card keyed).
- **Cast:** Kong's hand and forearm; the contact photo of น้ำเหนือ on the screen (a puppet portrait: ponytail, oxblood hooded jacket, `expr` happy).
- **Action:** screen shows the incoming call and the banner. Rain drops land on the glass and smear her photo; one drop runs across her face. Watch shows 21:47 (second hand moving).
- **Dialogue / caption (screen text, not a caption):** "น้ำเหนือ" / "4 สายที่ไม่ได้รับ". Caption band left empty so the screen reads.
- **Sound:** vibration continues (third pulse); a distant horn.
- **Light:** screen emission lights nothing (cards stay unlit); key rakes the phone body; watch crystal catches a red glint.
- **Transition out:** punch-in cut to Kong's face.
- **Sets up:** the 4 missed calls and the promise (paid off in Scene 05: "ครั้งนี้พ่ออย่าผิดสัญญานะ"); the wristwatch (Scene 02 INSERT: time passing toward 60 seconds).

### 09. He answers
- **Time:** 14.00-15.50 (1.50 s, f336-371)
- **Set / framing:** close-up on Kong, slightly low (1.6 D, +8 deg), head 300 px, centre 0.45; the phone glow under his chin.
- **Camera move:** drift push 8 %/s, eased; no shake.
- **Cast:** Kong: `expr` worried; at 14.6 blink-swap to sad (guilt); thumb press (arm gesture 8 f) and phone to his ear (arm to `hand` target by the ear, 10 f).
- **Action:** he turns his shoulder away from the wreck noise (yaw 0.2 to -0.3), shielding the call.
- **Dialogue / caption:** none.
- **Sound:** answer tone; the rain mix drops 4 dB and narrows (subjective focus on the call).
- **Light:** phone glow drawn on the sprite as a small cool highlight under the chin (puppet fx, not a light); beacon pulse.
- **Transition out:** hard cut.
- **Sets up:** -

### 10. "พ่อสัญญา"
- **Time:** 15.50-18.25 (2.75 s, f372-437)
- **Set / framing:** medium close-up, eye level, Kong screen-right holding the phone to his ear, the rescue truck's beacon out of focus behind (real depth: camera at 2.0 D, 22 mm).
- **Camera move:** slow slide left 30 px/s and push 6 %/s; held otherwise (listener moment).
- **Cast:** Kong listening: frozen (under 0.04 D travel), `expr` sad, `pitch` 0.6, blinks at 16.4 and 17.6; the phone in his hand.
- **Action:** a rain drip falls from his hair across his cheek (fx drips).
- **Dialogue / caption (V.O. colour, phone-filtered):** น้ำเหนือ: "พ่อ / วันนี้พ่อสัญญา / ว่าจะมารับหนูไง"
- **Sound:** her voice band-limited through the phone (with her own room tone: quiet, indoor, a clock), the rain outside stays low.
- **Light:** beacon pulse slows in feel (keep the beacon real; only the mix changes).
- **Transition out:** hard cut to the high two-shot.
- **Sets up:** the promise.

### 11. "เคสด่วน"
- **Time:** 18.25-20.50 (2.25 s, f438-491)
- **Set / framing:** high two-shot (3.4 D up, -18 deg): Kong near, screen-right, head 230 px; rescuer_b far at the sedan door, head 150 px (near/far 1.5).
- **Camera move:** eased crane-down 0.4 D with push 7 %/s; snap push (12 f) on "รออีกแป๊บเดียว" toward Kong.
- **Cast:** Kong talking (`expr` talking, lip-sync on the quoted line only, one head nod per 1.2 s), free hand rubs the back of his neck (gesture, 9 f). rescuer_b glances back over his shoulder at Kong (`yaw` toward camera, `expr` worried), then back to the door.
- **Action:** rain bounces off the sedan roof between them.
- **Dialogue / caption:** ก้อง: "พ่อมีเคสด่วนลูก / รออีกแป๊บเดียว"
- **Sound:** Kong's voice close and dry; rescuer_b's tools clinking off-mic; hazard tick under.
- **Light:** key from screen-left; both heads keep their crescent on the side away from the key.
- **Transition out:** punch-in cut.
- **Sets up:** Kong's partner waiting on him: the job he chooses over his daughter tonight.

### 12. "ทุกครั้งเลย..."
- **Time:** 20.50-22.00 (1.50 s, f492-527)
- **Set / framing:** extreme close-up on Kong's face (head 520 px, upper face only above the caption band; eyes at 0.40).
- **Camera move:** almost-held drift 3 %/s (never static more than 6 frames).
- **Cast:** Kong: `expr` sad; eyes close slowly on a blink-hold (half 1 f, closed 6 f, half 1 f); brows down further on the reopen (swap on the closed frame).
- **Action:** rain runs down his temple.
- **Dialogue / caption (V.O. colour):** น้ำเหนือ: "ทุกครั้งเลย..."
- **Sound:** her line, then 0.4 s of nothing but rain on the phone mic.
- **Light:** beacon pulse on the face tint at its lowest (deep blue).
- **Transition out:** hard cut.
- **Sets up:** "every time": Kong's pattern of broken promises (Scene 05).

### 13. "เดี๋ยวพ่อโทรกลับนะ"
- **Time:** 22.00-24.00 (2.00 s, f528-575)
- **Set / framing:** medium, low (1.2 D, +15 deg), Kong in profile three-quarter (yaw -0.5) looking off toward the sedan; the light bar behind.
- **Camera move:** eased orbit 6 deg toward his face while he turns.
- **Cast:** Kong talking (lip-sync), his eyes go to the wreck mid-line (gaze shift, head yaw -0.5 to -0.8): torn between the two. `expr` talking then worried after a blink at 23.4.
- **Action:** his free hand tightens on the cutter strap.
- **Dialogue / caption:** ก้อง: "เดี๋ยวพ่อ / โทรกลับนะ"
- **Sound:** his voice; a horn far behind cuts across the end of the line.
- **Light:** as 11.
- **Transition out:** hard cut.
- **Sets up:** the call-back that never happens (Scene 04: "ยังไม่มีสายจากลูก").

### 14. Silence on the line
- **Time:** 24.00-26.50 (2.50 s, f576-635)
- **Set / framing:** insert, phone screen held away from his ear (he looks at it): call timer 00:41, 00:42, 00:43; then at 25.8 the screen flips to "สิ้นสุดการโทร" and returns to the lock screen with her photo.
- **Camera move:** eased push 8 %/s; tiny roll as his hand lowers.
- **Cast:** Kong's hand; her photo.
- **Action:** a drop lands on the timer; the call ends on her side.
- **Dialogue / caption:** none (her silence is the line). Screen text: timer, "สิ้นสุดการโทร".
- **Sound:** her breath on the line once (0.3 s) at 24.6, then nothing; the end-call beep at 25.8 (the only clean, dry sound in the film); the rain returns to full level on the beep.
- **Light:** screen glow.
- **Transition out:** short dissolve 7 f (both moving) into his face.
- **Sets up:** she hung up on him; she will call him in Scene 05.

### 15. Kong swallows it
- **Time:** 26.50-28.00 (1.50 s, f636-671)
- **Set / framing:** close-up, eye level, head 290 px.
- **Camera move:** slow pull-out 7 %/s (the moment lets go).
- **Cast:** Kong: `expr` sad -> blink-swap at 27.3 -> determined (jaw set, small 2-frame squash on the swap); exhales (torso drop 0.03 D).
- **Action:** he lowers the phone.
- **Dialogue / caption:** none.
- **Sound:** a long exhale; rain full.
- **Light:** beacon pulse.
- **Transition out:** whip pan left to the sedan (6 f out), cut inside the blur, on the cue of the partner's call.
- **Sets up:** -

### 16. "เปิดได้แล้วครับ!"
- **Time:** 28.00-29.75 (1.75 s, f672-713)
- **Set / framing:** medium, eye level at the sedan: rescuer_b standing at the now-open driver door, head 220 px, facing camera three-quarter.
- **Camera move:** whip-on brake (6 f), then a small handheld follow (the energy rises: amplitude 5 px, eased random keys every 3 f, 0.8 s only).
- **Cast:** rescuer_b: `expr` excited, arm `wave` toward Kong, lip-sync on the line; then turns back to the door (yaw 0.4 to -0.4, 10 f).
- **Action:** the door hangs open on its hinge, swinging 4 deg in the wind; rain pours off its edge.
- **Dialogue / caption:** เจ้าหน้าที่กู้ภัย: "พี่ก้อง! / เปิดได้แล้วครับ!"
- **Sound:** his shout over the rain; door hinge creak; hazard tick now louder (we are at the car).
- **Light:** key from screen-left; the open door's interior light (warm-white courtesy lamp, small) spills on the seat: the first warm light in the film, and it falls on the driver's lap.
- **Transition out:** hard cut.
- **Sets up:** -

### 17. Phone away, moving in
- **Time:** 29.75-31.50 (1.75 s, f714-755)
- **Set / framing:** medium-full tracking, low (1.3 D, +12 deg), Kong walking fast left to right toward the car (the direction of action holds left to right toward the car for the rest of the hook).
- **Camera move:** tracking truck with him at walking speed, slight lag; walk bob in the sprite, not the camera.
- **Cast:** Kong: walk cycle (20 f period at 30 fps -> 16 f at 24 fps), shoves the phone into the vest pocket (gesture 8 f at 30.2), hefts the cutter; `expr` determined.
- **Action:** splashes at each footfall (splash ring cards spawned at the feet).
- **Dialogue / caption:** none.
- **Sound:** boots in water, vest rustle, radio on his shoulder gives one faint crackle (0.2 s) and goes quiet.
- **Light:** passes under a lamp post: key brightens then falls (a real shadow sweep across the road).
- **Transition out:** hard cut.
- **Sets up:** the phone is put away (he cannot see it until Scene 04); the radio crackle echoes shot 01.

### 18. The driver does not move
- **Time:** 31.50-33.50 (2.00 s, f756-803)
- **Set / framing:** over rescuer_b's shoulder (his card side-on, three-quarter, never his back), eye level, looking into the open door: the driver slumped over the wheel, head down, hands in his lap; seat belt across him.
- **Camera move:** slow push 8 %/s into the cabin; no shake (the quiet before).
- **Cast:** rescuer_b leans in (lean 15 deg, 10 f), `expr` worried; driver totally still (no breathing bob, no blink: the only puppet in the film without them).
- **Action:** rain drips from the door frame onto the driver's shoulder; he does not react.
- **Dialogue / caption:** none.
- **Sound:** the hazard relay tick close and centred; rain on the roof from inside (muffled drum); the dash chime pinging (door open).
- **Light:** courtesy lamp warm on the lap; dash cluster cold; beacon sweep through the windscreen every 0.9 s.
- **Transition out:** hard cut to the reverse.
- **Sets up:** -

### 19. From inside the car
- **Time:** 33.50-35.25 (1.75 s, f804-845)
- **Set / framing:** reverse from inside the cabin (camera at the passenger headrest, eye level, 22 mm): driver's head and shoulder in the foreground as a dark shape at frame left (back of the head is NOT drawn: the driver card is turned three-quarter away, only the hair and shoulder edge read, kept in shadow); rescuer_b's face filling the door opening, reaching in.
- **Camera move:** eased push 6 %/s, 2 deg roll drift.
- **Cast:** rescuer_b: `expr` worried, gaze on the driver, hand reaches to the driver's shoulder (IK to a world point on the driver's card, 12 f).
- **Action:** his hand touches the shoulder at 34.8.
- **Dialogue / caption:** none (the screenplay gives him no line here).
- **Sound:** the touch: wet fabric; tick; dash chime.
- **Light:** rescuer_b against the lit rain outside (lamp post backlight), the cabin dark.
- **Transition out:** hard cut.
- **Sets up:** -

### 20. Kong arrives, the radio hisses
- **Time:** 35.25-37.00 (1.75 s, f846-887)
- **Set / framing:** medium, low (1.2 D, +15 deg), Kong stepping into frame behind the open door, cutter down at his side; the light bar behind his head.
- **Camera move:** drift push 7 %/s; tilt up 3 deg as he stops.
- **Cast:** Kong: stops (2 f settle), `expr` neutral -> blink-swap at 36.2 -> stunned (something is off); head tilt (head_roll 8).
- **Action:** his shoulder radio hisses with a burst of open carrier and nothing else (no voice).
- **Dialogue / caption:** none.
- **Sound:** radio carrier hiss 0.5 s (same squelch sound as shot 01, so the ear connects them); tick; rain.
- **Light:** beacon pulse.
- **Transition out:** hard cut.
- **Sets up:** connects the opening radio to this car.

### 21. He lifts his head
- **Time:** 37.00-39.75 (2.75 s, f888-953)
- **Set / framing:** close-up on the driver inside the cabin, eye level, head 330 px at the end; framed through the open door frame (the door edge is a dark vertical at frame right).
- **Camera move:** very slow push 5 %/s (the longest calm shot: the fuse). Never static.
- **Cast:** driver: `pitch` eased from 1.3 to 0.1 over 50 f (slow-in slow-out), `head_roll` 15 to 0; face drawing `infected_hidden` while the head is down (eyes in shadow: no pupils drawn, brows none, mouth slack dash), then at 39.3, on the beacon sweep, the face swaps (on a beat with no blink: wrong on purpose) to `infected_eyes`: blank white ring eyes with no pupils, thin dark vein lines at the temples, mouth slack open.
- **Action:** the beacon sweep reveals the face for 6 frames, then leaves it in blue dark with the white eyes still visible.
- **Dialogue / caption:** none.
- **Sound:** the hazard tick slows feel by being the only rhythmic sound; the rain ducks 3 dB; a wet, low intake of breath from the driver (not a growl yet).
- **Light:** red beacon sweep (6 f peak on the sprite tint) is the reveal light; courtesy lamp under his chin.
- **Transition out:** hard cut.
- **Sets up:** the infected look for the whole series (one rule: blank eyes, no pupils).

### 22. Relief, wrongly
- **Time:** 39.75-41.00 (1.25 s, f954-983)
- **Set / framing:** close-up on rescuer_b in the door opening, eye level, head 300 px.
- **Camera move:** drift push 6 %/s.
- **Cast:** rescuer_b: `expr` worried -> blink-swap at 40.2 -> happy (a small relieved smile: the patient is conscious); leans further in, hands open toward the driver.
- **Action:** -
- **Dialogue / caption:** none.
- **Sound:** his relieved breath out; tick.
- **Light:** backlit by the lamp post; beacon pulse.
- **Transition out:** hard cut.
- **Sets up:** -

### 23. Kong sees it
- **Time:** 41.00-42.00 (1.00 s, f984-1007)
- **Set / framing:** extreme close-up, Kong's eyes (head 560 px, eyes at 0.40), slightly low.
- **Camera move:** snap push x1.5 (12 f) from the first frame.
- **Cast:** Kong: `expr` stunned -> swap on a 1-frame blink -> shocked (ring eyes, tiny pupils), 2-frame squash; mouth opens (`mouth` o).
- **Action:** his hand starts to come up (8 f), too late.
- **Dialogue / caption:** none (he has no line in the screenplay).
- **Sound:** rain cuts out entirely for 6 frames (a hole in the sound), only the tick.
- **Light:** beacon pulse at peak red.
- **Transition out:** hard cut on the lunge.
- **Sets up:** -

### 24. The lunge
- **Time:** 42.00-42.75 (0.75 s, f1008-1025)
- **Set / framing:** medium, eye level, side-on to the door opening: the driver launches out of the seat into rescuer_b (left to right).
- **Camera move:** crash zoom-in x2.5 (quintic, 15 f) with whole-frame streak on the set (actors stay sharp, as `post.py` does for fast frames), handheld shake starts (5 Hz, 12 px sd).
- **Cast:** driver: anticipation 2 f (head drops), stretch 3 f (squash 0.8 x 1.25 along the lunge), arms `forward` with hands as targets on rescuer_b's shoulders, `expr` `infected_snarl` (blank eyes, open mouth with teeth, brows none); the seat belt snaps taut then slips (it was unbuckled: drawn loose). rescuer_b: `expr` shocked (swap on the hit frame, no blink: shock), lean back 30 deg.
- **Action:** contact on f1022.
- **Dialogue / caption:** none.
- **Sound:** the rain slams back in; a wet snarl; the impact thud against the door frame; rescuer_b's gasp.
- **Light:** the lunge passes through the beacon sweep.
- **Transition out:** hard cut on the impact.
- **Sets up:** world rule 2 (they move fast) shown in the first second of the first attack.

### 25. The bite
- **Time:** 42.75-44.75 (2.00 s, f1026-1073)
- **Set / framing:** high wide-medium (3.6 D up, -20 deg): the open door, rescuer_b driven back against it and down onto the wet road, the driver on him; the bite happens behind the door's top edge (the door occludes the contact; only the driver's head driving down into the shoulder and rescuer_b's arm flailing read). Kong at the frame edge, frozen.
- **Camera move:** handheld shake continues 1.2 s then decays; eased pull-back 9 %/s.
- **Cast:** rescuer_b: shouting, arms pushing; legs kick (lift_r 1.0 cycling). driver: crouched over him, head drives down twice (8 f each), `infected_snarl`. Kong: `expr` shocked, frozen, cutter in his hands.
- **Action:** rescuer_b's helmet comes off and rolls (prop on its own card, real roll on the road); splashes from the struggle. No blood shown in this shot (non-graphic: the door hides the wound).
- **Dialogue / caption:** none.
- **Sound:** the scream begins (rescuer_b) under the rain; a door slam against the car body; helmet clatter; rain hiss on the road; the hazard tick continues as if nothing happened.
- **Light:** courtesy lamp, lamp post key; beacon sweeps.
- **Transition out:** hard cut.
- **Sets up:** the bite (world rule 1: the 60-second clock starts here, counted by the wristwatch in Scene 02).

### 26. The scream in the rain
- **Time:** 44.75-46.50 (1.75 s, f1074-1115)
- **Set / framing:** close-up, low and tilted (dutch 8 deg), rescuer_b on his back on the road, face to camera, head 320 px; rain falling toward the lens.
- **Camera move:** shake decaying from 8 px to 2 px; slow push.
- **Cast:** rescuer_b: `expr` shouting with `mouth` ("open", 0.30, 0.20) held: the scream; head_roll swings 12 deg twice; hand clamped to his shoulder (the wound covered by his hand: the place is set, the gore is not shown).
- **Action:** rain hitting his face; the driver's shape passes across the top of frame (out of focus band).
- **Dialogue / caption:** none (no words in the screenplay; no "[กรีดร้อง]" label: the picture carries it).
- **Sound:** the scream full, then it starts breaking up into the rain (reverb tail, wide); a far siren rises.
- **Light:** the beacon turns his face red every 0.9 s.
- **Transition out:** hard cut.
- **Sets up:** the wound on the shoulder (continuity for Scene 02: Kong stops the bleeding there).

### 27. Kong, in the frame with it
- **Time:** 46.50-48.75 (2.25 s, f1116-1169)
- **Set / framing:** high (4.2 D, -22 deg) over the car roof: in the foreground the driver hunched over rescuer_b behind the door; Kong in the middle ground (head 120 px), frozen, rain between them, gridlock tail lights to the horizon.
- **Camera move:** slow crane-up 0.5 D and pull 8 %/s (the world widens around him; NOT the city crane of Scene 02, which is kept for later).
- **Cast:** Kong: `expr` shocked, held; a single blink at 47.6; cutter hangs from one hand (arm drops 10 f). driver: head lifts from the shoulder (pitch -0.2), turning toward the noise of the far siren (world rule 3); rescuer_b: arm falls slack.
- **Action:** in the far gridlock a second set of hazard lights starts blinking out of rhythm (background only).
- **Dialogue / caption:** none.
- **Sound:** scream stops at 47.0 (cut off, not faded); rain; tick; sirens far.
- **Light:** lamp post key; beacons.
- **Transition out:** punch-in cut.
- **Sets up:** the infected respond to sound (the siren in Scene 03).

### 28. Final image: Kong's face, red, with the 3 bars
- **Time:** 48.75-51.50 (2.75 s, f1170-1235)
- **Set / framing:** close-up, low (1.2 D, +15 deg) on Kong, head 320 px at 0.40; in the lower foreground, out of the caption band's way at frame-left, the cutter's battery gauge glows 3 bars.
- **Camera move:** eased push 8 %/s; then a final snap push x1.4 (14 f) into his eyes from 50.9; the last frame is still moving.
- **Cast:** Kong: `expr` shocked -> blink-swap at 49.8 -> stunned; head turns slowly from the car toward the camera (yaw -0.6 to 0, 30 f) and his gaze lands on the lens on 50.9. Breathing visible (torso 0.03 D at 0.7 Hz). Rain drips on his face.
- **Action:** behind him, out of focus, the driver's shape rises from the road (a dark puppet silhouette at frame-right, 20 f): the threat is now standing.
- **Dialogue / caption:** none.
- **Sound:** rain; the tick; Kong's breath; on 50.9 the radio on his shoulder opens one more burst of squelch, voice-less.
- **Light:** the beacon pulse peaks red on his face at 51.2; the LED bars bloom.
- **Transition out:** smash cut to black on f1236 (mid-move, mid-pulse).
- **Sets up:** Scene 02 beat 2 (Kong and the crowbar, the partner's 60 seconds).

### 29. Black
- **Time:** 51.50-53.50 (2.00 s, f1236-1283)
- **Set / framing:** black.
- **Camera move:** none (no picture).
- **Cast:** none.
- **Action:** optional, for the standalone hook post: the series title card "เขตปิดตาย 09 / DEAD ZONE 09" fades in at 52.2 in red and white (the screenplay places this card after Scene 02; use it here only if this cut is published alone, otherwise leave the tail black and cut straight into Scene 02 beat 2).
- **Dialogue / caption:** none.
- **Sound:** for 1 s only the hazard tick and the rain, then the tick stops on its own (51.5 + 1.0) and the rain alone carries to the end.
- **Light:** -
- **Transition out:** end (or straight cut to Scene 02 beat 2).
- **Sets up:** next episode / next part.

---

## Rhythm check

| Block | Time | Shots | Mean length | What the viewer holds |
|---|---|---|---|---|
| Hook | 0.00-5.50 | 01-03 | 1.83 s | what happened on the radio; where are we |
| Hero and the fuse | 5.50-10.75 | 04-06 | 1.75 s | battery 3 bars, the still driver |
| The call | 10.75-28.00 | 07-15 | 1.92 s | the promise, "ทุกครั้งเลย", the hang-up |
| Approach | 28.00-37.00 | 16-20 | 1.80 s | the door is open, the driver does not move |
| Reveal and attack | 37.00-51.50 | 21-28 | 1.81 s | the face, the lunge, the bite, Kong's face |
| Tail | 51.50-53.50 | 29 | 2.00 s | black |

Angle mix: low 9, eye 10, high 4, inserts/macro 5; the height class or the shot size changes at every cut. Framing changes (cuts plus snaps) about every 1.4 s. Shake used only in 01 (tiny), 07 (buzz), 16 (0.8 s), 24-26 (attack); everything else is eased drift, so the shake means something.

## Assets to build

### Sets
1. **S1 `expressway3d`** (new module beside `v3/set3d/office3d.py`, same API shape: `build()`, anchors, marks, cameras, setters): road deck 3 lanes x 60 D with lane paint (SVG texture), wet-road shader (dark asphalt, glossy; see risks), concrete barriers with drainage stains, LED lamp posts every 12 D (cold white heads, the key light is one of them), 40+ instanced low-poly cars with SVG liveries and emissive tail/hazard lights (per-car blink phase), 4-5 crashed cars with crumpled panels (shape keys), rescue truck with "กู้ภัย" livery and a light bar (3 rotating red spot lights + emissive lenses), hero sedan with: openable driver door on a hinge (keyed), side window that can shatter (two states + falling glass cards), interior (seat, wheel, dash cluster emission, courtesy lamp), seat belt. Haze: depth mist in the compositor in blue-grey.
2. **S2 `radio_macro`**: the shoulder radio model at macro scale (grille, antenna, TX LED emission keyed to audio), black surround, rain-bead cards.
3. **Marks and cameras** for every shot above (anchor cameras: `ground_puddle`, `wide_high_barrier`, `low_kong`, `door_eye`, `door_ots`, `cabin_reverse`, `driver_cu`, `roof_high`).

### Puppets (one extension module, like `v3/cast/cast_ext.py`; `puppet.py` not edited)
4. **`kong`**: regular build, spiky black hair, stubble beard (dot texture), orange reflective rescue vest with silver strips and the "RESCUE" back/chest text, Thai flag patch on the arm, backpack with the crowbar strapped on, shoulder radio, dark cargo trousers, boots; wristwatch on the left forearm (small dial drawn on the ink limb); two-hand cutter hold.
5. **`rescuer_b`**: same uniform family, distinct silhouette: slimmer, younger, no beard, yellow rescue helmet (removable for shot 25: helmet as a separate prop card), glass punch prop.
6. **`driver`**: office worker, white shirt, loosened dark tie, grey trousers, seat belt; new faces `infected_hidden`, `infected_eyes`, `infected_snarl` (blank ring eyes without pupils, temple vein lines, teeth); no breathing or blinks while "dead".
7. **`namnuea_portrait`**: Namnuea as a still head-and-shoulders portrait for the phone's contact photo (ponytail, oxblood hooded jacket, `happy`), rasterised into the phone UI texture (it is a photo on a screen, so a still is correct there).
8. **New puppet fx:** `rain_drips` (drip lines and drops on head and costume, re-seeded every 3 frames, moving downward), `wet` (costume darken + flattened hair spikes), `phone_glow` (cool highlight under the chin), `beacon_pulse` (per-frame `tint` from the beacon angle, see risks).
9. **New props:** `rescue_cutter` (two grips, battery pack with 3-bar gauge texture that can show 0-3 bars), `phone` (screen texture swap: incoming call, missed-call banner, call timer, call ended, lock screen), `glass_punch`, `helmet` (free prop), `crowbar` (on the backpack, removable later).

### Inserts and textures
10. Phone UI in Thai (SVG): incoming call "น้ำเหนือ", banner "4 สายที่ไม่ได้รับ", timer 00:41-00:43, "สิ้นสุดการโทร", lock screen with her photo and 21:47; raindrop layer on the glass.
11. Cutter battery gauge (3 bars, emissive), wristwatch dial 21:47 with a moving second hand.
12. Rescue truck livery and light bar lenses; car liveries (generic, no real brands); Thai expressway signage (generic, no real operator logos).

### Effects
13. Rain: 3 depth layers of thin emissive streak cards around the camera (falling at about 1 D per frame, length from the shutter), splash-ring decals on the road and on the sedan roof (animated texture), window and phone-glass drops (texture + offset blobs), drip sheets off the door edge.
14. Static burst (2D overlay, 6 frames) for the cut 01 -> 02.
15. Camera shake generator per LOOK_SPEC 5.3 (5 Hz, random keys every 3 frames at 24 fps) and the fast-frame streak (`render_layers.py` + `post.py`) for the whip pans and the crash zoom.
16. Breaking side window (shot 06) and the rolling helmet (shot 25).

### Sound (all from free/local libraries or recorded; no paid API)
17. Rain beds (close fabric, wide road, inside car roof), radio squelch and band-limited voice chain, phone vibration, call answer and end tones, hazard relay tick, dash door chime, horns, distant sirens, glass punch and glass, door hinge and slam, wet impacts, scream, breaths.
18. Voices: radio man, Namnuea (phone-filtered), Kong, rescuer_b: Thai performances.

## Risks (honest)

1. **Red light on unlit puppets.** The look rule says cards are never lit or tinted, but the EP.1 grammar and this plan need the beacon to turn faces red. The plan uses the puppet's own `tint` key driven per frame by the beacon angle (fills only, ink untouched). It is a deliberate deviation; cap the tint (peak about `#ffc8c8`) and check it does not read as pink/magenta. If the director rejects it, the faces stay white and only the set pulses red, which weakens shots 21, 26 and 28.
2. **Colour band.** This is a night exterior with special light: it will sit outside the reference hue band (much more blue, little orange outside Kong's vest, more than 15 percent of pixels darker than V 0.25). Run `hue_report.py` anyway and record why; the target here is the EP.1 grammar (dark blue, grey, red), not the daylight reference band.
3. **Wet-road reflections.** The set setup hides set objects from secondary rays and shortens them to keep renders fast; glossy reflections of the tail lights and beacons may not appear. Fallback: painted reflection streaks on the road texture, animated with the beacon phase. Test this first; shot 02 depends on it.
4. **Rain cost and look.** Thousands of streak cards in Cycles at 12 samples may add noise and time; partial fallback is a 2D rain layer composited in front of the 3D render (but then rain does not pass behind objects). Rain must not "boil" the puppets: drips on the sprite re-seed every 3 frames only.
5. **Back views do not exist.** Shots 18 (over-the-shoulder) and 19 (from inside the cabin) are staged so nobody shows the back of the head; the driver in 19 is a shadowed shoulder edge. If it reads as a cheat, swap 19 for a second front angle of rescuer_b.
6. **Cards and the car body.** The driver card sits inside a cabin and lunges through a door opening: the card can cut into the door or the roof when the camera is off axis (stage API trap 3), and two overlapping cards in the bite (shot 25) can speckle. Staging puts the door edge over the contact point; keep `depth_bias`; check with `probe.py` before rendering.
7. **Two-handed cutter.** The puppet IK solves one prop per arm; a big prop held in both hands needs both hands pinned to grip points on a prop card. Not built yet; budget a day.
8. **Infected face is new design.** The 20 expressions do not include it; the three infected faces must be drawn and reviewed against the cast style (round white head, black line face) so they read as wrong without gore.
9. **Thai captions font.** Work Sans Black (the measured caption font) has no Thai glyphs; Kanit/Prompt Black must be available offline (npm @fontsource) and calibrated to the same stroke and size. Long Thai lines must be cut into 4-14 character phrases without splitting words.
10. **Voices without a paid API.** The plan needs four Thai performances, one of them a 14-year-old girl. Local TTS for Thai is weak and reads flat; the scream and breaths cannot be TTS. Best path is recorded voice actors or the director's own scratch track; timing above is an estimate until a real read is measured (the story notes say engines read slower than estimates).
11. **24 fps vs the spec's 30 fps.** All spec frame counts are converted (x 0.8); the existing render and post tools assume 30 fps (`timing.py`, `post.py`, `qa_motion.py`) and need an fps parameter.
12. **Render budget.** 1236 picture frames at about 18 CPU s each is about 6.2 CPU hours at final quality, before rain overhead and retakes; with 4 cores and one render per agent, plan two days of render.
13. **Violence level.** The bite is kept non-graphic (door occludes it, the hand covers the wound). If the platform needs it softer still, shot 25 can stay entirely behind the door with only the arm and the scream.
14. **Faithfulness checks.** Nothing here adds a story event: the radio squelch in 20 and 28 is wordless (no new radio line), rescuer_b has no invented dialogue, Namnuea is never shown in person, no title card unless the hook is published alone. The added visual details are the watch at 21:47, the 3-bar gauge, rain on the phone, the hazard tick, the courtesy lamp, the helmet roll and the driver standing up in shot 28. The last one moves slightly ahead of the screenplay (Scene 02 has Kong push the infected off with the crowbar next); if that reads as contradicting the next beat, keep the driver crouched over rescuer_b in 28.
