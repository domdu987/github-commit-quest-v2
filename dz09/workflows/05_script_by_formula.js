export const meta = {
  name: 'thai-script-v2-formula',
  description: 'Rewrite the Thai voice-over so its story structure matches the two reference clips on all 12 formula elements, then judge, edit and adversarially verify',
  phases: [
    { title: 'Draft', detail: 'three rewrites: mirror clip A, mirror clip B, best of both' },
    { title: 'Judge', detail: 'formula match beat by beat, native ear, facts timing and captions' },
    { title: 'Edit', detail: 'final script from the winner plus the best lines of the others' },
    { title: 'Verify', detail: 'independent 12-point formula check, facts, length, captions, spelling' },
  ],
}

const S = '__SCRATCH__'
const OUT = S + '/proj/script_th_v2'
const HOOK = 'เขาลากเส้นบนแผนที่อากาศ ชี้ตรงเข้านิวยอร์ก แล้วหัวหน้าก็ลบทิ้งเฉยเลย'
const HOOK_CAPS = 'เขาลากเส้น | บนแผนที่อากาศ | ชี้ตรงเข้า | นิวยอร์ก | แล้วหัวหน้า | ก็ลบทิ้ง | เฉยเลย'

const BRIEF = [
  'CONTEXT',
  'We are making a 60-65 second vertical animated short for a Thai audience that must feel like two English reference clips the client sent. Read both reference transcripts several times, they are the model: ' + S + '/media/a/script_clean.txt (clip A, the railroad gaps) and ' + S + '/media/b/script_clean.txt (clip B, the dragon jar). Our current Thai script (approved for language quality, NOT for structure) is in ' + S + '/proj/script_th/script_th.json; it tells the true story of the 1938 New England hurricane.',
  'THE PROBLEM: the client asked whether our story is told like his clips. It is only partly: 7 of 12 structural elements match. He then said: make it the same. Your job is the story structure, in natural spoken Thai.',
  '',
  'THE 12 ELEMENTS OF THE REFERENCE FORMULA (every one must be present in the new script, in an order that mirrors the references)',
  '1. Cold-open hook: "He" plus a strange physical act, one sentence. (A: sawed gaps into a railroad every 39 feet. B: put a bronze ball in a dragon mouth and told the emperor to run.)',
  '2. A spoken pivot ("You see, ...") that sets the world and the stakes.',
  '3. The hero is the youngest or the smallest person in the room.',
  '4. The authority mocks him in a quoted line of direct speech.',
  '5. THE HERO PERSISTS and keeps acting. (A: he will not close a single gap. B: he drags the jar up a hill and lives there alone.) MISSING in our current script: our hero vanishes.',
  '6. A MOCKING NICKNAME for his odd thing. (A: "The Clickety Clack Line". B: "the world most expensive toy", "the toy guy".) MISSING.',
  '7. A false defeat: the world seems to prove him wrong. (A: the rival finishes first, then his gaps shrink. B: a ball falls and nothing happens.) We have it: the next morning is an ordinary grey drizzle.',
  '8. A SECOND MOCKING QUOTE at the false defeat. (A: "See, even your gaps know you were wrong." B: "Hey, it is the toy guy. Did your frogs get hungry again?") MISSING: our boss only whistles.',
  '9. The turn: "Meanwhile, ..." or "Then one night, ...".',
  '10. THE DISASTER LANDS ON THE DOUBTERS and is shown as one physical image, with no casualty count and no aftermath. (A: the perfect railroad kicks sideways like a snake right as a train rolls onto it. B: the next morning the palace was a pile of rubble.) DIFFERENT in ours: we count 700 dead and the tone turns to grief.',
  '11. THE MECHANISM REVEAL: the script explains, simply and physically, why his odd thing was right. (A: rails grow in heat, so the gaps were room to grow. B: the pendulum, the rods, one ball means far away, all eight means right underneath.) WEAK in ours.',
  '12. It ends on an image or on the last line of the reveal. No moral, no summary, no "and that is why".',
  'Also copy the texture of the references: short spoken sentences; concrete countable details (a coin, a sheet of paper, eight dragons); a running object the viewer can watch change; wry understatement; the hero almost never speaks; the narrator never judges.',
  '',
  'HOW OUR STORY MAPS (use this skeleton; improve the wording, keep the logic)',
  '- The odd thing is his LINE: on the map every hurricane track curves out to sea, his is ruler-straight and points north at New York.',
  '- Persistence (element 5): the boss rubs it out, he draws it again; out, again. He will not bend it.',
  '- Nickname (element 6): the office gives the line a mocking name. Find a Thai nickname that is short, funny when heard, visual, and ties to the mechanism (for example a ruler-straight line). Use it at least three times as a running thread, including in the second boss quote and in the final beat.',
  '- False defeat and second quote (elements 7, 8): the official forecast goes out (rain, gusty winds), the next morning Long Island wakes to an ordinary grey drizzle, and the boss gloats in one quoted line that uses the nickname.',
  '- Turn and mechanism (elements 9, 11): meanwhile out at sea the storm is caught between two walls of high pressure, one on each side, with a single corridor left between them, and the corridor runs straight north. Nothing can curve inside a corridor. The wind in it flings the storm north at almost 100 km per hour, faster than any hurricane measured before. That is why his line was straight: he had drawn the corridor.',
  '- Disaster and ending (elements 10, 12): one physical image of the storm arriving exactly where the line pointed (for example people on the beach take the wall of water for a fog bank; it is taller than their houses), then end on the vindication image with a callback: the storm ran up his straight line, while the official forecast on the kitchen table still said rain. No casualty number anywhere in the script.',
  '',
  'FACTS YOU MUST KEEP TRUE: September 1938; U.S. Weather Bureau; the storm was off Florida and the senior forecasters expected it to curve out to sea as such storms usually did; a junior forecaster (historically Charles Pierce, unnamed in our script) reasoned that the storm was squeezed between two high-pressure areas and would ride the channel between them north into New England, and he was overruled by the chief forecaster; the official forecast spoke only of rain and gusty winds; New England had not had a major hurricane since 1815 (more than 120 years); the storm raced north at about 60 miles per hour, nearly 100 km per hour, among the fastest forward speeds on record; it came ashore on Long Island, New York, and went on into New England; people on the beach mistook the wall of water for a fog bank; it was taller than houses.',
  'DRAMATISED AND ALLOWED (the references dramatise in exactly this way): the line drawn on the wall map and rubbed out, the redraw-and-erase repetition, the nickname, the two quoted boss lines, the boss whistling, the forecast lying on a kitchen table, "he had drawn the corridor". Do not invent any other fact, name, date, number or quote, and never state a casualty figure.',
  '',
  'HARD CONSTRAINTS',
  '- Sentence 1 must stay EXACTLY, character for character: ' + HOOK + ' with caption phrases exactly: ' + HOOK_CAPS + ' (its audio and picture are already made).',
  '- Natural spoken Thai, the voice of a Thai short-video storyteller, not translationese. The boss is หัวหน้า. Place names: นิวยอร์ก, บอสตัน, ฟลอริดา, ลองไอแลนด์, นิวอิงแลนด์. Speed in km per hour. Year 1938.',
  '- Length: 290-325 Thai syllables in total (it is read at a brisk pace into 65 seconds). To make room for the new elements, compress the middle of the old script (newspapers, fishermen, families): one sentence of stakes is enough.',
  '- Two texts per sentence: "tts" = exactly what the voice says, for a Thai text-to-speech engine: no digits, no Latin letters, numbers and the year written as a narrator says them (the year as หนึ่งเก้าสามแปด), a space where a narrator pauses; and "captions" = the same sentence cut into on-screen phrases in order, each 4-14 Thai characters, never splitting a word, digits allowed where a viewer expects them (1938, 120, 100), no trailing punctuation except ? ! or a closing quote. Joined, the captions say the same as the tts.',
  '- Tag each sentence with: beat (hook, pivot, setup, hero, boss_quote, persist, nickname, forecast_out, false_defeat, boss_quote_2, meanwhile, mechanism, disaster, ending) and element (the list of formula element numbers 1-12 it carries).',
  '',
  'RULES: do not call any MCP or connector tools; do not generate audio; no network calls; write files only under ' + OUT + ' ; your final message is consumed by a script, return the structured result only.',
].join('\n')

