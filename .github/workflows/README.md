# GitHub Actions Workflows

## Manage Gist from Issue Comments

This workflow automatically manages the gist content when specific commands are commented on issues.

### How it works

When you comment on an issue with the following commands, the workflow will automatically update the corresponding gist file:

#### ADD Command
```
ADD <section> <URL>
```
- `<section>`: The name of the JSON file in the gist (without `.json` extension)
- `<URL>`: The URL to add to the section

Example:
```
ADD friends https://example.com/feed.xml
```

This will:
1. Check if the URL is accessible
2. Fetch the content from `friends.json` in the gist
3. Add the URL to the list (if not already present)
4. Update the gist file

#### DELETE Command
```
DELETE <section> <URL>
```
- `<section>`: The name of the JSON file in the gist (without `.json` extension)
- `<URL>`: The URL to remove from the section

Example:
```
DELETE friends https://example.com/feed.xml
```

This will:
1. Fetch the content from `friends.json` in the gist
2. Remove the URL from the list (if present)
3. Update the gist file

### Setup Requirements

To use this workflow, you need to set up the following secret:

- `GIST_TOKEN`: A GitHub Personal Access Token with `gist` scope to update the gist at `https://gist.github.com/caibingcheng/adf8f300dc50a61a965bdcc6ef0aecb3`

The workflow automatically uses the `GITHUB_TOKEN` provided by GitHub Actions to post feedback comments.

### Workflow Behavior

- The workflow triggers on issue comments (when a comment is created)
- **Security**: It only runs if the comment author is the repository owner (caibingcheng)
- It only runs if the comment contains "ADD " or "DELETE " commands
- After processing, it posts a comment with the result:
  - ✅ Success message if the operation completed
  - ❌ Error message if the URL is not accessible or operation failed
  - ℹ️ Info message if the URL already exists (ADD) or doesn't exist (DELETE)

### Gist Structure

The gist files are expected to be JSON arrays of URLs:
```json
[
  "https://example1.com/feed.xml",
  "https://example2.com/rss.xml"
]
```

Each section corresponds to a file in the gist: `https://gist.github.com/caibingcheng/adf8f300dc50a61a965bdcc6ef0aecb3#file-<section>-json`
