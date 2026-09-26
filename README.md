# github-agents-collaborative-planning

A GitHub template for coordinating deadline-driven projects and events — conferences, workshops, launches, anything — where **humans collaborate, mediated by AI agents**.

This is not a tool for autonomous agents talking to each other. In this model, each collaborator works with their own AI agent, and the agent's job is to help its human organize, plan, and follow up. Nothing happens without the human's explicit approval.

## Core principles

- **The repository is the single source of truth.** Plans, meeting notes, decisions, people involved, and signed agreements all live in this repository as Markdown documents. If it matters, it is written down here.
- **Agents draft, humans decide.** Before performing any operation, an agent must show a concrete draft of what it intends to do and wait for explicit authorization.
- **Issues are for discussions and tasks.** Use issues to discuss open questions and to track work over time. Every issue carries a `Due date`.
- **Pull requests are for feedback.** Feedback on documents happens through pull requests, so all changes are reviewed and recorded.
- **GitHub Projects manage deadlines.** A shared public project board tracks the lifecycle of every issue: `ToDo → Working → Snoozed → Done`.
- **GitHub Actions keep time.** A daily workflow (08:00 Pacific) moves snoozed issues back to `ToDo` when their due date arrives, and sends one notification a week after an issue is overdue.

## Repository structure

| Path | Purpose |
| --- | --- |
| `README.md` | This overview |
| `AGENTS.md` | General guidelines for agents (entry point, intentionally lightweight) |
| `SETUP.md` | Setup guide: an agent walks the user through project board, token, and workflow |
| `user_agent/AGENTS_<github-username>.md` | Per-collaborator agent configuration |
| `.github/workflows/reminders.yml` | Daily deadline reminder workflow |
| `scripts/reminders.py` | Logic used by the reminder workflow |
| `planning/` | Plans, schedules, agendas, proposals |
| `meetings/` | Meeting notes and outcomes |
| `decisions/` | Decision records: `YYYY-MM-DD-<topic>.md` |
| `people/` | One file per person involved (role, contact) |
| `agreements/` | Contracts, MOUs, letters of intent, signed documents |

## How to use this template

1. Create a new repository from this template.
2. Set up the GitHub Project and credentials — do it together with an agent following `SETUP.md`. The user only needs the GitHub CLI (`gh`) installed and authenticated.
3. Each collaborator adds their own `user_agent/AGENTS_<github-username>.md` with personal configuration (contacts, tools, preferences).
4. Start filling the top-level folders as the project evolves.

## The issue lifecycle

1. A new issue is created and automatically lands in `ToDo` (project automation rule).
2. An agent starts working on the issue: moves it to `Working`.
3. When work is finished, the issue goes to `Done` — or, if postponed, its `Due date` is updated and the issue moves to `Snoozed`.
4. Every day at 08:00 Pacific the reminder workflow:
   - moves issues whose due date has arrived from `Snoozed` back to `ToDo`;
   - sends a single notification (one week after the due date is missed) mentioning the assignee — or the default fallback user `zonca` if no one is assigned.

## Promotion procedure

When work tracked in an issue is finalized, the agent must propose promoting the result into the repository: it suggests the most appropriate folder (see the structure table above) and writes the outcome — a decision record, meeting summary, plan update, and so on — as a Markdown document. The human approves the change through a pull request.

## License

This template is released under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) license.

You are free to share and adapt this template, provided you attribute the original work. If you use this template for your own project, or if it inspires your work, please link back to it:

- GitHub: <https://github.com/zonca/github-agents-collaborative-planning>
- Blog post: link to be added — tracked in [issue #1](https://github.com/zonca/github-agents-collaborative-planning/issues/1).