const SENT = {
  type: 'array',
  items: {
    type: 'object',
    properties: {
      beat: { type: 'string' },
      element: { type: 'array', items: { type: 'number' } },
      tts: { type: 'string' },
      captions: { type: 'array', items: { type: 'string' } },
    },
    required: ['beat', 'element', 'tts', 'captions'],
  },
}
const DRAFT_SCHEMA = {
  type: 'object',
  properties: {
    nickname: { type: 'string' },
    sentences: SENT,
    syllables_estimate: { type: 'number' },
    english_gloss: { type: 'string', description: 'a plain English line-by-line gloss of the Thai, for non-Thai collaborators' },
    notes: { type: 'string' },
  },
  required: ['nickname', 'sentences', 'syllables_estimate', 'english_gloss', 'notes'],
}

const ANGLES = [
  { key: 'mirror-A', text: 'Your method: MIRROR CLIP A. Write out clip A beat by beat (about 14 beats), then write our story so that each beat does the same job in the same position: stakes, youngest, purple-faced boss quote, he will not change it, the "perfect" others win at first, the nickname spreads, something weird happens that seems to prove him wrong, the boss gloats, meanwhile the hidden force builds, the hottest moment, the catastrophe image. Then add the mechanism reveal in the last third the way clip B does.' },
  { key: 'mirror-B', text: 'Your method: MIRROR CLIP B. Write out clip B beat by beat (about 14 beats), then write our story so that each beat does the same job in the same position: hook with reaction, the laugh, "you see" plus the odd thing described, the proud authority, first test and nothing happens, they laugh harder and the nickname, he persists alone, then one night the signal, he is mocked once more with the nickname, the next morning the disaster image, then the mechanism explained in four short physical sentences, ending on the line that says what it meant.' },
  { key: 'blend', text: 'Your method: BEST OF BOTH, Thai first. Build the strongest possible Thai telling that hits all 12 elements, taking from each clip what suits this story (clip A has the better running object and false defeat; clip B has the better mechanism reveal and last line). Be bold about the nickname and the two boss quotes: they must be funny when heard in Thai.' },
]

