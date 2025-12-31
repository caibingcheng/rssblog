# Workflow Usage Examples

This document provides examples of how to use the "Manage Gist from Issue Comments" workflow.

## Prerequisites

Before using the workflow, ensure the repository owner has configured the `GIST_TOKEN` secret:

1. Go to repository Settings → Secrets and variables → Actions
2. Add a new secret named `GIST_TOKEN`
3. Value should be a GitHub Personal Access Token with `gist` scope
4. This token will be used to update the gist at `https://gist.github.com/caibingcheng/adf8f300dc50a61a965bdcc6ef0aecb3`

## Example Usage

### Adding a URL to a section

Comment on any issue with:
```
ADD friends https://example.com/feed.xml
```

The workflow will:
1. ✅ Check if `https://example.com/feed.xml` is accessible
2. ✅ Fetch the current content of `friends.json` from the gist
3. ✅ Add the URL to the list (if not already present)
4. ✅ Update the gist file
5. ✅ Post a confirmation comment

**Example comment from the bot:**
```
✅ Successfully added `https://example.com/feed.xml` to `friends.json`
```

### Deleting a URL from a section

Comment on any issue with:
```
DELETE friends https://example.com/feed.xml
```

The workflow will:
1. ✅ Fetch the current content of `friends.json` from the gist
2. ✅ Remove the URL from the list (if present)
3. ✅ Update the gist file
4. ✅ Post a confirmation comment

**Example comment from the bot:**
```
✅ Successfully removed `https://example.com/feed.xml` from `friends.json`
```

### Multiple commands in one comment

You can include ADD or DELETE commands along with other text:
```
I'd like to add my blog to the friends section.

ADD friends https://myblog.example.com/rss.xml

Thanks!
```

**Note:** The workflow will only process the first matching command found in the comment.

### Error scenarios

#### URL not accessible
If the URL returns an error or non-2xx status code:
```
❌ URL is not accessible: https://broken-site.example.com/feed.xml
```

#### URL already exists
If you try to ADD a URL that's already in the list:
```
ℹ️ URL `https://example.com/feed.xml` already exists in `friends.json`
```

#### URL not found
If you try to DELETE a URL that's not in the list:
```
ℹ️ URL `https://example.com/feed.xml` not found in `friends.json`
```

## Gist File Structure

Each section in the gist is stored as a JSON file containing an array of URLs:

**Example `friends.json`:**
```json
[
  "https://example1.com/feed.xml",
  "https://example2.com/rss.xml",
  "https://example3.com/atom.xml"
]
```

The gist URL structure is:
```
https://gist.github.com/caibingcheng/adf8f300dc50a61a965bdcc6ef0aecb3#file-<section>-json
```

For example:
- `friends` section → `friends.json` → https://gist.github.com/caibingcheng/adf8f300dc50a61a965bdcc6ef0aecb3#file-friends-json
- `tech` section → `tech.json` → https://gist.github.com/caibingcheng/adf8f300dc50a61a965bdcc6ef0aecb3#file-tech-json

## Workflow Trigger Conditions

The workflow only runs when:
1. A comment is created on an issue
2. **The comment author is the repository owner (caibingcheng)**
3. The comment contains "ADD " or "DELETE " (with space after the keyword)

This prevents accidental triggers from words like "ADDON" or "DELETED" in regular comments, and ensures only the repository owner can modify the gist.

## Security Features

- ✅ **Owner-only access**: Only the repository owner (caibingcheng) can trigger the workflow
- ✅ Uses Bearer token authentication (modern standard)
- ✅ Explicit permission grants (issues: write, contents: read)
- ✅ Specific exception handling for network errors
- ✅ URL validation (only 2xx status codes considered accessible)
- ✅ Environment variable validation
- ✅ Response validation for all API calls
- ✅ No secrets exposed in logs

## Troubleshooting

### Workflow doesn't trigger
- **Verify you are the repository owner (caibingcheng)** - only the owner can trigger this workflow
- Check that your comment contains "ADD " or "DELETE " (with space)
- Verify you're commenting on an issue, not a pull request

### "GIST_TOKEN secret not found" error
- Repository admin needs to add the `GIST_TOKEN` secret in repository settings

### "URL is not accessible" error
- Check that the URL is correct and returns a 2xx HTTP status code
- Verify the site is not blocking automated requests
- Try accessing the URL in a browser to confirm it works

### "Failed to update gist file" error
- Check that the `GIST_TOKEN` has the correct `gist` scope
- Verify the gist ID is correct in the workflow file
- Ensure the token hasn't expired
