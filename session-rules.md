# Session Rules

1. **Re-read a file immediately before editing it, especially after an external-change notice.**
   Prevents: **Stale picture** — today `store.py`/`test_store.py` were reverted on disk outside the conversation, and editing from memory instead of re-reading would have reintroduced changes the user didn't want.

2. **Before any irreversible action (discard, force-push, delete), state exactly what will be lost and get explicit confirmation.**
   Prevents: **Over-reach** — the `git checkout --` request named two files; confirming scope first stopped it from silently sweeping up `handoff.md` too.

3. **When a request is ambiguous or looks like a typo ("policies" vs "priority"), ask one targeted question instead of guessing.**
   Prevents: **Drift** — guessing wrong here would have built out a whole unwanted "policy" feature before anyone noticed.

4. **After every change, re-run the actual test suite and report the real pass count — never state a result you haven't just observed.**
   Prevents: **Contradiction** — each priority/due-date change was verified with a fresh test run, so later answers about "what's tested" matched what was actually true, not an earlier state.

5. **When a field's shape changes (e.g. priority: word → number), update the type everywhere it's used in the same pass — store, validation, and tests together.**
   Prevents: **Lost constraints** — the 1–5 numeric rule set for priority was applied to `add`, `set_priority`, *and* every existing test in one edit, not left half-migrated.

## When to stop rescuing a session and start clean

**Trigger:** the same file diverges from your last-known edit a second time without an explicit, attributable user action explaining the change. One unexplained divergence is worth a note and a re-read. A second one means your mental model of the file's history can no longer be trusted — stop patching forward and re-establish state from `git status`/`git diff` (or start a fresh session) before making any further edit.
