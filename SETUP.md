# SETUP

This guide is for an **agent** helping a human set up this repository. The agent should perform every step it can on its own and only stop when user input is genuinely required.

The user must have the GitHub CLI (`gh`) installed and authenticated (`gh auth status`) with a token that has at least the `project`, `repo`, and `workflow` scopes (`gh auth refresh -h github.com -s project,read:project`).

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

GitHub Projects ships with a built-in `Status` field (options `Todo / In Progress / Done`) that **cannot be deleted** and cannot be edited through the `gh` CLI. Set exactly our four options with the GraphQL API instead:

```bash
gh api graphql --input - <<'EOF'
{
  "query": "mutation($fieldId: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]!){ updateProjectV2Field(input: {fieldId: $fieldId, name: \"Status\", singleSelectOptions: $options}){ projectV2Field { ... on ProjectV2SingleSelectField { id name options { id name } } } } }",
  "variables": {
    "fieldId": "<STATUS_FIELD_ID>",
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

Find the Status field ID first with:

```bash
gh project field-list <number> --owner <owner> --format json --jq '.fields[] | select(.name=="Status") | .id'
```

Valid colors: `GRAY`, `BLUE`, `GREEN`, `YELLOW`, `ORANGE`, `RED`, `PINK`, `PURPLE`.

### 2b. Due date field

```bash
gh project field-create <number> --owner <owner> --name "Due date" --data-type DATE
```

### 2c. Link the repository

```bash
gh project link <number> --owner <owner> --repo <owner>/<repo>
```

### 2d. Automation rules (browser only)

There is no CLI or API for project automation rules; configure them in the browser. Open the project with `gh project view <number> --owner <owner> --web`, then:

1. Click the **⋯** (top right) → **Workflows**.
2. **Auto-add to project**: filter for the repository (`is:issue,is:open`) → *Save and turn on workflow*. This makes every new issue land in the project.
3. **Item added to project**: set `Status: ToDo` → *Save and turn on workflow*.
4. Optional: **Item reopened** → `Status: ToDo`.

---

## 3. Create the token for the workflow

The reminder workflow needs a **classic** personal access token.

> Why not a fine-grained PAT? Fine-grained tokens have a `Projects` permission only for **organization-owned** projects; user-owned projects (like this one, owned by `zonca`) cannot be accessed by fine-grained tokens. Fine-grained tokens also cannot use the GraphQL API, which the reminder script depends on.

Ask the user to create a classic token at <https://github.com/settings/tokens/new> with:

- **Note**: `github-agents-collaborative-planning`
- **Expiration**: per user preference (90 days is a reasonable default)
- **Scopes**: `repo` (carries Issues read/write) and `project` (Projects v2 read/write)

Ask the user to paste the token (it is shown only once), then store it as a repository secret without printing it:

```bash
gh secret set PROJECT_TOKEN
```

`gh` prompts for the value securely; do not write the token to the terminal history or anywhere else.

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

- GitHub Actions cron schedules are in **UTC**, not local time. `0 15 * * *` equals 08:00 Pacific during daylight saving; use `0 16 * * *` for 08:00 during standard time.
- Scheduled workflows run only on the default branch and only if Actions are enabled for the repository. If the user created the repo from a fork, Actions may be disabled — enable them under *Settings → Actions → General*.

### Verify

Trigger a manual test run (after the secret is set):

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
gh auth refresh -h github.com -s project,read:project

# Create project
gh project create --owner <owner> --title "Collaborative Planning" --format json

# Status options (GraphQL, see section 2a)
gh api graphql --input - <<'EOF'
{ "query": "mutation($fieldId: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]!){ updateProjectV2Field(input: {fieldId: $fieldId, name: \"Status\", singleSelectOptions: $options}){ projectV2Field { ... on ProjectV2SingleSelectField { id } } } }", "variables": { "fieldId": "<STATUS_FIELD_ID>", "options": [{"name":"ToDo","color":"GRAY","description":""},{"name":"Working","color":"GREEN","description":""},{"name":"Snoozed","color":"YELLOW","description":""},{"name":"Done","color":"PURPLE","description":""}] } }
EOF

# Due date field + link repo
gh project field-create <number> --owner <owner> --name "Due date" --data-type DATE
gh project link <number> --owner <owner> --repo <owner>/<repo>

# Secret (classic PAT: repo + project scopes)
gh secret set PROJECT_TOKEN

# Test
gh workflow run reminders.yml --repo <owner>/<repo>
```