phase('Draft')
const drafts = (await parallel(ANGLES.map(a => () =>
  agent(BRIEF + '\n\n' + a.text + '\nBefore returning: tick off the 12 elements against your own text one by one, read it aloud in your head at speed twice, cut what sounds written, count the syllables honestly.', { label: 'draft:' + a.key, phase: 'Draft', schema: DRAFT_SCHEMA })
    .then(d => d ? { key: a.key, draft: d } : null)
))).filter(Boolean)
log('drafts: ' + drafts.map(d => d.key + ' "' + d.draft.nickname + '" ' + d.draft.syllables_estimate + ' syl').join(', '))
if (drafts.length === 0) { return { error: 'no drafts' } }

const LETTERS = ['A', 'B', 'C']
const pack = drafts.map((d, i) => 'DRAFT ' + LETTERS[i] + ' (nickname: ' + d.draft.nickname + ')\n' + d.draft.sentences.map(s => '[' + s.beat + ' | elements ' + s.element.join(',') + '] ' + s.tts + '\n    captions: ' + s.captions.join(' | ')).join('\n') + '\nENGLISH GLOSS\n' + d.draft.english_gloss).join('\n\n')

const JUDGE_SCHEMA = {
  type: 'object',
  properties: {
    scores: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          draft: { type: 'string' },
          score: { type: 'number', description: '0-10 on your lens' },
          elements_missing_or_weak: { type: 'array', items: { type: 'string' } },
          problems: { type: 'array', items: { type: 'string' } },
          best_lines: { type: 'array', items: { type: 'string' } },
        },
        required: ['draft', 'score', 'elements_missing_or_weak', 'problems', 'best_lines'],
      },
    },
    winner: { type: 'string' },
    best_nickname: { type: 'string' },
    advice_for_editor: { type: 'string' },
  },
  required: ['scores', 'winner', 'best_nickname', 'advice_for_editor'],
}

const LENSES = [
  { key: 'formula-match', text: 'Your lens: structural match with the reference clips, and nothing else. First write the beat sheet of clip A and of clip B from the transcripts. Then for each draft check the 12 elements one by one: quote the exact Thai sentence that carries the element and say whether it does the same job, in a comparable position, with comparable force as in the references (strong, weak or missing). Be strict on the five that were missing before (5 persistence, 6 nickname used as a running thread, 8 second mocking quote, 10 disaster on the doubters as one image with no casualty count, 11 mechanism reveal that makes the odd thing right) and on the ending (12). Also judge the texture: countable concrete details, a running object, wry understatement, no narrator judgement.' },
  { key: 'native-ear', text: 'Your lens: the native ear. You are a Thai voice director for short-video story channels. Read each draft aloud in your head at speed. Flag every phrase that sounds translated, stiff, bookish, ambiguous when heard, hard to say quickly, or tonally off; judge whether the nickname and the two boss quotes are actually funny and natural in Thai; judge whether the mechanism reveal is clear on first hearing to someone who knows nothing about weather. Quote the exact Thai and propose the fix.' },
  { key: 'facts-timing-captions', text: 'Your lens: facts, timing and captions. (1) Sentence 1 identical to the required hook, character for character, with the required caption phrases. (2) Every factual statement against the fact list; every dramatised element inside the allowed list; no casualty figure; nothing else invented. Is "two walls of high pressure with one corridor between them" stated in a way that stays true to the fact list? (3) Count syllables carefully (you may pip install pythainlp; the dictionary engines work offline): total 290-325. (4) tts text has no digits or Latin letters and has sensible pause spaces. (5) Every caption phrase 4-14 Thai characters, no word split, natural breath unit, joined captions equal the tts meaning. List every violation with the exact phrase.' },
]

