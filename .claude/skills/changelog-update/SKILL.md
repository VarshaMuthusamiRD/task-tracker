---
name: changelog-update
description:  Updates CHANGELOG.md from recent git commits. Use when asked to update
  the changelog, summarize recent changes or commits for users, prepare
  release notes, document what was shipped, explain what is new in a
  version, or write up recent work for a release.
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

## Style guidance

If a commit subject is vague, ambiguous, or does not clearly explain
the user-visible change, read `style.md` before writing the changelog
entry. Use its rules and examples to determine how to describe the
change without inventing information.