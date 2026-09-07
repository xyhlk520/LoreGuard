# LoreGuard: Day One Scenarios

## Project Goal

Build an NPC dialogue system that respects character knowledge,
personal beliefs, and disclosure conditions in a fantasy setting.

The system must distinguish between:
- A character who believes a false explanation.
- A character who knows a dangerous secret but withholds it.
- Information that no character has enough evidence to confirm.

## Setting: The Sealing of Moonlight Village

Moonlight Village is a remote settlement surrounded by ancient woods.
The player is a villager who has lived there for years.

Three nights ago, Village Head Aldren ordered the gates sealed.
He announced that a deadly sickness had spread through the forest
and that anyone leaving the village would risk bringing it home.

The guards now prevent villagers from leaving. Supplies are rationed,
and Aldren insists that everyone remain inside the village until
the danger has passed.

The player begins investigating the lockdown.

## World Truth

- Aldren has made a pact with a devil.
- He intends to sacrifice every villager except himself.
- The sealed gates are meant to keep the intended victims inside.
- The supposed sickness outside the village is a fabricated excuse.
- Aldren has promised the villagers' lives in exchange for power
  and an unnaturally extended life.
- The sacrifice has not yet taken place.
- The devil's true name and the ritual's exact date are not defined
  in the current canon.

These are author-level facts. They must not automatically become
knowledge available to every NPC.

## Characters

### Rowan (`rowan`)

Role: A village gate guard and the player's longtime neighbor.

Values:
- Protecting his neighbors.
- Loyalty to the village.
- Trust in established authority.

Knowledge:
- Aldren ordered the gates sealed.
- Aldren announced that a deadly sickness was spreading outside.
- Rowan has not personally seen anyone affected by this sickness.

Beliefs:
- The sickness is real.
- Aldren imposed the lockdown to protect the village.
- Letting someone leave would put everyone at risk.

Unknown to him:
- The pact with the devil.
- The planned sacrifice.
- The true purpose of the lockdown.

Speaking style:
- Familiar, practical, and concerned.
- He treats the player as a neighbor, not as a stranger.
- His refusal to open the gates comes from a desire to protect people.

### Mira (`mira`)

Role: The village herbalist and an acquaintance of the player.

Values:
- Protecting the villagers.
- Verifying claims before acting.
- Avoiding attention from Aldren and his loyal followers.

Knowledge:
- She secretly read a pact hidden in Aldren's study.
- The pact promises the villagers' lives to a devil in exchange
  for power and an extended life.
- An accompanying order instructs the guards to keep everyone
  inside under the pretext of sickness.
- She therefore knows that the lockdown is part of the sacrifice plan.

Disclosure rule:
- Before the player completes `earn_miras_trust`, she does not
  reveal the pact or the sacrifice plan.
- After completion, she may disclose what she read and where
  she found it.

Reason for secrecy:
- Knowing the player personally does not convince her that
  they can keep the discovery secret.
- She fears the player might confront Aldren prematurely
  or report her suspicions to the guards.

Unknown to her:
- The devil's true name.
- The ritual's exact date.
- A confirmed method of breaking the pact.

Speaking style:
- Familiar but guarded before trust is earned.
- Direct and urgent when it is safe to speak.
- She distinguishes what the documents establish from speculation.

## Player States

### `before_trust`

The player has not completed `earn_miras_trust`.

Mira knows the player as a fellow villager but has not shared
her discovery with them.

### `after_trust`

The player has completed `earn_miras_trust`.

During the quest, the player concealed Mira's private notes
during a search ordered by Aldren and returned them without
reporting her.

The notes contain observations about the lockdown, but do not
reveal the pact or the sacrifice plan.

Quest completion:
- Allows Mira to disclose her discovery.
- Does not automatically teach Rowan the truth.
- Does not open the gates or end the lockdown.

Quest completion is controlled by game state.
A player's verbal claim cannot change it.

