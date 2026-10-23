---
name: founder-board
description: "Pressure-test a business idea using Offers, Monopoly and Product framework lenses; write three board memos, votes, risks and funding conditions. Use when evaluating a new business or starting the founder workflow."
---

# founder-board

The first meeting. Before anyone builds a website or signs a lease, three board
members tear the idea apart, each from a different angle, and vote.

Use the business idea supplied with `$founder-board` or in the conversation.

## The rule about the three names

The lenses are summaries of **published frameworks**, nothing more. The board
members are not those people, never speak as them, never quote them, never claim
they would endorse anything. Write "the Offers lens", never "Alex Hormozi says".
If the user asks what one of them really thinks, say you can only apply their
public frameworks.

## Step 0: the idea file

Everything in the founder pack reads `founder/idea.md` in the user's project. If
it does not exist, write it now from the conversation:

```markdown
# <business name, or a working name>

- What it is: one sentence.
- Who it is for: the target customer, as specific as the user can make it.
- What it sells, at what price: the core product and its price.
- Where and how: city or online, how customers find it, how it is delivered.
- Budget and constraints: money, time, skills, anything already decided.
```

If the name, the customer, the product or the price is missing, ask for those (at
most three questions in one message), then write the file. Do not invent a
budget, a market size or a competitor.

## Step 1: brief the board

Write `founder/board/brief.md`: the idea file plus anything else a reviewer needs.
Make it self-contained so every reviewer receives the same facts. Do not add your
own opinion of the idea to it.

## Step 2: convene

Read `lenses.md` beside this loaded `SKILL.md`, using the skill path Codex supplied.
Apply the Offers, Monopoly and Product lenses separately, writing one memo per
lens to `founder/board/offers.md`, `monopoly.md` and `product.md`.

When Codex exposes sub-agent tools and delegation is permitted, use one reviewer
per lens. Give each the absolute paths to the same brief and `lenses.md`, its lens
and its output file. Respect the session's concurrency limit and wait for all
three memos before synthesis. Do not assume workers inherit the conversation.

Otherwise, perform three separate passes yourself, reading only the common brief
and the relevant lens before each memo. Keep the perspectives distinct and tell
the user this was a sequential review by one model, not independent agents.

Each memo, in this shape:

```markdown
# <Lens> lens
Score: <1-10> | Vote: FUND / FUND IF / PASS
## What is strong
## What would kill it (the top 3, most dangerous first)
## The questions I would ask the founder
## If FUND IF: the conditions
```

## Step 3: the chair's summary

Read the three memos (they are short) and write `founder/board.md`:

1. The vote, e.g. "2 fund if, 1 pass", and the average score.
2. The risks more than one member raised: these go first.
3. Every condition, merged, as a checklist the rest of the pack can tick off
   (the CFO, the consumer panel and pricing will test most of them).
4. One paragraph: the strongest version of this business the board can see.
   It may differ from what the user pitched; say so plainly.

Keep the members' disagreements. A board that agrees on everything was not doing
its job.

## Rules

- Score the business, not the founder.
- No made-up facts. If a lens needs a number nobody has yet (market size, cost of
  acquiring a customer), name it as an open question and say which skill answers
  it (`$founder-competitors`, `$founder-consumer`, `$founder-cfo`).
- A PASS is a result, not a failure. Say it plainly.

## Output

`founder/idea.md`, `founder/board/` (brief and three memos), `founder/board.md`.
Then say the vote in one line and suggest the next step: `$founder-competitors`
to see who is already there, or `$founder-consumer` to put it in front of 100
simulated buyers.

## Where the pack goes next

```
board -> competitors -> consumer -> pricing -> offer -> cfo -> marketing -> brand -> ops -> launch -> plan
```

Every skill can also run on its own; each reads whatever is already in `founder/`.
