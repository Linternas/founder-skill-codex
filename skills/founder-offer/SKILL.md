---
name: founder-offer
description: "Build an affordable offer stack from buyer objections: core product, bonuses, guarantee and honest urgency; compare it with a repeat buyer panel. Use to improve an offer or address reasons buyers pass."
---

# founder-offer

Most businesses sell a product. Good ones sell an offer: the product plus
everything that makes buying it an easy yes. This skill builds that, using the
Offers lens in `../founder-board/lenses.md` as the method (a summary of the
framework in Alex Hormozi's *$100M Offers*; never present it as his words).

## Step 1: read what is already known

- `founder/idea.md` and `founder/pitch.md`: what is sold today.
- `founder/panel/results.md`: why buyers pass, in their words. This is the raw
  material: every top objection should be answered by something in the offer.
- `founder/numbers.json`: what each extra costs, so the stack stays profitable.
- `founder/board.md`: the board's conditions.

## Step 2: the problem list

Write every obstacle between the buyer and the result they want, in the buyer's
words: before buying (doubt, price, effort to switch), during (waiting, learning,
inconvenience), after (does it last, what if it fails). Aim for 15 to 30. Pull
from the panel objections and the competitor complaints first.

## Step 3: solutions, trimmed and stacked

Turn each problem into a solution (a feature, a service, a guarantee, a format).
Score each on value to the buyer (1 to 5) and cost to deliver (1 to 5, from the
CFO's numbers). Keep high value, low cost. Stack what is left into:

- **The core**: the thing itself, described by the outcome, not the ingredients.
- **Bonuses**: two or three, each killing one specific objection.
- **The guarantee**: what happens if it does not deliver. Model what it costs at a
  realistic claim rate with the CFO's tool before promising it.
- **Urgency and scarcity**: only if they are true (a launch week, a limited first
  batch). Never fake a countdown or a "only 3 left".
- **The name**: a clear, specific name for the offer, not the company.

## Step 4: score it

On the value equation, before and after, 1 to 10 each: dream outcome, perceived
likelihood of getting it, time to the result, effort and sacrifice. Say which
element of the stack moves which score.

## Step 5: re-test it

Write the new offer into `founder/pitch.md` (keep the old one as
`founder/pitch-v1.md`, or another unused version). Archive the original panel
before re-testing so old answers cannot leak into the new run. Run
`$founder-consumer --quick` with the same customer profile and seed. For a matched
comparison, use the same panel size too; if the original had 100 buyers, either
repeat 100 or run both pitches on matching 20-buyer cards. Record panel size, seed
and execution mode for both runs.
Report the buy rate before and after and which objections dropped. If nothing
moved, say so: the problem may be the market or the price, not the offer.

## Rules

- Every promise must be deliverable and affordable; check costs with the CFO.
- No fake reviews, testimonials, scarcity, discounts or "as seen on".
- Follow the advertising and consumer-protection rules of the user's market for
  guarantees and claims (health claims especially). Not legal advice.

## Output

`founder/offer.md` (problem list, the stack, costs, the value-equation scores, the
re-test result) and the updated `founder/pitch.md`. Next: `$founder-cfo` to re-run
the numbers with the stack, then `$founder-marketing`.