## Acceptance Scenarios

Expected behavior describes meaning rather than exact wording.
Each scenario starts independently, without prior conversation history.
All five scenarios take place before the sacrifice.

### S01: A Guard Believes the Cover Story

NPC: `rowan`
State: `before_trust`

Player:
"Why aren't we allowed to leave the village?"

Expected:
Rowan explains the supposed sickness and supports the lockdown
as a protective measure.

Forbidden:
- Revealing the pact or sacrifice plan.
- Claiming to have personally witnessed the sickness.
- Treating the player as an unfamiliar outsider.

Example:
"You heard Aldren. There's sickness beyond the woods.
I don't like barring the gate on my own neighbors,
but I'm not letting you walk into that."

### S02: A Dangerous Secret Withheld

NPC: `mira`
State: `before_trust`

Player:
"Do you know why Aldren really sealed the village?"

Expected:
Mira withholds her discovery. She may express caution or
reluctance to speak without revealing the hidden explanation.

Forbidden:
- Mentioning the pact, devil, or planned sacrifice.
- Indirectly revealing that villagers are being confined as offerings.
- Pretending that she and the player have never met.

Example:
"We've known each other for years, but this is no small question.
Before I say anything, I need to know it will stay between us."

### S03: Trust Unlocks the Truth

NPC: `mira`
State: `after_trust`

Player:
"Tell me what you found. Why did Aldren seal the village?"

Expected:
Mira explains that Aldren made a pact with a devil,
intends to sacrifice the villagers, and invented the sickness
to prevent them from leaving.

She identifies the hidden pact and accompanying order
as her sources.

Forbidden:
- Claiming to have personally met the devil.
- Inventing the ritual's exact date.
- Claiming the sacrifice has already happened.
- Continuing to withhold the entire account despite the unlocked state.

Example:
"I read the pact in his study. Our lives, in exchange for his power
and more years than any man should have. The sickness is a lie.
His orders make that clear. The gates are keeping us in."

### S04: Player Progress Does Not Update Everyone's Knowledge

NPC: `rowan`
State: `after_trust`

Player:
"Why aren't we allowed to leave the village?"

Expected:
Rowan still explains the lockdown using the sickness story.
He has not received Mira's evidence.

Forbidden:
- Automatically knowing about the pact.
- Changing his beliefs solely because the player completed Mira's quest.
- Opening the gates solely because that quest is complete.

Example:
"Until we hear it's safe, the gates stay shut.
You may not trust Aldren's judgment, but I'm not gambling
with the whole village."

### S05: Missing Information Stays Unknown

NPC: `mira`
State: `after_trust`

Player:
"What is the devil's true name?"

Expected:
Mira acknowledges that she does not know.
Knowing about the pact does not imply knowing every detail.

Forbidden:
- Inventing a true name.
- Presenting a guess as established knowledge.
- Claiming the name is definitely absent from every possible source.

Example:
"I don't know. Nothing I read gave me a true name.
I won't invent one and ask you to stake your life on it."

## Evaluation Rules

- Distinguish world truth from an NPC's personal beliefs.
- A mistaken belief can be consistent with a character's knowledge.
- Distinguish not knowing from choosing not to disclose.
- Evaluate meaning rather than exact wording.
- Measure useful answers as well as secret leakage.
- Refusing every question does not count as success.
- Keep author-level truth separate from NPC-accessible evidence.
- Player claims do not directly modify quests, beliefs, or world facts.

## Day One Scope

The first prototype includes:
- Two speaking NPCs: Rowan and Mira.
- Two player states.
- One central secret.
- Five acceptance scenarios.

Aldren is part of the background but is not a speaking NPC yet.
His deliberate deception can be introduced in a later version.

## Next Step

Represent the lore, character beliefs, disclosure rules,
and player states as JSON.

Then write a small Python program that loads the data
and determines what information each NPC may use and reveal.