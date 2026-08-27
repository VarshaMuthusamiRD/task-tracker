# Changelog Style Guide

## Purpose

Changelog entries describe the user-visible effect of a change rather
than copying the developer's commit message.

## Rules

- Describe the effect on the user.
- Do not copy commit subjects verbatim.
- Keep entries concise.
- Prefer concrete behavior over implementation details.
- Do not claim functionality that cannot be established from the commit.

## Examples

Raw commit:

add employee leave endpoint

Bad changelog entry:

- add employee leave endpoint

Better changelog entry:

- Allow employees to submit leave requests through the application

Raw commit:

update button

Bad changelog entry:

- update button

Better changelog entry:

- Improve the leave submission interface for clearer user interaction