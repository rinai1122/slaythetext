# Slay the Text — Slay-the-Spire Parity Audit

Date: 2026-06-30. Scope: validate card / relic / potion / enemy-boss definitions
against canonical Slay the Spire (StS), and identify how the game logic differs
from the real game. **This is an audit only — no gameplay code was changed.**
Line numbers refer to the current (post-revert) `entities.py` unless noted.

## 0. Headline

The game is **systemically very complete**: 3 characters (Silent, Ironclad,
Defect), Orbs + Focus, Powers, ~168 relics, ~33 potions, ~47 events, shops,
campfires, a generated map, all 4 acts, and every act boss correctly assigned.
The work is therefore **mostly correctness bugs in the data, plus a handful of
real logic bugs** — not missing systems. Findings below are grouped by severity.

Counts: cards 546 entries (≈273 cards ×2), potions 39, relics 168, enemies 70+.

---

## A. Structural / data-integrity bugs

**A1. Duplicate dict keys (silent overwrite).** `Strike`, `Strike +`, `Defend`,
`Defend +` are each defined three times in one dict — Silent (L682/683/685/686),
Ironclad (L909/910/912/913), Defect (L1135/1136/1138/1139). Python keeps the
**last**, so at runtime all four basics are the **Defect** copies. Impact is low
(Basics are excluded from reward pools by `Rarity != "Basic"`, and the stats are
identical), but: the Silent/Ironclad `Defend` "Gain 6 Block" entries are dead,
and `cards["Strike"]["Owner"]` is `"Defect"`. Fix needs a design choice (namespace
basics per owner, or accept the collision and delete the dead duplicates).

**A2. Card key ≠ `"Name"` field** (breaks name/upgrade lookups & display):
- `Tactician +` → Name `"Tactician"` (L839)
- `Anger +` → Name `"Anger"` (L919)
- `Dramatic Entrance +` → Name `"Dramatic Entrance"` (L1382)
- `Enlightenment +` → Name `"Enlightenment"` (L1385)
- `Madness +` → Name `"Madness"` (L1406)
- `NoxiousFumes` / `NoxiousFumes +` keys (L889/890) have no space, Name is
  `"Noxious Fumes"`. Any lookup by key `"Noxious Fumes"` will miss.

---

## B. Card logic bugs (these change gameplay)

Confirmed that the `Ethereal` field drives end-of-turn self-exhaust
(`climber.py:5746`), so stray `Ethereal` flags are real bugs:

**B1.** `Dropkick` / `Dropkick +` (L966-967) carry `Ethereal:True` — not an
ethereal card in StS. They will wrongly exhaust if held.
**B2.** `Hemokinesis` / `Hemokinesis +` (L969-970) carry `Ethereal:True`; and
`Hemokinesis +` also has a stray `Energy Gain:1` (L970) → free energy it
shouldn't give. (StS Hemokinesis: lose 2 HP, deal 15/20, no ethereal, no energy.)
**B3.** `Echo Form` base (L1351) has `Ethereal:True` — Echo Form is a non-ethereal
Power; the `+` correctly drops it but base shouldn't have it.
**B4.** `Brutality` base (L1121) has a stray `Vulnerable:2` — grants the player
2 Vulnerable it should not. (`Brutality +` correctly omits it but adds Innate.)
**B5.** `Flash of Steel` / `+` (L1390-1391) have an **empty `Info`** — blank card
text in-game.
**B6.** `Ritual Dagger` base (L1471) carries an inline warning in its own Info:
"UPGRADING THIS CARD IS CURRENLY ILL-ADVISED AS IT'S BUGGED!" — a known broken
upgrade path to fix.
**B7.** `Armaments +` (L1008) has a stray `Attack:5` field where the upgrade-all
behaviour is expected — verify the handler honours "upgrade ALL" and that `Attack:5`
isn't doing something unintended.

---

## C. Card text / value mismatches

Format: card — *what's wrong* (StS canonical). "[text]" = data is right, the
Info string is wrong; "[value]" = the number itself deviates.

