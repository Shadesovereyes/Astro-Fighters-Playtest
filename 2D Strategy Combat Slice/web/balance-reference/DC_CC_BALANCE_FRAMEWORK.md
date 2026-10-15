# Astro Fighters — DC / CC / DOT Balance Framework

_Last updated: 2026-08-12._

This document captures the owner-approved framework for the upcoming DC difficulty and status-cost balance pass. It is intended to keep save reliability, crowd-control strength, DOT value, resource cost, and action-slot cost from being tuned as if they were the same variable.

## 1. Core distinction: effect tier is not final action cost

A status effect has an **intrinsic utility tier** based on what happens after it lands. That tier does **not** automatically determine how many action slots the ability should consume.

Final action/resource pricing must also account for:

- whether the ability must first pass an attack roll;
- the rider's save / landing probability after the hit;
- setup requirements such as stance, grapple, mount, or another prerequisite;
- the ability's existing damage, Guard Break, range, AoE, reach, Priority, or other advantages;
- authored Stamina, Chakra, Supplies, and other resource premiums;
- repetition strain and the five-action round structure;
- whether the effect is a pure-control action or a secondary rider on an attack.

Therefore, **CC tier determines intrinsic value; reliability and setup determine how much of that value must be paid through resources and action economy.**

## 2. Working CC / DOT reliability targets

For an equally invested attacker and defender, current owner targets are:

| Tier | Baseline rider landing rate | Intended feel |
|---|---:|---|
| C | 60% | Common consequence of being hit; e.g. a sword strike is more likely than not to cause a light Bleed. |
| B | 45% | Reliable tactical rider, but not expected every time. |
| A | ~35% | Strong control that should feel threatening rather than routine. |
| S | ~30% | Fight-swinging hard control / action denial that should remain uncertain. |

For damaging attacks, these are **post-hit rider rates**, not total attempt rates. An attack must first hit, then the status check is resolved. Pure-control abilities that do not require an attack roll have only the save gate and therefore generally require a larger action/resource premium for the same intrinsic status.

## 3. Working intrinsic status tiers

These tiers are based on the current engine behavior and can be revised if the underlying status implementation changes.

### S tier — hard action-economy control

Examples: **Prone, Stun, Fear, Sleep**.

These effects directly remove actions, can erase meaningful portions of a five-action round, or create severe follow-up windows. Prone is especially valuable because it cancels the target's next action, applies the heavy initiative penalty, and grants attackers a large hit bonus while the target is down.

Mounted is also S-tier in practical value, but is a special setup state rather than a normal one-step status and must be priced through its grapple/mount sequence.

### A tier — major control / denial

Examples: **Grappled, Confusion, Blind, strong Root variants**.

These effects strongly distort positioning, hit reliability, or the opponent's ability to execute a planned turn, but are generally less absolute than direct hard action denial.

### B tier — tactical control

Examples: **Slow, Snare, Silence, Disarm** (matchup-dependent).

These effects materially alter movement, initiative, or access to parts of a kit without usually deleting a whole action by themselves.

### C tier — attrition / light rider effects

Examples: **light Bleed, Burn, Poison, Psychosomatic, Cripple**.

These are expected to land relatively often and add attrition or modest output reduction rather than immediately swinging the action economy.

DOT tier can rise with total authored damage. Bleed/Burn/Poison/Psychosomatic share the same basic tick machinery today, so magnitude and duration matter more than the status name alone.

## 4. Action-slot framework

The five-slot round is itself a balance lever. Strong control should sometimes be constrained by slots in addition to resource cost, but **not every A/S rider automatically receives the same slot tax**.

Working test targets:

| Effect package | Slot target | Notes |
|---|---:|---|
| C rider | 1 | Common rider; reliability/resource premium does most of the balancing. |
| B rider | 1 | Tactical rider; normally remains combo-friendly. |
| A rider on damaging attack | 2 normally | Strong effect plus damage; test exceptions where reliability/setup is low. |
| S rider on damaging attack | 1–2 | Attack roll + low post-hit rider reliability can justify 1 slot; otherwise 2. |
| A pure CC | 2 | Only one landing gate, so stronger action tax. |
| S pure CC | 3 normally | Direct hard control should generally be limited to one use per five-slot round. |
| A/S setup-gated grapple technique | 1–2 | Clinch/mount/setup already consumed actions/resources and acts as part of the tax. |

A 2-slot action naturally caps at two uses in one five-action round. A 3-slot action naturally caps at one use.

## 5. Important example: Sweeping Low

**Sweeping Low remains a 1-slot technique during the DC calibration even though Prone is S-tier.**

Reasoning:

- the attack must hit first;
- Prone then has only the S-tier post-hit landing chance (~30% at equal investment);
- the move has low base damage;
- the Karate kit is deliberately built around the five-action string:
  `Karate Blitz → Side Kick → Side Kick → Sweeping Low → Hammer Fist`;
- increasing Sweeping Low to 2+ slots would destroy that intended kit flow before reliability is even tested;
- its S-tier value can instead be reflected through a higher Stamina premium and repetition strain.

At a representative 75% attack hit chance and a 30% post-hit Prone rate, Prone occurs on roughly **22.5% of raw Sweeping Low attempts** before any stat matchup or progression adjustments.

## 6. Important example: Hilt Bash / stacked premium mechanics

An attack such as **Hilt Bash** combines damage, Guard Break, and S-tier Stun. That package should be tested closer to **2 slots plus a substantial resource premium**, because it stacks multiple premium mechanics on a single successful attack.

Guard Break remains a separate premium from CC/DOT. An ability carrying both must satisfy both pricing rules.

## 7. DC scaling work that follows from this framework

The DC pass must now determine a scaling function that preserves the landing-rate targets from low level through high-stat play.

The test matrix should include:

- equal relevant stats;
- attacker +5 / defender +5 stat advantages;
- representative low, mid, and high character-stat bands;
- ability levels 0, 5, and 10;
- damaging-rider versus pure-control versions of the same intrinsic tier;
- attack hit chance × rider probability, so total attempt reliability is visible;
- slot/resource cost alongside expected control value per round.

The final DC model should prevent static low DCs from becoming obsolete as stats rise while also preventing high-investment control from becoming automatic. Natural-floor/ceiling rules (for example, natural 1 always fails the save and natural 20 always succeeds) should be tested as protection against literal 0%/100% outcomes.

## 8. Balance equation

Use this ordering when evaluating a CC/DOT ability:

**Intrinsic effect tier → authored magnitude/duration → landing reliability → setup/attack gates → existing advantages → resource premium → action-slot premium.**

Do not tune one variable in isolation. Strong effects that are difficult to land or require setup should not pay the same action tax as equally strong pure-control effects with only one gate.
