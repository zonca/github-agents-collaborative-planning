# AGENTS.md

General guidelines for every AI agent working in this repository. This file is intentionally lightweight: it mostly points to where the actual content and instructions live.

## What an agent is

Agents assist their human collaborator. There are no autonomous agents here: every meaningful operation requires explicit authorization from the user.

## Authorization rule

- Before performing any operation, present a short, specific draft of what you are going to do.
- Do not perform the operation until the user explicitly approves it.
- If in doubt, ask.

## Repository conventions

- The repository is the single source of truth for the project: plans, meeting notes, decisions, people, and agreements.
- Documents live in the top-level folders (see `README.md` → Repository structure). Pick the most fitting folder when writing or promoting content.

## Issue workflow

- Every issue belongs to the GitHub Project with status `ToDo / Working / Snoozed / Done` and has a `Due date`.
- A new issue starts in `ToDo` (enforced by the project's automation rule — see `SETUP.md`).
- When an agent starts working on an issue, move it to `Working`.
- When work on an issue is finished, move it to `Done`; if the work is postponed, update its `Due date` and move it to `Snoozed`.

## Check-up procedure

Whenever a collaborator asks for a "check issues" (or similar), the agent must:

1. Review all issues and pull requests in status `ToDo` or `Working` that are assigned to that collaborator.
2. Read each issue in full, plus everything related in the repository (documents, folders, referenced content).
3. Propose a concrete next action per issue — e.g. draft an email, write a document, create a calendar event.
4. Show the proposal to the user, who decides or steers the agent in a different direction.
5. Record every action actually executed as an update comment on the issue.

## Promotion procedure

When in-progress work tracked by an issue is finalized, the agent must propose promoting it into the repository: suggest the most appropriate folder and describe the resulting decision/outcome as a Markdown document. Do not create the document until the user approves.

## Where guidelines live

- General guidelines that apply to all users → this file. Keep it light: mostly pointers, no big content.
- Personal settings, contacts, and preferences → `user_agent/AGENTS_<github-username>.md`.
- Setup instructions (project board, token, reminders) → `SETUP.md`.

## Defaults

- Default fallback assignee for reminders when an issue has no assignee: `zonca`.
