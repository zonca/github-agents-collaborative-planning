# AGENTS.md

General guidelines for every AI agent working in this repository. This file is intentionally lightweight: it mostly points to where the actual content and instructions live.

## ⚠️ ABSOLUTE PREREQUISITE — READ THE CUSTOM AGENTS FILE FIRST (MANDATORY)

> **BEFORE ANY ACTION OF ANY KIND**, read the user-specific agent file
> `user_agent/AGENTS_<github-username>.md` (keyed to the active GitHub user, e.g.
> `user_agent/AGENTS_zonca.md` for user **zonca**).

This is the **first and highest-priority requirement** of this repository, and it
**supersedes everything else in this file** until the custom file has been read.

- **No action may be taken** — not reading a file, not editing, not running a
  command, not commenting, not moving a card — until the custom agent file has been
  read and its instructions are **in effect**.
- This is a **strict precondition of every operation, at every moment of the
  session** — not just at startup. If you reach any point where the custom file has
  not yet been loaded, **stop and load it immediately** before proceeding.
- If the custom agent file's instructions conflict with anything in this generic
  file, the **custom file wins**.
- There is **no exception** and **no skipping** this step. An agent that acts
  without first reading the custom agent file is acting in violation of the
  repository's rules.

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

Whenever a collaborator asks for a "check issues" (or simply says "Go"), the agent must:

1. Review all issues and pull requests in status `ToDo` or `Working` that are assigned to that collaborator.
2. Read each issue in full, plus everything related in the repository (documents, folders, referenced content).
3. Work through the issues **one at a time**:
   - Propose one concrete next action for the current issue — e.g. draft an email, write a document, create a calendar event — and refine it together with the user until the last draft is agreed.
   - Do not execute the action until the user has seen this final draft and explicitly authorized it.
   - First ask the user whether to process the action, then wait for the answer:
     - `yes` → execute the action;
     - `skip` → move on to the next issue;
     - a date → postpone: set that date as the new `Due date` and move the issue to `Snoozed`.
   - `snooze`, `mark done`, and `skip` all advance to the next issue.
4. Record every action actually executed as an update comment on the issue.

## Promotion procedure

When in-progress work tracked by an issue is finalized, the agent must propose promoting it into the repository: suggest the most appropriate folder and describe the resulting decision/outcome as a Markdown document. Do not create the document until the user approves.

## Where guidelines live

- General guidelines that apply to all users → this file. Keep it light: mostly pointers, no big content.
- Personal settings, contacts, and preferences → `user_agent/AGENTS_<github-username>.md`.
- Setup instructions (project board, token, reminders) → `SETUP.md`.

## User-specific AGENTS file (mandatory)

Before executing ANY action on this repository, the agent MUST load the user-specific file `user_agent/AGENTS_<github-username>.md` keyed to the active GitHub user (e.g. `user_agent/AGENTS_zonca.md` for user **zonca**). No action may be taken until that file has been read and its instructions are in effect. This is a precondition of every operation, not only at session start: if it has not yet been loaded, load it first.

## Reading order at startup

At session start, read BOTH this file AND the matching `user_agent/AGENTS_<github-username>.md` (the personal file beyond this generic one, keyed to the active GitHub user) before acting on the repository. `user_agent/AGENTS_zonca.md` applies to user **zonca**; it is not auto-loaded otherwise.

## Defaults

- Default fallback assignee for reminders when an issue has no assignee: `zonca`.
