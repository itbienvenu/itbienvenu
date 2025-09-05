import os
import requests

USERNAME = os.getenv("itbienvenu")
TOKEN = os.getenv("PRIVATE_TOKEN")
README_FILE = "README.md"

# Fetch all repos (including private)
url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=all"
response = requests.get(url, auth=(USERNAME, TOKEN))
repos = response.json()

# Filter private repos
private_repos = [r for r in repos if r.get('private')]

# Prepare content for private repos
lines = ["\n# My Private Repos\n"]
for repo in private_repos:
    lines.append(f"- [{repo['name']}]({repo['html_url']}): {repo.get('description') or 'No description'}\n")

# Read current README
with open(README_FILE, "r") as f:
    readme = f.read()

# Markers
start_marker = "<!--PRIVATE-REPOS-START-->"
end_marker = "<!--PRIVATE-REPOS-END-->"

# Check if markers exist
start_index = readme.find(start_marker)
end_index = readme.find(end_marker)

if start_index != -1 and end_index != -1:
    # Replace section between markers
    new_readme = readme[:start_index + len(start_marker)] + "\n" + "".join(lines) + readme[end_index:]
else:
    # Add markers + content at the end if they don't exist
    new_readme = readme + "\n" + start_marker + "\n" + "".join(lines) + end_marker

# Write back to README
with open(README_FILE, "w") as f:
    f.write(new_readme)
