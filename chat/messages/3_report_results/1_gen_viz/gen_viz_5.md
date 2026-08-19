# gen_viz_5 — report_results

> Phase: `gen_paper_repo` · `gen_viz`
> Run: `run_DyrN7YJjJoEX` — Longer Reasoning Chains Reduce Self-Check Agreement in Language Models
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_viz_5` (sdk_openhands_agent, openai/nvidia/nemotron-3-super-120b-a12b)

### [1] CONFIG · 2026-08-19 19:24:08 UTC

```
Model: openai/nvidia/nemotron-3-super-120b-a12b | Session: 9e82e0d5-e8ec-41c4-a680-69c32be1bbb7 | CWD: /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5 | Tools: 3 | Permission: acceptEdits
```

### [2] SYSTEM PROMPT · 2026-08-19 19:24:10 UTC

```
<research_methodology>
Create figures that belong in a top-venue paper.

- Every figure needs a clear takeaway visible at a glance.
- Choose chart types that match the data relationship (comparisons, trends, correlations, distributions).
- Include uncertainty (error bars, confidence intervals) when showing experimental results.
- Keep it clean — no clutter, clear labels with units, readable at print size.
</research_methodology>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>
```

### [3] SYSTEM-USER prompt · 2026-08-19 19:24:10 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/`:
GOOD: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/file.py`, `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Render a publication-quality DATA figure for a top-tier venue research paper.

This figure plots numbers, so it is RENDERED from those numbers — not drawn by an image model. Use the aii-data-fig-gen skill. The output is deterministic: run it once, look at it, fix the spec if the data or labels are wrong, run it again.

STEPS:
1. Read the skill: `.claude/skills/aii-data-fig-gen/SKILL.md`.
2. Pick the chart type that fits the specification below. `python <skill>/scripts/chart_gen.py --list-types` lists them; `--example <type>` prints a complete spec to copy.
3. Write your spec to `fig5_spec.json` in your workspace. Put EVERY numeric value from the specification into it — the spec is the figure.
4. Render it:
   `python <skill>/scripts/chart_gen.py --spec fig5_spec.json --out fig5_v0`
   That writes `fig5_v0.pdf` (the deliverable, vector) and `fig5_v0.png` (for you to look at).
5. READ THE PNG BACK and check it against the checklist below.
6. If anything is wrong, edit the spec and re-render. Repeat until clean — this is cheap and deterministic, so there is no attempt limit and no reason to accept a flawed figure.

DELIVERABLE: `fig5_v0.pdf` in your workspace root. Leave `fig5_spec.json` there too — it is the figure's source, and the step files it next to the figure so the figure stays reproducible.

Verification checklist (after EVERY render) — these are the things only you can check, because they are about whether the figure says what you meant:
- Every number in the figure matches the specification — no invented or dropped values
- Axis labels state what is measured AND its units
- Axis ranges make the comparison readable rather than flattening it
- The chart type still makes the point once you can see it drawn
- The caption describes what is actually drawn

The generator already REFUSES the rest rather than shipping them, so a figure you can read back cannot have them: overlapping or cut-off labels, a legend covering the data, a series drawn without a name beside named ones, two series a reader cannot tell apart, and a fit or a scale that the data cannot support. When it exits non-zero the message names the exact key, index or label and what to change — do that rather than re-rolling.

Reach for a generator first, and hand-write only if none fits. Every type in `--list-types` already carries the house style, the data-integrity checks and the layout fixes, so using one is less work than plotting by hand and the result matches every other figure in the paper.

If nothing in the catalogue fits, writing matplotlib yourself is expected and supported — novel figures exist. When you do, import the house style AND its layout passes so the figure still belongs to the set — `apply_house_style`, `place_legend`, `place_point_label`, `fit_legends`, `clear_legends_of_data`, `fit_tick_labels`, `fit_titles`, `rasterize_dense_clouds`, `assert_legends_clear_of_data`, `assert_series_are_distinguishable`, `assert_axis_names_are_unique` from `chart_style`, and `fit_point_labels` + `assert_text_is_legible` from `chart_geometry`, the last of which raises if any label ends up printed over another or cut off at the edge. Build legends with `place_legend` and point names with `place_point_label` — a legend made with a bare `ax.legend` cannot be reflowed when it turns out too wide, and a name written with a bare `ax.annotate` will not be moved off the marker it landed on. The "Use a generator when one fits" section of SKILL.md has the exact snippet and the order to call them in. What you lose is the automatic checking that the picture agrees with the numbers, so verify every value yourself against the specification.
</task>

<figure_specification>
Figure ID: fig5
Title: Agreement by Difficulty and CoT Length
Caption: Self-check agreement rate stratified by difficulty tier (easy, medium, hard) and CoT length (short, medium, long). Long CoT produces the lowest agreement across all tiers, with the largest drop for hard problems (76.0% to 50.7%).
Data and chart description: Grouped bar chart with three groups (Easy, Medium, Hard) and three bars per group (Short, Medium, Long). Y-axis: Agreement Rate (0% to 100%). Easy group: Short=69.5, Medium=71.1, Long=49.2. Medium group: Short=66.7, Medium=80.2, Long=66.7. Hard group: Short=68.0, Medium=76.0, Long=50.7. Three colors for Short/Medium/Long. Clean white background, sans-serif font.
Aspect Ratio: 16:9
Summary: Difficulty-stratified analysis showing self-check divergence across tiers
</figure_specification>


