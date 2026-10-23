---
name: founder-plan
description: "Compile existing founder research and financial inputs into a business plan and one-pager with a computed profitability verdict. Use to assemble the plan after analysis; use founder-cfo to calculate the underlying economics."
---

# founder-plan

The last step. One document a founder can act on, or hand to a partner or a
lender, built only from what the pack found.

If the user supplies `--min-buy-rate`, pass it to every compile command below
and state the chosen threshold. Otherwise use the default 0.25.

## Locate the bundled tool

Set the shell variable `SKILL_DIR` to the absolute directory containing this
loaded `SKILL.md`, using the skill path Codex supplied. Codex does not set this
variable automatically. Resolve bundled files there; keep the working directory
at the user's project root so `founder/` stays in their project.
This tool also needs the sibling `founder-cfo` folder; install the full pack.

Tool in this folder:

```bash
python3 "${SKILL_DIR}/compile.py" --dir founder
```

## Step 1: see what is there

```bash
python3 "${SKILL_DIR}/compile.py" --dir founder --check
```

prints the verdict and each check. The checks, all computed:

1. Each unit earns money before fixed costs (`founder/numbers.json`).
2. Year 1 makes an operating profit.
3. The break-even fits inside capacity, if a capacity was given.
4. Enough simulated buyers buy (`founder/panel/results.json`; default bar 25%,
   change it with `--min-buy-rate` and say why).

If there are no numbers, the verdict is Incomplete: offer to run `$founder-cfo`.
List the other missing sections with the skill that fills each. Do not fill a
missing section yourself from guesses.

## Step 2: the summary

Write `founder/summary.md`, half a page, plain words:

- What the business is and who it is for, in two sentences.
- The verdict and the three numbers behind it (margin, break-even, year 1).
- What the buyer panel and the board agreed on, and where they disagreed.
- The biggest risk and what will be done about it.
- What the founder needs to start (cash from the CFO, the first test from launch).
- The one thing to do this week.

If the verdict is Not yet, the summary leads with what has to change and which skill
changes it. Never soften a failing check.

## Step 3: compile

```bash
python3 "${SKILL_DIR}/compile.py" --dir founder
```

writes `founder/business-plan.md`: title, the verdict and its checks, the key numbers
table, the idea, then every section the pack produced (summary, board, competition,
panel, pricing, offer, numbers, marketing, brand, operations, launch), and what is
not done yet.

## Step 4: the one-pager

Write `founder/one-pager.md` for someone deciding in two minutes: the problem, the
customer, the offer and price, the numbers table, the evidence (panel result,
competitor gap, any real test), what the money is for, and the ask. Same numbers as
the plan, word for word.

## Rules

- The verdict comes from `compile.py`. Never write Profitable by hand, and never
  round a failing number into a passing one.
- Say once, clearly: the panel is simulated buyers and the numbers are projections;
  real customers and real quotes confirm them. Not financial, legal or tax advice.
- If the user wants a PDF or a deck, offer to export the plan, but keep the
  markdown as the source of truth.

## Output

`founder/summary.md`, `founder/business-plan.md`, `founder/one-pager.md`. Then give
the user the verdict in one line and the one thing to do this week.
