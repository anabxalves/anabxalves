import requests

GITHUB_USERNAME = "anabxalves"
HEADER_TARGET = "### 🗞️ Latest Activity"

def get_latest_github_activity():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public"
    try:
        response = requests.get(url)
        response.raise_for_status()
        events = response.json()
    except Exception as e:
        return f"⚠️ Error fetching activity: {e}"

    activity = []
    for event in events:
        if len(activity) >= 5: break

        event_type = event.get('type')
        repo_name = event.get('repo', {}).get('name', '').replace(f"{GITHUB_USERNAME}/", "")

        if event_type == 'PushEvent':
            commits = event.get('payload', {}).get('commits', [])
            if commits:
                msg = commits[0]['message'].split('\n')[0]
                if not any(skip in msg.lower() for skip in ["docs:", "readme-bot", "update readme", "skip ci"]):
                    activity.append(f"🛠️ **Push**: {msg} ({repo_name})")

        elif event_type == 'PullRequestEvent':
            action = event.get('payload', {}).get('action')
            title = event.get('payload', {}).get('pull_request', {}).get('title')
            activity.append(f"📦 **PR {action}**: {title} ({repo_name})")

        elif event_type == 'CreateEvent' and event.get('payload', {}).get('ref_type') == 'repository':
            activity.append(f"🌟 **Created Repo**: {repo_name}")

    return "\n".join(activity) if activity else "*No public activity in the last 30 days.*"

def update_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("README.md not found.")
        return

    if HEADER_TARGET not in content:
        print(f"Error: Could not find '{HEADER_TARGET}' in README.md")
        return

    static_content = content.split(HEADER_TARGET)[0]
    new_activity = get_latest_github_activity()

    updated_content = f"{static_content}{HEADER_TARGET}\n\n{new_activity}\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()