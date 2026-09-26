import json
import os
import subprocess
import sys
from datetime import date, timedelta


def run(args, parse=True):
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    output = result.stdout.strip()
    return json.loads(output) if parse else output


def gql(query):
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    if "errors" in data:
        print("GraphQL errors:", data["errors"], file=sys.stderr)
        sys.exit(1)
    return data["data"]


def marker_for(due_date):
    return f"<!-- overdue-reminder:{due_date} -->"


def find_project(owner, title):
    raw = run(["gh", "project", "list", "--owner", owner, "--limit", "100", "--format", "json"])
    projects = raw.get("projects", []) if isinstance(raw, dict) else raw
    for project in projects:
        if project.get("title") == title:
            return project
    return None


def issue_page(repo, number):
    return run(
        ["gh", "api", f"repos/{repo}/issues/{number}/comments", "--paginate"],
        parse=True,
    )


def post_reminder(repo, number, target, due_date, days_late):
    body = (
        f"{marker_for(due_date)}\n\n"
        f"@{target} This issue is {days_late} days past its due date ({due_date}). "
        "Please mark it Done or update its Due date and status."
    )
    subprocess.run(
        ["gh", "api", "-X", "POST", f"repos/{repo}/issues/{number}/comments", "-f", f"body={body}"],
        check=True,
        capture_output=True,
        text=True,
    )
    print(f"reminded @{target} on issue #{number}")


def move_status(project_id, item_id, field_id, option_id):
    query = (
        "mutation {"
        "updateProjectV2ItemFieldValue(input: {"
        f"projectId: \"{project_id}\", itemId: \"{item_id}\", fieldId: \"{field_id}\", "
        f"value: {{singleSelectOptionId: \"{option_id}\"}}"
        "}) { projectV2Item { id } }"
        "}"
    )
    gql(query)
    print(f"moved item {item_id} to Working")


def main():
    repo = os.environ["GH_REPO"]
    owner = os.environ.get("PROJECT_OWNER") or repo.split("/", 1)[0]
    title = os.environ.get("PROJECT_TITLE", "Collaborative Planning")
    default_assignee = os.environ.get("DEFAULT_ASSIGNEE", "zonca")
    overdue_days = int(os.environ.get("OVERDUE_DAYS", "7"))

    project = find_project(owner, title)
    if project is None:
        print(f"Project '{title}' not found for owner {owner}", file=sys.stderr)
        sys.exit(1)
    project_id = project["id"]

    query = f"""
query {{
  node(id: "{project_id}") {{
    ... on ProjectV2 {{
      id
      title
      statusField: field(name: "Status") {{
        ... on ProjectV2SingleSelectField {{
          id
          options {{ id name }}
        }}
      }}
      dueDateField: field(name: "Due date") {{
        ... on ProjectV2Field {{ id }}
      }}
      items(first: 100) {{
        nodes {{
          id
          content {{
            ... on Issue {{
              number
              assignees(first: 10) {{ nodes {{ login }} }}
            }}
            ... on PullRequest {{
              number
            }}
          }}
          fieldValues(first: 50) {{
            nodes {{
              ... on ProjectV2ItemFieldSingleSelectValue {{
                name
                field {{ ... on ProjectV2Field {{ name }} }}
              }}
              ... on ProjectV2ItemFieldDateValue {{
                date
                field {{ ... on ProjectV2Field {{ name }} }}
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""
    data = gql(query)
    project_node = data["node"]
    status_field = project_node.get("statusField") or {}
    due_field = project_node.get("dueDateField") or {}
    options = {opt["name"]: opt["id"] for opt in status_field.get("options", [])}
    working_option = options.get("Working")
    status_field_id = status_field.get("id")

    today = date.today()
    for item in project_node["items"]["nodes"]:
        content = item.get("content") or {}
        number = content.get("number")
        if number is None:
            continue
        status = None
        due = None
        for value in item.get("fieldValues", {}).get("nodes", []):
            field_name = (value.get("field") or {}).get("name")
            if field_name == "Status":
                status = value.get("name")
            elif field_name == "Due date":
                due = value.get("date")
        if due is None:
            continue
        due_date = date.fromisoformat(due)
        if status == "Snoozed" and due_date <= today and working_option and status_field_id:
            move_status(project_id, item["id"], status_field_id, working_option)
        if status == "Done":
            continue
        days_late = (today - due_date).days
        if days_late < overdue_days:
            continue
        assignees = [a["login"] for a in content.get("assignees", {}).get("nodes", [])]
        target = assignees[0] if assignees else default_assignee
        comments = issue_page(repo, number)
        marker = marker_for(due)
        if any(marker in (c.get("body") or "") for c in comments):
            continue
        post_reminder(repo, number, target, due, days_late)


if __name__ == "__main__":
    main()
