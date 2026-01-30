import requests
from datetime import datetime

GITHUB_USERNAME = "anabxalves"
HEADER_TARGET = "### 🗞️ Latest Activity"

def get_latest_github_activity():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public"
    try:
        response = requests.get(url)
        response.raise_for_status()
        events = response.json()
    except Exception:
        return "⚠️ *Unable to fetch recent activity at the moment.*"

    activity = []
    for event in events:
        if len(activity) >= 5: break

        event_type = event.get('type')
        repo_name = event.get('repo', {}).get('name', '').split('/')[-1]
        payload = event.get('payload', {})

        if event_type == 'PushEvent':
            commits = payload.get('commits', [])
            if commits:
                msg = commits[0]['message'].split('\n')[0]
                if not any(skip in msg.lower() for skip in ["docs:", "readme-bot", "update readme"]):
                    activity.append(f"🔹 **Push**: `{msg}` in `{repo_name}`")

        elif event_type == 'PullRequestEvent':
            action = payload.get('action')
            pr = payload.get('pull_request', {})
            title = pr.get('title')

            if title:
                activity.append(f"📦 **PR {action.capitalize()}**: `{title}` in `{repo_name}`")

        elif event_type == 'CreateEvent' and payload.get('ref_type') == 'repository':
            activity.append(f"🚀 **New Project**: Started `{repo_name}`")

    if not activity:
        return "*No public activity detected in the last 30 days.*"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    footer = f"\n\n> 🕒 *Last synced: {now}*"

    return "\n".join(activity) + footer

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    if HEADER_TARGET not in content:
        return

    static_content = content.split(HEADER_TARGET)[0]
    new_activity = get_latest_github_activity()

    updated_content = f"{static_content}{HEADER_TARGET}\n\n{new_activity}\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()