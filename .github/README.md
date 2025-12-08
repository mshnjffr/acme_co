# Amp PR Review Bot - Complete Implementation Guide

This repository uses an automated PR review bot powered by [Amp](https://ampcode.com) to provide intelligent code reviews on every pull request. This guide will help you implement the same bot in your own repository.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Architecture Overview](#architecture-overview)
- [Quick Setup (5 Minutes)](#quick-setup-5-minutes)
- [Detailed Setup Instructions](#detailed-setup-instructions)
- [File Structure Explanation](#file-structure-explanation)
- [How It Works](#how-it-works)
- [Customization Guide](#customization-guide)
- [What the Bot Reviews](#what-the-bot-reviews)
- [Example Review Output](#example-review-output)
- [Troubleshooting](#troubleshooting)
- [Cost & Performance](#cost--performance)
- [Security Considerations](#security-considerations)
- [Advanced Configuration](#advanced-configuration)
- [FAQ](#faq)

## Features

- 🤖 **Automated Code Review**: AI-powered analysis of every PR using GPT-4 level intelligence
- 🔍 **SOLID Principles Check**: Ensures code follows best practices and design patterns
- 🐛 **Bug Detection**: Identifies potential issues, edge cases, and logic errors
- 🔒 **Security Analysis**: Flags security vulnerabilities and concerns
- ✅ **Quality Feedback**: Constructive suggestions for improvement
- 👍 **Positive Reinforcement**: Highlights what was done well
- 📊 **Test Coverage**: Suggests areas that need testing
- 🎯 **Context-Aware**: Understands your codebase and provides relevant feedback
- ⚡ **Fast**: Reviews complete in 30-60 seconds
- 💬 **GitHub Integration**: Posts reviews as PR comments automatically

## Prerequisites

Before implementing this bot, you'll need:

1. **GitHub Repository**: A repository where you have admin access
2. **Amp Account**: Sign up at [ampcode.com](https://ampcode.com)
3. **Amp API Key**: Available in your [Amp settings](https://ampcode.com/settings)
4. **GitHub Actions Enabled**: Should be enabled by default on public repos
5. **Node.js 18+**: Required for the bot script (handled by GitHub Actions)

**Cost**: Amp has a free tier. Check pricing at [ampcode.com/pricing](https://ampcode.com/pricing)

## Architecture Overview

The PR review bot consists of three main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Pull Request                      │
│                     (Trigger Event)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Actions Workflow                        │
│         (.github/workflows/pr-review.yml)                   │
│  • Checks out code                                          │
│  • Sets up Node.js environment                              │
│  • Installs dependencies                                    │
│  • Runs review script                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│               Review Script                                 │
│         (.github/scripts/pr-review.js)                      │
│  • Gets PR diff and changed files                           │
│  • Calls Amp with review prompt                          │
│  • Receives AI analysis                                     │
│  • Posts comment to PR                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Amp Service                            │
│              (@sourcegraph/amp-sdk)                │
│  • Analyzes code changes                                    │
│  • Reviews for bugs, security, quality                      │
│  • Returns detailed feedback                                │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Developer opens/updates a PR** → GitHub webhook triggers
2. **GitHub Actions starts** → Checks out code, sets up environment
3. **Review script executes** → Gets diff, calls Amp
4. **Amp analyzes** → Reviews code, generates feedback
5. **Script posts comment** → Review appears on PR as a comment

## Quick Setup (5 Minutes)

Follow these steps to get the bot running quickly:

### Step 1: Get Your Amp API Key (1 minute)

1. Visit [https://ampcode.com/settings](https://ampcode.com/settings)
2. Click "Generate API Key"
3. Copy the key (format: `sgamp_xxxxxxxxxxxxx`)

### Step 2: Add API Key to GitHub Secrets (1 minute)

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Set:
   - **Name**: `AMP_API_KEY`
   - **Secret**: Paste your API key
5. Click **Add secret**

### Step 3: Copy Bot Files to Your Repo (2 minutes)

Create the following directory structure in your repository:

```
your-repo/
├── .github/
│   ├── workflows/
│   │   └── pr-review.yml          # GitHub Actions workflow
│   └── scripts/
│       ├── package.json            # Node.js dependencies
│       └── pr-review.js            # Review script
```

Copy these three files from this repository to yours:
- [`.github/workflows/pr-review.yml`](workflows/pr-review.yml)
- [`.github/scripts/package.json`](scripts/package.json)
- [`.github/scripts/pr-review.js`](scripts/pr-review.js)

### Step 4: Test the Bot (1 minute)

1. Create a test branch and make a small change:
   ```bash
   git checkout -b test/pr-bot
   echo "# Test" >> README.md
   git add README.md
   git commit -m "Test PR review bot"
   git push origin test/pr-bot
   ```

2. Open a Pull Request on GitHub

3. Wait 30-60 seconds and check the PR for a review comment! 🎉

## Detailed Setup Instructions

### Understanding the Files

Your bot implementation requires exactly **3 files**:

#### 1. `.github/workflows/pr-review.yml` - GitHub Actions Workflow

**Purpose**: Orchestrates the entire review process when a PR is created or updated.

**Key Sections Explained**:

```yaml
name: PR Review Bot

# WHEN TO RUN: Triggers on PR events
on:
  pull_request:
    types: [opened, synchronize, reopened]
    # opened: New PR created
    # synchronize: New commits pushed to existing PR
    # reopened: Closed PR is reopened

# PERMISSIONS: What the workflow can access
permissions:
  contents: read           # Read repository files
  pull-requests: write     # Post comments on PRs

jobs:
  review:
    runs-on: ubuntu-latest  # Ubuntu VM with Node.js available
    
    steps:
      # 1. Get the code
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git diff
      
      # 2. Setup Node.js (required for Amp SDK)
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'  # Use Node 20 (has built-in fetch)
      
      # 3. Install dependencies (@sourcegraph/amp-sdk)
      - name: Install dependencies
        run: |
          cd .github/scripts
          npm install
      
      # 4. Run the review script
      - name: Run Amp PR Review
        env:
          # These environment variables are passed to the script
          AMP_API_KEY: ${{ secrets.AMP_API_KEY }}      # Your API key
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}    # Auto-provided by GitHub
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPO_NAME: ${{ github.repository }}          # owner/repo format
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
        run: node .github/scripts/pr-review.js
```

**Customization Options**:
- Change `node-version` if you need a specific Node.js version
- Add more triggers (e.g., `labeled`, `review_requested`)
- Add conditions with `if:` to skip certain PRs
- Adjust timeouts with `timeout-minutes:`

---

#### 2. `.github/scripts/package.json` - Node.js Dependencies

**Purpose**: Defines the Node.js packages required for the review script.

**Contents Explained**:

```json
{
  "name": "amp-pr-review-bot",
  "version": "1.0.0",
  "description": "Automated PR review bot using Amp SDK",
  "type": "module",                    // IMPORTANT: Enables ES modules (import/export)
  "main": "pr-review.js",
  "scripts": {
    "review": "node pr-review.js"
  },
  "dependencies": {
    "@sourcegraph/amp-sdk": "latest"  // Amp SDK
  },
  "engines": {
    "node": ">=18.0.0"                 // Requires Node 18+ (for fetch API)
  }
}
```

**Why ES Modules?**: 
The Amp SDK uses modern JavaScript with `import` statements instead of `require()`. Setting `"type": "module"` enables this.

---

#### 3. `.github/scripts/pr-review.js` - Review Script

**Purpose**: The main script that analyzes the PR and posts the review.

**High-Level Flow**:

```javascript
// 1. IMPORT DEPENDENCIES
import { execute } from '@sourcegraph/amp-sdk';  // Amp SDK
import { execSync } from 'child_process';                // For git commands

// 2. FUNCTION: Post comment to GitHub PR
async function postComment(prNumber, comment) {
  // Uses GitHub API to post a comment
  // Authenticates with GITHUB_TOKEN
  // Posts to: /repos/{owner}/{repo}/issues/{prNumber}/comments
}

// 3. FUNCTION: Get PR changes
async function getDiffSummary() {
  // Runs: git diff BASE_SHA..HEAD_SHA
  // Returns: { diff, filesChanged }
}

// 4. MAIN FUNCTION: Review the PR
async function reviewPullRequest() {
  // A. Validate environment variables
  // B. Get PR diff and file list
  // C. Build review prompt for Amp
  // D. Call Amp with execute()
  // E. Stream response and extract result
  // F. Post review as PR comment
}

// 5. RUN IT
reviewPullRequest();
```

**Key Code Sections Explained**:

```javascript
// POSTING COMMENTS TO GITHUB
async function postComment(prNumber, comment) {
  const [owner, repo] = process.env.REPO_NAME.split('/');
  const token = process.env.GITHUB_TOKEN;
  
  const url = `https://api.github.com/repos/${owner}/${repo}/issues/${prNumber}/comments`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Accept': 'application/vnd.github.v3+json',     // GitHub API version
      'Authorization': `Bearer ${token}`,              // Authentication
      'Content-Type': 'application/json',
      'User-Agent': 'Amp-PR-Review-Bot',              // Required by GitHub
    },
    body: JSON.stringify({
      body: String(comment),  // Comment text (Markdown supported)
    }),
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to post comment: ${response.status} - ${errorText}`);
  }
  
  return response.json();
}

// GETTING PR CHANGES
async function getDiffSummary() {
  try {
    const baseSha = process.env.BASE_SHA;  // PR base branch commit
    const headSha = process.env.HEAD_SHA;  // PR head branch commit
    
    // Get diff statistics (files changed, lines added/removed)
    const diff = execSync(`git diff ${baseSha}..${headSha} --stat`, { encoding: 'utf-8' });
    
    // Get list of changed file paths
    const filesChanged = execSync(`git diff ${baseSha}..${headSha} --name-only`, { encoding: 'utf-8' });
    
    return {
      diff,
      filesChanged: filesChanged.split('\n').filter(f => f.trim()),
    };
  } catch (error) {
    console.error('Error getting diff:', error.message);
    return { diff: 'Unable to get diff', filesChanged: [] };
  }
}

// CALLING AMP AI
for await (const message of execute({
  prompt: `Your review instructions...`,  // What to review
  options: {
    dangerouslyAllowAll: true,  // Skip permission prompts (required for automation)
    cwd: process.cwd(),         // Working directory
  },
})) {
  if (message.type === 'assistant') {
    console.log('🔄 Amp is analyzing...');
  } else if (message.type === 'result') {
    // Final result is here
    if (message.is_error) {
      console.error('❌ Review Failed:', message.error);
    } else {
      console.log('✅ Review Completed');
      reviewResult = message.result;  // The actual review text
    }
    break;
  }
}
```

## File Structure Explanation

After setup, your repository should have this structure:

```
your-repository/
│
├── .github/
│   ├── workflows/
│   │   └── pr-review.yml          # 📋 GitHub Actions workflow definition
│   │                              #    Triggers: PR events
│   │                              #    Runs: Install deps → Execute review script
│   │                              #    Permissions: read contents, write PR comments
│   │
│   ├── scripts/
│   │   ├── package.json           # 📦 Node.js dependencies
│   │   │                          #    Dependencies: @sourcegraph/amp-sdk
│   │   │                          #    Type: ES module (for import/export)
│   │   │
│   │   └── pr-review.js           # 🤖 Main review script
│   │                              #    1. Gets PR diff via git
│   │                              #    2. Calls Amp with review prompt
│   │                              #    3. Posts review to PR as comment
│   │
│   └── README.md                  # 📖 This documentation file
│
├── (your application code...)
```

### What Each File Does

| File | Purpose | Can Skip? |
|------|---------|-----------|
| `pr-review.yml` | Defines when and how the bot runs | ❌ Required |
| `package.json` | Lists npm dependencies | ❌ Required |
| `pr-review.js` | Contains review logic | ❌ Required |
| `.github/README.md` | Documentation | ✅ Optional |

## How It Works

### Step-by-Step Execution Flow

1. **Developer Activity**
   ```
   Developer opens PR or pushes commits
   ↓
   GitHub webhook triggers "pull_request" event
   ```

2. **GitHub Actions Starts**
   ```
   Actions runner starts Ubuntu VM
   ↓
   Checks out repository code (with full git history)
   ↓
   Installs Node.js 20
   ```

3. **Dependencies Installation**
   ```
   cd .github/scripts
   npm install
   ↓
   Installs @sourcegraph/amp-sdk package
   ```

4. **Review Script Executes**
   ```
   node .github/scripts/pr-review.js
   ↓
   Reads environment variables (API key, PR info)
   ↓
   Runs: git diff BASE_SHA..HEAD_SHA
   ↓
   Builds review prompt with file changes
   ```

5. **Amp Analysis**
   ```
   Script calls execute() with prompt
   ↓
   Amp analyzes:
   - Code changes (what was added/removed)
   - File structure (what files were modified)
   - Code patterns (SOLID, DRY, KISS principles)
   - Potential bugs (edge cases, logic errors)
   - Security issues (injection, exposure, etc.)
   - Best practices (language-specific conventions)
   ↓
   Returns detailed review text
   ```

6. **Post Review Comment**
   ```
   Script receives review from Amp
   ↓
   Formats as Markdown
   ↓
   POST to GitHub API: /repos/{owner}/{repo}/issues/{pr}/comments
   ↓
   Review comment appears on PR
   ```

### Timing

- **Small PR (1-5 files)**: 30-45 seconds
- **Medium PR (5-15 files)**: 45-90 seconds
- **Large PR (15+ files)**: 90-180 seconds

## Customization Guide

### 1. Change What Gets Reviewed

Edit the `prompt` variable in `.github/scripts/pr-review.js`:

```javascript
const prompt = `
You are a senior software engineer reviewing a pull request.

**Context**: This is a ${languageOrFramework} project.

**Files Changed**:
${filesChanged.join('\n')}

**Diff Summary**:
${diff}

**Review Focus Areas**:
1. Architecture and design patterns
2. Performance implications
3. Error handling
4. Documentation completeness
5. Breaking changes

**Output Format**:
- Use bullet points
- Be specific with line numbers when possible
- Suggest improvements with code examples
- Rate overall quality (1-10)

Keep the review concise and actionable.
`;
```

**Customization Ideas**:
- Add language-specific checks (e.g., TypeScript types, Python type hints)
- Focus on specific frameworks (React hooks, FastAPI patterns)
- Check for documentation requirements
- Enforce team coding standards
- Check commit message quality

### 2. Filter Which PRs Get Reviewed

Add conditions to `.github/workflows/pr-review.yml`:

```yaml
jobs:
  review:
    runs-on: ubuntu-latest
    # Only review PRs that:
    # - Target 'main' or 'develop' branch
    # - Don't have 'skip-review' label
    # - Aren't from dependabot
    if: |
      github.event.pull_request.base.ref == 'main' &&
      !contains(github.event.pull_request.labels.*.name, 'skip-review') &&
      github.event.pull_request.user.login != 'dependabot[bot]'
```

### 3. Review Only Specific File Types

Modify `getDiffSummary()` in `pr-review.js`:

```javascript
async function getDiffSummary() {
  // ... existing code ...
  
  // Filter for specific file types
  const relevantFiles = filesChanged.filter(file => {
    return file.endsWith('.js') || 
           file.endsWith('.ts') || 
           file.endsWith('.py') ||
           file.endsWith('.go');
  });
  
  if (relevantFiles.length === 0) {
    console.log('No relevant files to review');
    process.exit(0);  // Exit gracefully
  }
  
  return {
    diff,
    filesChanged: relevantFiles,
  };
}
```

### 4. Add Multiple Review Strategies

Create different prompts for different situations:

```javascript
function getReviewPrompt(filesChanged, diff) {
  const hasTests = filesChanged.some(f => f.includes('test'));
  const hasDatabase = filesChanged.some(f => f.includes('migration') || f.includes('schema'));
  
  if (hasDatabase) {
    return `
      DATABASE MIGRATION REVIEW CHECKLIST:
      - Are migrations reversible?
      - Are indexes added for new columns?
      - Is data loss prevented?
      ...
    `;
  }
  
  if (!hasTests) {
    return `
      NO TESTS DETECTED:
      Please suggest what tests should be added for these changes.
      ...
    `;
  }
  
  // Default prompt
  return `Standard code review...`;
}
```

### 5. Add Severity Levels

Categorize issues by severity:

```javascript
const prompt = `
Review this PR and categorize issues by severity:

🔴 **CRITICAL** - Security vulnerabilities, data loss risks
🟡 **MEDIUM** - Bugs, poor practices, performance issues
🟢 **LOW** - Style issues, minor improvements

For each issue, provide:
- Severity emoji
- Description
- File and line number
- Suggested fix
`;
```

### 6. Team-Specific Rules

Add your team's conventions:

```javascript
const prompt = `
Review according to our team standards:

✅ **Required Checks**:
- All functions have JSDoc comments
- No console.log statements
- Error handling with try-catch
- Input validation for public APIs
- Tests for new features

❌ **Forbidden Patterns**:
- No 'any' type in TypeScript
- No nested ternary operators
- No mutations in reducers
- No inline styles in React

Rate compliance: [PASS/FAIL]
`;
```

## What the Bot Reviews

### Code Quality Checks

✅ **SOLID Principles**
- Single Responsibility Principle violations
- Open/Closed Principle adherence
- Liskov Substitution correctness
- Interface Segregation
- Dependency Inversion patterns

✅ **Clean Code Practices**
- DRY (Don't Repeat Yourself) violations
- KISS (Keep It Simple, Stupid) compliance
- Function/method length and complexity
- Variable and function naming clarity
- Code duplication detection

✅ **Bug Detection**
- Potential null/undefined errors
- Off-by-one errors
- Race conditions
- Resource leaks (unclosed connections, files)
- Infinite loop risks
- Type mismatches

✅ **Security Analysis**
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- CSRF token handling
- Authentication/authorization issues
- Sensitive data exposure
- Insecure dependencies

✅ **Best Practices**
- Error handling completeness
- Input validation
- Logging appropriateness
- Performance considerations
- Memory management
- API design quality

✅ **Testing**
- Test coverage suggestions
- Missing edge case tests
- Test quality assessment

## Example Review Output

Here's what a typical bot review looks like:

```markdown
## 🤖 Amp Code Review

### 1. Overall Assessment ⭐

This PR adds a comprehensive test suite with excellent coverage (97%). Well-structured and follows clean architecture principles.

**Score: 8.5/10**

### 2. Potential Issues 🐛

#### Medium Priority

**File: `repositories/organisation_repository.py`**
- Line 62: Using deprecated `datetime.utcnow()`. 
  ```python
  # Replace with:
  from datetime import datetime, timezone
  now = datetime.now(timezone.utc)
  ```

**File: `api/schemas.py`**
- Line 8: Mutable default argument `tags = []` can cause bugs
  ```python
  # Use:
  from pydantic import Field
  tags: List[str] = Field(default_factory=list)
  ```

### 3. Code Quality Observations ✅

**Excellent**:
- ✅ Clear separation of concerns (Repository, Service, API layers)
- ✅ Comprehensive test coverage across all layers
- ✅ Type hints used throughout
- ✅ Follows SOLID principles consistently

**Good**:
- ✅ Fixtures in `conftest.py` promote test reusability
- ✅ Descriptive test names
- ✅ Tests isolated with temporary database

### 4. Suggestions for Improvement 💡

1. **Add async/await support** for better scalability
2. **Consider pagination** for the list endpoint
3. **Add request/response examples** to API documentation
4. **Add integration tests** for end-to-end workflows

### 5. Security Considerations 🔒

- ✅ SQL injection prevention via parameterized queries
- ⚠️  No authentication/authorization implemented (acceptable for demo)
- ⚠️  Consider rate limiting for production

### 6. What Was Done Well 👍

- Excellent test organization and coverage
- Clean architecture implementation
- Proper use of dependency injection
- Well-documented code structure

---
*Powered by [Amp](https://ampcode.com)*
```

## Troubleshooting

### Issue 1: Bot Doesn't Comment on PR

**Symptoms**: PR is opened, but no comment appears

**Debugging Steps**:

1. **Check GitHub Actions status**
   - Go to **Actions** tab in your repository
   - Find the workflow run for your PR
   - Look for red X (failed) or yellow circle (in progress)

2. **Check workflow logs**
   ```
   Actions → [Your workflow run] → [Job: review] → [Each step]
   ```
   
   Look for errors in:
   - "Install dependencies" step
   - "Run Amp PR Review" step

3. **Verify API key is set**
   - Settings → Secrets → Actions
   - Confirm `AMP_API_KEY` exists
   - Key should start with `sgamp_`
   - Try regenerating the key if unsure

4. **Check permissions**
   - Settings → Actions → General → Workflow permissions
   - Should be "Read and write permissions"
   - Or workflow must explicitly set `pull-requests: write`

5. **Common error messages**:

   | Error | Cause | Solution |
   |-------|-------|----------|
   | `AMP_API_KEY is not set` | Secret not configured | Add secret in repo settings |
   | `npm ERR! 404 Not Found` | Wrong package name | Check package.json has correct package |
   | `Failed to post comment: 403` | Insufficient permissions | Check workflow permissions |
   | `Failed to post comment: 422` | Invalid comment body | Check for special characters in result |

### Issue 2: Installation Fails

**Error**: `npm ERR! code ETARGET`

**Solution**: Update `package.json`:
```json
{
  "dependencies": {
    "@sourcegraph/amp-sdk": "latest"  // Ensure correct package name and version
  }
}
```

### Issue 3: Module Import Error

**Error**: `Error [ERR_PACKAGE_PATH_NOT_EXPORTED]`

**Solution**: Ensure `package.json` has `"type": "module"`:
```json
{
  "type": "module",  // This is required!
  "dependencies": {
    "@sourcegraph/amp-sdk": "latest"
  }
}
```

### Issue 4: Review Takes Too Long / Timeout

**Symptoms**: Workflow times out after 6+ minutes

**Causes**:
- Very large PR (100+ files)
- Amp API rate limiting
- Network issues

**Solutions**:

1. **Increase timeout**:
```yaml
jobs:
  review:
    timeout-minutes: 10  # Default is 360 (6 hours), but good to set explicitly
```

2. **Skip large PRs**:
```yaml
jobs:
  review:
    if: github.event.pull_request.changed_files < 50
```

3. **Review only recent commits**:
```javascript
// In pr-review.js, modify getDiffSummary():
const diff = execSync(`git diff ${baseSha}..${headSha} --stat --diff-filter=M`, { encoding: 'utf-8' });
// Only shows modified files, not added/deleted
```

### Issue 5: API Rate Limits

**Error**: `Rate limit exceeded`

**Causes**:
- Many PRs reviewed in short time
- Free tier limits exceeded

**Solutions**:

1. **Check your usage**: Visit [ampcode.com/settings](https://ampcode.com/settings)

2. **Add rate limit handling**:
```javascript
try {
  for await (const message of execute({ prompt, options })) {
    // ... handle messages
  }
} catch (error) {
  if (error.message.includes('rate limit')) {
    await postComment(prNumber, 
      '⚠️ Review delayed due to rate limits. Will retry shortly.');
    // Exit gracefully
    process.exit(0);
  }
  throw error;
}
```

3. **Upgrade Amp plan** if needed

### Issue 6: Review Is Empty or Gibberish

**Symptoms**: Bot posts comment but content is odd

**Debugging**:

Add logging to see what Amp returns:
```javascript
} else if (message.type === 'result') {
  console.log('Result type:', typeof message.result);
  console.log('Result length:', String(message.result).length);
  console.log('Result preview:', String(message.result).substring(0, 500));
  reviewResult = message.result;
}
```

Check logs in GitHub Actions to see the actual response.

### Issue 7: Bot Comments Multiple Times

**Cause**: Workflow triggers multiple times for same PR

**Solution**: 
```yaml
on:
  pull_request:
    types: [opened, synchronize]  # Remove 'reopened' if not needed
```

Or add deduplication:
```javascript
// Check if bot already commented
const existingComments = await fetch(
  `https://api.github.com/repos/${owner}/${repo}/issues/${prNumber}/comments`,
  { headers: { Authorization: `Bearer ${token}` } }
).then(r => r.json());

const botAlreadyCommented = existingComments.some(
  c => c.user.login === 'github-actions[bot]' && 
       c.body.includes('Amp Code Review')
);

if (botAlreadyCommented) {
  console.log('Already reviewed this PR');
  process.exit(0);
}
```

## Cost & Performance

### Pricing Model

Amp charges based on token usage (similar to OpenAI):

| PR Size | Files | Estimated Tokens | Approx. Cost (USD) |
|---------|-------|------------------|--------------------|
| Small   | 1-5   | ~1,000           | $0.002 - $0.01     |
| Medium  | 5-15  | ~3,000           | $0.006 - $0.03     |
| Large   | 15-30 | ~5,000           | $0.01 - $0.05      |
| Huge    | 30+   | ~10,000+         | $0.02 - $0.10      |

**Note**: Costs are approximate. Check current pricing at [ampcode.com/pricing](https://ampcode.com/pricing)

### Performance Benchmarks

| Metric | Average | 95th Percentile |
|--------|---------|-----------------|
| Review Time | 45 sec | 120 sec |
| API Latency | 2-5 sec | 10 sec |
| Workflow Total | 60 sec | 150 sec |

**Bottlenecks**:
1. npm install (~15-20 seconds)
2. Amp analysis (~30-60 seconds)
3. GitHub API calls (~2-5 seconds)

### Optimization Tips

1. **Cache dependencies**:
```yaml
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: .github/scripts/node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('.github/scripts/package-lock.json') }}
```

2. **Review only changed files** (not entire codebase)

3. **Skip trivial PRs**:
```yaml
if: github.event.pull_request.changed_files > 0
```

4. **Use concurrency limits**:
```yaml
concurrency:
  group: pr-review-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

## Security Considerations

### API Key Protection

✅ **Do**:
- Store API key in GitHub Secrets (never in code)
- Use repository secrets (not environment secrets for public repos)
- Regenerate key if accidentally exposed
- Use read-only API keys if possible

❌ **Don't**:
- Commit API keys to repository
- Share keys in PR descriptions
- Log API keys in workflow output
- Use same key across multiple repositories

### Workflow Security

✅ **Best Practices**:

1. **Limit workflow permissions**:
```yaml
permissions:
  contents: read          # Only read access to code
  pull-requests: write    # Only write to PRs, not issues
```

2. **Validate inputs**:
```javascript
if (!process.env.AMP_API_KEY || !process.env.AMP_API_KEY.startsWith('sgamp_')) {
  throw new Error('Invalid AMP_API_KEY');
}
```

3. **Pin action versions**:
```yaml
- uses: actions/checkout@v4      # Use specific version, not @main
- uses: actions/setup-node@v4
```

4. **Review third-party actions**:
- Only use actions from verified publishers
- Check action source code before use

### PR from Forks

**Warning**: PRs from forked repositories **don't have access to secrets** by default (this is a GitHub security feature).

**Options**:

1. **Disable for forks** (recommended):
```yaml
jobs:
  review:
    if: github.event.pull_request.head.repo.full_name == github.repository
```

2. **Use pull_request_target** (advanced, be careful):
```yaml
on:
  pull_request_target:  # Runs in base repo context
```
⚠️ **Security Risk**: This gives fork PRs access to secrets. Only use if you trust contributors.

### Data Privacy

**What data is sent to Amp**:
- Code diff (what changed in the PR)
- File names and paths
- Commit messages (indirectly, via diff)

**What is NOT sent**:
- Full repository contents (unless changed)
- Git history
- Environment variables
- Secrets

**Privacy Best Practices**:
1. Review Amp's privacy policy
2. Don't review PRs with sensitive data
3. Use self-hosted runners for private code
4. Add exclusions for sensitive files:
   ```javascript
   const sensitiveFiles = ['.env', 'secrets.yml', 'keys.pem'];
   filesChanged = filesChanged.filter(f => 
     !sensitiveFiles.some(s => f.includes(s))
   );
   ```

## Advanced Configuration

### Multi-Stage Review

Review PRs in stages (quick check → detailed analysis):

```javascript
async function quickReview(filesChanged) {
  const prompt = `
    Quick 30-second review:
    - Any obvious bugs?
    - Any security red flags?
    Keep it to 3 bullet points max.
  `;
  
  // ... execute quick review
  return result;
}

async function detailedReview(filesChanged) {
  const prompt = `
    Comprehensive review:
    - Full analysis of all changes
    - ...
  `;
  
  // ... execute detailed review
  return result;
}

// Run quick review first
const quickResult = await quickReview(filesChanged);
await postComment(prNumber, `### Quick Review\n${quickResult}`);

// If no critical issues, do detailed review
if (!quickResult.includes('🔴')) {
  const detailedResult = await detailedReview(filesChanged);
  await postComment(prNumber, `### Detailed Review\n${detailedResult}`);
}
```

### Integration with Other Tools

**Example: Combine with test coverage reports**:

```yaml
- name: Run tests with coverage
  run: pytest --cov=. --cov-report=json

- name: Run Amp PR Review
  env:
    AMP_API_KEY: ${{ secrets.AMP_API_KEY }}
    COVERAGE_REPORT: coverage.json  # Pass coverage data
  run: node .github/scripts/pr-review.js
```

```javascript
// In pr-review.js
const coverageData = fs.readFileSync(process.env.COVERAGE_REPORT, 'utf8');
const coverage = JSON.parse(coverageData);

const prompt = `
Review this PR. Current test coverage: ${coverage.totals.percent_covered}%

Focus on:
- Are new files tested?
- Did coverage increase or decrease?
`;
```

### Custom Review Templates

Create templates for different PR types:

```javascript
function getTemplateByLabels(labels) {
  if (labels.includes('bug-fix')) {
    return `
      BUG FIX REVIEW:
      1. Does this fix the root cause or just the symptom?
      2. Are there tests that prevent regression?
      3. What's the impact on existing functionality?
    `;
  }
  
  if (labels.includes('feature')) {
    return `
      NEW FEATURE REVIEW:
      1. Is the feature documented?
      2. Are there tests?
      3. Does it follow our architecture?
      4. Performance implications?
    `;
  }
  
  // Default template
  return standardReviewTemplate;
}
```

### Notification Integration

Send review summaries to Slack/Discord:

```javascript
async function sendSlackNotification(prNumber, reviewSummary) {
  const webhookUrl = process.env.SLACK_WEBHOOK_URL;
  
  await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `PR #${prNumber} reviewed by Amp`,
      blocks: [
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: reviewSummary,
          },
        },
      ],
    }),
  });
}
```

## FAQ

### Q: Does the bot work with private repositories?

**A**: Yes, but you need to ensure:
1. Your Amp plan supports private repos
2. GitHub Actions is enabled for private repos
3. Workflow has proper permissions

### Q: Can I use this with GitHub Enterprise?

**A**: Yes, the bot works with GitHub Enterprise. Just ensure:
- Actions are enabled in your enterprise
- You can install Node.js 18+
- Amp API is accessible from your network

### Q: How do I disable reviews for certain file types?

**A**: Add filtering in `getDiffSummary()`:

```javascript
const ignoredExtensions = ['.md', '.txt', '.json', '.yaml'];
const filteredFiles = filesChanged.filter(file => 
  !ignoredExtensions.some(ext => file.endsWith(ext))
);

if (filteredFiles.length === 0) {
  console.log('No relevant files to review');
  process.exit(0);
}
```

### Q: Can the bot approve/reject PRs automatically?

**A**: Technically possible, but **NOT RECOMMENDED**. The bot should assist humans, not replace them. To add approval:

```javascript
// Post an approval (use with extreme caution)
await fetch(`https://api.github.com/repos/${owner}/${repo}/pulls/${prNumber}/reviews`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    event: 'APPROVE',
    body: 'Automated approval from Amp',
  }),
});
```

**Better approach**: Use required reviewers and let bot provide information only.

### Q: How do I review only specific branches?

**A**: Add conditions to workflow:

```yaml
on:
  pull_request:
    branches:
      - main
      - develop
    types: [opened, synchronize]
```

### Q: Can I run this locally for testing?

**A**: Yes! 

```bash
# Set environment variables
export AMP_API_KEY=sgamp_your_key_here
export GITHUB_TOKEN=your_github_token
export PR_NUMBER=123
export REPO_NAME=owner/repo
export BASE_SHA=abc123
export HEAD_SHA=def456

# Install dependencies
cd .github/scripts
npm install

# Run script
node pr-review.js
```

### Q: What programming languages does it support?

**A**: Amp understands virtually all programming languages:
- Python, JavaScript, TypeScript, Go, Rust
- Java, C#, C++, Swift, Kotlin
- Ruby, PHP, Scala, Elixir
- And many more!

The review quality is consistent across languages.

### Q: How do I upgrade the bot?

**A**: To get the latest version:

1. Check for SDK updates:
```bash
cd .github/scripts
npm update @sourcegraph/amp-sdk
```

2. Update workflow file from this repo if needed

3. Test on a non-critical PR

### Q: Can I use multiple review bots?

**A**: Yes, create multiple workflows:

```
.github/workflows/
├── pr-review-security.yml    # Security-focused review
├── pr-review-performance.yml # Performance review
└── pr-review-style.yml       # Code style review
```

Each can run different prompts and post separate comments.

## Additional Resources

### Documentation
- **Amp Manual**: [ampcode.com/manual](https://ampcode.com/manual)
- **Amp SDK**: [npmjs.com/package/@sourcegraph/amp-sdk](https://www.npmjs.com/package/@sourcegraph/amp-sdk)
- **GitHub Actions**: [docs.github.com/actions](https://docs.github.com/en/actions)
- **GitHub REST API**: [docs.github.com/rest](https://docs.github.com/en/rest)

### Example Repositories
- **This Repository**: Full working example
- **Amp Examples**: [github.com/sourcegraph/amp-examples](https://github.com/sourcegraph/amp-examples) (if available)

### Community
- **Amp Discord**: Join for support and discussions
- **GitHub Discussions**: Ask questions about the bot
- **Stack Overflow**: Tag with `amp-ai` for technical questions

### Getting Help

1. **Check logs first**: 90% of issues are visible in GitHub Actions logs
2. **Search existing issues**: Someone may have solved your problem
3. **Create detailed issue**: Include logs, code snippets, and steps to reproduce
4. **Contact Amp support**: For API-related issues

## Contributing

Found a bug or have an improvement? Contributions are welcome!

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This PR review bot implementation is provided as-is for demonstration purposes. Feel free to adapt it to your needs.

---

## Quick Reference Card

**Essential Commands**:

```bash
# Test bot locally
export AMP_API_KEY=sgamp_xxx
node .github/scripts/pr-review.js

# Reinstall dependencies
cd .github/scripts && npm install

# Check workflow syntax
gh workflow view pr-review.yml

# Manually trigger workflow
gh workflow run pr-review.yml
```

**Essential Files**:
- Workflow: `.github/workflows/pr-review.yml`
- Script: `.github/scripts/pr-review.js`
- Deps: `.github/scripts/package.json`

**Essential Links**:
- API Key: https://ampcode.com/settings
- Actions: https://github.com/YOUR_REPO/actions
- Secrets: https://github.com/YOUR_REPO/settings/secrets/actions

---

**Built with ❤️ using [Amp](https://ampcode.com) 🚀**

*Last updated: October 2025*
