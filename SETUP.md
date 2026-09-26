# SETUP

This guide is for an **agent** helping a human set up this repository. The agent should perform every step it can on its own and only stop when user input is genuinely required.

The user must have the GitHub CLI (`gh`) installed and authenticated (`gh auth status`) with a token that has at least the `project`, `repo`, and `workflow` scopes.

---

## 1. Verify prerequisites

```bash
gh auth status
```

Confirm the authenticated user is the repository owner and that the repository exists:

```bash
gh repo view <owner>/<repo>
```

---

## 2. Create the GitHub Project

Create a project with the title **`Collaborative Planning`** (this title is what the reminder workflow looks for):

```bash
gh project create --owner <owner> --title "Collaborative Planning" --format json
```

Capture from the output:

- `number` — the project number
- `id` — the project ID (starts with `PVT_`)

### 2a. Status field

Create a single-select field named `Status` with exactly these options, in this order:

```bash
gh project field-create <number> --owner <owner> \
  --name "Status" \
  --data-type SINGLE_SELECT \
  --single-select-options "ToDo,Working,Snoozed,Done"
```

If a default `Status` field already exists (new projects ship with one), either:

- use the project UI to rename/clear options: project → Settings → `Status` field → edit the options to `ToDo`, `Working`, `Snoozed`, `Done`; or
- delete the default field with `gh project field-delete <number> --owner <owner> --field-id <id>` (find the field ID with `gh project field-list <number> --owner <owner> --format json`), then create the field as above.

### 2b. Due date field

```bash
gh project field-create <number> --owner <owner> --name "Due date" --data-type DATE
```

### 2c. Link the repository

```bash
gh project link <number> --owner <owner> --repo <owner>/<repo>
```

### 2d. Automation rule: new issue → ToDo

There is no CLI for project automation rules; configure it in the browser (the agent can open the project with `gh project view <number> --owner <owner> --web`):

1. Open the project.
2. Go to the automation/workflow section (project settings → Automation, or the three-dots menu → Workflows).
3. Create a workflow on **"Item added to project"** that sets `Status` to `ToDo`.

Repeat the same rule for **"Issue reopened"**, if desired, so reopened issues return to `ToDo`.

---

## 3. Create the fine-grained token

The reminder workflow needs a fine-grained personal access token because `GITHUB_TOKEN` cannot read or write GitHub Projects v2.

Open the token creation page and ask the user to create a token:

```bash
gh project view <number> --owner <owner> --web
```

Then guide the user to <https://github.com/settings/personal-access-tokens/new> with these settings:

- **Token name**: `github-agents-collaborative-planning`
- **Expiration**: per user preference (90 days is a reasonable default)
- **Repository access**: *Only select repositories* → this repository
- **Permissions**:
  - Metadata: **Read-only** (required)
  - Issues: **Read and write**
  - Projects: **Read and write**

Ask the user to paste the token (it is shown only once). Store it as a repository secret:

```bash
gh secret set PROJECT_TOKEN
```

`gh` prompts for the value securely; do not print the token to the terminal or store it anywhere else.

---

## 4. Configure and enable the reminders workflow

The workflow `.github/workflows/reminders.yml` ships with this template. Its defaults are:

| Setting | Default | Where to change |
| --- | --- | --- |
| Run time | daily 08:00 Pacific | `on.schedule.cron` |
| Project title | `Collaborative Planning` | `env.PROJECT_TITLE` in the workflow |
| Default assignee | `zonca` | `env.DEFAULT_ASSIGNEE` |
| Overdue threshold | 7 days | `env.OVERDUE_DAYS` |

Notes:

- GitHub Actions cron schedules are in **UTC**, not local time. `0 15 * * *` equals 08:00 Pacific during daylight saving; use `0 16 * * *` for 08:00 during standard time. Pick the entry that suits the user's time of year, or keep `0 15` as a reasonable default.
- Scheduled workflows run only on the default branch and only if Actions are enabled for the repository. If the user created the repo from a fork, Actions may be disabled — enable them under *Settings → Actions → General*.

### Verify

Trigger a manual test run:

```bash
gh workflow run reminders.yml --repo <owner>/<repo>
gh run watch --repo <owner>/<repo>
```

Create a test issue with a `Due date` of today and `Status` `Snoozed`; the next run should move it to `Working`.

---

## 5. Create the user agent file

Each collaborator gets their own `user_agent/AGENTS_<github-username>.md` file. The agent can scaffold the file for the user (see `user_agent/AGENTS_zonca.md` for an example) and then fill in personal details with the user: contacts, tools used for communication, preferences.

---

## Summary of commands

```bash
# Create project
gh project create --owner <owner> --title "Collaborative Planning" --format json

# Status + Due date fields
gh project field-create <number> --owner <owner> --name "Status" --data-type SINGLE_SELECT --single-select-options "ToDo,Working,Snoozed,Done"
gh project field-create <number> --owner <owner> --name "Due date" --data-type DATE

# Link repo
gh project link <number> --owner <owner> --repo <owner>/<repo>

# Secret
gh secret set PROJECT_TOKEN

# Test
gh workflow run reminders.yml --repo <owner>/<repo>
```
