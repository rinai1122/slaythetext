# CLAUDE.md

## Deployment constraint (read before editing anything)

This game must run on a **closed/air-gapped server**. The only way code gets in
is: it's *printed* on the outside and a human *types it back in* on the inside.
There is no file copy, USB, paste, or camera/scanner channel.

We **keep the code as normal, readable `.py` files** (a compressed/base64 blob
was considered and rejected — typing random characters is harder and more
error-prone for a human than typing real code).

Therefore: **every character here is eventually typed by hand, and every changed
line may have to be re-typed.** Optimize edits for that.

### Editing rules
- **Minimal diffs.** Change the fewest lines possible. Never reflow, re-indent,
  re-order, or reformat code you aren't functionally changing — churn becomes
  hand-typing on the server.
- **Fewer characters, honestly.** Prefer compact, readable code; kill real
  redundancy. But never sacrifice correctness or clarity to save a line.
- **Define once, reference many.** Repeated dict/data literals (e.g. the same
  `{"Name":"Shiv",...}` typed inline in several places) should be a single named
  constant or a small builder, referenced everywhere else.
- **Cards/relics/potions use the compact builders** in entities.py — add new
  entries as `"Name": c(Type, Rarity, Owner, Info, **stats)` (relics `r(...)`,
  potions `p(...)`), NOT raw dict literals. "Name" is auto-filled from the key;
  keys with spaces go in `**{"Key": val}`. The built dict is what consumers see,
  so this is purely a shorter way to type the same data.
- **No new dependencies** (stdlib + colorama + ansimarkup only) and **avoid new
  files** — both mean more setup/typing on the closed box. Extend the existing 8
  source files unless a new file is clearly justified.
- **Line-count/dedup refactors are a separate, deliberate pass** — never bundled
  into a feature edit (keeps diffs reviewable and update payloads small).

### Proving "nothing changed"
- Data-layer refactors (builders, dedup, auto-filling repeated keys) must be
  verified by **deep-equality against a snapshot** of the original built
  structures — i.e. the card/relic dicts come out byte-identical. No gameplay run
  needed.
- All modules must still import: `python -c "import entities, climber, enemy,
  helping_functions, acts, save_handlery, spelling_correction"`.
- Logic refactors (changing code flow, not data) need a scripted, seeded
  playthrough comparison before they're considered safe — don't do them blind.

## Updating the server after a change here
1. Tag the last synced state: `git tag -f internal-synced` (re-tag after each sync).
2. Make the minimal-diff change and commit.
3. `git diff internal-synced -- '*.py'` shows exactly which lines to re-type on
   the server. Keep edits to whole-line replacements so "go to line N, type
   this" is unambiguous.
