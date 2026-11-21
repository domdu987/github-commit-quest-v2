# Film 17 SFX

## Reused (copied unchanged)
| file | from |
|---|---|
| crowd_laugh.mp3 | film/film10/audio/sfx/crowd_laugh.mp3 |
| whoosh.mp3 | film/film10/audio/sfx/whoosh.mp3 |
| gasp.mp3 | film/film6/audio/sfx/gasp.mp3 |

No existing laugh/ding variant was needed. Nothing suitable for the rest existed in film5/6/10.

## Generated (fal-ai/elevenlabs/sound-effects/v2, queue.fal.run submit + poll, `python3 gen_sfx.py [name]`, prompt_influence 0.5)
| file | seconds | prompt |
|---|---|---|
| caliper_click.mp3 | 1.5 | A single sharp metallic click of steel measuring calipers closing on a surface, dry, close-up, short, with a tiny ring. No music, no voice, no speech. |
| caliper_click2.mp3 | 1.5 | Two quick crisp steel caliper clicks, slightly different pitch, tight dry foley, close microphone. No music, no voice, no speech. |
| drawer_slide.mp3 | 2.5 | A heavy wooden filing-cabinet drawer sliding open on old runners, soft wooden rumble and a gentle thunk at the end, dry close foley. No music, no voice, no speech. |
| wagon_horse.mp3 | 4 | A horse-drawn police wagon rolling slowly on Paris cobblestones, iron-rimmed wheels rattling, horse hooves clip-clopping, harness jingle, outdoors at dusk. No music, no voice, no speech. |
| paper_flutter.mp3 | 2 | Index cards and papers fluttering and riffling quickly, a stack of paper cards flipping, dry foley. No music, no voice, no speech. |
| clock_tick.mp3 | 4 | A steady slow wall clock ticking, tick tock tick tock, dry, quiet room, evenly spaced, ticks only. No music, no voice, no speech. |
| sting.mp3 | 2.5 | A short comedic orchestral sting: sharp staccato string and brass hit, one dramatic 'dun dun' stab with a quick decay, cartoon revelation. No voice. |

Cue timing lives in film/conform17.py (CUES, narration time; +0.10 s to film time). Every effect is peak-normalised by film/audio/mixer.py; SFX overlapping narration are ducked as in conform10; the sting is not ducked.
