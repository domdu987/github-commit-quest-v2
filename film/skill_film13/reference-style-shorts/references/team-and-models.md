# Running the work as a team, and on which model

Multi-agent workflows did almost all of the first production. This file records what worked, what it cost, and how to spend less next time.

## What the first production spent (subagent tokens, top model unless noted)

| Workflow | Agents | Tokens | Verdict |
|---|---|---|---|
| Measure the reference look (6 lenses, synthesis, 2 verifiers) | 9 | 3.4 M | Needed once per reference style. Reuse `pipeline/spec/` when the style is the same. |
| 2D puppet and flat set, reviews, first 5 s | 5 | about 1.5 M | The puppet is reusable as is. The flat set was the wrong approach. |
| Likeness scoring tool and validation | 2 | 1.1 M | Reusable as is. |
| Script in Thai, then rewrite to the story formula | 8 + 8 | 2.7 M | Write to the formula the first time and this halves. |
| 3D set, staging system, reviews, 5 s film | 5 | about 3 M | Reusable as is; new sets cost one builder and one reviewer each. |
| Shot plan for the whole film | 8 | 3.0 M | Could run a tier down with the same structure. |
| Colour fix with a numeric band (Opus class) | 1 | 0.26 M | One pass, all targets met. |

The pattern: discovery is expensive and happens once. This skill bundles its results, so a new clip in the same style should start at the script and the sets.

## Which model for which work

Pass the model in every agent call (`agent(prompt, {model: 'opus', ...})`) and confirm in the agent's transcript that the messages really come from that model; the metadata field named "pickedEffortModel" does not show it.

- Strongest model: the main conversation, judging likeness by eye, creative direction (shot plan merge, final review), anything where the brief cannot be reduced to a band.
- One tier down: builders and reviewers of sets, cast, props, shots, colour and light, when the brief gives numeric acceptance bands and names the measuring tool.
- Cheapest tier that follows procedures: render loops, assembly, mixing from a cue list, scripted QA, file handling.

Quality holds when the brief contains: the files to read first, the exact folder the worker owns, the acceptance numbers, the tool that measures them, and an instruction to look at the result next to named reference frames. It drops when the brief asks for taste.

## Workflow shapes that earned their cost

- Build then independent review-and-repair. Reviewers found real defects every time: stale sprites after a re-pose, shadows detached from feet, a cast copied from the reference, a set too thin on detail.
- Three attempts, three judges with different lenses, one editor, one adversarial checker, for scripts and shot plans.
- Lenses then synthesis then verification, for measurement.
- One worker with a numeric band, for corrections.
The scripts are in `workflows/`, numbered in the order they were used. They carry placeholders (`__PROJ__`); replace them with the project path before running.

## Operating rules learned the hard way

- **Check that work is alive, not that it is listed.** After a user interrupt both background workflows stopped; the journal still listed their agents and progress was reported as running for hours. Compare each agent transcript's modification time with the clock.
- **Resume, do not restart.** Workflows resume from their run id with finished agents served from cache; only edit the prompts of stages that have not finished. To change a later stage's brief, wait for the earlier stages, stop, edit, resume.
- **One owner per file.** Give each worker a folder. Extend shared modules with extension modules.
- **Wake-ups.** A background shell loop that exits when a journal shows the expected number of results is a cheap way to be called back at a stage boundary. It has a maximum lifetime; do not rely on it for more than two hours.
- **Concurrency.** Each workflow runs about two agents at once on a 4-core machine. Several workflows can run side by side when their workers own different folders; final renders compete for the same cores, so cap render threads per worker.
- **Keep the main conversation small.** Read summaries and specific fields from results, not whole transcripts; view a few downscaled sheets instead of many frames.
- **Paid tools stay in the main conversation.** Forbid workers from calling paid APIs and connectors; make purchases yourself so spending is counted and reported.
- **Temporary machines.** Work in a scratch folder survives a restart of the same session but not the end of the session. Send the user a source archive at milestones, and commit the pipeline to a repository if they want to keep it.
