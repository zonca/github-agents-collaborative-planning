# SETUP

This guide tells an **agent** how to set up this repository for a human. Run every step you can on your own; stop only where the human has to act (browser, token, keyboard).

Before starting: `gh` CLI must be installed and authenticated (`gh auth status`), and the human must have gone through step 0.

---

## 0. Human prerequisites

The human must do two things that no terminal command can do:

1. **Give `gh` the project scope**:

   ```bash
   gh auth refresh -h github.com -s project,read:project
   ```

   This starts a device flow: the human opens the printed URL and enters the one-time code.

2. **Create a classic personal access token** at https://github.com/settings/tokens/new:
   - Note: anything (e.g. `github-agents-collaborative-planning`)
   - Scopes: `repo` and `project`
   - Expiration: 90 days is a reasonable default

   The human pastes the token to the agent (or sets the secret themselves, see step 4).

> Why a classic token? The reminder workflow needs Projects v2 access plus the GraphQL API. Fine-grained tokens only cover **organization-owned** projects and do not support GraphQL, so for a user-owned project a classic token is the only option.

---

## 1. Create the project

```bash
gh project create --owner <owner> --title "Collaborative Planning" --format json
```

Write down `number` (e.g. `2`) and `id` (starts with `PVT_`).

If the project should be visible to everyone (recommended for a public repo), make it public:

```bash
gh project edit <number> --owner <owner> --visibility PUBLIC
```

## 2. Configure the fields

### Status

A new project already has a built-in `Status` field with `To Do / In Progress / Done`. It cannot be deleted and cannot be edited with `gh project`; use GraphQL to replace its options:

```bash
STATUS_FIELD_ID=$(gh project field-list <number> --owner <owner> --format json --jq '.fields[] | select(.name=="Status") | .id')

gh api graphql --input - <<EOF
{
  "query": "mutation(\$fieldId: ID!, \$options: [ProjectV2SingleSelectFieldOptionInput!]!){ updateProjectV2Field(input: {fieldId: \$fieldId, name: \"Status\", singleSelectOptions: \$options}){ projectV2Field { id } } }",
  "variables": {
    "fieldId": "$STATUS_FIELD_ID",
    "options": [
      {"name": "ToDo", "color": "GRAY", "description": ""},
      {"name": "Working", "color": "GREEN", "description": ""},
      {"name": "Snoozed", "color": "YELLOW", "description": ""},
      {"name": "Done", "color": "PURPLE", "description": ""}
    ]
  }
}
EOF
```

### Due date

```bash
gh project field-create <number> --owner <owner> --name "Due date" --data-type DATE
```

### Link the repository

```bash
gh project link <number> --owner <owner> --repo <owner>/<repo>
```

## 3. Point the workflow at the project

In `.github/workflows/reminders.yml`, set:

```yaml
env:
  PROJECT_NUMBER: "<number>"
```

(The reminder script looks up the project by this number; it does not use `gh project list`, which would require the extra `read:org` scope.)

Adjust the other defaults if needed: `DEFAULT_ASSIGNEE`, `OVERDUE_DAYS`, and the cron time (GitHub cron is UTC: `0 15 * * *` = 08:00 Pacific in daylight saving time, `0 16 * * *` in standard time).

Behavior: the workflow moves an issue from `Snoozed` to `ToDo` on its due date, and sends a reminder at most once per due date (a week after it is missed). No repeated pinging.

## 4. Store the token as a secret

```bash
gh secret set PROJECT_TOKEN
```

The agent asks the human for the token from step 0 (or the human runs this command themselves). Keep the token out of logs and history.

## 5. Test

```bash
gh workflow run reminders.yml --repo <owner>/<repo>
gh run watch --repo <owner>/<repo>
```

Expected: the run succeeds and prints nothing (or a list of moved items). A quick end-to-end check: create a test issue, set its `Due date` to today and `Status` to `Snoozed` on the board — the next run should move it to `ToDo`.

## 6. Automation rules (browser only)

Open the project with `gh project view <number> --owner <owner> --web` or give the human the URL (`https://github.com/users/<owner>/projects/<number>`), then ask them to:

1. Click **⋯** (top right) → **Workflows**.
2. **Auto-add to project** → filter `is:issue,is:open` → enable.
3. **Item added to project** → set `Status: ToDo` → enable.
4. Optional: **Item reopened** → `Status: ToDo`.

This makes every new issue start in `ToDo` automatically.

## 7. Per-collaborator agent file

Create `user_agent/AGENTS_<github-username>.md` for each collaborator (see `user_agent/AGENTS_zonca.md` as an example): fill in contacts (e.g. email tooling), roles, and preferences with the user.

---

## Summary

| Step | Who | What |
| --- | --- | --- |
| 0 | Human | `gh auth refresh` (project scope) + create classic PAT (`repo`, `project`) |
| 1 | Agent | `gh project create` |
| 2 | Agent | Status options via GraphQL, `Due date` field, link repo |
| 3 | Agent | Set `PROJECT_NUMBER` in the workflow |
| 4 | Agent/Human | `gh secret set PROJECT_TOKEN` |
| 5 | Agent | `gh workflow run` + watch |
| 6 | Human | Enable the two automation rules in the browser |
| 7 | Agent | Create per-user agent files |
