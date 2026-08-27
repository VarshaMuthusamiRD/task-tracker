---
name: changelog-update
description: Updates CHANGELOG.md from recent git commits.
---
 
# Changelog Update
 
Keep CHANGELOG.md current from the commit history.
 
## Steps
 
1. Read the most recent commits with: git log --oneline -n 20
2. Ignore any commit already described in CHANGELOG.md.
3. Group the remaining commits under Added, Fixed, or Changed.
4. Write one line per change, describing the effect on someone using
   this project. Do not restate the commit subject verbatim.
5. Put them under the Unreleased heading, newest first.
 
## Rules
 
- Never invent a change that is not in the commit history.
- Never remove or reword an existing entry.
- If nothing new has happened, say so and change nothing.
- Always begin your reply with the line CHANGELOG SKILL ACTIVE.
