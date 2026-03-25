#!/usr/bin/env python3
"""Create Jira issues from a generated backlog JSON payload.

Expected environment variables:
- JIRA_BASE_URL (e.g. https://your-domain.atlassian.net)
- JIRA_EMAIL
- JIRA_API_TOKEN
- JIRA_EPIC_NAME_FIELD (optional, defaults to customfield_10011)

Usage:
    python create_jira_issues.py --backlog backlog.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

import requests
from requests.exceptions import ProxyError, RequestException


ISSUE_TYPE_MAP = {
    "epic": "Epic",
    "story": "Story",
    "task": "Task",
    "subtask": "Sub-task",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Jira issues from backlog JSON.")
    parser.add_argument("--backlog", required=True, help="Path to generated backlog JSON file")
    return parser.parse_args()


def load_backlog(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "project_key" not in data or "items" not in data:
        raise ValueError("Backlog JSON must include 'project_key' and 'items'.")
    if not isinstance(data["items"], list) or not data["items"]:
        raise ValueError("Backlog 'items' must be a non-empty list.")

    return data


def jira_request(
    method: str,
    endpoint: str,
    email: str,
    token: str,
    base_url: str,
    payload: Dict[str, Any],
    item: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}{endpoint}"
    request_kwargs = {
        "method": method,
        "url": url,
        "auth": (email, token),
        "headers": {"Accept": "application/json", "Content-Type": "application/json"},
        "json": payload,
        "timeout": 30,
    }

    print(f"\nRequest payload for {method} {endpoint}:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    try:
        response = requests.request(**request_kwargs)
    except ProxyError as first_proxy_error:
        # Retry once without environment proxy settings. This addresses
        # environments where HTTPS proxy rules block Atlassian traffic.
        try:
            with requests.Session() as session:
                session.trust_env = False
                response = session.request(**request_kwargs)
        except RequestException as second_error:
            raise RuntimeError(
                "Unable to reach Jira API. Proxy request failed and direct connection "
                f"also failed. Proxy error: {first_proxy_error}; direct error: {second_error}"
            ) from second_error
    except RequestException as request_error:
        raise RuntimeError(f"Unable to reach Jira API endpoint {endpoint}: {request_error}") from request_error

    if response.status_code >= 400:
        item_info = ""
        if item:
            item_info = f" while creating {item.get('type', 'item').title()} '{item.get('id', 'unknown')}'"
        print(f"\nERROR: Jira API call failed{item_info}.")
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")
        raise RuntimeError(
            f"Jira API error {response.status_code} for {endpoint}: {response.text}"
        )

    return response.json()


def text_paragraph(text: str) -> Dict[str, Any]:
    return {
        "type": "paragraph",
        "content": [{"type": "text", "text": text}],
    }


def build_description(item: Dict[str, Any]) -> Dict[str, Any]:
    content: List[Dict[str, Any]] = [text_paragraph(item["description"]), text_paragraph("Acceptance Criteria:")]
    for criterion in item.get("acceptance_criteria", []):
        content.append(text_paragraph(f"- {criterion}"))
    return {
        "type": "doc",
        "version": 1,
        "content": content,
    }


def create_issue(
    item: Dict[str, Any],
    project_key: str,
    email: str,
    token: str,
    base_url: str,
    parent_issue_key: str | None = None,
    epic_key: str | None = None,
    epic_name_field: str = "customfield_10011",
    default_original_estimate: str = "1h",
) -> str:
    issue_type = ISSUE_TYPE_MAP[item["type"]]

    fields: Dict[str, Any] = {
        "project": {"key": project_key},
        "summary": item["title"],
        "description": build_description(item),
        "issuetype": {"name": issue_type},
        "labels": item.get("labels", []),
        "timetracking": {
            "originalEstimate": item.get("original_estimate", default_original_estimate),
            "remainingEstimate": item.get("remaining_estimate", item.get("original_estimate", default_original_estimate)),
        },
    }

    if item["type"] == "epic":
        fields[epic_name_field] = item["title"]
    elif item["type"] == "subtask":
        if not parent_issue_key:
            raise ValueError(f"Subtask {item['id']} missing parent issue key.")
        fields["parent"] = {"key": parent_issue_key}
    elif epic_key:
        fields["parent"] = {"key": epic_key}

    payload = {"fields": fields}
    response = jira_request(
        method="POST",
        endpoint="/rest/api/3/issue",
        email=email,
        token=token,
        base_url=base_url,
        payload=payload,
        item=item,
    )
    return response["key"]


def find_existing_issue_key(
    project_key: str,
    summary: str,
    issue_type: str,
    email: str,
    token: str,
    base_url: str,
) -> str | None:
    jql = (
        f'project = "{project_key}" AND summary ~ "\\"{summary}\\"" '
        f'AND issuetype = "{issue_type}" ORDER BY created DESC'
    )
    payload = {
        "jql": jql,
        "fields": ["key"],
        "maxResults": 1,
    }
    response = jira_request(
        method="POST",
        endpoint="/rest/api/3/search/jql",
        email=email,
        token=token,
        base_url=base_url,
        payload=payload,
    )
    issues = response.get("issues", [])
    if not issues:
        return None
    return issues[0]["key"]


def split_items(items: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    epics: List[Dict[str, Any]] = []
    story_tasks: List[Dict[str, Any]] = []
    subtasks: List[Dict[str, Any]] = []

    for item in items:
        item_type = item.get("type")
        if item_type == "epic":
            epics.append(item)
        elif item_type in {"story", "task"}:
            story_tasks.append(item)
        elif item_type == "subtask":
            subtasks.append(item)
        else:
            raise ValueError(f"Unsupported item type: {item_type}")

    return epics, story_tasks, subtasks


def ensure_no_duplicate_titles(items: List[Dict[str, Any]]) -> None:
    seen: Dict[Tuple[str | None, str], str] = {}
    for item in items:
        parent_id = item.get("parent_id")
        normalized_title = " ".join(item.get("title", "").strip().lower().split())
        key = (parent_id, normalized_title)
        existing_id = seen.get(key)
        if existing_id:
            raise ValueError(
                f"Duplicate title in the same parent scope detected: '{item['title']}' "
                f"for items {existing_id} and {item['id']} (parent_id={parent_id})."
            )
        seen[key] = item["id"]


def build_epic_ancestor_map(items: List[Dict[str, Any]]) -> Dict[str, str]:
    by_id = {item["id"]: item for item in items}
    cache: Dict[str, str] = {}

    def resolve_epic_id(item_id: str) -> str:
        if item_id in cache:
            return cache[item_id]
        current = by_id[item_id]
        if current["type"] == "epic":
            cache[item_id] = item_id
            return item_id

        parent_id = current.get("parent_id")
        if not parent_id or parent_id not in by_id:
            raise ValueError(f"Item {item_id} has no valid ancestor epic.")
        epic_id = resolve_epic_id(parent_id)
        cache[item_id] = epic_id
        return epic_id

    for item in items:
        resolve_epic_id(item["id"])

    return cache


def main() -> int:
    args = parse_args()

    base_url = os.getenv("JIRA_BASE_URL")
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")
    epic_name_field = os.getenv("JIRA_EPIC_NAME_FIELD", "customfield_10011")
    default_original_estimate = os.getenv("JIRA_DEFAULT_ORIGINAL_ESTIMATE", "1h")

    if not base_url or not email or not token:
        print(
            "Missing required environment variables: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN",
            file=sys.stderr,
        )
        return 1

    backlog = load_backlog(args.backlog)
    project_key: str = os.getenv("JIRA_PROJECT_KEY") or backlog["project_key"]
    items: List[Dict[str, Any]] = backlog["items"]

    host = urlparse(base_url).netloc
    print(f"Using Jira host: {host}")
    print(f"Using Jira project key: {project_key}")

    ensure_no_duplicate_titles(items)
    epics, story_tasks, subtasks = split_items(items)
    epic_ancestor_by_id = build_epic_ancestor_map(items)

    local_to_jira_key: Dict[str, str] = {}
    created_epics: List[Tuple[str, str]] = []
    created_story_tasks: List[Tuple[str, str]] = []
    created_subtasks: List[Tuple[str, str]] = []

    print("Creating Epics...")
    for item in epics:
        issue_type = ISSUE_TYPE_MAP[item["type"]]
        key = find_existing_issue_key(
            project_key=project_key,
            summary=item["title"],
            issue_type=issue_type,
            email=email,
            token=token,
            base_url=base_url,
        )
        if key:
            print(f"Reusing existing Epic: {item['id']} -> {key}")
        else:
            key = create_issue(
                item=item,
                project_key=project_key,
                email=email,
                token=token,
                base_url=base_url,
                epic_name_field=epic_name_field,
                default_original_estimate=default_original_estimate,
            )
        local_to_jira_key[item["id"]] = key
        print(f"Created Epic: {item['id']} -> {key}")
        created_epics.append((item["id"], key))

    print("Creating Stories/Tasks...")
    for item in story_tasks:
        issue_type = ISSUE_TYPE_MAP[item["type"]]
        key = find_existing_issue_key(
            project_key=project_key,
            summary=item["title"],
            issue_type=issue_type,
            email=email,
            token=token,
            base_url=base_url,
        )
        if key:
            print(f"Reusing existing {item['type'].title()}: {item['id']} -> {key}")
        else:
            epic_id = epic_ancestor_by_id[item["id"]]
            epic_key = local_to_jira_key.get(epic_id)
            key = create_issue(
                item=item,
                project_key=project_key,
                email=email,
                token=token,
                base_url=base_url,
                epic_key=epic_key,
                epic_name_field=epic_name_field,
                default_original_estimate=default_original_estimate,
            )
        local_to_jira_key[item["id"]] = key
        print(f"Created {item['type'].title()}: {item['id']} -> {key}")
        created_story_tasks.append((item["id"], key))

    if subtasks:
        print("Creating Subtasks...")
    for item in subtasks:
        issue_type = ISSUE_TYPE_MAP[item["type"]]
        key = find_existing_issue_key(
            project_key=project_key,
            summary=item["title"],
            issue_type=issue_type,
            email=email,
            token=token,
            base_url=base_url,
        )
        if key:
            print(f"Reusing existing Subtask: {item['id']} -> {key}")
        else:
            parent_id = item.get("parent_id")
            parent_issue_key = local_to_jira_key.get(parent_id)
            key = create_issue(
                item=item,
                project_key=project_key,
                email=email,
                token=token,
                base_url=base_url,
                parent_issue_key=parent_issue_key,
                epic_name_field=epic_name_field,
                default_original_estimate=default_original_estimate,
            )
        local_to_jira_key[item["id"]] = key
        print(f"Created Subtask: {item['id']} -> {key}")
        created_subtasks.append((item["id"], key))

    print("\nCreated Jira issue keys:")
    for local_id, issue_key in local_to_jira_key.items():
        print(f"- {local_id}: {issue_key}")

    print("\nSummary")
    print("Epics:")
    for local_id, issue_key in created_epics:
        print(f"- {local_id} -> {issue_key}")
    print("Stories/Tasks:")
    for local_id, issue_key in created_story_tasks:
        print(f"- {local_id} -> {issue_key}")
    print("Subtasks:")
    for local_id, issue_key in created_subtasks:
        print(f"- {local_id} -> {issue_key}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
