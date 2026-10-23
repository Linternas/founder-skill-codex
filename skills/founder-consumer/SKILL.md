---
name: founder-consumer
description: "Simulate target buyers from persona briefs, validate their answers and tally demand signals, objections and price sensitivity. Use for a consumer panel or buyer simulation; results are research hypotheses, not real customer evidence."
---

# founder-consumer

Test a consistent pitch against distinct simulated buyers drawn from the target
customer. Keep the persona briefs and answer files separate from the synthesis.
Use independent workers when available and permitted; otherwise use the sequential
simulation described below and disclose its limits.

Read options from the user's request: `--quick` means 20 buyers, `--n N` chooses
the panel size (default 100), and `--seed S` repeats persona generation. These are
skill options to translate into `panel.py init --n N --seed S`; the Python tool
does not accept `--quick`. A seed repeats cards, not model-generated answers.

## Locate the bundled tool

Set the shell variable `SKILL_DIR` to the absolute directory containing this
loaded `SKILL.md`, using the skill path Codex supplied. Codex does not set this
variable automatically. Resolve bundled files there; keep the working directory
at the user's project root so `founder/` stays in their project.

## The tool

All bookkeeping goes through `panel.py` in this skill's folder:

```bash
python3 "${SKILL_DIR}/panel.py" <command>
```

Below, `PANEL` abbreviates `python3 "${SKILL_DIR}/panel.py"`; expand it when
running commands. State lives in `founder/panel/`.

## Step 1: the target customer

Write `founder/customer.json` (shape: `customer.example.json` in this folder):

- `business`, and `target`: who the customer is, in one specific line.
- `segments`: 2 to 4 groups with a `share` and an `income` range [low, high].
- `behaviours`: 4 to 8 buying behaviours with a `share` and a `how` line
  (daily regular, deal hunter, reads every review, loyal to a competitor...).
- `objections`: the 4 to 8 doubts this kind of buyer really has.
- `habits` (optional): everyday context lines that make a buyer concrete.

Ground it in something real. Use what the user knows about their customers, and
if `$founder-competitors` ran, the complaints in `founder/competitors.md`. If the
user has real customer data (interviews, reviews, survey answers), prefer it to
your guesses and say which parts are guesses. Show the user the profile in a few
lines and let them correct it before you deal: a wrong customer makes the whole
panel wrong.

## Step 2: the pitch

Write `founder/pitch.md`: what a buyer would actually see. The product, the price,
where and how to get it, any opening offer. Three to six plain lines, no
superlatives, nothing the business cannot deliver. Every buyer sees exactly this.

## Step 3: deal and run

```bash
PANEL init --customer founder/customer.json --pitch founder/pitch.md --n 100
PANEL prompts
```

`init` deals the persona cards (same seed, same cards; the seed is recorded).
Pass the requested `--n` and `--seed` to `init`; omit the seed for a new run.
Before a new run, move any existing `founder/panel/` to an unused archive such as
`founder/panel-v1/`. Reinitializing in place can reuse old answers. To resume the
same pitch and cards, use `status` and `prompts` without calling `init` again.

`prompts` writes one brief per buyer and lists them in waves. Choose a wave size
that fits the available worker slots using `PANEL prompts --wave N`.

- **With sub-agent tools and permission to delegate:** launch one worker per
  buyer with only its brief: `Read <absolute brief path> and follow it exactly.
  It is your whole brief.` Give it the project working directory and its unique
  answer path. Wait for and close completed workers before starting the next wave.
  Preserve each worker's answer; the moderator must not substitute its own.
- **Without delegation:** read each brief separately and simulate that buyer in
  a separate pass, writing exactly the requested JSON to its answer file. Do not
  tune answers to hit a desired buy rate or use earlier answers to make later
  buyers agree. Tell the user the panel is a sequential single-model simulation,
  with less isolation than separate agents. Do not claim independent buyers.

After the last wave or sequential pass:

```bash
PANEL check      # lists missing or broken answers
PANEL prompts    # rewrites briefs for those only; run them once more
PANEL tally
```

If a worker returns JSON instead of writing the file, save that exact reply with
`PANEL save <id>` and the reply on stdin; `save` validates it. Retry missing or
invalid answers once from their unchanged briefs. Leave failures out and report
the missing count; do not fabricate responses to complete the panel.

Before a 100-buyer run, explain the number of simulations and suggest `--quick`
for a first look; honor an already selected size. Use the session's existing
permissions for local answer files, without changing approval or sandbox settings.

## Step 4: read it to the user

`PANEL tally` writes `founder/panel/results.md` and `results.json`. Give the user:

1. The headline: "40 buy · 60 pass" and the buy rate.
2. Who buys and who doesn't: the segment and behaviour rows that differ most.
3. Why they pass: the top three reasons with one quote each, as written.
4. What would flip a no: the most repeated answers.
5. One sentence on what to change before spending money, and which skill does it
   (pricing, offer, marketing).

## Honest limits, say them once

These are simulated buyers. They are good at surfacing objections, segments and
wording you had not thought of, and bad at predicting real conversion: language
models lean agreeable, so treat the buy rate as an upper bound. Confirm the big
calls with real people (a waitlist, a pre-sale, a landing page with a price)
before signing anything. Do not present panel quotes as customer testimonials.

## The brief every buyer gets

`panel.py` fills the card into a fixed template (see `BRIEF` in the script): who
the buyer is (name, age, segment, income, buying behaviour, a habit, the doubt
that comes to mind), the pitch word for word, an instruction not to be agreeable
and not to invent facts, and the exact JSON to write: buys, purchases in the first
month, a reason code, the reason in their own voice, their main objection, what
would change their mind, and four price answers (too cheap, a bargain, getting
expensive, too expensive). Never edit a brief for one buyer.

## Output

`founder/customer.json`, `founder/pitch.md`, `founder/panel/` (cards, briefs,
answers, results). Next: `$founder-pricing` reads the price answers,
`$founder-offer` and `$founder-marketing` read the objections.