---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "VizExpectedFiles": {
      "description": "Expected output files from viz generation.",
      "properties": {
        "image_path": {
          "description": "Path to the generated figure image file. Example: 'fig1_v0.jpg'",
          "title": "Image Path",
          "type": "string"
        }
      },
      "required": [
        "image_path"
      ],
      "title": "VizExpectedFiles",
      "type": "object"
    }
  },
  "description": "Structured output from viz figure generation agent.",
  "properties": {
    "title": {
      "description": "Figure title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated figure: what it shows, style, any issues fixed",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/VizExpectedFiles",
      "description": "Output file you created. Must include the generated figure image path."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "VizFigureOutput",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [4] HUMAN-USER prompt · 2026-08-19 19:24:10 UTC

```
Can shorter chain-of-thought reduce contradiction in model self-checks?
```

### [5] RETRY (attempt 1) · 2026-08-19 19:26:17 UTC

```
Agent result indicates failure (attempt 1/6): structured_output is None
```

### [6] RETRY (attempt 2) · 2026-08-19 19:26:17 UTC

```
Agent retry... (attempt 2/6): structured_output is None
```

### [7] CONFIG · 2026-08-19 19:26:17 UTC

```
Model: openai/z-ai/glm-5.2 | Session: 098d2b46-569e-4b0b-8579-9459af40564c | CWD: /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5 | Tools: 3 | Permission: acceptEdits
```

### [8] SYSTEM PROMPT · 2026-08-19 19:26:19 UTC

```
<research_methodology>
Create figures that belong in a top-venue paper.

- Every figure needs a clear takeaway visible at a glance.
- Choose chart types that match the data relationship (comparisons, trends, correlations, distributions).
- Include uncertainty (error bars, confidence intervals) when showing experimental results.
- Keep it clean — no clutter, clear labels with units, readable at print size.
</research_methodology>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>
```

### [9] SYSTEM-USER prompt · 2026-08-19 19:26:19 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: structured_output is None
Last actions before failure:
  - [agent_system_user_prompt]: <workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-
  - [agent_human_user_prompt]: Can shorter chain-of-thought reduce contradiction in model self-checks?
  - [status_public_warning]: [ConversationErrorEvent]

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/`:
GOOD: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/file.py`, `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Render a publication-quality DATA figure for a top-tier venue research paper.

This figure plots numbers, so it is RENDERED from those numbers — not drawn by an image model. Use the aii-data-fig-gen skill. The output is deterministic: run it once, look at it, fix the spec if the data or labels are wrong, run it again.

STEPS:
1. Read the skill: `.claude/skills/aii-data-fig-gen/SKILL.md`.
2. Pick the chart type that fits the specification below. `python <skill>/scripts/chart_gen.py --list-types` lists them; `--example <type>` prints a complete spec to copy.
3. Write your spec to `fig5_spec.json` in your workspace. Put EVERY numeric value from the specification into it — the spec is the figure.
4. Render it:
   `python <skill>/scripts/chart_gen.py --spec fig5_spec.json --out fig5_v0`
   That writes `fig5_v0.pdf` (the deliverable, vector) and `fig5_v0.png` (for you to look at).
5. READ THE PNG BACK and check it against the checklist below.
6. If anything is wrong, edit the spec and re-render. Repeat until clean — this is cheap and deterministic, so there is no attempt limit and no reason to accept a flawed figure.

DELIVERABLE: `fig5_v0.pdf` in your workspace root. Leave `fig5_spec.json` there too — it is the figure's source, and the step files it next to the figure so the figure stays reproducible.

Verification checklist (after EVERY render) — these are the things only you can check, because they are about whether the figure says what you meant:
- Every number in the figure matches the specification — no invented or dropped values
- Axis labels state what is measured AND its units
- Axis ranges make the comparison readable rather than flattening it
- The chart type still makes the point once you can see it drawn
- The caption describes what is actually drawn

The generator already REFUSES the rest rather than shipping them, so a figure you can read back cannot have them: overlapping or cut-off labels, a legend covering the data, a series drawn without a name beside named ones, two series a reader cannot tell apart, and a fit or a scale that the data cannot support. When it exits non-zero the message names the exact key, index or label and what to change — do that rather than re-rolling.

Reach for a generator first, and hand-write only if none fits. Every type in `--list-types` already carries the house style, the data-integrity checks and the layout fixes, so using one is less work than plotting by hand and the result matches every other figure in the paper.

If nothing in the catalogue fits, writing matplotlib yourself is expected and supported — novel figures exist. When you do, import the house style AND its layout passes so the figure still belongs to the set — `apply_house_style`, `place_legend`, `place_point_label`, `fit_legends`, `clear_legends_of_data`, `fit_tick_labels`, `fit_titles`, `rasterize_dense_clouds`, `assert_legends_clear_of_data`, `assert_series_are_distinguishable`, `assert_axis_names_are_unique` from `chart_style`, and `fit_point_labels` + `assert_text_is_legible` from `chart_geometry`, the last of which raises if any label ends up printed over another or cut off at the edge. Build legends with `place_legend` and point names with `place_point_label` — a legend made with a bare `ax.legend` cannot be reflowed when it turns out too wide, and a name written with a bare `ax.annotate` will not be moved off the marker it landed on. The "Use a generator when one fits" section of SKILL.md has the exact snippet and the order to call them in. What you lose is the automatic checking that the picture agrees with the numbers, so verify every value yourself against the specification.
</task>

<figure_specification>
Figure ID: fig5
Title: Agreement by Difficulty and CoT Length
Caption: Self-check agreement rate stratified by difficulty tier (easy, medium, hard) and CoT length (short, medium, long). Long CoT produces the lowest agreement across all tiers, with the largest drop for hard problems (76.0% to 50.7%).
Data and chart description: Grouped bar chart with three groups (Easy, Medium, Hard) and three bars per group (Short, Medium, Long). Y-axis: Agreement Rate (0% to 100%). Easy group: Short=69.5, Medium=71.1, Long=49.2. Medium group: Short=66.7, Medium=80.2, Long=66.7. Hard group: Short=68.0, Medium=76.0, Long=50.7. Three colors for Short/Medium/Long. Clean white background, sans-serif font.
Aspect Ratio: 16:9
Summary: Difficulty-stratified analysis showing self-check divergence across tiers
</figure_specification>


---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "VizExpectedFiles": {
      "description": "Expected output files from viz generation.",
      "properties": {
        "image_path": {
          "description": "Path to the generated figure image file. Example: 'fig1_v0.jpg'",
          "title": "Image Path",
          "type": "string"
        }
      },
      "required": [
        "image_path"
      ],
      "title": "VizExpectedFiles",
      "type": "object"
    }
  },
  "description": "Structured output from viz figure generation agent.",
  "properties": {
    "title": {
      "description": "Figure title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated figure: what it shows, style, any issues fixed",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/VizExpectedFiles",
      "description": "Output file you created. Must include the generated figure image path."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "VizFigureOutput",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [10] HUMAN-USER prompt · 2026-08-19 19:26:19 UTC

```
Can shorter chain-of-thought reduce contradiction in model self-checks?
```

### [11] RETRY (attempt 2) · 2026-08-19 19:28:29 UTC

```
Agent result indicates failure (attempt 2/6): structured_output is None
```

### [12] RETRY (attempt 3) · 2026-08-19 19:28:30 UTC

```
Agent retry... (attempt 3/6): structured_output is None
```

### [13] CONFIG · 2026-08-19 19:28:30 UTC

```
Model: openai/nvidia/nemotron-3-super-120b-a12b:free | Session: 926b1e50-3f32-431c-b1d5-e81b4877ecd8 | CWD: /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5 | Tools: 3 | Permission: acceptEdits
```

### [14] SYSTEM PROMPT · 2026-08-19 19:28:32 UTC

```
<research_methodology>
Create figures that belong in a top-venue paper.

- Every figure needs a clear takeaway visible at a glance.
- Choose chart types that match the data relationship (comparisons, trends, correlations, distributions).
- Include uncertainty (error bars, confidence intervals) when showing experimental results.
- Keep it clean — no clutter, clear labels with units, readable at print size.
</research_methodology>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>
```

### [15] SYSTEM-USER prompt · 2026-08-19 19:28:32 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: structured_output is None
Last actions before failure:
  - [agent_system_user_prompt]: <workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-
  - [agent_human_user_prompt]: Can shorter chain-of-thought reduce contradiction in model self-checks?
  - [status_public_warning]: [ConversationErrorEvent]
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: structured_output is None
Last actions before failure:
  - [agent_system_user_prompt]: <workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be insi
  - [agent_human_user_prompt]: Can shorter chain-of-thought reduce contradiction in model self-checks?
  - [status_public_warning]: [ConversationErrorEvent]

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/`:
GOOD: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/file.py`, `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Render a publication-quality DATA figure for a top-tier venue research paper.

This figure plots numbers, so it is RENDERED from those numbers — not drawn by an image model. Use the aii-data-fig-gen skill. The output is deterministic: run it once, look at it, fix the spec if the data or labels are wrong, run it again.

STEPS:
1. Read the skill: `.claude/skills/aii-data-fig-gen/SKILL.md`.
2. Pick the chart type that fits the specification below. `python <skill>/scripts/chart_gen.py --list-types` lists them; `--example <type>` prints a complete spec to copy.
3. Write your spec to `fig5_spec.json` in your workspace. Put EVERY numeric value from the specification into it — the spec is the figure.
4. Render it:
   `python <skill>/scripts/chart_gen.py --spec fig5_spec.json --out fig5_v0`
   That writes `fig5_v0.pdf` (the deliverable, vector) and `fig5_v0.png` (for you to look at).
5. READ THE PNG BACK and check it against the checklist below.
6. If anything is wrong, edit the spec and re-render. Repeat until clean — this is cheap and deterministic, so there is no attempt limit and no reason to accept a flawed figure.

DELIVERABLE: `fig5_v0.pdf` in your workspace root. Leave `fig5_spec.json` there too — it is the figure's source, and the step files it next to the figure so the figure stays reproducible.

Verification checklist (after EVERY render) — these are the things only you can check, because they are about whether the figure says what you meant:
- Every number in the figure matches the specification — no invented or dropped values
- Axis labels state what is measured AND its units
- Axis ranges make the comparison readable rather than flattening it
- The chart type still makes the point once you can see it drawn
- The caption describes what is actually drawn

The generator already REFUSES the rest rather than shipping them, so a figure you can read back cannot have them: overlapping or cut-off labels, a legend covering the data, a series drawn without a name beside named ones, two series a reader cannot tell apart, and a fit or a scale that the data cannot support. When it exits non-zero the message names the exact key, index or label and what to change — do that rather than re-rolling.

Reach for a generator first, and hand-write only if none fits. Every type in `--list-types` already carries the house style, the data-integrity checks and the layout fixes, so using one is less work than plotting by hand and the result matches every other figure in the paper.

If nothing in the catalogue fits, writing matplotlib yourself is expected and supported — novel figures exist. When you do, import the house style AND its layout passes so the figure still belongs to the set — `apply_house_style`, `place_legend`, `place_point_label`, `fit_legends`, `clear_legends_of_data`, `fit_tick_labels`, `fit_titles`, `rasterize_dense_clouds`, `assert_legends_clear_of_data`, `assert_series_are_distinguishable`, `assert_axis_names_are_unique` from `chart_style`, and `fit_point_labels` + `assert_text_is_legible` from `chart_geometry`, the last of which raises if any label ends up printed over another or cut off at the edge. Build legends with `place_legend` and point names with `place_point_label` — a legend made with a bare `ax.legend` cannot be reflowed when it turns out too wide, and a name written with a bare `ax.annotate` will not be moved off the marker it landed on. The "Use a generator when one fits" section of SKILL.md has the exact snippet and the order to call them in. What you lose is the automatic checking that the picture agrees with the numbers, so verify every value yourself against the specification.
</task>

<figure_specification>
Figure ID: fig5
Title: Agreement by Difficulty and CoT Length
Caption: Self-check agreement rate stratified by difficulty tier (easy, medium, hard) and CoT length (short, medium, long). Long CoT produces the lowest agreement across all tiers, with the largest drop for hard problems (76.0% to 50.7%).
Data and chart description: Grouped bar chart with three groups (Easy, Medium, Hard) and three bars per group (Short, Medium, Long). Y-axis: Agreement Rate (0% to 100%). Easy group: Short=69.5, Medium=71.1, Long=49.2. Medium group: Short=66.7, Medium=80.2, Long=66.7. Hard group: Short=68.0, Medium=76.0, Long=50.7. Three colors for Short/Medium/Long. Clean white background, sans-serif font.
Aspect Ratio: 16:9
Summary: Difficulty-stratified analysis showing self-check divergence across tiers
</figure_specification>


---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "VizExpectedFiles": {
      "description": "Expected output files from viz generation.",
      "properties": {
        "image_path": {
          "description": "Path to the generated figure image file. Example: 'fig1_v0.jpg'",
          "title": "Image Path",
          "type": "string"
        }
      },
      "required": [
        "image_path"
      ],
      "title": "VizExpectedFiles",
      "type": "object"
    }
  },
  "description": "Structured output from viz figure generation agent.",
  "properties": {
    "title": {
      "description": "Figure title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated figure: what it shows, style, any issues fixed",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/VizExpectedFiles",
      "description": "Output file you created. Must include the generated figure image path."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "VizFigureOutput",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [16] HUMAN-USER prompt · 2026-08-19 19:28:32 UTC

```
Can shorter chain-of-thought reduce contradiction in model self-checks?
```

### [17] RETRY (attempt 3) · 2026-08-19 19:30:39 UTC

```
Agent result indicates failure (attempt 3/6): structured_output is None
```

### [18] RETRY (attempt 4) · 2026-08-19 19:30:39 UTC

```
Agent retry... (attempt 4/6): structured_output is None
```

### [19] CONFIG · 2026-08-19 19:30:39 UTC

```
Model: openai/agnes-2.0-flash | Session: 6684e880-be7d-4110-a271-de38651f8afa | CWD: /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5 | Tools: 3 | Permission: acceptEdits
```

### [20] SYSTEM PROMPT · 2026-08-19 19:30:41 UTC

```
<research_methodology>
Create figures that belong in a top-venue paper.

- Every figure needs a clear takeaway visible at a glance.
- Choose chart types that match the data relationship (comparisons, trends, correlations, distributions).
- Include uncertainty (error bars, confidence intervals) when showing experimental results.
- Keep it clean — no clutter, clear labels with units, readable at print size.
</research_methodology>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>
```

### [21] SYSTEM-USER prompt · 2026-08-19 19:30:41 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: structured_output is None
Last actions before failure:
  - [agent_system_user_prompt]: <workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-
  - [agent_human_user_prompt]: Can shorter chain-of-thought reduce contradiction in model self-checks?
  - [status_public_warning]: [ConversationErrorEvent]
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: structured_output is None
Last actions before failure:
  - [agent_system_user_prompt]: <workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be insi
  - [agent_human_user_prompt]: Can shorter chain-of-thought reduce contradiction in model self-checks?
  - [status_public_warning]: [ConversationErrorEvent]
  - [agent_system_user_prompt]: PREVIOUS ATTEMPT FAILED
Failure reason: structured_output is None
Last actions before failure:
  - [agent_system_user_prompt]: <workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be insi
  - [agent_human_user_prompt]: Can shorter chain-of-thought reduce contradiction in model self-checks?
  - [status_public_warning]: [ConversationErrorEvent]

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/`:
GOOD: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/file.py`, `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Render a publication-quality DATA figure for a top-tier venue research paper.

This figure plots numbers, so it is RENDERED from those numbers — not drawn by an image model. Use the aii-data-fig-gen skill. The output is deterministic: run it once, look at it, fix the spec if the data or labels are wrong, run it again.

STEPS:
1. Read the skill: `.claude/skills/aii-data-fig-gen/SKILL.md`.
2. Pick the chart type that fits the specification below. `python <skill>/scripts/chart_gen.py --list-types` lists them; `--example <type>` prints a complete spec to copy.
3. Write your spec to `fig5_spec.json` in your workspace. Put EVERY numeric value from the specification into it — the spec is the figure.
4. Render it:
   `python <skill>/scripts/chart_gen.py --spec fig5_spec.json --out fig5_v0`
   That writes `fig5_v0.pdf` (the deliverable, vector) and `fig5_v0.png` (for you to look at).
5. READ THE PNG BACK and check it against the checklist below.
6. If anything is wrong, edit the spec and re-render. Repeat until clean — this is cheap and deterministic, so there is no attempt limit and no reason to accept a flawed figure.

DELIVERABLE: `fig5_v0.pdf` in your workspace root. Leave `fig5_spec.json` there too — it is the figure's source, and the step files it next to the figure so the figure stays reproducible.

Verification checklist (after EVERY render) — these are the things only you can check, because they are about whether the figure says what you meant:
- Every number in the figure matches the specification — no invented or dropped values
- Axis labels state what is measured AND its units
- Axis ranges make the comparison readable rather than flattening it
- The chart type still makes the point once you can see it drawn
- The caption describes what is actually drawn

The generator already REFUSES the rest rather than shipping them, so a figure you can read back cannot have them: overlapping or cut-off labels, a legend covering the data, a series drawn without a name beside named ones, two series a reader cannot tell apart, and a fit or a scale that the data cannot support. When it exits non-zero the message names the exact key, index or label and what to change — do that rather than re-rolling.

Reach for a generator first, and hand-write only if none fits. Every type in `--list-types` already carries the house style, the data-integrity checks and the layout fixes, so using one is less work than plotting by hand and the result matches every other figure in the paper.

If nothing in the catalogue fits, writing matplotlib yourself is expected and supported — novel figures exist. When you do, import the house style AND its layout passes so the figure still belongs to the set — `apply_house_style`, `place_legend`, `place_point_label`, `fit_legends`, `clear_legends_of_data`, `fit_tick_labels`, `fit_titles`, `rasterize_dense_clouds`, `assert_legends_clear_of_data`, `assert_series_are_distinguishable`, `assert_axis_names_are_unique` from `chart_style`, and `fit_point_labels` + `assert_text_is_legible` from `chart_geometry`, the last of which raises if any label ends up printed over another or cut off at the edge. Build legends with `place_legend` and point names with `place_point_label` — a legend made with a bare `ax.legend` cannot be reflowed when it turns out too wide, and a name written with a bare `ax.annotate` will not be moved off the marker it landed on. The "Use a generator when one fits" section of SKILL.md has the exact snippet and the order to call them in. What you lose is the automatic checking that the picture agrees with the numbers, so verify every value yourself against the specification.
</task>

<figure_specification>
Figure ID: fig5
Title: Agreement by Difficulty and CoT Length
Caption: Self-check agreement rate stratified by difficulty tier (easy, medium, hard) and CoT length (short, medium, long). Long CoT produces the lowest agreement across all tiers, with the largest drop for hard problems (76.0% to 50.7%).
Data and chart description: Grouped bar chart with three groups (Easy, Medium, Hard) and three bars per group (Short, Medium, Long). Y-axis: Agreement Rate (0% to 100%). Easy group: Short=69.5, Medium=71.1, Long=49.2. Medium group: Short=66.7, Medium=80.2, Long=66.7. Hard group: Short=68.0, Medium=76.0, Long=50.7. Three colors for Short/Medium/Long. Clean white background, sans-serif font.
Aspect Ratio: 16:9
Summary: Difficulty-stratified analysis showing self-check divergence across tiers
</figure_specification>


---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "VizExpectedFiles": {
      "description": "Expected output files from viz generation.",
      "properties": {
        "image_path": {
          "description": "Path to the generated figure image file. Example: 'fig1_v0.jpg'",
          "title": "Image Path",
          "type": "string"
        }
      },
      "required": [
        "image_path"
      ],
      "title": "VizExpectedFiles",
      "type": "object"
    }
  },
  "description": "Structured output from viz figure generation agent.",
  "properties": {
    "title": {
      "description": "Figure title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated figure: what it shows, style, any issues fixed",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/VizExpectedFiles",
      "description": "Output file you created. Must include the generated figure image path."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "VizFigureOutput",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [22] HUMAN-USER prompt · 2026-08-19 19:30:41 UTC

```
Can shorter chain-of-thought reduce contradiction in model self-checks?
```

### [23] THINKING · 2026-08-19 19:30:47 UTC

```
Let me start by reading the skill file and then creating the figure specification.
```

### [24] ASSISTANT · 2026-08-19 19:30:47 UTC

_(empty)_

### [25] TOOL CALL — file_editor · 2026-08-19 19:30:47 UTC

```
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
```

### [26] TOOL CALL — file_editor · 2026-08-19 19:30:47 UTC

```
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.claude/skills/aii-data-fig-gen/SKILL.md",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
```

### [27] TOOL RESULT — file_editor · 2026-08-19 19:30:47 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "Here's the files and directories up to 2 levels deep in /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5, excluding hidden items:\n/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/"}], "is_error": false, "command": "view", "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5", "prev_exist": true, "old_content": null, "new_content": null, "kind": "FileEditorObservation"}
```

### [28] TOOL RESULT — file_editor · 2026-08-19 19:30:47 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "Invalid `path` parameter: /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.claude/skills/aii-data-fig-gen/SKILL.md. The path /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.claude/skills/aii-data-fig-gen/SKILL.md does not exist. Please provide a valid path."}], "is_error": true, "command": "view", "path": null, "prev_exist": true, "old_content": null, "new_content": null, "kind": "FileEditorObservation"}
```

### [29] THINKING · 2026-08-19 19:30:53 UTC

```
The workspace is empty. Let me find the skill files first.
```

### [30] ASSISTANT · 2026-08-19 19:30:53 UTC

_(empty)_

### [31] TOOL CALL — invoke_skill · 2026-08-19 19:30:53 UTC

```
{
  "name": "aii-data-fig-gen"
}
```

### [32] TOOL CALL — task_tracker · 2026-08-19 19:30:53 UTC

```
{
  "command": "view",
  "task_list": []
}
```

### [33] TOOL RESULT — invoke_skill · 2026-08-19 19:30:53 UTC

````
{"content": [{"cache_prompt": false, "type": "text", "text": "# Data figures \u2014 charts rendered from their numbers\n\nDeterministic figures from a JSON spec: the numbers go in, matplotlib draws\nthem, and the picture cannot disagree with the data. Nothing is generated by\na model, so a bar is the height of its value and every axis is computed.\nRe-running a spec gives a byte-identical PNG; the PDF differs only in its\nembedded creation timestamp.\n\n## Data figure or concept figure?\n\n| The figure is\u2026 | Use |\n|---|---|\n| A chart of numbers you have | **this skill** (data figure) |\n| A confusion matrix, ablation grid, correlation | **this skill** (data figure) |\n| A scaling law, training curve, Pareto trade-off | **this skill** (data figure) |\n| Conceptual artwork, a metaphor, a cover image | `aii-concept-fig-gen` (concept figure) |\n| An architecture or flow diagram | `aii-concept-fig-gen` (concept figure \u2014 see *Limits*) |\n\nThe test is whether the figure has underlying numbers. If it does, an image\nmodel will approximate them \u2014 bars that do not match their labels, axis\nticks that do not divide evenly, invented data points. That failure is\ninvisible to a reviewer of the prompt and obvious to a reviewer of the\npaper.\n\n## Use a generator when one fits \u2014 hand-write only when none does\n\nThe generators are a menu, not a fence. Every type below is a shortcut that\nalready has the house style, the data-integrity guards and the layout fixes\nbaked in, so reaching for one is almost always less work than plotting by\nhand and the result is consistent with every other figure in the paper.\n\n**Check `--list-types` first.** If a type matches what you need, use it.\nTwo-thirds of research figures are a bar, a line, a scatter or a heatmap,\nand those are solved.\n\n**If nothing fits, write matplotlib yourself** \u2014 that is expected and\nsupported, not a failure. Novel or one-off figures exist. When you do:\n\n```python\nimport sys; sys.path.insert(0, \"<skill>/scripts\")\nimport matplotlib.pyplot as plt\nfrom chart_geometry import assert_text_is_legible, fit_point_labels\nfrom chart_style import (\n    apply_house_style, PALETTE, literal, place_legend, place_point_label,\n    fit_legends, clear_legends_of_data, fit_tick_labels, fit_titles,\n    rasterize_dense_clouds, assert_legends_clear_of_data,\n    assert_series_are_distinguishable, assert_axis_names_are_unique,\n)\n\napply_house_style()                 # fonts, palette, grid, Type-42 PDF fonts\nfig, ax = plt.subplots(figsize=(7, 3.94), layout=\"constrained\")\n...\nplace_legend(ax, loc=\"best\")        # a legend fit_legends can reflow\nplace_point_label(ax, literal(\"Ours\"), (1, 2))   # a name, nudged off the data\nfit_legends(fig)                    # reflow a legend wider than its axes\nclear_legends_of_data(fig)          # move it below the axes if it sits on data\nfit_tick_labels(fig)                # wrap/tilt tick labels that would collide\nfit_titles(fig)                     # wrap any title wider than its axes\nclear_legends_of_data(fig)          # AGAIN \u2014 the two above reshaped the axes\nfit_point_labels(fig)               # move point names off markers and curves\nrasterize_dense_clouds(fig)         # >25k points as a bitmap, text stays vector\nassert_text_is_legible(fig)         # raises if any text collides or is cut off\nassert_legends_clear_of_data(fig)   # raises if a legend still hides its data\nassert_series_are_distinguishable(fig)  # raises on two identical legend keys\nassert_axis_names_are_unique(fig)   # raises if one name labels two positions\nfig.savefig(\"figX_v0.pdf\")          # vector, so LaTeX renders text at page res\n```\n\nCall the fitters in that order \u2014 the legend decides how much room the axes\nhas, whether it then has to move out of the data is only knowable once it is\nplaced, tick labels change the axes height, the title is measured against the\naxes it ends up on, and a point's name can only be placed once nothing above\nit will move the point again. `clear_legends_of_data` appears TWICE on\npurpose: it decides by measuring, and the two passes between its calls shrink\nthe axes under a legend that is already placed and a fixed size. A wrapped\ntitle took a lone chart from 179 px of axes height to 141, and a legend that\ncovered nothing before covered half a curve after \u2014 with the mover's turn\nalready past, so the figure was refused rather than fixed. The first call\nstill has to happen first, because the room the legend needs is an input to\nthe passes below it. Two further gates are warning-based and so are\nnot in the snippet: `assert_layout_applied` and `assert_all_glyphs_rendered`\nread what matplotlib warned about during the draw, so they need the figure\nbuilt inside `warnings.catch_warnings(record=True)` \u2014 worth doing, since a\nmissing glyph is only ever a warning and ships as a hollow box.\n`place_legend` and `place_point_label` are how\nthe fitters find what to fix: a legend built with a bare `ax.legend` cannot\nbe reflowed, and a name written with a bare `ax.annotate` will not be moved\noff the marker it landed on.\n\nThat keeps a hand-written figure looking like the rest of the paper and\nstill gets you colourblind-safe colours, submission-compliant fonts, no\nclipped labels and no overprinted ones. What you lose is the data-integrity\nchecking \u2014 so verify the numbers yourself.\n\n**If you hand-write the same figure type twice, add a renderer instead.**\n`chart_renderers*.py` \u2014 one function, `(ax, spec) -> None`, registered in\nits family's dict. That is how this catalogue got here.\n\n## Use it\n\n```bash\nSKILL_DIR=\"$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-data-fig-gen\"\nG=\"$SKILL_DIR/scripts/chart_gen.py\"\n\npython \"$G\" --list-types            # the catalogue\npython \"$G\" --example bar           # a complete spec to copy and edit\npython \"$G\" --spec fig1.json --out figures/fig1\n```\n\n`python` here is the pipeline image's interpreter, which has matplotlib and\nscipy installed system-wide. Outside the image use the project venv \u2014\n`.venv/bin/python` \u2014 since a bare `python3` will not have them.\n\nWrites `figures/fig1.pdf` **and** `figures/fig1.png`. The PDF is the\ndeliverable \u2014 LaTeX renders vector text at page resolution, so it stays\nsharp and selectable at any zoom. The PNG exists so you can read the figure\nback and look at it.\n\n`--format pdf`, `--format png`, `--format pdf,png,svg` narrows the output.\nSVG keeps its labels as TEXT rather than paths, so it stays editable and\nsearchable. EPS is refused: the PostScript backend cannot draw transparency\nand flattens it silently, which the house style uses on nine of every ten\nfigures \u2014 the file would not match the PNG you checked.\n`--spec -` reads the spec from stdin.\n\nRuns on `matplotlib` + `numpy`, both already `aii_pipeline` dependencies \u2014\nnothing to install.\n\n## The catalogue\n\n`--example <type>` prints a complete spec for any of these. The \"instead of\"\ncolumn is the useful one: most figures have two plausible types and the\nchoice between them is what decides whether a reviewer reads the point.\n\n### Comparing categories\n\n| type | draws | choose it over |\n|---|---|---|\n| `bar` | Vertical bars, grouped or stacked, optional error bars. | The default. `barh` if names are long. |\n| `barh` | Horizontal bars \u2014 labels on the y-axis with room to run. | `bar`, whenever names exceed ~40 chars, or for a ranking. |\n| `lollipop` | A stem and a dot per category. | `barh`, past ~20 categories, where bars become a picket fence. |\n| `dumbbell` | Two markers per row joined by a line. | Paired bars, when the GAP between them is the story. |\n| `slope` | One line per item from a before value to an after value. | Paired bars, when which items changed RANK is the story. |\n| `bump` | Rank against time, one line per item; the crossings are the finding. | `slope`, which shows a reordering for exactly TWO time points and cannot show the path between more. |\n| `volcano` | Effect size against significance, with both thresholds drawn. | A `bar` of effects, which cannot show what survived correction, or a table of p-values, which cannot show what was big enough to matter. |\n| `diverging` | Signed bars either side of zero, sorted. | `bar`, for deltas \u2014 direction reads instantly. |\n| `waterfall` | Steps from a starting total to a final total. | `bar`, for an ablation \u2014 it shows contributions compounding. |\n| `bar_sig` | Grouped bars with significance brackets and stars. | `bar`, when the comparison being claimed is pairwise. |\n| `forest` | Point estimates with confidence intervals and a null line. | `bar`, when whether an interval crosses zero is the question. |\n| `radar` | A closed polygon per method over 3+ metrics. | Several bar charts, for a multi-metric profile at a glance. |\n| `parallel` | One polyline per configuration across independently scaled axes. | A table, for a hyperparameter sweep \u2014 trends across axes show up. |\n| `funnel` | Stage attrition with retention vs. previous and vs. intake. | `barh`, when the stages are sequential and losses compound. |\n| `stacked_pct` | Composition as percentages; every bar full height. | Stacked `bar`, when categories have very different totals. |\n| `treemap` | Nested rectangles with AREA proportional to value. | `bar`, only when there are too many parts for one axis \u2014 length beats area for precise reading. |\n| `upset` | Set intersections as sorted bars over a membership matrix. | A Venn diagram, past 3 sets \u2014 circles cannot stay area-true and stop reading as sets. |\n\n### Trends and relationships\n\n| type | draws | choose it over |\n|---|---|---|\n| `line` | Multi-series lines with optional uncertainty bands. | The default for anything against time or steps. |\n| `fan` | A median with nested quantile bands around it. | `line` with a band, when the spread is skewed or bounded \u2014 a symmetric \u00b1 band on an accuracy near its ceiling implies scores above 100%. |\n| `step` | A piecewise-constant series \u2014 value holds, then jumps. | `line`, for schedules \u2014 a slope implies values that never occurred. |\n| `scatter` | Points with an optional least-squares fit and R\u00b2. | `line`, when x is not ordered and the relationship is the point. |\n| `joint` | Scatter with the marginal distribution of each variable beside it. | `scatter`, when \"and how is each one distributed?\" is the obvious next question \u2014 which for a headline correlation it always is. |\n| `splom` | Every pair of variables as its own scatter, distributions down the diagonal. | `corr`, when the SHAPE of each relationship is the claim \u2014 one number cannot tell a straight line from two clusters or an outlier. |\n| `bubble` | Scatter with a third variable as marker AREA, plus a size key. | `scatter`, when a third quantity matters but not enough for its own axis. |\n| `scaling` | Log-log points with a fitted power law and its exponent. | `line`, for scaling laws \u2014 the exponent is computed and annotated. |\n| `speedup` | Measured speedup against worker count, with the ideal line. | `line`, for parallel results \u2014 the ideal reference is what the claim is measured against. |\n| `pareto` | Scatter with the non-dominated frontier drawn through it. | `scatter`, for trade-offs where the frontier is the finding. |\n| `area` | Stacked areas \u2014 a total and how it divides. | `line`, when the total matters as much as the parts. |\n| `residual` | Residuals against fitted values, with the zero line. | Predicted-vs-actual, where heteroscedasticity hides on the diagonal. |\n| `bland_altman` | Difference between two methods against their mean, with limits of agreement. | A scatter of A against B, where the diagonal reads as agreement and r = 0.99 hides a 10% offset. |\n| `acf` | Autocorrelation per lag as stems, with the significance band. | `line`, which shows the level and hides whether each point predicts the next. |\n| `sankey` | Flows between stages at proportional widths. | `area`, when what matters is what became what. |\n| `timeline` | Gantt-style spans, one row per task. | A table of timestamps, when overlap and duration are the point. |\n\n### Model evaluation\n\nGive these raw `labels` and `scores` rather than a precomputed curve wherever\nyou can: the renderer sweeps the threshold itself, so the AUC or AP in the\nlegend is integrated from the points actually drawn and cannot drift from\nthe curve beside it.\n\nWhen only the curve survives \u2014 it came from a paper, or from a logged\nartefact \u2014 pass it directly instead: `fpr`/`tpr` for `roc`, `recall`/\n`precision` for `pr`, `probabilities`/`labels` for `calibration`. The\nsummary statistic is still integrated from the plotted points, so a PR curve\nthat stops short reports `AP = 0.375 up to recall 0.60` rather than quietly\nextrapolating the rest. One evaluation set per figure: `pr`'s baseline and\n`calibration`'s bins both move with class balance, so curves from different\ntest sets cannot share axes honestly.\n\n| type | draws | choose it over |\n|---|---|---|\n| `roc` | ROC curves with AUC in the legend, plus the chance diagonal. | `pr`, when the classes are roughly balanced. |\n| `pr` | Precision-recall curves with average precision and the prevalence baseline. | `roc`, when positives are rare \u2014 ROC flatters a rare-class model. |\n| `calibration` | Reliability diagram with the ideal diagonal, ECE, and per-bin counts. | `roc`/`pr`, when whether to TRUST a probability is the question. |\n| `learning_curve` | Score against training-set size, train and validation with \u00b1std bands. | `line`, to show whether more data or a better model is the bottleneck. |\n| `qq` | Sample quantiles against theoretical normal quantiles, with a reference line. | `hist`, for judging normality \u2014 the eye reads a straight line far better than a bell. |\n| `cd_diagram` | Mean ranks over many datasets, joining methods a test cannot separate. | `bar_sig`, which compares pairwise on ONE dataset \u2014 this is the many-datasets headline figure. |\n\n### Distributions\n\n| type | draws | choose it over |\n|---|---|---|\n| `box` | Median, quartiles, whiskers, outliers per group. | The compact default for a few groups. |\n| `violin` | Full mirrored density per group. | `box`, when a distribution may be multi-modal \u2014 a box hides that. |\n| `strip` | Every raw observation, jittered, with the mean marked. | `box`, when n is small enough that each point should be visible. |\n| `beeswarm` | Every observation, packed sideways so none hides another. | `strip`, whose random jitter still overlaps at any real n \u2014 the eye reads the clumps as density and they are partly collision. |\n| `ridgeline` | Stacked density curves, one row per group. | `violin`, past ~6 groups, where a violin grid gets too wide. |\n| `raincloud` | Half violin, box and jittered points together, with n. | `violin`, when the reader must see the observations \u2014 twelve seeds look as smooth as twelve thousand. |\n| `hist` | Binned counts or density. | `ecdf`, only when the shape of ONE distribution is the point. |\n| `ecdf` | Empirical cumulative distribution, stepped. | `hist`, for comparing distributions \u2014 no bin width to argue about. |\n| `survival` | Kaplan-Meier curves with censoring ticks and confidence bands. | `ecdf`, when some subjects have not finished \u2014 an ECDF must drop or invent those. |\n| `hexbin` | Hexagonal density bins with a colourbar. | `scatter`, past ~2000 points where it becomes a solid blob. |\n| `hist2d` | A joint distribution as a rectangular binned grid. | `hexbin`, when the axes are naturally rectangular. |\n\n### Matrices and fields\n\n| type | draws | choose it over |\n|---|---|---|\n| `heatmap` | Annotated matrix with a colourbar. | A table, when the pattern matters more than the digits. |\n| `seqheat` | A per-token quantity drawn on the tokens themselves. | `heatmap`, for anything measured per token \u2014 it puts indices on an axis and leaves the reader rebuilding the sentence from a legend. |\n| `corr` | Correlation matrix, diverging map centred at zero. | `heatmap`, for correlations \u2014 sign reads from colour direction. |\n| `contour` | Filled contours of a 2-D field, levels labelled. | `heatmap`, for a smooth field like a loss surface. |\n| `clustermap` | Heatmap with rows and columns reordered into their clusters, trees drawn beside. | `heatmap`, whenever the row order is arbitrary \u2014 block structure that is obvious once reordered is invisible in the order the log happened to emit. |\n| `catmap` | A grid whose cells hold a CATEGORY, with a discrete legend and no scale. | `heatmap`, for any nominal cell \u2014 expert IDs, pass/fail/timeout, which variant won. A ramp asserts that expert 4 is more than expert 1 and that 2 lies between them, and a reader takes the ordering as real. |\n| `quiver` | A field of arrows: where each sample is, and where it went. | A `scatter` of the before and after positions, which carries the same numbers and leaves the reader pairing points up by eye. |\n\n### Structure\n\n| type | draws | choose it over |\n|---|---|---|\n| `dendrogram` | Hierarchical clustering as a tree, branch heights the real merge distances. | `corr`, which shows every pairwise relationship and no grouping. |\n| `tree` | A rooted tree from a parent/child structure you already have. | `dendrogram`, which computes its own linkage from a matrix and cannot be given a tree \u2014 and `network`, whose force layout loses depth. |\n| `network` | A graph as nodes and links, node area and edge width from the data. | A concept figure, for anything with REAL edges \u2014 an image model draws a plausible graph, not yours. Use `sankey` for flows between ordered stages and `heatmap` for a dense graph. |\n\n### Composites\n\n| type | draws | choose it over |\n|---|---|---|\n| `panel` | Any of the above in a lettered grid, `(a)`\u2013`(p)`. | Several separate figures, when they are read together. |\n\n## Spec shape\n\n```json\n{\n  \"type\": \"bar\",\n  \"title\": \"Accuracy by benchmark\",\n  \"xlabel\": \"Benchmark\",\n  \"ylabel\": \"Accuracy (%)\",\n  \"aspect\": \"16:9\",\n  \"categories\": [\"ARC\", \"GSM8K\", \"HumanEval\"],\n  \"series\": [\n    {\"label\": \"Baseline\", \"values\": [41.2, 55.8, 33.1], \"errors\": [1.8, 2.4, 2.9]},\n    {\"label\": \"Ours\",     \"values\": [48.9, 67.3, 45.6], \"errors\": [1.5, 2.0, 2.6]}\n  ]\n}\n```\n\nKeys every type takes: `title`, `aspect` (`\"W:H\"`), `width_in` (default 7.0\n\u2014 a full text-width figure), `font_pt`, `font_family`.\n\nKeys that depend on what the type actually draws. Passing one to a type that\nnever reads it is REFUSED by name \u2014 *\"nothing read this key\"* \u2014 rather than\ndropped quietly, so a figure never comes back missing what the spec asked\nfor. \"Applies to\" below is therefore the set that is accepted, not a hint:\n\n| key | applies to |\n|---|---|\n| `xlabel`, `ylabel` | every type with axes, which is all of them but `panel` \u2014 a panel has none of its own, so put the labels on the sub-specs and a label at panel level is refused. `radar`, `treemap`, `sankey`, `parallel` and `upset` do read the key, but draw their own geometry with the axis turned off, so the label is accepted and never painted. |\n| `xlim`, `ylim` | every type \u2014 the shared layer applies them whatever the geometry, so these two are never refused as unread. Limits that would crop data are refused rather than applied. |\n| `legend_loc` | only the types that actually draw a legend, i.e. two or more named series. A one-series chart gets none, because a one-entry legend restates the y-label \u2014 and asking to place a legend that is not drawn is refused. Takes matplotlib's in-axes placements (`best`, `upper right`, `lower left`, \u2026) and NOT `outside \u2026`: that is what the layout pass itself uses when it moves a legend off the data, and matplotlib accepts it only on a figure legend. You do not need to ask for it \u2014 the move happens on its own. |\n| `cmap` | only the eight types that encode a value as colour \u2014 `heatmap`, `clustermap`, `corr`, `hist2d`, `hexbin`, `contour`, `quiver`, `seqheat`. Anywhere else it is refused: a bar chart given a colour map is a spec expecting colour to carry a meaning that chart never encodes. The default is already perceptually uniform (`cividis`, or `RdBu_r` where the scale has a meaningful zero), so reach for this only with a reason. Rainbow and cyclic maps are refused: `jet` puts a bright band in the middle of a run that is monotonic in the data, and a reader takes the band for a boundary in the result. |\n\n`font_family` REPLACES the font, it does not add a fallback. matplotlib uses\nthe first family it can find and only that one, so the font you name has to\ncover everything on the figure \u2014 the script AND the Latin labels, digits and\naxis numbers around it. Needed only for a script the default cannot draw \u2014\nCJK, Devanagari, Thai \u2014 and picking a script-only face (e.g. \"Noto Sans Thai\",\nwhich has no Latin) trades one set of hollow boxes for another. Measured: with\nthat font the missing-glyph gate refuses again, naming `l`, `p` and the\ndigits. See *Legibility*.\n\nPer-type keys are documented by `--example <type>`; start from the example\nrather than the schema.\n\n### Multi-panel\n\n```json\n{\"type\": \"panel\", \"title\": \"Overview\", \"ncols\": 2, \"panels\": [\n  {\"type\": \"bar\", \"categories\": [\"A\", \"B\"], \"series\": [{\"values\": [3, 5]}]},\n  {\"type\": \"line\", \"series\": [{\"values\": [1, 2, 4, 8]}]}\n]}\n```\n\nAny chart type nests inside `panels`. Sub-panels are lettered `(a)`, `(b)`\u2026\nautomatically \u2014 do not put the letter in the panel's own `title`, which is\nhow panel labels end up collided with their titles.\n\n`ncols` and `aspect` both default from the panel count: the grid is squared\n(capped at three columns, which is the most that fits at the 7-inch text\nwidth) and the canvas is sized so each cell is about 4:3. Pinning `ncols: 4`\nis allowed but leaves each cell 1.75 inches wide, which is narrower than a\nlabelled chart needs \u2014 it will be refused rather than drawn on top of\nitself.\n\n## How long text may be\n\nHard caps, checked before anything is drawn, so an over-long string is a\nmessage rather than a figure with its labels cut off. Each was set by\ngrowing that slot until the figure broke, then backing off:\n\n| key | max | what happened past it |\n|---|---|---|\n| `title` | 120 | Never refused, never collided \u2014 it just ate the canvas. At 600 characters the chart was 38% of its own figure. |\n| `xlabel`, `ylabel`, `cbar_label` | 80 | Silently CLIPPED. An x-label ran off both edges from ~90 characters, a y-label from ~50, cut mid-word, at exit 0. |\n| `series[].label` | 60 | Legend entries collided at 80 and collapsed the layout at 100. |\n| `categories[]`, any other text | 80 | Under a *vertical* bar the limit is 40, with a pointer to `barh` \u2014 see *Legibility*. |\n\nA title is a heading; an axis label is a quantity and its unit. Detail\nbelongs in the caption, which has the full column width and as many lines as\nit needs.\n\nThese are coarse budgets that cannot know the figure's real width \u2014 a\n3.5-inch column fits about half as much \u2014 so the drawn result is measured\ntoo, and anything that still does not fit is refused with the same kind of\nmessage.\n\n## It refuses rather than lying\n\nThe generator exits non-zero, writing nothing, when the figure would not\nmatch its data or a reader would not be able to read it. These were live\ndefects, each of which exited 0 and produced a confident, plausible, wrong\npicture:\n\n- **Length mismatches.** Five categories against three values used to render\n  three bars and silently drop two categories. Ragged series were zero-filled,\n  inventing measurements nobody made.\n- **NaN / Infinity / null / strings in values.** matplotlib draws NaN as\n  *nothing*, so the gap reads as a measured zero.\n- **Right-to-left text.** matplotlib does no bidi reordering and no Arabic\n  joining, so Hebrew and Arabic draw left to right in isolated forms \u2014\n  reversed and unjoined. Every glyph exists, so the missing-glyph gate above\n  sees nothing; the reader who can read the script is the first to know.\n- **Glyphs the font cannot draw.** A missing glyph renders as a hollow box\n  and matplotlib only warns. It is machine-dependent too: CJK looks right on\n  a laptop with a CJK font and ships as boxes from the pipeline image.\n- **Labels printed over each other.** Measured on the drawn figure, on the\n  ORIENTED box of each label so a tilted tick is judged on its ink rather\n  than on the much larger box around it. A 7x7 correlation matrix forced to\n  `21:9` rendered its cells as `0.290.360.581.00`.\n- **Labels running off the canvas.** A 300-character x-label was drawn with\n  30% of itself visible, cut mid-word at both ends, with no warning.\n- **A legend sitting on the data it explains.** The legend is opaque by\n  design, so whatever is under it is gone rather than faint. A lone chart's\n  legend is measured after layout and moved below the axes; a panel cell has\n  nowhere to move it and is refused. A `timeline` in a two-column grid drew\n  its legend over eight of its nine bars, and the `bar` cell beside it had\n  its bar TOPS masked \u2014 GSM8K reading as ~40 where the spec said 55.8.\n- **Keys nothing reads.** `x_label`/`y_label` instead of `xlabel`/`ylabel` is\n  a natural guess; it used to be accepted in silence and the figure came back\n  with no axis labels at all \u2014 failing the first item on your own checklist,\n  visibly only if you look closely. Every key is now checked against what the\n  render actually looked up, at every level, so a typo inside a series or a\n  panel is caught too, and the message suggests the real spelling.\n- **A series drawn without a name while its neighbours have one.** The\n  legend names only the series that carry a `label`, so the rest are drawn\n  and left unidentified \u2014 three series with two labelled shows blue, amber\n  and green bars and names two colours. Nothing about the picture looks\n  wrong, which is what makes it worth refusing. Naming none of them is fine:\n  that is a chart with one meaning, and the y-label carries it.\n- **A stated limit that crops the data.** `xlim`/`ylim` outside the values,\n  `vmin`/`vmax` outside the matrix, or an explicit `levels` list narrower than\n  `z`. Each one hides part of the finding while the axis or colourbar states a\n  range the data does not have: `vmax: 0.3` on a matrix running 0.10..0.95\n  painted 0.30 and 0.95 the identical yellow under a bar labelled\n  0.100..0.300, and `levels: [2.6..3.2]` over a field of 2.3..4.6 left 70% of\n  the plot area as bare page \u2014 the basin holding the optimum included, drawn\n  exactly like no-data. Cropping is a legitimate wish; it just has to be a\n  stated one, so widen the limit or drop it and let the axis fit.\n- **Non-positive values on a log axis.** matplotlib MASKS them rather than\n  complaining, so the figure comes back with fewer points than the data. Five\n  points drawn trending up carried a fit annotation reading `y = -1.75x +\n  53.2`, because the slope was still computed over the two at `x = 0` that the\n  reader cannot see. Applies wherever `logx`/`logy` does \u2014 `line`, `scaling`,\n  `scatter`, `pareto`.\n- **A negative band in a stacked chart.** Bands and segments are drawn end to\n  end, so a negative one folds back over the one beneath it and every height\n  stops matching its value: 10 / -8 / 5 drew as three bands of 10 / 8 / 5,\n  with a top edge of 10 where the total is 7. Use `line` with one line per\n  part for signed quantities. Same for stacked `bar` and `stacked_pct`.\n- **Tied scores in a `bump` chart.** It has one row per rank, so a tie can\n  only be broken by the order the series happen to appear in \u2014 two models\n  level at 80.0 drew as a permanent one-rank gap, and moving them past each\n  other in the spec, numbers unchanged, showed a crossing that is not in the\n  data. Crossings are what this chart type is read for. Use `line`, or\n  `slope` for two periods, which draw the scores themselves.\n- **Two series a reader cannot tell apart.** The palette holds eight colours\n  and wraps; the dash pattern is a second channel and multiplies that to 32\n  for line charts, but a solid shape has no dash. A twelve-series `bar`\n  shipped four PAIRS of identical swatches and a fifty-series `line` wrapped\n  both channels at series 32. Measured on the drawn legend, so it holds for\n  bars, lines and markers alike \u2014 and `bubble`'s size key, whose entries\n  share a colour on purpose, is judged on size as well and passes.\n\nErrors name the offending key and index (`series[1].values has 2 entries but\n5 were expected`), so a bad spec is one edit from correct. Nothing partial is\never written \u2014 a half-file would pass the downstream existence check.\n\n## Legibility\n\n- **Non-Latin scripts.** The default font covers Latin, Greek and Cyrillic \u2014\n  all three verified, not assumed. Hebrew and Arabic are refused even though\n  the glyphs are there: matplotlib does no bidi reordering and no Arabic\n  joining, so it draws the characters left to right in isolated forms and the\n  label comes out reversed and unjoined, with every glyph present and nothing\n  else noticing. Transliterate, or write the label in the paper's own script.\n  For any other script set\n  `font_family` (e.g. `\"Noto Sans CJK JP\"`) \u2014 matplotlib uses the *first*\n  resolvable family and does no per-glyph fallback, so the covering font has\n  to go first. Without it the figure is refused rather than shipped full of\n  boxes.\n\n  **`font_family` only helps where that font is installed, and the pipeline\n  image has none.** It ships 23 families, not one of which covers CJK, Indic\n  or Thai \u2014 so inside the image the escape hatch resolves to nothing and the\n  figure is refused either way. The refusal now names the FONT rather than\n  the script: a name that does not resolve is caught before anything is\n  drawn, with the closest installed families listed, because matplotlib\n  otherwise falls back in silence and the glyph gate then blames the text.\n  Label it in Latin script, or add the font to\n  `Dockerfile.pipeline` (Noto Sans CJK is ~20 MB). On a developer machine\n  with the font present it works: verified rendering a Japanese title and\n  Japanese category labels with no missing glyph.\n- **Dense categories.** Labels wrap when long, tilt at 30\u00b0 when that isn't\n  enough, and stand up at 90\u00b0 when even that collides \u2014 where neighbours\n  cannot touch however long they get. Which of the three applies is decided\n  by MEASURING the drawn labels against the axes after layout, so a panel\n  cell gets the treatment its own width needs rather than the one the whole\n  figure's width would suggest. Names past ~40 characters do not fit under a\n  vertical bar at all and are refused with a pointer to `barh`, which puts\n  the label on the y-axis where the full width is available.\n- **Column-width figures.** `width_in: 3.5` works for the ordinary types \u2014\n  bar, barh, line, scatter, box, hist, ecdf, heatmap \u2014 provided the spec is\n  written for that size: about four categories, two or three series, and a\n  title under ~45 characters. These of the catalogue's own examples are\n  refused at 3.5 inches, because each is written for the full text width \u2014\n  the list is pinned by a test that measures it, so it cannot go stale:\n\n  > `bar_sig`, `bland_altman`, `bubble`, `bump`, `catmap`, `cd_diagram`,\n  > `clustermap`, `contour`, `corr`, `dendrogram`, `dumbbell`, `fan`,\n  > `funnel`, `panel`, `parallel`, `radar`, `sankey`, `seqheat`, `slope`,\n  > `speedup`, `survival`, `timeline`, `treemap`, `upset`, `volcano`\n\n  A leaner spec fits for every one of them \u2014 measured, including the\n  label-dense ones (`corr`, `upset`, `sankey`, `treemap`, `parallel`,\n  `radar`, `cd_diagram`), which only refuse above a lower ceiling than the\n  ordinary types. Three one-letter categories draw at 3.5 inches; `upset`\n  is the tightest, taking two sets before its own \"Intersection size\" axis\n  label runs off the edge. What the list above says is that the SHIPPED\n  EXAMPLES do not fit, because each is written for the full text width.\n  Every refusal names what is in the way, and `upset` and `cd_diagram`\n  quantify it (\"the method names need 4.2 inches of margin\") rather than\n  shipping something unreadable.\n- **Many series.** Past eight the palette wraps, so the line style becomes a\n  second channel \u2014 otherwise series 1 and 9 were the same colour. Past six,\n  the legend moves below the axes. Inside, it\n  covered the data at twelve series and hid a tick label; outside, layout\n  reserves real space for it.\n- **Long titles** are measured after layout and wrapped. On a chart whose\n  axes is a narrow strip (a `barh` with long names) the title is promoted to\n  a figure heading, since an axes title would centre on the strip and run\n  off the page.\n- **`$` is safe.** A matched pair used to be read as mathtext, so\n  \"Cost $5 to $9\" rendered as \"Cost 5to9\". All user text is now escaped, so\n  dollars print verbatim. The trade: mathtext is unavailable \u2014 write\n  superscripts in Unicode (`R\u00b2`, `10\u207b\u00b3`), which the fits already do.\n\n## What the house style already handles\n\nDo not re-solve these; they are set globally in `chart_style.py`.\n\n- **Colourblind-safe palette** (seaborn's `colorblind` set). Never override\n  it with a red/green pair. The separations are measured, not assumed: the\n  closest pair is \u0394E*ab 14.0 under protanopia and 10.3 under deuteranopia,\n  against a just-noticeable difference of ~1. **Greyscale print separates\n  the first three series and no more** \u2014 past that the lightnesses cluster,\n  and violet against grey is \u0394L* 0.3, the same shade in print. If the paper\n  will be read in B&W, keep it to three series or give the extras a second\n  channel of your own.\n- **Sans-serif**, sized for the figure's final print size.\n- **No chartjunk** \u2014 no 3D, gradients, shadows, coloured plot background;\n  faint horizontal grid behind the data only.\n- **Constrained layout**, so an axis label can never be clipped off the\n  canvas. This was the single most common defect across every library\n  surveyed, including in otherwise flawless output. Layout alone does not\n  cover TITLES \u2014 it reflows axes but cannot wrap a line \u2014 so titles wider\n  than their axes are measured after layout and wrapped.\n- **TrueType (Type 42) fonts, never Type 3.** matplotlib emits Type 3 by\n  default and **IEEE and ACM submission systems reject PDFs containing\n  it**, so every default matplotlib figure is non-compliant.\n- **Legend headroom** \u2014 the y-range is widened before an inside legend is\n  placed, because `loc=\"best\"` lands on the data when nothing is free. Where\n  headroom cannot help \u2014 a horizontal chart, whose free space is on the\n  x-axis, or a plot area that is full by construction \u2014 the placed legend is\n  MEASURED against the drawn bars and moved below the axes if it covers any.\n- **Very dense point clouds are drawn as a bitmap inside the vector file.**\n  A scatter writes every marker as its own path \u2014 360,000 points is a 5.7 MB\n  PDF, and six of those do not fit a venue's upload limit. Past ~25,000\n  points in one series the cloud alone is rasterized; the axes, ticks,\n  labels and legend stay vector, so the text is still selectable and sharp\n  at any zoom. Below that threshold the bitmap would be the *larger* of the\n  two, so nothing changes.\n- **Cell annotations are outlined against their own fill.** A heatmap's\n  numbers take near-black or near-white, whichever contrasts better with the\n  cell \u2014 and over a continuous colour map the better one is not always\n  enough: cividis bottoms out at 4.18:1 and RdBu_r at 4.19:1, against the\n  4.5:1 the rest of the style holds itself to, in exactly the mid-range cells\n  that make up most of a matrix. A hairline in the opposite ink fixes that\n  without touching the map, which is the part that cannot change.\n- **Sub-decade log axes keep their tick labels.** A log axis spanning less\n  than one decade \u2014 a loss curve from 2.90 to 2.05, say \u2014 contains no power\n  of ten. matplotlib ticks only at powers of ten, so it places 10\u2070 and 10\u00b9,\n  *both outside the view*, and the visible axis carries no label at all.\n  Silently. Handled.\n\n## Verify what you generated\n\nRead the PNG back and look at it. The generator prevents the structural\ndefects above, but it cannot know that your data was wrong. Check:\n\n- every number in the figure matches the number you meant to plot;\n- axis labels state units;\n- the caption describes what is actually drawn;\n- the chart type still says what you meant once you can see it.\n\nTwo things that used to be on this list are now refused instead, so a figure\nyou can read back cannot have them: overlapping category labels, and a\nseries drawn without a name while its neighbours have one.\n\nIf a figure is crowded, widen `aspect` (`\"21:9\"`) or split it into a\n`panel` \u2014 do not shrink the font.\n\n## Limits\n\n- **Hand-drawn architecture diagrams** (a pipeline, a block diagram, a\n  flowchart with prose in the boxes) are out of scope: they have no\n  underlying numbers and a layout engine has nothing to compute from. Those\n  go to `aii-concept-fig-gen`. A graph whose edges ARE data \u2014 citations,\n  message counts, co-occurrence \u2014 is a `network` here, because the picture\n  has to match the edge list.\n- **No LaTeX-native output.** PGFPlots produces the best camera-ready\n  result of anything surveyed, because the figure text is typeset by the\n  paper's own engine in the paper's own font. What is missing is a second\n  backend behind 60 renderers, not the toolchain: `texlive-pictures` is\n  already in the pipeline image, pulled in as a dependency of\n  `texlive-latex-extra`, and a pgfplots document compiles there at exit 0.\n  (This entry used to say the package was absent and would cost +81 MB.\n  Measured in the built image, both halves were wrong.)\n- **The legibility gate reads TEXT.** It refuses a label printed over another\n  label or cut off by the canvas. A label printed over the DATA is only\n  handled where a renderer registers it with `place_point_label`, which five\n  types do: `pareto`, `network`, `tree`, `volcano` and `bubble`. If you\n  hand-write a figure, call `fit_point_labels` too.\n  `bubble` registers only the names it draws OUTSIDE their disc \u2014 a name\n  small enough to sit inside its own bubble is already where it belongs and\n  no nudge improves it. That registration became worth doing once the\n  clearance test started measuring each marker against ITS OWN radius: with\n  a single radius for the axes (the largest drawn) a bubble field running\n  4 px to 88 px left no candidate position measuring clean, so every name\n  stayed on its first guess.\n  One limit remains, and it is the candidate SET rather than the model: the\n  nudger tries corners a few pixels out, which cannot clear a very large\n  neighbouring disc. On a crowded bubble chart a small bubble's name can\n  still touch a big one \u2014 give those names in a legend, or space the points.\n- Still uncovered: geographic/choropleth (needs a basemap and boundary data,\n  neither of which is in the image). Add a renderer to its family's\n  `chart_renderers*.py` rather than hand-writing matplotlib at the call site\n  \u2014 that is what keeps every figure in a paper looking like a set.\n\n---\nThis skill is located at `/ai-inventor/.claude/skills/aii-data-fig-gen`. Any files it references (e.g. under `scripts/`, `references/`, `assets/`) are relative to that directory."}], "is_error": false, "skill_name": "aii-data-fig-gen", "kind": "InvokeSkillObservation"}
````

### [34] TOOL RESULT — task_tracker · 2026-08-19 19:30:53 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "No task list found. Use the \"plan\" command to create one."}], "is_error": false, "command": "view", "task_list": [], "kind": "TaskTrackerObservation"}
```

### [35] THINKING · 2026-08-19 19:30:57 UTC

```
Let me now get the example spec for a bar chart and create the figure.
```

### [36] ASSISTANT · 2026-08-19 19:30:57 UTC

_(empty)_

### [37] TOOL CALL — terminal · 2026-08-19 19:30:57 UTC

```
{
  "command": "python .claude/skills/aii-data-fig-gen/scripts/chart_gen.py --example bar",
  "is_input": false,
  "timeout": null,
  "reset": false
}
```

### [38] TOOL CALL — task_tracker · 2026-08-19 19:30:57 UTC

```
{
  "command": "plan",
  "task_list": [
    {
      "title": "Create fig5_spec.json and render grouped bar chart",
      "notes": "Create grouped bar chart spec and render Fig 5",
      "status": "in_progress"
    },
    {
      "title": "Verify rendered figure against checklist",
      "notes": "Verify every number, axis labels, units, and chart readability",
      "status": "todo"
    },
    {
      "title": "Write structured output JSON",
      "notes": "Write final output JSON to .sdk_openhands_agent_struct_out.json",
      "status": "todo"
    }
  ]
}
```

### [39] TOOL RESULT — terminal · 2026-08-19 19:30:57 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "python: can't open file '/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py': [Errno 2] No such file or directory"}], "is_error": false, "command": "python .claude/skills/aii-data-fig-gen/scripts/chart_gen.py --example bar", "exit_code": 2, "timeout": false, "metadata": {"exit_code": 2, "pid": -1, "username": "root", "hostname": "c3a494f84ff3", "working_dir": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5", "py_interpreter_path": "/usr/local/bin/python", "prefix": "", "suffix": "\n[The command completed with exit code 2.]"}, "full_output_save_dir": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/.oh_sessions/6684e880be7d4110a271de38651f8afa/observations", "kind": "TerminalObservation"}
```

### [40] TOOL RESULT — task_tracker · 2026-08-19 19:30:57 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "Task list has been updated with 3 item(s)."}], "is_error": false, "command": "plan", "task_list": [{"title": "Create fig5_spec.json and render grouped bar chart", "notes": "Create grouped bar chart spec and render Fig 5", "status": "in_progress"}, {"title": "Verify rendered figure against checklist", "notes": "Verify every number, axis labels, units, and chart readability", "status": "todo"}, {"title": "Write structured output JSON", "notes": "Write final output JSON to .sdk_openhands_agent_struct_out.json", "status": "todo"}], "kind": "TaskTrackerObservation"}
```

### [41] THINKING · 2026-08-19 19:31:01 UTC

```
The skill is at `/ai-inventor/.claude/skills/aii-data-fig-gen` according to the SKILL.md. Let me find the correct path.
```

### [42] ASSISTANT · 2026-08-19 19:31:01 UTC

_(empty)_

### [43] TOOL CALL — terminal · 2026-08-19 19:31:01 UTC

```
{
  "command": "python /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py --example bar",
  "is_input": false,
  "timeout": null,
  "reset": false
}
```

### [44] TOOL RESULT — terminal · 2026-08-19 19:31:01 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "{\n  \"type\": \"bar\",\n  \"title\": \"Accuracy by benchmark\",\n  \"xlabel\": \"Benchmark\",\n  \"ylabel\": \"Accuracy (%)\",\n  \"aspect\": \"16:9\",\n  \"categories\": [\n    \"ARC\",\n    \"GSM8K\",\n    \"HumanEval\",\n    \"MMLU\"\n  ],\n  \"series\": [\n    {\n      \"label\": \"Baseline\",\n      \"values\": [\n        41.2,\n        55.8,\n        33.1,\n        62.4\n      ],\n      \"errors\": [\n        1.8,\n        2.4,\n        2.9,\n        1.1\n      ]\n    },\n    {\n      \"label\": \"Ours\",\n      \"values\": [\n        48.9,\n        67.3,\n        45.6,\n        68.1\n      ],\n      \"errors\": [\n        1.5,\n        2.0,\n        2.6,\n        1.0\n      ]\n    }\n  ]\n}"}], "is_error": false, "command": "python /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py --example bar", "exit_code": 0, "timeout": false, "metadata": {"exit_code": 0, "pid": -1, "username": "root", "hostname": "c3a494f84ff3", "working_dir": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5", "py_interpreter_path": "/usr/local/bin/python", "prefix": "", "suffix": "\n[The command completed with exit code 0.]"}, "full_output_save_dir": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/.oh_sessions/6684e880be7d4110a271de38651f8afa/observations", "kind": "TerminalObservation"}
```

### [45] THINKING · 2026-08-19 19:31:05 UTC

```
Now I have the example spec. Let me create the spec for Figure 5 - a grouped bar chart with:
- Categories: Easy, Medium, Hard
- Series: Short, Medium, Long (three CoT lengths)
- Values as specified

Let me create the spec file and render it.
```

### [46] ASSISTANT · 2026-08-19 19:31:05 UTC

_(empty)_

### [47] TOOL CALL — file_editor · 2026-08-19 19:31:05 UTC

```
{
  "command": "create",
  "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/fig5_spec.json",
  "file_text": "{\n  \"type\": \"bar\",\n  \"title\": \"Agreement by Difficulty and CoT Length\",\n  \"xlabel\": \"Difficulty Tier\",\n  \"ylabel\": \"Agreement Rate (%)\",\n  \"aspect\": \"16:9\",\n  \"categories\": [\"Easy\", \"Medium\", \"Hard\"],\n  \"series\": [\n    {\n      \"label\": \"Short\",\n      \"values\": [69.5, 66.7, 68.0]\n    },\n    {\n      \"label\": \"Medium\",\n      \"values\": [71.1, 80.2, 76.0]\n    },\n    {\n      \"label\": \"Long\",\n      \"values\": [49.2, 66.7, 50.7]\n    }\n  ]\n}\n",
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
```

### [48] TOOL CALL — terminal · 2026-08-19 19:31:05 UTC

```
{
  "command": "python /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py --spec fig5_spec.json --out fig5_v0",
  "is_input": false,
  "timeout": null,
  "reset": false
}
```

### [49] TOOL RESULT — file_editor · 2026-08-19 19:31:07 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "File created successfully at: /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/fig5_spec.json"}], "is_error": false, "command": "create", "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/fig5_spec.json", "prev_exist": false, "old_content": null, "new_content": "{\n  \"type\": \"bar\",\n  \"title\": \"Agreement by Difficulty and CoT Length\",\n  \"xlabel\": \"Difficulty Tier\",\n  \"ylabel\": \"Agreement Rate (%)\",\n  \"aspect\": \"16:9\",\n  \"categories\": [\"Easy\", \"Medium\", \"Hard\"],\n  \"series\": [\n    {\n      \"label\": \"Short\",\n      \"values\": [69.5, 66.7, 68.0]\n    },\n    {\n      \"label\": \"Medium\",\n      \"values\": [71.1, 80.2, 76.0]\n    },\n    {\n      \"label\": \"Long\",\n      \"values\": [49.2, 66.7, 50.7]\n    }\n  ]\n}\n", "kind": "FileEditorObservation"}
```

### [50] TOOL RESULT — terminal · 2026-08-19 19:31:08 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "{\"ok\": true, \"written\": [\"fig5_v0.pdf\", \"fig5_v0.png\"]}"}], "is_error": false, "command": "python /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py --spec fig5_spec.json --out fig5_v0", "exit_code": 0, "timeout": false, "metadata": {"exit_code": 0, "pid": -1, "username": "root", "hostname": "c3a494f84ff3", "working_dir": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5", "py_interpreter_path": "/usr/local/bin/python", "prefix": "", "suffix": "\n[The command completed with exit code 0.]"}, "full_output_save_dir": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/.oh_sessions/6684e880be7d4110a271de38651f8afa/observations", "kind": "TerminalObservation"}
```

### [51] THINKING · 2026-08-19 19:31:14 UTC

```
The figure has been rendered successfully. Now I need to verify it against the checklist. Let me view the PNG to check:
1. Every number matches the specification
2. Axis labels have units
3. Axis ranges are readable
4. Chart type still makes the point
5. Caption describes what is drawn

Let me view the generated PNG.
```

### [52] ASSISTANT · 2026-08-19 19:31:14 UTC

_(empty)_

### [53] TOOL CALL — file_editor · 2026-08-19 19:31:14 UTC

```
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/fig5_v0.png",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
```

### [54] TOOL CALL — task_tracker · 2026-08-19 19:31:16 UTC

```
{
  "command": "view",
  "task_list": []
}
```

### [55] TOOL RESULT — file_editor · 2026-08-19 19:31:16 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "Image file /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/fig5_v0.png read successfully. Displaying image content."}, {"cache_prompt": false, "type": "image", "image_urls": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABXgAAAMTCAYAAAAb6H+UAAAAOnRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjExLjEsIGh0dHBzOi8vbWF0cGxvdGxpYi5vcmcvctoD+AAAAAlwSFlzAAAewgAAHsIBbtB1PgAAvipJREFUeJzs3Xd4FGX7//3PJiEJJCRAQkIJvYRepCsd6VIUFKQqKILi/VUR+y3eeBcFRFQUEQEBFZAiiIAgVToovUovoaQAAUJCSDLPHzyZX5bspk4IG96v48jBtTvXXHPOZnaWnHvNOTbDMAwBAAAAAAAAAFyOW24HAAAAAAAAAADIGhK8AAAAAAAAAOCiSPACAAAAAAAAgIsiwQsAAAAAAAAALooELwAAAAAAAAC4KBK8AAAAAAAAAOCiSPACAAAAAAAAgIsiwQsAAAAAAAAALooELwAAAAAAAAC4KBK8AAAAAAAAAOCiPHI7AAAAAPw/YWFhunLliiSpVKlS8vf3z+WI7m/h4eEKDw+XJBUvXlwBAQEZWi8yMlKXL19WfHy8JKlw4cIqWbKkw77Xr19XRESEbt68KUny9fVV2bJlJUnHjx9XbGysJKlixYry9vbOzu7cc1l9/XDvnDt3TlevXpUklS5dWn5+frkbEGChuLg4HTt2TJJUoEABlS9fPpcjAgDXZDMMw8jtIAAASE9ERIQuXbpkPi5Xrpx8fHxyMSIgZzzzzDOaMWOGJGnWrFnq169fLkeUdVeuXFFYWJjDZR4eHvLz85Ofn598fX2zvI333ntP//nPfyRJY8eO1euvv+60b0xMjP79739r1qxZqeIaOHCgvvvuO/NxYmKixo8fr2nTpunw4cN2fdu0aaNVq1ZJkurXr6+//vpLkrRr1y7VqVMny/uSGzLz+iF39OvXTz/88IMkad68eerZs2eObu/atWuKjIyUYRjy9/dXkSJF5OZ2by78PH36tK5fv27ZeGl9ceNMyvOWp6enKleubFk8SO3PP/9UgwYNJEmNGjXS1q1bczkiAHBNzOAFALiEgQMHavny5ebj0aNH65///GcuRoQH2cWLFxUZGSlJKlGihIoUKZLLEd2fFixYoOeffz7dfp6enqpevboeeughNW3aVD179sxW0teRmzdvqlmzZtq1a1e6fZOSktS1a1ctW7bM0hhcFcd73nbhwgXNmDFDq1at0ubNm80Z6cl8fHxUq1YttW7dWr169VLNmjVzLJYXXnhBK1assGy8u7+4yYiU560yZcro1KlTlsWT18XHx+vvv/+WJHl5ealSpUq5HBEAPDiowQsAuO+dP39eK1eutHvuu+++ExehILd89NFHqlmzpmrWrKkff/wxt8NxefHx8dq1a5emTp2qZ599VsWLF9fQoUMVFRVl2Ta++OILu+Sut7e3KlSooOrVq6t69eoKCQkxl82bN88uuevp6aly5cqZfcuVK2dZXK6A4z1vunHjhl555RWVL19eb7/9tlavXp0quSvdmfm+ZcsW/ec//1GtWrXUpk0b/fnnn7kQMe53Z86cMc8VXbp0ye1wAOCBwgxeAMB977vvvlNiYqLdcydOnNC6devUqlWrXIoKQGbky5cv1aXOMTExio6O1tWrV+2+sLlx44YmT56sRYsWafr06erYsaPTcYODg1W9enVJUmBgoNN+8+fPN9svvfSSxo0b57Rebsq+Tz75pL799lundU8rVqyouLg4SVL+/Pmdbh+4n5w8eVJdu3bV/v37Uy3z8fFRQECAvLy8FB0drcuXLyshIcFcvmbNGk2cODHTM2MzomzZsub72ZG4uDgdP37cfBwaGioPD+d/0qb84gYAgLyMBC8A4L6X8o/IgQMHmvVJp02bRoIXcBElSpRwmEyS7tzEbOfOnVq+fLmmTZumiIgISdKlS5fUvXt3rVixQi1btnS47ssvv6yXX3453e0fOHDAbI8ePTrNm6Gl7Pvee++leVOrOXPmpLtt4H4SHh6uZs2a2dWhDgkJ0auvvqqOHTuqatWqdv1v3bqlvXv3at26dZo9e3aGypxk1ddff53m8t27d6tu3brm43Xr1qlYsWI5Fg8AAK6CEg0AgPvahg0bdPToUUlS9erV9cknn8jT01PSnTp5165dy83wAFigYMGCatGihT766COdOXNGw4cPN5fFx8friSeesLvJYmbdvn3bvPQ8f/786daQjY6ONtvMAERekpSUpF69etkld1944QUdP35cr732WqrkrnSnlmqDBg00cuRI7dy5U+vWrVPDhg3vZdgAACAdzOAFANzXpk2bZrafeeYZBQQE6LHHHtPChQsVGxurOXPmaMiQIVka2zAMhYeH6/r16woODlbBggXtlh85ckS3b9+WJFWrVs3hXcRT9qlSpYrdpaIJ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czVq1EhXrlxReHi4mjdvrnbt2qlr166qXr26/P39dfPmTV24cEFbt27VkiVLdOTIkXs2Xm5zhf1JOTtwzpw5Cg0NVcuWLeXn52d+kVC0aFFzZnlWubu76+TJk6pdu7aGDx+uNm3aqFChQjp//rwWL16s6dOnm7P7ChcubJdUcKZAgQIaOHCgPv/8c0VHR5uXSZcoUUJdu3bNVrxpuX37dqrkYGxsrKKjo3XmzBn9+eef+u2331IlhapUqaKff/5Z7u7uORZbTvv888/VsGFD3bhxQzdu3FDXrl3Vtm1b9ezZU9WqVZOPj4/Cw8N14cIF7dixQ7/++quGDRumt956y26cXr166a233lJSUpIuXLig+vXr6/XXX1ejRo3k6empM2fOaOnSpZo5c6bi4+Pt6q1mR3aP93t1zD366KMaN26cJOmXX35R48aN9dxzz6lKlSry9fXVxYsX9ccff2jatGkKDw+37PXJDJvNpo8//lg9e/aUdOcLx2rVqun//u//1LRpU/n6+urMmTOaN2+eZs+eLcMwLI/z/fff1/79+82rXY4fP67WrVurQYMG6tSpk+rXr6/AwEB5eXkpOjpaYWFh2rVrl9auXaudO3dKkllLOeV+jRs3To899pgkmeetYcOGqW3btgoICFBERISWL1+uyZMnKzY2VtKdz9nk39n9yNF5Ky0BAQEqXry4OnfurN69e5tfXI8bN04//fST+vbtq8aNG6t48eJyd3dXVFSU9u3bp7Vr1+q3335TQkKCevXqlVO7Y2fo0KH68ssvdfr0acXHx+uxxx5T37591aNHD5UqVUoxMTHasmWLvvjiC507dy5Dx6G3t7eqVq2qAwcOKDExUb169dLLL7+sUqVKycPjTurB3d1dVatWvRe7CAAPFgMAgPtA69atDUmGJKNv375ZGqNGjRrmGO+++26q5VevXjVq1qxp9knr57XXXjOCg4PNxzExMQ63WbJkSbPPhQsXMhzrhg0bjMDAwAzFkvJn+/btOT7ewIEDzeWzZs1Kd198fHzM/rGxsWn2/f33382+7du3vyevT2b358MPPzT7f/jhhw77JCQkGCEhIWnG8uabb6a7LUdSxvvuu+8aBQsWTHe/PTw8jMWLF2d4G4cOHUo1xqhRo7IUb1qmTJmS6d9hyp9+/foZV65cSXMb7777rtl/7NixDvvExsaafXx8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f0nSrVu3FBsba5fwutvly5czvA1HksuOJCUlpdnv7lmQQGYkn1sNw9DVq1ft3id3Sz4fp1zPSsnvrxs3bighISHNZHFGPj9yEwleAAAAAECuSXlZeU5cgm2z2VS5cmUdPnxYf/31V5p94+Pjzcvoq1atankscC1PP/20XnvtNTOh2bBhQ6e1Yh1J2ffXX3816ztnRsrjcNeuXXr44Yed9t25c2emx08p+YaI6SWKDx06lK3t4MFWpUoVs/3nn3+qbdu2TvumPGfnxDk5OZbExETt379fderUcdp3z549lm/fStxkDQAAAABgqeTZjhmRMllUpkyZnAjHvIHV8ePH9ccffzjt99NPP+nGjRuSMndJvSMpL6lP6+7vuH8VLFhQw4cPV+3atVW7dm394x//yNT6HTt2NC9BnzVrVpZiePTRR83jaObMmU77nThxQhs2bMjSNpIlf9myb98+p5fDX7x4UatWrcrWdvBgS3lunT59utN+MTExmjt3riSpYsWKKleunOWxtGnTxmz/8MMPTvudOHHC7oZs9yMSvAAAAAAAS/Xv31+vvfaazp49m2a/Xbt2afz48ZLuXB6e3h3Vs2r48OHKly+fJGnIkCHmTddSOnnypEaOHCnpzmW7mbkU3xE3NzcFBQVJko4dO5atsZB7PvroI+3evVu7d+9W3759M7VusWLF9NJLL0mSPvzwQ/3222/prpOy/q5058ZOHTt2lCR9++23DpOrcXFxGjRoULo1etOTnOy6efOmvvzyy1TLb926pWeeeUYJCQnZ2g4ebFWrVlWHDh0kSbNnz9a8efNS9TEMQ8OHD1d4eLgkacSIETkSS82aNdW8eXNJ0hdffOEwiXvr1i0999xz2X5/5TRKNAAAAAAALBUbG6tPP/1Un332mVq1aqU2bdqodu3aKlq0qBISEnTq1CmtWLFCP/74ozm79Z133smxu5RXrFhRH330kUaMGKEjR46oTp06ev3119WwYUMlJiZqw4YN+uSTT3T58mXZbDZNnTrVknqPLVq00E8//aRFixbp008/VZMmTcwb9fj7++fIjDTcX/73v/9p586dWr9+vTp27KjOnTure/fuCg0NVf78+RUVFaVLly7p2LFj+v3337Vv3z5zFnmyiRMnqm7duoqOjlbnzp314osv6rHHHpOvr68OHDig8ePH6+zZsxoyZIgmTZqU5Vgff/xxVahQQcePH9ebb76p8+fPq1u3bvLy8tK+ffv02Wef6cqVK3rhhRf01VdfZfelQR5x8+ZN7d69O91+fn5+Kl++vCRp8uTJqlevniIjI9W7d2+tXLlSPXr0UJEiRXT8+HFNmjTJnJHevn17DRkyJMfinzRpkho0aKCbN2+qTZs2evnll9W+fXv5+PjowIEDmjBhgs6dO6dBgwZpypQpORZHdpHgBQAAAABYKjAwUNKdmzWtXr1aq1evdtrX399fo0ePzvTl75n12muvycvLS2+88YbCwsL06quvpupTpEgRTZkyRU888YQl23z//fe1YsUKRUdH67XXXrNb1q1bNy1atMiS7eD+5eXlpRUrVuitt97Sl19+qaVLl2rp0qVO+6e8wVqycuXKafXq1erevbvOnTunCRMmaMKECebyQoUK6eeff9b27duzHeu8efPUoUMHhYeH69NPP9Wnn35qLi9TpoyWL1+uhQsXZms7yFv27dununXrptuvffv25iz20qVLa9OmTerZs6f27dunb7/9Vt9++61df5vNpv79+2vy5Mlyc8u5AgTVqlXT8uXL9eSTTyo8PFxjxozRmDFjzOUBAQFavHixfv/9d0mSh4dHmjdjyy33X0QAAAAAAJf23XffaezYsdq6dau2bdums2fPKiIiQpGRkXJ3d5e/v78qV66shx9+2JyJ6IiHh4dq164tSWa5A2cqVaqkGzduqGLFik77vPTSS+rZs6d++OEHbdiwQRcvXpSbm5tCQkLUsmVL9e3bV35+ftmOJVn16tV14MABTZs2Tdu3b1d4eLji4+NlGAazd+8TRYsWNX+vzo7DtAQFBaW7vpeXlz799FONHDlS8+fP1+bNm3X+/HnFxcUpMDBQQUFBCg0N1aOPPqp69eo5HKNevXo6dOiQvvvuO/3++++6ePGiAgIC1LhxYz3//PMqXry4Tp8+bcbi7u6eaoySJUuqdu3a8vLycro/devW1eHDh/X111/rjz/+UFRUlIKDg9W6dWsNGjRI/v7+2rx5s7kdR5etlylTRrVr11ZwcHCar13FihUVGRmp0NDQNPslL0+e/Yn7Q506dTJVruPuKzQqV66s3bt365dfftGyZct09OhRxcTEqEiRInrooYf01FNPpXnTs3Llyql27doqXbp0mtstUqSIebwmX0Fxt+bNm+vvv//W1KlTtWbNGkVERCgwMFCPPPKInnvuOQUFBZmlJPz9/TO8z/eSzTAMI7eDQMZdunRJnTt3liQtXbo03RMmAAAAAAAAgKxr1aqV1q1bpyZNmmjz5s25HU4q3GQNAAAAAAAAABw4ffq0WRO4adOmuRyNYyR4AQAAAAAAADyQbt686XTZ9evX1b9/fyUmJspms2nQoEH3MLKMowYvAAAAAAAAgAdS8+bNVbZsWbVu3VqlS5dWcHCwrl+/ru3bt2vSpEk6c+aMpDs366xSpUouR+sYCV4AAAAAAAAADyQPDw8tWLBACxYscLjc3d1dr776qj7++ON7HFnGkeAFAAAAAAAA8ED6448/tGzZMq1bt05nzpzRpUuXlJSUpKCgIDVs2FC9e/dWhQoVcjvMNJHgBQAAAAAAAPBA8vT0VPfu3dW9e/fcDiXLuMkaAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAi/LI7QDupYiICM2bN09btmzRuXPnFBcXp4IFC6py5cpq3bq1HnvsMXl6emZorL/++ktz5szRwYMHFR0draCgID388MPq06ePSpQokcN7AgAAAAAAAACSzTAMI7eDuBe++OILvf3224qJiXHap0KFCvr+++/VuHFjp31u376tl156SVOmTHG43NfXV1988YWeeeaZ7Ibs0KVLl9S5c2dJ0tKlSxUcHJwj2wEAAAAAAABw/3sgSjR88803+sc//qGYmBj5+vrq9ddf188//6wNGzboxx9/VLdu3SRJx48f16OPPqqjR486HevZZ581k7utW7fWvHnztGHDBk2aNEnlypXTjRs3NGjQIM2ePfue7BsAAAAAAACAB1een8GblJSkkiVL6uLFi/Ly8tKmTZtUr169VP2++OIL/eMf/5AkDRo0SFOnTk3VZ8mSJerataskqU+fPvr+++9ls9nM5VFRUWrQoIFOnjypwoUL6/jx4ypcuLCl+8MMXgAAAAAAAADJ8vwM3rNnz+rixYuSpFatWjlM7krSiy++qIIFC0qSduzY4bDPf/7zH0mSj4+PJk6caJfclaSAgACNGzdOknTlyhV99dVXluwDAAAAAAAAADiS5xO8BQoUMNsBAQFO+7m7u5sJ3pTrJDtz5oy2bdsmSerevbvTmbndunUzt/PTTz9lOW4AAAAAAAAASE+eT/AWLVpUVapUkSRt3LhRsbGxDvsdOHBA58+flyS1aNEi1fKNGzeabUfLk7m7u6tZs2aSpL179+ratWtZjh0AAAAAAAAA0pLnE7yS9OWXX8rLy0unT5/WU089pRMnTtgt//333/X4449LkipWrKh33nkn1RgHDhww26GhoWluL+XygwcPZid0AAAAAAAAAHDKI7cDuBdat26tTZs26c0339SyZcu0dOlSFStWTEWKFNG5c+cUHR0tX19fDR48WGPHjpW/v3+qMZJn90pSiRIl0txeyZIlHa6XEefOnUtzeWRkZKbGAwAAeFCdnOCZ2yHAgXKvxOd2CAAAAHnKA5HglaTy5curffv2Onr0qM6cOaMLFy7owoUL5vI6deqoTZs2KlSokMP1b9y4YbZ9fHzS3FbKGr4p18uIUqVKpbk8X758qlWrliTp0qVLSkxMzNT4AAAAQG7K7AQIAACAB016k0vv9kAkeA8dOqQuXbro+PHj8vPz01tvvaWWLVvKz89P58+f18KFCzV79mxt3LhRP/30k77//vtUSdyEhASz7e7unub2PDz+38t6+/Zta3cGAAAAAAAAAP5/eT7Be/PmTXXs2FGnT59WQECANm/erMqVK9v16dGjhzp16qR+/fpp0aJFevnllzVt2jS7PikTvs5u1JZym8l8fX0zFe/Zs2fTXB4ZGannnntOkhQcHKzg4OBMjQ8AAPCgOJnbAcChzM5IAQAAQNry/E3W5s2bp9OnT0uS3nnnnVTJ3WR9+/bVo48+KkmaOXOmXfkGSSpcuLDZvnz5cprbTLk85XoZERISkuZP8eLFMzUeAAAAAAAAgLwrzyd4t23bZrZbt26dZt/k5YmJifrzzz/tloWGhprtkyfTng+ScnnK9QAAAAAAAADASnk+wRsf///u0pvy5meOpFx+69Ytu2V169Y12ymTxo5s3bpVklSkSBGVLl06w7ECAAAAAAAAQGbk+QRvyhpfhw8fTrPvoUOHHK4nSU2aNDHr3S5evNjpGH///bcOHjwoSeratatsNlumYwYAAAAAAACAjMjzCd42bdqY7U8//VRJSUkO+4WFhWn27NmSJD8/P9WvX99uuZubmwYPHixJOnLkiNn3bh988IEMw5AkDRkyJNvxAwAAAAAAAIAzeT7B26JFCzVt2lSStG7dOj311FPmTdeS/fHHH2rdurWuXbsmSXrjjTfk6emZaqw333xTJUuWlHQnefvTTz+ZydyYmBi9+eabZuL36aefVpMmTXJsvwAAAAAAAADAZiRnKPOwixcvqm3bttq/f7/5XNmyZeXv76+wsDBFRkaazw8YMEDTp0+Xm5vj3PfevXvVpk0bc52iRYsqKChIp06dUkxMjCSpadOmWrFiRbo1f7Pi0qVL6ty5syRp6dKlZtkIAAAA2Ds5IfUX9sh95V6JT78TAAAAMizPz+CVpGLFiunPP//UuHHjVKNGDdlsNp06dUp79uxRZGSkvLy81KZNG/3888+aMWOG0+SuJNWqVUv79+/X888/r0KFCikiIkIHDhxQTEyMKlSooDFjxmjt2rU5ktwFAAAAAAAAgJQeiBm8d7t+/brOnz+vuLg4FSxYUKVKlVK+fPkyPU5CQoLOnz+v6OhoBQUF3ZPZtMzgBQAAyBhm8N6fmMELAABgLY/cDiA3FCxYUKGhodkex8PDQ6VLl7YgIgAAAAAAAADIvAeiRAMAAAAAAAAA5EUkeAEAAAAAAADARZHgBQAAAAAAAAAXRYIXAAAAAAAAAFwUCV4AAAAAAAAAcFEkeAEAAAAAAADARZHgBQAAAAAAAAAXRYIXAAAAAAAAAFwUCV4AAAAAAAAAcFEkeAEAAAAAAADARZHgBQAAAAAAAAAXRYIXAAAAAAAAAFwUCV4AAAAAAAAAcFEeuR0AAAAAAABAXnNygmduhwAHyr0Sn9shAJZjBi8AAAAAAAAAuCgSvAAAAAAAAADgokjwAgAAAAAAAICLIsELAAAAAAAAAC6KBC8AAAAAAAAAuCgSvAAAAAAAAADgokjwAgAAAAAAAICLIsELAAAAAAAAAC6KBC8AAAAAAAAAuCgSvAAAAAAAAADgojxyauDo6GidPHlS58+f140bN2Sz2eTr66sSJUqoXLly8vPzy6lNAwAAAAAAAMADwbIEb0xMjJYtW6bly5dr48aNOnbsmAzDcNjXZrOpUqVKeuSRR9SxY0d16tRJPj4+VoUCAAAAAAAAAA+EbCd4d+zYoYkTJ2rBggWKiYnJ0DqGYejvv//W33//renTp8vHx0dPPPGEhg8froYNG2Y3JAAAAAAAAAB4IGQ5wbt+/Xq9//77+uOPP1Its9lsqlChgooWLaqAgAAFBAQoKSlJly9f1uXLlxUeHq4TJ06YM3xjYmI0a9YszZo1S82aNdOHH36oFi1aZH2vAAAAAAAAAOABkOkE79GjR/XKK69o2bJl5nPu7u5q2rSpHn30UTVu3FgNGjSQv79/muNER0dr+/bt2rp1q1atWqWNGzcqKSlJGzZsUMuWLdWpUydNmDBBlSpVyvxeAQAAAAAAAMADwGY4K5TrhJeXl+Lj4yVJoaGhev7559W/f38FBQVlK5Dw8HDNmjVL3377rQ4fPixJ8vT01K1bt7I1bl5z6dIlde7cWZK0dOlSBQcH53JEAAAA96eTEzxzOwQ4UO6V+NwOAQDuCT6H7k98DiEvcsvsCvHx8WrQoIEWLVqkQ4cOacSIEdlO7kpSUFCQRowYoYMHD2rRokVq0KCBmUgGAAAAAAAAAKSW6RIN8+fPV48ePXIiFkl36vd269ZN3bp10/z583NsOwAAAAAAAADg6jI9gzcnk7t369mz5z3bFgAAAAAAAAC4mkwneAEAAAAAAAAA9wcSvAAAAAAAAADgojJdgzerkpKStHLlSq1fv15hYWEyDEMhISFq2bKl2rZtKzc3cs0AAAAAAAAAkBn3JMG7d+9e9enTRwcOHEi17KOPPlKNGjU0Z84cVa9e/V6EAwAAAAAAAAB5Qo4neM+cOaPWrVsrKipKklSkSBGVLl1aNptNp0+f1uXLl7V//361atVKO3fuVEhISE6HBAAAAAAAAAB5Qo7XRfjwww8VFRWlkJAQLV68WBEREdq1a5d27typiIgILV68WCEhIYqIiNCHH36Y0+EAAAAAAAAAQJ6R4zN4f/vtN0nS999/rxYtWtgtc3NzU9euXeXv76+WLVtq2bJlOR0OAAAAAAAAAOQZWZrBO3DgQEVERGSo76VLlyRJTZo0cdqncePGkqTw8PCshAMAAAAAAAAAD6QsJXhnzpyp0NBQffPNNzIMI82+RYoUkSTt27fPaZ/kZcl9AQAAAAAAAADpy1KCt1GjRrpy5YpeeOEFPfLII9qzZ4/Tvq1bt5YkDRgwQDt37ky1fOfOnRo4cKBdXwAAAAAAAABA+rKU4N28ebMmTZqkQoUKacuWLapXr55ee+013bhxI1Xf9957T/nz59fBgwdVr1491axZU926dVPXrl1Vs2ZN1atXTwcPHlSBAgX03nvvZXuHAAAAAAAAAOBBYTPSq7GQhvDwcI0YMULff/+9JCkkJEQTJkxQjx497PqtXr1affr0cVpjNzg4WLNnz1arVq2yGsoD49KlS+rcubMkaenSpQoODs7liADHTk7wzO0Q4ES5V+JzOwQAuCf4LLo/8TkE4EHB59D9ic8h5EUe2Vk5KChIs2bN0qBBg/Tiiy/q8OHD6tmzpzp16qSJEyeqXLlykqQ2bdro2LFjmj17ttavX6+wsDBJUsmSJdWyZUs9/fTT8vX1zf7eAAAAAAAAAMADJFsJ3mStWrXSnj17NHbsWP3nP//RsmXLVL16db377rsaOXKkPD09VbBgQQ0ZMkRDhgyxYpMAAAAAAAAA8MDLUg1eRzw9PfXuu+9q//796tixo2JjY/Xee++pdu3aWrt2rVWbAQAAAAAAAAD8/yxL8CYrX768li1bpvnz5yskJESHDx9W69atNWDAAKc1eAEAAAAAAAAAmWd5gjdZjx49dOjQIb366qtyd3fXrFmzFBoaqq+//lpJSUk5tVkAAAAAAAAAeGBYluC9efOmYmJi7J7z9fXV+PHj9ddff6lx48a6evWqhg0bpocffli7d++2atMAAAAAAAAA8EDKVoJ33bp16t69uwoXLiwfHx/5+vqqUKFC6t69u9atW2f2q127tjZv3qzJkyercOHC2rZtm+rXr69XX31V169fz+4+AAAAAAAAAMADKcsJ3lGjRqlVq1ZavHixrl69aj4fHR2txYsXq1WrVho1apT5vM1m05AhQ3TkyBENGDBAiYmJmjBhgqpUqaJ58+ZlaycAAAAAAAAA4EGUpQTv4sWLNXr0aElSyZIl9cYbb+jrr7/W5MmT9dZbb6lUqVKSpNGjR2vRokV26xYtWlQzZszQunXrVLVqVZ0/f15PPfWUOnbsqOPHj2dvbwAAAAAAAADgAeKRlZUmTJggSerdu7dmzpypfPny2S3/8MMPNXDgQP3444/6/PPP1b1791RjtGjRQnv27NG4ceP04Ycf6rffflONGjUUGxublZCQR7m9viS3Q4ATSeO65HYIAAAAAAAAD7wszeDduXOnJGncuHGpkruS5OHhoTFjxtj1dSRfvnx6++23dfDgQXXu3FlxcXFZCQcAAAAAAAAAHkhZmsEbHx8vSSpUqJDTPsnLbt26le54ZcuW1a+//qqFCxdmJRwAAAAAAAAAeCBlaQZvhQoVJEkzZsxw2mfmzJl2fTPiiSeeyEo4AAAAAAAAAPBAylKCt2/fvpKkf/zjHxoyZIg2bdqkCxcu6Pz589q8ebOGDRuml19+WZLUp08f66IFAAAAAAAAAJiyVKLh1Vdf1a+//qrNmzdrypQpmjJlisN+jRs31quvvpqtAAEAAAAAAAAAjmVpBq+3t7dWrVqlESNGyNfXN9VyHx8fvfLKK1q1apXy58+f7SABAAAAAAAAAKllaQavJOXPn1/jxo3Thx9+qD///FNhYWGSpJIlS6pevXoqUKCAZUECAAAAAAAAAFLLcoI3Wf78+dWsWTMrYgEAAAAAAAAAZEKWSjQAAAAAAAAAAHJftmfwAgAAAAAA67m9viS3Q4ATSeO65HYIAGDK9AzeNWvW5EQcub4tAAAAAAAAAHA1mU7wtmnTRh06dNCmTZtyIh5J0oYNG9S+fXu1adMmx7YBAAAAAAAAAK4u0wleNzc3rVixQk2bNtXDDz+smTNnKjY2NtuB3Lx5U999950aN26s5s2ba+XKlXJzo0QwAAAAAAAAADiT6Qzq9u3b1bhxY0nSli1bNHDgQBUtWlRPPvmkJk+erF27dikhISHdcW7fvq2dO3fq66+/Vo8ePVS0aFE9++yz2rZtmySpSZMm2rFjR2bDAwAAAAAAAIAHRqZvslavXj1t3rxZCxcu1AcffKD9+/crJiZG8+fP1/z58yVJ+fPnV40aNRQUFKQiRYqoSJEiMgxDV65c0eXLlxUeHq59+/YpLi4u1fg1a9bUv/71Lz3++OPZ3zsAAAAAAAAAyMMyneCVJJvNph49euiJJ57Q8uXL9cUXX+j3339XYmKiJCk2NjZTs289PDzUoUMHDR8+XO3bt89KSAAAAAAAAADwwMlSgjeZzWZTp06d1KlTJ128eFE///yzfvvtN23evFmRkZFprhscHKxHHnlEHTp0UPfu3VW0aNHshAIAAAAAAAAAD5xsJXhTKlasmIYNG6Zhw4ZJks6dO6fjx4/rwoULiomJkST5+vqqRIkSqlChgkqUKGHVpgEAAHKE2+tLcjsEOJE0rktuh4Ac5D799dwOAU4kPjsut0MAAAB3sSzBe7eQkBCFhITk1PAAAAAAAAAA8MBzy+0AAAAAAAAAAABZQ4IXAAAAAAAAAFwUCV4AAAAAAAAAcFEkeAEAAAAAAADARZHgBQAAAAAAAAAXRYIXAAAAAAAAAFwUCV4AAAAAAAAAcFEkeAEAAAAAAADARZHgBQAAAAAAAAAXRYIXAAAAAAAAAFwUCV4AAAAAAAAAcFEkeAEAAAAAAADARXnk9AZiY2O1d+9eRUREKCYmRoZhqHfv3jm9WQAAAAAAAADI83Iswbt27VqNGTNGq1ev1u3bt+2WJSd4X3/9dR07dkySNH78eJUvXz6nwgEAAAAAAACAPMfyBK9hGHr11Vf12Wefpdu3efPm+uSTTyRJ+fLl07x586wOBwAAAAAAAADyLMtr8I4cOdIuuduqVSv961//cti3a9euqlq1qiRpwYIFOnHihNXhAAAAAAAAAECeZWmCd/fu3Ro/fvydgd3c9OOPP2rNmjV6//33na7zzDPPSLoz83fWrFlWhgMAAAAAAAAAeZqlCd5JkybJMAxJ0rBhw/T000+nu06rVq3M9po1a6wMBwAAAAAAAADyNEsTvOvWrTPbgwYNytA6KW+sdvjwYSvDAQAAAAAAAIA8zdIEb1hYmNlOrq2bHn9/f7N95coVK8MBAAAAAAAAgDzN0gRvYmKi2XZ3d7dbZrPZHK4TExNjtgsWLGhlOAAAAAAAAACQp1ma4C1atKjZPnfuXIbWOX78uNkuVqyYleEAAAAAAAAAQJ5maYL3oYceMturVq2yW+ZsBu/q1avN9sMPP2xlOAAAAAAAAACQp1ma4O3WrZvZHjdunGJjY9PsHxsbq4kTJ5qPu3fvbmU4AAAAAAAAAJCnWZrg7du3r8qWLStJOnr0qLp06aILFy447Hvjxg317t1bZ86ckSTVqVNHnTp1sjIcAAAAAAAAAMjTLE3wenp66scff5SXl5ekO+UXypYtq3bt2skwDLPfM888o7Jly+qXX36RJBUoUEDff/+90zIOAAAAAAAAAIDULE3wSlKTJk20dOlSBQYGSpLi4+P1+++/2yV4Z8yYoaioKElSYGCgfvvtN1WvXt3qUAAAAAAAAAAgT7M8wStJbdq00YEDBzRy5EgFBQU57FOoUCG9/PLL2rdvn5o1a5YTYQAAAAAAAABAnuaRUwMHBQVpzJgx+vjjj3Xo0CGdOnVKV69elY+Pj0JCQlSnTh25u7vn1OYBAAAAAAAAIM/LsQRvMpvNpmrVqqlatWo5vSkAAAAAAAAAeKBYmuCdP3++2e7Zs2eOrwcAAAAAAAAADzJLE7xPPvmk2U55U7WcWi+rYmNjtWrVKm3fvl2XLl1SgQIFVLp0aTVr1kwNGjTI0BhRUVFatGiRDh48qOjoaAUFBenhhx9Wu3bt5OnpmcN7AAAAAAAAAAD3oETD/SQxMVFffvmlRo0apatXrzrsU758ea1bt06lSpVyOs748eP13nvvKTY2NtWycuXKafr06WrRooVVYQMAAAAAAACAQ7me4E05Y9dms+XYdm7fvq0+ffqY5SAqVKigJ554QhUqVJCbm5tOnz6tNWvWaMuWLYqOjnaa4H3//ff14YcfSpIqVqyogQMHqlixYtq/f7+mT5+ukydPqn379lq5cqWaN2+eY/sDAAAAAAAAALme4E05k9bX1zfHtvPKK6+Yyd1//vOfev/99+XhkXr3T506pSJFijgcY9u2bWZyt2XLllq6dKkKFChgLh86dKgeeeQRXb58Wf3799eRI0fk7e2dA3sDAAAAAAAAAJJbbgewbNkys12mTJkc2cYff/yhr776StKdJOzo0aMdJnclqWzZsvLz83O4bNSoUZIkDw8PzZgxwy65K0lVqlTRRx99JEk6c+aMvv32W6t2AQAAAAAAAABSyfIM3qFDh2ZreUJCgs6cOaN169aZz7Vs2TKr4aRpzJgxkiRvb2/997//zdIYkZGRWrVqlSSpU6dOKl26tMN+/fr102uvvaYbN25ozpw5Gj58eNaCBgAAAAAAAIB0ZDnBO3ny5Gwtv1vBggX1yiuvZDUcp6KiorR8+XJJUpcuXVS4cOEsjbN+/XolJiZKktq0aeO0X/78+fXII49oxYoV2rJli2JjY5U/f/4sbRMAAAAAAAAA0pLrNXi9vb3Vrl07/fvf/1aFChUsH3/Lli1KSkqSJDVr1kySdPjwYS1atEgnT56Um5ubSpcurTZt2qhhw4ZOx9m/f7/Zrl69eprbrF69ulasWKGkpCQdOnRIDz30kAV7AgAAAAAAAAD2spzg3bFjR6rnGjRokObylPLlyyc/Pz+VLl1a7u7uWQ0jXSkTs2XLltXgwYM1bdo0h32bNm2qmTNnqly5cqmWnT171myHhISkuc1SpUqZ7TNnzmQqwXvu3Lk0l0dGRmZ4LAAAAAAAAAB5W5YTvPXr18/W8nvl8uXLZvvNN9/UoUOHVLx4cQ0cOFCVKlXSlStXtGTJEq1fv14bN25U48aNtWPHjlQ1dq9fv262fX1909ymj4+P2b5x40am4k2ZHHYkX758qlWrliTp0qVLZtkI4F47f/58boeALOJ3ByAv4FzmuvjduTZ+f8AdvBdcF787uIISJUpkqr+lJRrWrl1r5XCWuHnzptk+dOiQGjVqpBUrVsjf3998fsSIEfroo4/09ttvKzw8XEOHDtWyZcvsxrl165bZzpcvX5rb9PLyMttxcXHZ3QUAAAAAAAAAcMjSBG/Lli2tHM4SKWfT2mw2zZgxwy65m+ytt97S0qVLtXHjRi1fvlzHjx+3qwlcoEABs50y2etIbGysw+1nRMpSEI5ERkbqueeekyQFBwcrODg4U+O7nr9yOwA4kd63SSfvURzIvMx+Ewg82Pgcul9l5FzGZ9H9ic8h18bv717jc+h+xeeQ6+I8hrwo12+yltNSJnNr166t0NBQp3179eqljRs3SpI2btxol+BNOc7Vq1fTLKVw9epVh+tlRHr1fdObPQwAAAAAAADgwXFPErw3btzQtWvXlJSUlG7f9BKcmVW5cmWz7ejmaSmlXH7x4kW7ZZUqVTLbp0+fVs2aNZ2Oc/r0aYfrAQAAAAAAAICVciTBm5CQoDlz5mjmzJnaunWr3Q3K0mMYhqWx1KlTx2zfvn07zb4pl3t6etotS76xmST99ddfeuyxx5yO8+eff0q6U9ahfPnymQkXAAAAAAAAADLMzeoBL126pObNm6t///76/fffM5XczQkVK1ZU1apVJUl79+5Ns++ePXvMdsryDJLUrFkz+fn5SVKqG7CldOHCBe3cuVOS1LFjR7m7u2cpbgAAAAAAAABIj6UJ3qSkJPXo0UNbtmyRJHl5ealNmzZ2fbp06aI6derIZrOZz7Vs2VLdunVTt27drAzHNHjwYEnSmTNn9Ouvvzrsc/PmTU2fPl2S5Ovrm+qGcV5eXnr66aclSdu3b9fatWsdjjNu3DglJiZKkp555hkLogcAAAAAAAAAxyxN8C5evFibNm2SdOfmYjt37tSqVavs+vzyyy/atWuXDh06pHr16kmSzp8/r7Fjx2rRokVWhmMaPny4WQv32Wef1R9//GG3PCoqSk8++aRZO/eNN94wZ+umNGrUKBUsWFCS1L9/f+3evdtu+fTp0zVhwgRJUosWLdIs4wAAAAAAAAAA2WVpDd45c+aY7REjRqhatWpO+4aGhmrVqlWqVauW/v77bz3++OP6888/5e3tbWVIku7Mvl2yZImaN2+u8PBwtWjRQnXr1lWlSpV09epVbdq0STExMZKkXr166d1333U4TvHixTVv3jx16dJFYWFhqlevnpo0aaJixYrpwIEDOnz4sCSpfPnydq8FAAAAAAAAAOQES2fw7tixw2xnZPZqoUKF9Pbbb0uSDhw4oGnTplkZjp3Q0FDt3r1bffr0kZeXl3bt2qWffvpJK1euVExMjMqWLauvv/5ac+bMkZub85elffv22rZtm5o1a6akpCRt2rRJCxYs0OHDh+Xt7a1BgwZpx44dKlasWI7tCwAAAAAAAABIFs/gDQ8PN9vJJREkyWazyTAMSdLt27eVL18+c1mHDh3M9rx58/Tiiy9aGZKd4sWL64cfftCkSZO0a9cuhYeHy9vb2+5GbBlRt25d/fHHHzp79qwOHTqk6OhoBQUF6aGHHjJLOAAAAAAAAABATrM0wZuQkGC2U5ZaKFCggFkC4dq1awoICDCXlSxZ0mz//fffVobjlJ+fn1q0aJHtcUqVKqVSpUpZEBEAAAAAAAAAZJ6lJRqCgoLM9uXLl812yoRuWFiY3TrXrl0z2xEREVaGAwAAAAAAAAB5mqUJ3uDgYLOdslxDyput/fXXX3br7Nmzx2z7+flZGQ4AAAAAAAAA5GmWJnirV69utk+cOGG227Zta7YnTZqk+Ph4SXfq8f7vf/8zlz300ENWhgMAAAAAAAAAeZqlCd5WrVqZ7ZUrV5rtfv36mbNzd+zYobp162rIkCGqW7euVq9ebfYbPHiwleEAAAAAAAAAQJ5m6U3WWrVqJS8vL0nS2rVrzeeDgoL0xRdf6JlnnpFhGDp48KAOHjxot+6TTz6pXr16WRkOAAAAAAAAAORpls7gLV26tOLi4hQXF6cDBw7YLRswYIB++eUX1axZ0+75gIAAjR49WrNnz7YyFAAAAAAAAADI8yydwZuexx57TI899pguXLigixcvysfHRxUrVpSbm6V5ZgAAAAAAAAB4INzTBG+y4sWLq3jx4rmxaQAAAAAAAADIM+6rqbPXrl3L7RAAAAAAAAAAwGXcFwneyMhIvffeeypdunRuhwIAAAAAAAAALiNXSjQkCwsL07hx4/TNN9/o5s2buRkKAAAAAAAAALgcSxK8sbGxOnXqlG7evKnSpUuraNGiafY/fvy4Pv74Y82YMUPx8fFWhAAAAAAAAAAAD5xslWg4cOCAunfvrsKFC6tatWqqX7++goKCVLFiRU2bNi1V/zNnzmjw4MGqUqWKpkyZYpfcbdq0qZYuXZqdcAAAAAAAAADggZLlGbzr169X586dFRMTk2rZ8ePHNXjwYB0+fFhjxoyRJH3zzTcaMWKEbty4Yde3ffv2euedd9S8efOshgIAAAAAAAAAD6QsJXhv3Lihfv36OUzupjR27Fh17dpV69at0z//+U/zeTc3Nz3++ON655139NBDD2UlBAAAAAAAAAB44GWpRMPcuXN17tw58/FLL72k48ePKz4+XkePHtWQIUPMZf/3f/+nDz74wHzcqVMn7d27V/Pnzye5CwAAAAAAAADZkKUZvL/++qvZ7tWrlyZOnGg+rlixoiZPnqyoqCgtWLBAO3fulCTZbDZ9+eWXGjZsWDZDBgAAAAAAAABIWZzBu3fvXrP94osvOuwzfPhwu8fPP/88yV0AAAAAAAAAsFCWErzh4eFmu3bt2g773P38Cy+8kJVNAQAAAAAAAACcyFKCN+XN1fz8/Bz2KVSokN3jihUrZmVTAAAAAAAAAAAnspTgNQzDbNtsNod97n7eWSIYAAAAAAAAAJA1WUrwAgAAAAAAAAByHwleAAAAAAAAAHBRHtkdoHv37pb2W7RoUZZjAQAAAAAAAIAHSbYTvIsXL7a0HwAAAAAAAAAgYyjRAAAAAAAAAAAuKkszeGfNmmV1HAAAAAAAAACATMpSgrdfv35WxwEAAAAAAAAAyCRKNAAAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KJI8AIAAAAAAACAiyLBCwAAAAAAAAAuigQvAAAAAAAAALgoErwAAAAAAAAA4KI8rBzMZrOZbcMwcnw9AAAAAAAAAHiQMYMXAAAAAAAAAFwUCV4AAAAAAAAAcFG5nuCNjY012/nz58/FSAAAAAAAAADAteR6gnffvn1mu2jRorkYCQAAAAAAAAC4lizfZG3VqlXZWp6QkKAzZ87os88+M5+rV69eVsMBAAAAAAAAgAdOlhO8bdu2zdZyR4YMGZLVcAAAAAAAAADggZPlBK+V8ufPr9GjR6tDhw65HQoAAAAAAAAeYO7TX8/tEOBE4rPjcjuE+1KWE7xvvvlmquc+/vjjNJenlC9fPvn5+Sk0NFQtWrSQv79/VkMBAAAAAAAAgAdSlhO8H330UarnUiZ4HS0HAAAAAAAAAFjH0hINL730kpXDAQAAAAAAAADSYGmCd+LEiVYOBwAAAAAAAABIg1tuBwAAAAAAAAAAyBoSvAAAAAAAAADgoiwt0ZBSZGSk1qxZo3379unKlSuKi4vL0HrffvttToUEAAAAAAAAAHmK5QneGzdu6I033tDUqVMVHx+f6fVJ8AIAAAAAAABAxlia4L19+7Y6deqkDRs2WDksAOAec5/+em6HACcSnx2X2yEAAAAAAO4jliZ4p0yZYpfcbdKkiYYOHaqqVasqf/78Vm4KAAAAAAAAAB54liZ4f/zxR7PduXNn/fLLL3Jz4z5uAAAAAAAAAJATLM2+7t+/32yPGjWK5C4AAAAAAAAA5CBLM7BxcXFmu2bNmlYODQAAAAAAAAC4i6UJ3hIlSphtwzCsHBoAAAAAAAAAcBdLE7ytWrUy24cOHbJyaAAAAAAAAADAXSxN8L788svy8Lhz37aZM2daOTQAAAAAAAAA4C6WJnjr1Kmjjz/+WJI0ceJELVmyxMrhAQAAAAAAAAApeFg52J9//qnmzZtr2LBhmjRpkrp3766nn35ajz/+uEJCQuTu7p7uGPXr17cyJAAAAAAAAADIsyxN8DZo0MDucVJSkn744Qf98MMPGR6Dm7MBAAAAAAAAQMZYWqIBAAAAAAAAAHDvWDqD94UXXrByOAAAAAAAAABAGixN8H799ddWDgcAAAAAAAAASAMlGgAAAAAAAADARZHgBQAAAAAAAAAXdU8TvImJiUpISLiXmwQAAAAAAACAPMvSGrwpxcXF6YcfftCSJUv0119/KSIiQrdu3ZIkGYYhSVq4cKFu3rwpSerRo4fy58+fU+EAAAAAAAAAQJ6TIwnetWvXqn///goLC0uz3759+/TBBx9Ikk6dOqX33nsvJ8IBAAAAAAAAgDzJ8hINv/32m9q1a2cmdz08PFSzZk2HfUeOHKlChQpJksaMGaMbN25YHQ4AAAAAAAAA5FmWJngvX76sp59+2qyz++STTyosLEx79+512L9AgQIaMGCAJOn69euaO3euleEAAAAAAAAAQJ5maYL3yy+/1NWrVyVJTZs21Zw5cxQUFJTmOu3btzfby5cvtzIcAAAAAAAAAMjTLE3wLl261Gy/9dZbcnNLf/i6deua7R07dlgZDgAAAAAAAADkaZYmeI8ePWq2H3744QytExAQYLbDw8OtDAcAAAAAAAAA8jRLE7zXr183235+fnbLbDabw3WS6/VKkru7u5XhAAAAAAAAAECeZmmCt1ChQmb78uXLGVrn/PnzZjswMNDKcAAAAAAAAAAgT7M0wVupUiWzvX379gyts23bNrNdp04dK8MBAAAAAAAAgDzN0gRvu3btzPbkyZPtljkr0TBt2jSz3bZtWyvDAQAAAAAAAIA8zdIE7/PPPy9vb29J0pIlSzR+/Pg0+0+ePFlr1qyRJBUuXFgDBgywMhwAAAAAAAAAyNMsTfCWKFFCo0ePNh+PGDFCrVu31jfffGPX79dff1Xfvn01dOhQ87lPPvlEBQsWtDIcAAAAAAAAAMjTPKwecOTIkQoLC9Nnn30mSVq7dq3Wrl1r16dLly52j99++209++yzVocCAAAAAAAAAHmapTN4k02YMEFz5861u+maI2XKlNHs2bP13//+NyfCAAAAAAAAAIA8zfIZvMmeeuop9ezZUxs2bND69et16tQpXb16VT4+PgoJCVHLli3VunVr5cuXL6dCAAAAAAAAAIA8LccSvJLk5uamFi1aqEWLFjm5GQAAAAAAAAB4IOVIiQYAAAAAAAAAQM4jwQsAAAAAAAAALipHSzRIUnR0tK5cuaK4uLgM9a9SpUoORwQAAAAAAAAAeUOOJHgPHjyozz77TMuWLdO5c+cyta5hGDkREgAAAAAAAADkOZYneCdPnqyXX35Zt2/ftnpoAAAAAAAAAEAKliZ4N27cqGHDhtnNwq1Vq5YqVaokb29vKzcFAAAAAAAAAA88SxO8Y8aMMZO7QUFBWr58uR566CErNwEAAAAAAAAA+P+5WTnYli1bzPann35KchcAAAAAAAAAcpClCd7r16+b7ZYtW1o5NAAAAAAAAADgLpYmeEuUKGG2AwMDrRwaAAAAAAAAAHAXSxO8jRs3NtvHjx+3cmgAAAAAAAAAwF0sTfC+9NJLZvvHH3+0cmgAAAAAAAAAwF0sTfA+8sgjeuuttyRJY8eO1dq1a60cHgAAAAAAAACQgofVA/73v/9VgQIFNHr0aLVr104DBw5U165dVbJkSbm7u6e7fp06dawOCQAAAAAAAADyJMsTvDabTT179tSvv/6q7du3a+rUqZo6dWqG1zcMw+qQAAAAAAAAACBPsjzBO336dD333HNKSkqyeugcMWXKFEVFRUmSSpYsqf79+2doPcMwtH37dh08eFDR0dEKCgpSkyZNVK5cuZwMFwAAAAAAAABMliZ4t27dapfctdlsql+/vipXrixvb28rN2WJ2bNna8iQIebjRo0aZSjB+9tvv+mll17SiRMnUi1r166dvv76axK9AAAAAAAAAHKcpQneMWPGmMnd4OBg/f7776pZs6aVm7DM+fPnNXz48Eyv9/3332vAgAEyDEMFChRQly5dVKxYMe3fv19r1qzRypUr1ahRI23evFkVK1bMgcgBAAAAAAAA4A43KwfbsWOH2f7000/v2+SuJD333HO6fPmynnnmGXl5eWVonWPHjmnw4MEyDEOhoaE6fPiw5syZowkTJmjVqlVavny5vLy8FBERoSeffNJlylQAAAAAAAAAcE2WJngjIiLMdsuWLa0c2lJTpkzR8uXLVbx4cX366acZXm/UqFGKj4+XJP34448qVaqU3fL27dvr3XfflSTt3r1bc+fOtS5oAAAAAAAAALiLpQneYsWKme0iRYpYObRlTp06pREjRkiSvvrqKxUqVChD68XExOjnn3+WdCd5/dBDDzns99JLL8nT01PSnXIOAAAAAAAAAJBTLE3wPvLII2b7+PHjVg5tCcMw9Mwzz+j69evq1auXunfvnuF1169fr9jYWEl3Zuo6U6RIETVs2FCStGrVKt2+fTtbMQMAAAAAAACAM5YmeF988UXZbDZJ0qxZs6wc2hITJkzQ+vXrFRgYqC+++CJT6+7bt89s165dO82+devWlSTFx8fr6NGjmQ8UAAAAAAAAADLA8hm8//znPyVJn3zyiVasWGHl8Nly+PBhvfPOO5Kkzz77TEWLFs3U+idOnDDbZcqUSbNv6dKlzXZmZzKfO3cuzZ8LFy5kajwAAAAAAAAAeZeHlYP9+eef6tKli8LCwjR16lR17txZffr0Ubdu3RQSEiJ3d/d0x6hfv76VIUmSEhISNGDAAMXFxalLly7q06dPpse4du2a2fbz80uzb8rl169fz9R27r5x293y5cunWrVqSZIuXbqkxMTETI0PWOX8+fO5HQKyiN+da+P3B9zBe8F18btzbfz+gDt4L7gufneu7UH5/ZUoUSJT/S1N8DZo0MDucWJiombNmpWpcg2GYVgZkiTpf//7n3bs2CF/f39NmjQpS2PcvHnTbCffRM0Zb29vh+sBAAAAAAAAgJUsTfDej3bv3q0PP/xQ0p2yESVLlszSOPnz5zfb8fHxafaNi4tzuF5GnD17Ns3lkZGReu655yRJwcHBCg4OztT4ruev3A4ATqT3bdLJexQHMi+z3wTi/sLv717jc+h+lZH3Ap9F9yfOY66N39+9xufQ/YrPIdfFecy18ftzzNIE7wsvvGDlcNkWHx+v/v376/bt23r00Uc1ePDgLI+VmbILKZcXLFgwU9sJCQlJc3m+fPkyNR4AAAAAAACAvMvSBO/XX39t5XDZ9vfff2v//v2SpIoVK+qjjz5y2C+5ju358+fNPhUrVlTPnj3NPmXLljXbZ86cUdWqVZ1u98yZM2a7XLlyWY4fAAAAAAAAANKS50s0JMtI8vns2bN6++23JUmdO3e2S/DWrFnTbO/bt0/t27d3Os7evXslSR4eHgoNDc1qyAAAAAAAAACQpjyd4C1atKjefPPNdPuNGzdOiYmJKlGihPr37y9JqWbotmjRQl5eXrp165ZWrlyp119/3eFY165d09atWyVJrVq1SveGbAAAAAAAAACQVfc0wZuYmCjDMOThcW82Gxwc7LQsQ0oTJkxQYmKiSpUq5bS/n5+fHnvsMS1YsECrV6/WwYMHVa1atVT9vvnmG/Mma3369MneDgAAAAAAAABAGtxyauC4uDhNnTpV3bt3V6lSpeTt7S0PDw+7m4QtXLhQ33//vb7//nvFxsbmVCiWGT16tNzd3ZWUlKS+ffsqIiLCbvmmTZs0atQoSXdmACfPBgYAAAAAAACAnJAjU2nXrl2r/v37KywsLM1++/bt0wcffCBJOnXqlN57772cCMcy1apV0+eff66XXnpJu3fvVpUqVfTkk0+qWLFi2r9/vxYvXqyEhAT5+/tr7ty5cnd3z+2QAQAAAAAAAORhls/g/e2339SuXTszuevh4WF3g7KURo4cqUKFCkmSxowZoxs3blgdjuVefPFFzZkzR0FBQbp8+bImT56sf/3rX1qwYIESEhLUsGFDbdq0yek+AwAAAAAAAIBVLJ3Be/nyZT399NNKSEiQJD355JOaOHGigoKCZLPZUvUvUKCABgwYoM8//1zXr1/X3LlzNXjwYCtDypCRI0fq9u3bKl26dIb69+rVS0888YRZizc6OlpBQUF6+OGHVbdu3RyOFgAAAAAAAADusDTB++WXX+rq1auSpKZNm2rOnDlyc0t7knD79u31+eefS5KWL1+eKwneDz/8MNPr5MuXTx06dFCHDh1yICIAAAAAAAAASJ+lJRqWLl1qtt966610k7uS7Ga87tixw8pwAAAAAAAAACBPszTBe/ToUbP98MMPZ2idgIAAsx0eHm5lOAAAAAAAAACQp1ma4L1+/brZ9vPzs1vmqAavJLNeryS5u7tbGQ4AAAAAAAAA5GmWJngLFSpkti9fvpyhdc6fP2+2AwMDrQwHAAAAAAAAAPI0SxO8lSpVMtvbt2/P0Drbtm0z23Xq1LEyHAAAAAAAAADI0yxN8LZr185sT5482W6ZsxIN06ZNM9tt27a1MhwAAAAAAAAAyNMsTfA+//zz8vb2liQtWbJE48ePT7P/5MmTtWbNGklS4cKFNWDAACvDAQAAAAAAAIA8zdIEb4kSJTR69Gjz8YgRI9S6dWt98803dv1+/fVX9e3bV0OHDjWf++STT1SwYEErwwEAAAAAAACAPM3D6gFHjhypsLAwffbZZ5KktWvXau3atXZ9unTpYvf47bff1rPPPmt1KAAAAAAAAACQp1k6gzfZhAkTNHfuXLubrjlSpkwZzZ49W//9739zIgwAAAAAAAAAyNMsn8Gb7KmnnlLPnj21YcMGrV+/XqdOndLVq1fl4+OjkJAQtWzZUq1bt1a+fPlyKgQAAAAAAAAAyNNyLMErSW5ubmrRooVatGiRk5sBAAAAAAAAgAdSjpRoAAAAAAAAAADkvHua4E1MTFRCQsK93CQAAAAAAAAA5Fk5VqIhLi5OP/zwg5YsWaK//vpLERERunXrliTJMAxJ0sKFC3Xz5k1JUo8ePZQ/f/6cCgf/X3v3Ht9z/f9//L6jwzYzm51n5nyoUIYoPg5FpSZCGsmHcsqvUNTn04lKffog1adIJ0IIoVLIqRz6OJRkc6ax2cHGNhtjp/fvD9+9Ppud3uM989pu18vFpef7/Ty8Hu/35OV993o/XwAAAAAAAAAqnXIJeDdv3qwhQ4bo9OnTJY7bv3+/XnvtNUlSVFSUXnrppfIoBwAAAAAAAAAqJZtv0bB27Vrde++9Rrjr6OioW2+9tcixzz//vGrXri1Jeuedd5Senm7rcgAAAAAAAACg0rJpwHvu3DkNGjTI2Ge3f//+On36tP78888ix9esWVOPP/64JCktLU1Lly61ZTkAAAAAAAAAUKnZNOD98MMPlZKSIkm66667tGTJEnl7e5c4p2fPnkb7xx9/tGU5AAAAAAAAAFCp2TTgXbNmjdF+4YUXZG9f+vJt2rQx2rt377ZlOQAAAAAAAABQqdk04D169KjR7tixo1VzPD09jfaZM2dsWQ4AAAAAAAAAVGo2DXjT0tKMdq1atQr02dnZFTknb79eSXJwcLBlOQAAAAAAAABQqdk04K1du7bRPnfunFVzYmNjjbaXl5ctywEAAAAAAACASs2mAW/jxo2N9q5du6yas3PnTqPdunVrW5YDAAAAAAAAAJWaTQPee++912h//PHHBfqK26Lh888/N9r33HOPLcsBAAAAAAAAgErNpgHvk08+qerVq0uSvvvuO82cObPE8R9//LE2bdokSfLw8NDjjz9uy3IAAAAAAAAAoFKzacDr7++vqVOnGo8nTpyobt26ae7cuQXGff/99woPD9eoUaOM52bMmCE3NzdblgMAAAAAAAAAlZqjrRd8/vnndfr0ab333nuSpM2bN2vz5s0Fxjz44IMFHr/44osaNmyYrUsBAAAAAAAAgErNplfw5pk1a5aWLl1a4KZrRQkODtbixYs1bdq08igDAAAAAAAAACo1m1/Bm2fAgAF65JFHtHXrVv3888+KiopSSkqKXFxcFBgYqL/97W/q1q2bnJycyqsEAAAAAAAAAKjUbB7wWiwWWSwW2dvby97eXl26dFGXLl1sfRgAAAAAAAAAqPJsGvDa2dkZbYvFYsulAQAAAAAAAABXsekevI6O5bbjAwAAAAAAAADgKjYNeL29vY12VlaWLZcGAAAAAAAAAFzFpgFvy5YtjXZ0dLQtlwYAAAAAAAAAXMWmAe+gQYOM9urVq225NAAAAAAAAADgKjYNeB9//HF16tRJkjRt2jQdP37clssDAAAAAAAAAPKxacDr4OCglStXqnv37kpKSlL79u310UcfKTEx0ZaHAQAAAAAAAABIcrTlYvXr15ck5ebmSpLOnj2rsWPHauzYsfL09JSrq2upa0RFRdmyJAAAAAAAAACotGwa8J48ebLYvrNnz+rs2bO2PBwAAAAAAAAAVGk2DXg9PT1tuRwAAAAAAAAAoAQ2DXiTkpJsuRwAAAAAAAAAoAQ2vckaAAAAAAAAAODGIeAFAAAAAAAAAJMi4AUAAAAAAAAAkyLgBQAAAAAAAACTsulN1qKioq6tCEdHubu7y9XVVXZ2drYsCQAAAAAAAAAqLZsGvCEhIdc1v2bNmmrdurV69uyp4cOHKyAgwEaVAQAAAAAAAEDlc1Nt0XDx4kXt2LFDr776qho1aqT33nuvoksCAAAAAAAAgJuWTa/gHThwoCQpKSlJGzduNJ738/PTrbfeKjc3N50/f14RERGKi4sz+rt3764aNWroxIkTOnDggCTp0qVLevbZZ5WTk6MJEybYskwAAAAAAAAAqBRsegXvkiVLNGnSJB0+fFiS1KJFC23cuFGxsbFat26dli9frvXr1ys2NlYbNmxQs2bNJEmHDx/WlClTFBkZqYiICLVr185Y88UXX9SpU6dsWSYAAAAAAAAAVAo2DXjPnj2rsLAwxcTEqFGjRtq2bZu6detW5Nju3btr+/btatCggWJiYtSnTx+dPXtWLVu21IYNG1S/fn1JUmZmpj7++GNblgkAAAAAAAAAlYJNA96PPvpIMTExkqQpU6bIw8OjxPF16tTRlClTJEnR0dGaPXu2JMnNzU3PPfecMW7z5s22LBMAAAAAAAAAKgWbBrzffPON0e7Ro4dVc+655x6jvWLFCqPdvXt3o338+HEbVAcAAAAAAAAAlYtNA96//vrLaJd29W5R46Kioox2UFCQ0U5OTr7+4gAAAAAAAACgkrFpwJuVlWW04+LirJoTGxtrtDMzM422nZ2d0a5Vq5YNqgMAAAAAAACAysWmAW/+q25Xrlxp1Zz844KDg412/uDXx8fHBtUBAAAAAAAAQOVi04D3gQceMNpTp07VoUOHShwfGRmp119/3Xh83333Ge1Tp04Z7cDAQBtWCQAAAAAAAACVg00D3vHjx8vV1VWSdO7cObVv317//ve/dfr06QLjTp8+rXfeeUd33nmnsb+um5ubJkyYYIzZtm2b0e7YsaMtywQAAAAAAACASsGmAW9gYKAWLlwoJycnSdL58+c1adIkBQYGytPTU/Xr15enp6cCAwM1efJkpaWlSZKcnJy0YMECBQQEGGutXLlSDg4OcnBwUL9+/WxZJgAAAAAAAABUCjYNeCUpLCxMGzZsUMOGDQs8f+7cOZ08eVLnzp0r8HzDhg21ceNGhYWFFXh+7969ys7OVnZ2tm655RZblwkAAAAAAAAApudYHot27txZBw8e1MqVK/XNN99o165dio2N1eXLl1WtWjX5+/urXbt26tu3rx5++GHjil8AAAAAAAAAgPXKJeCVrmy7MGDAAA0YMMB4LicnRw4ODuV1SAAAAAAAAACoUmy+RUNJSgt3U1JSbkwhAAAAAAAAAFAJ3NCAtyg5OTlau3atHn30Ufn5+VV0OQAAAAAAAABgGuW2RUNpDh06pHnz5mnBggWKjY2tqDIAAAAAAAAAwLRuaMCbnJysJUuWaN68edq1a9eNPDQAAAAAAAAAVDrlHvDm5ORo/fr1mjdvnlavXq3Lly8XGlOrVi0NHjxYo0ePLu9yAAAAAAAAAKDSKLeA98CBA5o3b54WLlyouLi4Ise0bt1ao0aNUnh4uFxdXcurFAAAAAAAAAColGwa8CYnJ2vx4sWaN2+edu/eXer4vXv32vLwAAAAAAAAAFClXHfAm5OTo7Vr12r+/Pn69ttvi9yCoUmTJho0aJDCw8PVpEmT6z0kAAAAAAAAAEDXEfBGRkYaWzDEx8cX6vfz89PAgQMVHh6utm3bXleRAAAAAAAAAIDCringDQ0N1Z49ewo97+7urr59+yo8PFxdu3aVvb39dRcIAAAAAAAAACjaNQW8+cPd6tWr64EHHtBjjz2mBx54QNWqVbNZcQAAAAAAAACA4l33Jba33nqrevXqpa5duxLuAgAAAAAAAMANdE0Br7Ozs9HevXu3nnzySfn6+iosLExLly7VxYsXbVYgAAAAAAAAAKBo1xTwxsbG6v3339ftt99uPJeZmalvv/1Wjz76qHx8fDR48GCtWbNGWVlZNisWAAAAAAAAAPA/1xTwenp6aty4cfrtt9+0f/9+TZgwQT4+PkZ/enq6Fi1apN69e8vPz0+jR4/WL7/8IovFYrPCAQAAAAAAAKCqu+49eG+55RbNmDFDMTEx+vbbb9W3b98CWzicPXtWc+bMUZcuXRQcHHy9hwMAAAAAAAAA/J/rDnjzODo66sEHH9SKFSuK3MJBkqKjows8Hj16tPbv32+rEgAAAAAAAACgSrFZwJtfaVs45JkzZ45uu+023X333frqq6+UmZlZHuUAAAAAAAAAQKVULgFvfqVt4SBJ27ZtU3h4uIKCgsq7HAAAAAAAAACoNMo94M1jzRYOZ86cuVHlAAAAAAAAAIDp3bCANz9rt3AAAAAAAAAAABSvQgLe/K7ewgEAAAAAAAAAYJ0KD3jz5G3hAAAAAAAAAACwzk0T8AIAAAAAAAAAyoaAFwAAAAAAAABMioAXAAAAAAAAAEyKgBcAAAAAAAAATIqAFwAAAAAAAABMioAXAAAAAAAAAEyKgBcAAAAAAAAATIqAFwAAAAAAAABMioAXAAAAAAAAAEyKgBcAAAAAAAAATIqAFwAAAAAAAABMioAXAAAAAAAAAEyKgBcAAAAAAAAATIqAFwAAAAAAAABMioAXAAAAAAAAAEyKgBcAAAAAAAAATIqAFwAAAAAAAABMioAXAAAAAAAAAEyKgBcAAAAAAAAATMqxogu4kbKzsxUbG6v4+HglJyerVq1aatKkiTw9Pa9pvZSUFB09elSpqany9vZW8+bN5eTkZOOqAQAAAAAAAKBolT7gPXnypL744gv98ssv+u9//6uMjIxCY26//XaNHz9egwcPtmrNo0ePauLEiVq7dq2ysrKM5z08PDRs2DBNnTpVLi4uNnsNAAAAAAAAAFCUSh/wbt26VVOmTDEeV69eXbfccovq1Kmj+Ph4RURE6Pfff9eQIUO0atUqLV68uMSrcLdt26aePXvq4sWLkqSWLVvK19dXBw8eVGxsrGbOnKl169Zp69at8vDwKPfXBwAAAAAAAKDqqjJ78Pbs2VPffvutUlJStHv3bq1bt0779u3T4cOH1bFjR0nSihUr9M9//rPYNZKSkhQWFqaLFy/Ky8tLP//8syIiIrRhwwadOnVKM2bMkJ2dnSIjIxUeHn6jXhoAAAAAAACAKqrSB7yNGzfWtm3btHbtWj344IOqVq1agf5GjRpp7dq1CgwMlCS9//77SktLK3Kt119/XefOnZMkzZ8/X507dzb6HBwcNGHCBI0aNUqS9OOPP2rDhg3l8ZIAAAAAAAAAQFIVCHjbt2+vTp06lTjGzc1Njz32mCTp8uXL2rlzZ6ExWVlZWrBggSSpVatWuv/++4tc64UXXpC9/ZW39bPPPrue0gEAAAAAAACgRJU+4LWWl5eX0U5OTi7Uv337duP5Bx98sNh16tWrp1atWkmS1qxZo9zcXBtXCgAAAAAAAABXEPD+n4iICKMdEBBQqP+PP/4w2qGhoSWu1a5dO0lSWlqa/vrrL9sUCAAAAAAAAABXcazoAm4G8fHxWrFihSSpTp06RQa4R48eNdrBwcElrle/fn2jfeTIETVs2NDqWmJiYkrsT0pKsnotAAAAAAAAAJVblQ94LRaLRo0apQsXLkiS/vGPf8jJyanQuJSUFKPt4eFR4pq1a9c22qmpqWWqJygoqMR+Jycn3XbbbZKkhIQE5eTklGl9wFZiY2MrugRcI3525sbPD7iC/xfMi5+dufHzA67g/wXz4mdnblXl5+fv71+m8VV+i4YpU6Zo9erVkqS7775bzzzzTJHj8gJgSapevXqJa9asWdNop6en26BKAAAAAAAAACisSl/BO3fuXE2ZMkXSlW0Vli5dKkfHot8SZ2dno52dnV3iupmZmUa7WrVqZaopOjq6xP6kpCSNGDFCkuTj4yMfH58yrW8+v1V0AShGaf+axO7TN6+y/ksgbi78/G40zkM3K2v+X+BcdHPizzFz4+d3o3EeullxHjIv/hwzN35+RauyAe+XX36p0aNHS5ICAwO1ceNG+fn5FTvezc3NaJd2VW7+q33zz7NGYGBgif1FbR8BAAAAAAAAoGqqkls0LFq0SMOGDVNubq78/f21adMmNWjQoMQ5+YPX06dPlzg2/43SSgtsAQAAAAAAAOBaVbmA96uvvtLQoUONcHfz5s1q3LhxqfNatmxptA8ePFji2Lx+Ozs7NW/e/PoKBgAAAAAAAIBiVKmAd8mSJXr88ceVk5MjPz8/bd68WU2aNLFqbufOnWVvf+Xt2rx5c7HjMjMztW3bNklSaGioXFxcrr9wAAAAAAAAAChClQl4ly5dqsGDBysnJ0f+/v7asmWL1eGuJPn6+qpz586SpO+++07x8fHFHic1NVWSNHDgwOsvHAAAAAAAAACKUSUC3uXLlxvhbkBAQJnD3TyvvfaaJOny5csaPny4MjMzC/SfPHlSzz//vKQrgfBTTz113bUDAAAAAAAAQHEcK7qA8rZ+/XoNGjRI2dnZcnBw0HPPPafDhw/r8OHDxc5p3ry5GjZsWOj5Ll266JlnntF7772nH374Qe3atdOIESPk6+uriIgIffTRR0pMTJSjo6M+//xzubq6ludLAwAAAAAAAFDFVfqAd8eOHcrOzpYk5eTkaPz48aXOeeutt/TCCy8U2Tdz5ky5ubnp7bff1r59+zRu3LgC/T4+Pvr000913333XX/xAAAAAAAAAFCCSh/wNmnSRA888ECZ5jRq1KjYPnt7e73++usaMWKEli1bpgMHDig1NVXe3t7q2LGj+vTpIzc3t+stGwAAAAAAAABKVekD3scee0yPPfaYzdcNDg7Wc889Z/N1AQAAAAAAAMBaVeImawAAAAAAAABQGRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAAAAAAgEkR8AIAAAAAAACASRHwAgAAAAAAAIBJEfACAAAA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"]}], "is_error": false, "command": "view", "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/fig5_v0.png", "prev_exist": true, "old_content": null, "new_content": null, "kind": "FileEditorObservation"}
```

### [56] TOOL RESULT — task_tracker · 2026-08-19 19:31:16 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "# Task List\n\n1. \ud83d\udd04 Create fig5_spec.json and render grouped bar chart\n   Create grouped bar chart spec and render Fig 5\n\n2. \u23f3 Verify rendered figure against checklist\n   Verify every number, axis labels, units, and chart readability\n\n3. \u23f3 Write structured output JSON\n   Write final output JSON to .sdk_openhands_agent_struct_out.json"}], "is_error": false, "command": "view", "task_list": [{"title": "Create fig5_spec.json and render grouped bar chart", "notes": "Create grouped bar chart spec and render Fig 5", "status": "in_progress"}, {"title": "Verify rendered figure against checklist", "notes": "Verify every number, axis labels, units, and chart readability", "status": "todo"}, {"title": "Write structured output JSON", "notes": "Write final output JSON to .sdk_openhands_agent_struct_out.json", "status": "todo"}], "kind": "TaskTrackerObservation"}
```

### [57] THINKING · 2026-08-19 19:31:26 UTC

```
The figure has been rendered. Let me verify it against the checklist:

1. Every number in the figure matches the specification:
   - Easy: Short=69.5, Medium=71.1, Long=49.2 ✓
   - Medium: Short=66.7, Medium=80.2, Long=66.7 ✓
   - Hard: Short=68.0, Medium=76.0, Long=50.7 ✓

2. Axis labels state what is measured AND its units:
   - xlabel: "Difficulty Tier" ✓
   - ylabel: "Agreement Rate (%)" ✓

3. Axis ranges make the comparison readable:
   - Y-axis starts at 0 and goes to 100 (or close), showing the full range ✓

4. Chart type still makes the point:
   - Grouped bar chart clearly shows the comparison across difficulty tiers and CoT lengths ✓
   - The drop for Long CoT on Hard problems is visible ✓

5. Caption describes what is drawn:
   - The caption would say: "Self-check agreement rate stratified by difficulty tier (easy, medium, hard) and CoT length (short, medium, long). Long CoT produces the lowest agreement across all tiers, with the largest drop for hard problems (76.0% to 50.7%)." ✓

The figure looks good. Let me update the tasks and write the output JSON.
```

### [58] ASSISTANT · 2026-08-19 19:31:26 UTC

_(empty)_

### [59] TOOL CALL — task_tracker · 2026-08-19 19:31:26 UTC

```
{
  "command": "plan",
  "task_list": [
    {
      "title": "Create fig5_spec.json and render grouped bar chart",
      "notes": "Create grouped bar chart spec and render Fig 5",
      "status": "done"
    },
    {
      "title": "Verify rendered figure against checklist",
      "notes": "Verified: all numbers match, axis labels have units, ranges readable, chart type appropriate",
      "status": "done"
    },
    {
      "title": "Write structured output JSON",
      "notes": "Write final output JSON to .sdk_openhands_agent_struct_out.json",
      "status": "in_progress"
    }
  ]
}
```

### [60] TOOL CALL — file_editor · 2026-08-19 19:31:26 UTC

```
{
  "command": "create",
  "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json",
  "file_text": "{\n  \"title\": \"Agreement by Difficulty and CoT Length\",\n  \"summary\": \"Rendered a publication-quality grouped bar chart (Figure 5) showing self-check agreement rates stratified by difficulty tier (Easy, Medium, Hard) and chain-of-thought length (Short, Medium, Long). The chart clearly demonstrates that Long CoT produces the lowest agreement across all tiers, with the most dramatic drop on Hard problems (from 76.0% with Medium CoT to 50.7% with Long CoT). All numeric values from the specification are accurately represented: Easy (Short=69.5, Medium=71.1, Long=49.2), Medium (Short=66.7, Medium=80.2, Long=66.7), Hard (Short=68.0, Medium=76.0, Long=50.7). The y-axis shows Agreement Rate in percent from 0 to 100, and the x-axis labels the three difficulty tiers. The figure uses a clean white background with sans-serif fonts and a colorblind-safe palette. The 16:9 aspect ratio provides good visual balance for journal publication.\",\n  \"out_expected_files\": {\n    \"image_path\": \"fig5_v0.png\"\n  }\n}\n",
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
```

### [61] TOOL CALL — task_tracker · 2026-08-19 19:31:26 UTC

```
{
  "command": "view",
  "task_list": []
}
```

### [62] TOOL RESULT — task_tracker · 2026-08-19 19:31:28 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "Task list has been updated with 3 item(s)."}], "is_error": false, "command": "plan", "task_list": [{"title": "Create fig5_spec.json and render grouped bar chart", "notes": "Create grouped bar chart spec and render Fig 5", "status": "done"}, {"title": "Verify rendered figure against checklist", "notes": "Verified: all numbers match, axis labels have units, ranges readable, chart type appropriate", "status": "done"}, {"title": "Write structured output JSON", "notes": "Write final output JSON to .sdk_openhands_agent_struct_out.json", "status": "in_progress"}], "kind": "TaskTrackerObservation"}
```

### [63] TOOL RESULT — file_editor · 2026-08-19 19:31:28 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "File created successfully at: /ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json"}], "is_error": false, "command": "create", "path": "/ai-inventor/aii_data/runs/run_DyrN7YJjJoEX/4_gen_paper_repo/_2_gen_viz/gen_viz_5/.sdk_openhands_agent_struct_out.json", "prev_exist": false, "old_content": null, "new_content": "{\n  \"title\": \"Agreement by Difficulty and CoT Length\",\n  \"summary\": \"Rendered a publication-quality grouped bar chart (Figure 5) showing self-check agreement rates stratified by difficulty tier (Easy, Medium, Hard) and chain-of-thought length (Short, Medium, Long). The chart clearly demonstrates that Long CoT produces the lowest agreement across all tiers, with the most dramatic drop on Hard problems (from 76.0% with Medium CoT to 50.7% with Long CoT). All numeric values from the specification are accurately represented: Easy (Short=69.5, Medium=71.1, Long=49.2), Medium (Short=66.7, Medium=80.2, Long=66.7), Hard (Short=68.0, Medium=76.0, Long=50.7). The y-axis shows Agreement Rate in percent from 0 to 100, and the x-axis labels the three difficulty tiers. The figure uses a clean white background with sans-serif fonts and a colorblind-safe palette. The 16:9 aspect ratio provides good visual balance for journal publication.\",\n  \"out_expected_files\": {\n    \"image_path\": \"fig5_v0.png\"\n  }\n}\n", "kind": "FileEditorObservation"}
```

### [64] TOOL RESULT — task_tracker · 2026-08-19 19:31:28 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "# Task List\n\n1. \u2705 Create fig5_spec.json and render grouped bar chart\n   Create grouped bar chart spec and render Fig 5\n\n2. \u2705 Verify rendered figure against checklist\n   Verified: all numbers match, axis labels have units, ranges readable, chart type appropriate\n\n3. \ud83d\udd04 Write structured output JSON\n   Write final output JSON to .sdk_openhands_agent_struct_out.json"}], "is_error": false, "command": "view", "task_list": [{"title": "Create fig5_spec.json and render grouped bar chart", "notes": "Create grouped bar chart spec and render Fig 5", "status": "done"}, {"title": "Verify rendered figure against checklist", "notes": "Verified: all numbers match, axis labels have units, ranges readable, chart type appropriate", "status": "done"}, {"title": "Write structured output JSON", "notes": "Write final output JSON to .sdk_openhands_agent_struct_out.json", "status": "in_progress"}], "kind": "TaskTrackerObservation"}
```

### [65] THINKING · 2026-08-19 19:31:30 UTC

```
I've completed the task. Let me update the task tracker and finish with the structured output.
```

### [66] ASSISTANT · 2026-08-19 19:31:30 UTC

_(empty)_

### [67] TOOL CALL — task_tracker · 2026-08-19 19:31:30 UTC

```
{
  "command": "plan",
  "task_list": [
    {
      "title": "Create fig5_spec.json and render grouped bar chart",
      "notes": "Create grouped bar chart spec and render Fig 5",
      "status": "done"
    },
    {
      "title": "Verify rendered figure against checklist",
      "notes": "Verified: all numbers match, axis labels have units, ranges readable, chart type appropriate",
      "status": "done"
    },
    {
      "title": "Write structured output JSON",
      "notes": "Write final output JSON to .sdk_openhands_agent_struct_out.json",
      "status": "done"
    }
  ]
}
```

### [68] TOOL CALL — finish · 2026-08-19 19:31:30 UTC

```
{
  "message": "Successfully rendered Figure 5: Agreement by Difficulty and CoT Length. The grouped bar chart shows self-check agreement rates across three difficulty tiers (Easy, Medium, Hard) and three CoT lengths (Short, Medium, Long). Key finding: Long CoT produces the lowest agreement across all tiers, with the largest drop for hard problems (76.0% to 50.7%).\n\nOutput files:\n- fig5_v0.pdf (vector deliverable)\n- fig5_v0.png (preview)\n- fig5_spec.json (specification source)\n- .sdk_openhands_agent_struct_out.json (structured output)"
}
```

### [69] TOOL RESULT — task_tracker · 2026-08-19 19:31:30 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "Task list has been updated with 3 item(s)."}], "is_error": false, "command": "plan", "task_list": [{"title": "Create fig5_spec.json and render grouped bar chart", "notes": "Create grouped bar chart spec and render Fig 5", "status": "done"}, {"title": "Verify rendered figure against checklist", "notes": "Verified: all numbers match, axis labels have units, ranges readable, chart type appropriate", "status": "done"}, {"title": "Write structured output JSON", "notes": "Write final output JSON to .sdk_openhands_agent_struct_out.json", "status": "done"}], "kind": "TaskTrackerObservation"}
```

### [70] TOOL RESULT — finish · 2026-08-19 19:31:30 UTC

```
{"content": [{"cache_prompt": false, "type": "text", "text": "Successfully rendered Figure 5: Agreement by Difficulty and CoT Length. The grouped bar chart shows self-check agreement rates across three difficulty tiers (Easy, Medium, Hard) and three CoT lengths (Short, Medium, Long). Key finding: Long CoT produces the lowest agreement across all tiers, with the largest drop for hard problems (76.0% to 50.7%).\n\nOutput files:\n- fig5_v0.pdf (vector deliverable)\n- fig5_v0.png (preview)\n- fig5_spec.json (specification source)\n- .sdk_openhands_agent_struct_out.json (structured output)"}], "is_error": false, "kind": "FinishObservation"}
```

### [71] HOOK — PostToolUse · 2026-08-19 19:31:30 UTC

```
<system-reminder>You have 114.1 minutes remaining to finish all your tasks.</system-reminder>
```