phase('Judge')
const verdicts = (await parallel(LENSES.map(l => () =>
  agent(BRIEF + '\n\nYOU ARE A JUDGE, not a writer. ' + l.text + '\nScore every draft from 0 to 10 on your lens only, name a winner and the best nickname, and list the best individual lines across all drafts that the editor should keep.\n\n' + pack, { label: 'judge:' + l.key, phase: 'Judge', schema: JUDGE_SCHEMA })
    .then(v => v ? { lens: l.key, verdict: v } : null)
))).filter(Boolean)
log('judges: ' + verdicts.map(v => v.lens + ' -> ' + v.verdict.winner + ' / ' + v.verdict.best_nickname).join(', '))

const FINAL_SCHEMA = {
  type: 'object',
  properties: {
    nickname: { type: 'string' },
    sentences: SENT,
    syllables_total: { type: 'number' },
    element_check: { type: 'array', items: { type: 'object', properties: { element: { type: 'number' }, verdict: { type: 'string' }, thai_quote: { type: 'string' } }, required: ['element', 'verdict', 'thai_quote'] } },
    english_gloss: { type: 'string' },
    files: { type: 'array', items: { type: 'string' } },
    changes: { type: 'string' },
    open_issues: { type: 'array', items: { type: 'string' } },
  },
  required: ['nickname', 'sentences', 'syllables_total', 'element_check', 'english_gloss', 'files', 'changes', 'open_issues'],
}

phase('Edit')
const edited = await agent(BRIEF + '\n\nYOU ARE THE EDITOR. Write the final script: start from the draft the judges prefer overall, graft in the best lines of the others, use the best nickname, and fix every problem the judges listed (the formula judge wins on structure, the native ear wins on wording, the facts judge wins on facts and length). Sentence 1 stays exactly as required. Then write these files: ' + OUT + '/script_th.json (an object with nickname and sentences), ' + OUT + '/script_th_tts.txt (the tts text, one sentence per line), ' + OUT + '/script_th_captions.txt (one caption phrase per line, a blank line between sentences), ' + OUT + '/script_en_gloss.txt (a line-by-line English gloss with the beat and element tags).\n\nDRAFTS\n' + pack + '\n\nJUDGES\n' + JSON.stringify(verdicts, null, 1).slice(0, 36000), { label: 'edit:final-script', phase: 'Edit', schema: FINAL_SCHEMA })

phase('Verify')
const verified = await agent(BRIEF + '\n\nYOU ARE THE LAST CHECK before this script goes to a paid voice engine and to the animators, and you did not write it. Assume the editor missed something. Work from the files in ' + OUT + ' . Check, with evidence: (1) THE 12 ELEMENTS, independently: write the beat sheets of clip A and clip B yourself from the transcripts, then go through the 12 elements and for each quote the Thai sentence that carries it and judge strong, weak or missing; a weak or missing element is a defect you must repair. Check the nickname is used as a running thread (at least three times, including the second boss quote and the final beat), the hero persists, the disaster is one physical image with no casualty figure, the mechanism reveal makes the line right, and the ending has no moral. (2) Sentence 1 identical to the required hook and caption phrases. (3) Facts against the fact list and the allowed dramatisations; nothing else invented. (4) Natural spoken Thai at speed; quote anything that stumbles or sounds translated. (5) Length: count syllables with a tool (pip install pythainlp is allowed; dictionary engines work offline) and adjust to 290-325. (6) tts text: no digits, no Latin letters, year and numbers as spoken, pause spaces. (7) captions: 4-14 Thai characters each, no word split, joined captions equal the tts meaning. (8) spelling and tone marks. Repair the files directly for every real defect (minimal changes, same structure), re-run your checks, update the English gloss, and return the final script exactly as it now stands in the files, with your own element_check table.\n\nThe editor reported:\n' + JSON.stringify(edited, null, 1).slice(0, 24000), { label: 'verify:final-script', phase: 'Verify', schema: FINAL_SCHEMA })

return { final: verified || edited, drafts: drafts.map(d => ({ key: d.key, nickname: d.draft.nickname, syllables: d.draft.syllables_estimate })), judges: verdicts.map(v => ({ lens: v.lens, winner: v.verdict.winner, nickname: v.verdict.best_nickname })) }
