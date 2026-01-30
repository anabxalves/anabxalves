import requests
import re

GITHUB_USERNAME = "anabxalves"

def get_latest_github_activity():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public"
    response = requests.get(url).json()
    activity = []
    
    for event in response:
        if len(activity) >= 5: break
        
        if event['type'] == 'PushEvent':
            payload = event.get('payload', {})
            commits = payload.get('commits', [])
            
            if not commits:
                continue

            repo = event['repo']['name'].replace(f"{GITHUB_USERNAME}/", "")
            msg = commits[0]['message'].split('\n')[0]
            
            if any(skip in msg.lower() for skip in ["docs:", "readme-bot", "update readme", "skip ci"]):
                continue
                
            activity.append(f"- **{repo}**: {msg}")
            
    return "\n".join(activity) if activity else "No recent public activity!"

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_activity = get_latest_github_activity()
    
    pattern = r"().*()"
    updated_content = re.sub(pattern, f"\\1\n{new_activity}\n\\2", content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()