- `Defend` (all owners) — Info "Gain 6 Block" but Block=5 (StS 5). [text]
- `Deflect` / `+` — 5/8 Block; StS is **4/7**. [value]
- `Neutralize +` — Info "1 Weak" but applies 2. [text]
- `Heel Hook +` — Info "Deal 5 damage" but deals 8. [text]
- `Glass Knife +` — Info "Deal 8 damage" but deals 12. [text]
- `Crippling Cloud +` — Info "6 Poison" but applies 7. [text]
- `Uppercut` / `+` — Info copied from Reckless Charge ("Deal 7/10 damage. Shuffle
  a Dazed"); should be "Deal 13 damage. Apply Vulnerable + Weak" (data is correct). [text]
- `Disarm` / `+` — Info copied from Burning Pact ("Exhaust 1 card. Draw 2/3");
  should be "Enemy loses 2/3 Strength. Exhaust" (data `Strength:-2/-3` is correct). [text]
- `Rampage +` — Info "increase by 5" but `Damage Gain=8`. [text]
- `Feed +` — Info "Deal 14 damage" but deals 12. [text]
- `Shockwave` base — Info "5 Vulnerable" but applies 3 (3 Weak / 3 Vuln). [text]
- `Juggernaut +` — Info "deal 5 damage" but deals 7. [text]
- `Ball Lightning +` — Info "Deal 7 damage" but deals 10. [text]
- `All for One +` — Info copied from Sunder; should be "Deal 14 damage. Put all
  cost-0 cards from discard into hand" (data is correct). [text]
- `Charge Battery +` — Info "Gain 7 Block" but gains 10. [text]
- `Steam Barrier +` — Info "Gain 6 Block" but gains 8. [text]
- `Aggregate +` — Info "every 4 cards" but `Energy Divider=3` (every 3). [text]
- `Trip` base — Info "Apply 2 Weak" but it applies Vulnerable (data `Vulnerable:2`). [text]
- `Bite` / `+` — Info "Deal 6/9 damage" but deals 7/8 (StS 7/8). [text]
- `Thinking Ahead +` — Info "Draw 3 Cards … Exhaust" but `Draw=2` and no Exhaust
  field (StS `+` removes Exhaust, keeps draw 2). [text]
- `Cloak and Dagger +` — "Add 2 Shiv" → "Shivs" (cosmetic).

(I validated these against StS values from knowledge; the [value] item `Deflect`
is the only true balance deviation — worth confirming it's not an intentional buff.)

---

## D. Spelling errors in player-visible text

`additonal` (Predator, Bullet Time, others), `discared` (Reflex, Tactician),
`Stength` (Malaise), `unblocked damaged` (Envenom), `inteds` (Go for the Eyes),
`Currenly` (Ritual Dagger). Internal **field-name** typos are harmless to players
but ugly: `Multiplikator` (Catalyst), `Amplificicy` (Amplify), `Painfull Stabs`
(Book of Stabbing), `Well Planed` (Well-Laid Plans).

---

## E. Relic bugs

- **Strawberry** (L1609) — Info is Orichalcum's: "If you end your turn without
  Block, gain 6 Block." StS Strawberry is **"Raise your Max HP by 7"**. Verify the
  actual effect, not just the text, is correct.
- **Turnip** (L1679) — Info is Old Coin's: "Gain 300 Gold." StS Turnip is **"You
  can no longer become Frail."** Verify the effect too.
- Markup typos (cosmetic): `Meat on the Bone` `</HP>` (L1630), `Black Blood`
  unclosed `<light-red>` (L1684), `Lizard Tail` stray `</red>` (L1663),
  `Red Mask` "1 Weakness" → "1 Weak" (L1727).

---

## F. Potion bugs

- **Regen Potion** (L1543) — `Potion Yield=5` but Info "Gain 6 Regeneration"
  (StS = 5). Pick one. Otherwise potions look accurate and complete.

---

## G. Enemy / boss bugs

- **"Gemlin Nob"** (L1801) — Name typo, should be "Gremlin Nob".
- **Red Slaver `"Scape 9/2"`** (L1782) — dispatcher matches `"Scrape"`
  (`enemy.py:562`), so this move silently fails. Should be `"Scrape 9/2"`
  (cf. Chosen at L1814 which spells it correctly).
- **`create_superElite`** (entities.py L672-674) — the `buff == 3` "regen" branch
  computes `regen` then calls `set_metallicice(regen)` instead of `set_regen` →
  the "regenerating" super-elite gets Metallicize instead.
- A few base HP ranges differ slightly from StS base values (e.g. Lagavulin
  112-115, Hexaghost 264) — these look like Ascension numbers; low priority.
- Boss-per-act assignment, leader/minion handling, and the Act-4 sequence
  (Shop → Campfire → Spire Shield+Spear → Corrupt Heart) are all **correct**.

---

## H. Systemic parity gaps (need a product decision before "filling")

These are design-level differences from full StS, not bugs:

1. **No Ascension levels.** Replaced by a custom "Super Elite" buff system
   (`create_superElite`). Real StS has 20 ascension tiers altering HP, damage,
   shop prices, elites, etc.
2. **Map generation is approximate.** `acts.py` builds a 5-wide / ~12-row graph
   with custom room weights; it does not follow StS's exact path rules (6 paths,
   15 floors, fixed treasure floor 9, rest before boss, no consecutive elites in
   the first stretch, etc.). It is functional but not faithful.
3. **Unverified handlers** (trace before relying on them when fixing): the
   `Energy Change Type` mechanic (Setup / Forethought), `Armaments +`'s
   `Attack` field, X-cost interactions with Chemical X, and multi- vs single-target
   conventions across attacks. Not individually validated in this pass.

---

## Recommended fix order

1. **Tier 1 — zero logic risk:** all of C/D/E-text/F (Info strings, spellings,
   markup), and the A2 Name-key fixes. Pure data edits.
2. **Tier 2 — small logic fixes:** B1-B6 stray fields, G1 (Gemlin Nob), G2
   (Scape→Scrape), G3 (create_superElite regen), Deflect value (C), relic E
   effects.
3. **Tier 3 — structural:** A1 duplicate basics (needs design choice); B7/H3
   handler verification; Ritual Dagger upgrade (B6).
4. **Tier 4 — parity:** Ascension (H1), faithful map (H2) — only if desired.
