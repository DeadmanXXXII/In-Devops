### gitnav.py

```python
import argparse
import requests
from base64 import b64decode

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"

def search_repositories(query, token, page=1, per_page=10):
    """Search GitHub repositories with the given query."""
    headers = {"Authorization": f"token {token}"}
    response = requests.get(
        f"{GITHUB_API_URL}/search/repositories",
        params={"q": query, "page": page, "per_page": per_page},
        headers=headers
    )
    response.raise_for_status()
    return response.json()

def fetch_file(repo_full_name, path, token):
    """Fetch a file from a GitHub repository."""
    headers = {"Authorization": f"token {token}"}
    response = requests.get(f"{GITHUB_API_URL}/repos/{repo_full_name}/contents/{path}", headers=headers)
    response.raise_for_status()
    return response.json()["content"]

def decode_content(content):
    """Decode Base64-encoded content."""
    return b64decode(content).decode('utf-8')

def search_keyword_in_content(content, keyword):
    """Check if the keyword is in the content."""
    return keyword.lower() in content.lower()

def main():
    parser = argparse.ArgumentParser(description="Search GitHub repositories and analyze markdown files.")
    parser.add_argument("query", help="Search query for GitHub repositories (e.g., 'machine learning language:Python stars:>100')")
    parser.add_argument("keyword", help="Keyword to search for in markdown files (e.g., 'installation')")
    parser.add_argument("token", help="GitHub personal access token")
    args = parser.parse_args()

    search_query = args.query  # Example: 'machine learning language:Python stars:>100'
    keyword = args.keyword
    token = args.token

    # Print the title
    print("GitNav")
    print("Built by DeadmanXXXII")
    print("=" * 40)
    
    page = 1
    per_page = 10

    while True:
        print(f"Fetching page {page} of search results...")
        search_results = search_repositories(search_query, token, page, per_page)
        repos = search_results.get("items", [])
        if not repos:
            print("No more repositories found.")
            break
        
        for repo in repos:
            print(f"Searching in repository: {repo['full_name']}")
            repo_full_name = repo["full_name"]

            # Check README.md
            try:
                readme_content = fetch_file(repo_full_name, "README.md", token)
                readme_text = decode_content(readme_content)
                if search_keyword_in_content(readme_text, keyword):
                    print(f"Keyword '{keyword}' found in {repo_full_name}/README.md")
            except Exception as e:
                print(f"README.md not found or error fetching for {repo_full_name}: {e}")

            # Check other markdown files
            files_to_check = ["CONTRIBUTING.md", "CHANGELOG.md"]
            for file in files_to_check:
                try:
                    file_content = fetch_file(repo_full_name, file, token)
                    file_text = decode_content(file_content)
                    if search_keyword_in_content(file_text, keyword):
                        print(f"Keyword '{keyword}' found in {repo_full_name}/{file}")
                except Exception:
                    continue

        page += 1

    # Print the end line
    print("=" * 40)

if __name__ == "__main__":
    main()
```


### Running the Script

To execute the script, use the following command from the CLI:

```bash
python search_github.py "machine learning language:Python stars:>100" "installation" "your-github-token"
```

This will produce output like:

```plaintext
GitNav
Built by DeadmanXXXII
========================================
Fetching page 1 of search results...
Searching in repository: example-org/example-repo1
Keyword 'installation' found in example-org/example-repo1/README.md
Keyword 'installation' found in example-org/example-repo1/CONTRIBUTING.md

Searching in repository: example-org/example-repo2
README.md not found or error fetching for example-org/example-repo2: 404 Client Error: Not Found for url: https://api.github.com/repos/example-org/example-repo2/contents/README.md

Fetching page 2 of search results...
Searching in repository: example-org/example-repo4
Keyword 'installation' found in example-org/example-repo4/README.md
Keyword 'installation' found in example-org/example-repo4/CHANGELOG.md

No more repositories found.
========================================
```