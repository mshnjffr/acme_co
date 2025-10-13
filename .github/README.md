# Amp AI PR Review Bot Setup

This repository uses an automated PR review bot powered by [Amp AI](https://ampcode.com) to provide intelligent code reviews on every pull request.

## Features

- 🤖 **Automated Code Review**: AI-powered analysis of every PR
- 🔍 **SOLID Principles Check**: Ensures code follows best practices
- 🐛 **Bug Detection**: Identifies potential issues and bugs
- 🔒 **Security Analysis**: Flags security concerns
- ✅ **Quality Feedback**: Constructive suggestions for improvement
- 👍 **Positive Reinforcement**: Highlights what was done well

## Setup Instructions

### 1. Get Your Amp API Key

1. Visit [https://ampcode.com/settings](https://ampcode.com/settings)
2. Generate an API key (it will look like `sgamp_xxxxxxxxxxxxx`)
3. Copy the key

### 2. Add API Key to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `AMP_API_KEY`
5. Value: Paste your Amp API key
6. Click **Add secret**

### 3. Enable GitHub Actions

The workflow is already configured in `.github/workflows/pr-review.yml`. It will automatically run when:
- A new pull request is opened
- New commits are pushed to an existing PR
- A closed PR is reopened

### 4. Test the Bot

1. Create a new branch:
   ```bash
   git checkout -b test/pr-review-bot
   ```

2. Make a small change (e.g., update README.md)

3. Commit and push:
   ```bash
   git add .
   git commit -m "Test PR review bot"
   git push origin test/pr-review-bot
   ```

4. Open a Pull Request on GitHub

5. Wait for the bot to analyze your PR (usually 30-60 seconds)

6. You should see a comment from the bot with the review!

## What the Bot Reviews

The bot analyzes:
- ✅ Code changes and their impact
- ✅ Adherence to SOLID principles
- ✅ Code quality (DRY, KISS)
- ✅ Potential bugs and edge cases
- ✅ Security vulnerabilities
- ✅ Best practices and patterns
- ✅ Test coverage considerations

## Workflow Details

**File**: `.github/workflows/pr-review.yml`

**Triggers**:
- `pull_request` events: opened, synchronize, reopened

**Permissions**:
- `contents: read` - To read repository files
- `pull-requests: write` - To post review comments

**Environment Variables**:
- `AMP_API_KEY` - Your Amp API key (from secrets)
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions
- `PR_NUMBER` - Pull request number
- `REPO_NAME` - Repository name
- `BASE_SHA` - Base commit SHA
- `HEAD_SHA` - Head commit SHA

## Customization

### Adjust Review Prompt

Edit `.github/scripts/pr-review.js` and modify the `prompt` variable to customize what the bot focuses on:

```javascript
const prompt = `
You are a code review bot. Review this pull request and provide constructive feedback.

// Add your custom instructions here
`;
```

### Change Review Frequency

Modify `.github/workflows/pr-review.yml` triggers:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]  # Customize these events
```

## Troubleshooting

### Bot doesn't comment on PR

1. **Check GitHub Actions logs**:
   - Go to **Actions** tab in your repository
   - Find the failed workflow run
   - Review the logs for errors

2. **Verify API key**:
   - Ensure `AMP_API_KEY` is set in repository secrets
   - Key should start with `sgamp_`

3. **Check permissions**:
   - Workflow needs `pull-requests: write` permission
   - In repo settings, ensure Actions have write permissions

### API Rate Limits

If you hit rate limits:
- The bot will fail gracefully and post an error comment
- Wait a few minutes and re-trigger by pushing a new commit

### Review Takes Too Long

- Normal review time: 30-60 seconds
- Large PRs may take 2-3 minutes
- If it times out, check the GitHub Actions logs

## Cost Considerations

Each PR review consumes Amp API credits. Monitor your usage at [https://ampcode.com/settings](https://ampcode.com/settings).

**Estimated usage**:
- Small PR (1-5 files): ~1,000 tokens
- Medium PR (5-15 files): ~3,000 tokens
- Large PR (15+ files): ~5,000+ tokens

## Disable the Bot

To temporarily disable:

1. Go to `.github/workflows/pr-review.yml`
2. Add `if: false` to the job:
   ```yaml
   jobs:
     review:
       if: false  # Add this line
       runs-on: ubuntu-latest
   ```

Or delete the workflow file entirely.

## Support

- **Amp Documentation**: [https://ampcode.com/manual](https://ampcode.com/manual)
- **SDK Documentation**: [https://www.npmjs.com/package/@sourcegraph/the-orb-is-awake](https://www.npmjs.com/package/@sourcegraph/the-orb-is-awake)
- **Issues**: Open an issue in this repository

---

**Built with [Amp AI](https://ampcode.com) 🚀**
