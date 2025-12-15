/**
 * Amp AI PR Review Bot
 * 
 * This script automates code reviews for pull requests using the Amp AI SDK.
 * It runs as a GitHub Action on every PR (opened, synchronized, or reopened).
 * 
 * ## How It Works:
 * 
 * 1. TRIGGER: GitHub Actions workflow triggers this script when a PR is created/updated
 * 2. DIFF EXTRACTION: We extract the git diff between base and head commits
 * 3. CONTEXT INJECTION: The Amp agent uses the `librarian` tool to fetch OOP guidelines
 *    from an external GitHub repository (Understanding-Object-Oriented-Programming)
 * 4. AI REVIEW: Amp analyzes the code changes against OOP principles and best practices
 * 5. COMMENT: The review is posted as a comment on the PR
 * 
 * ## External Context:
 * 
 * The review uses OOP principles from: github.com/ma-px/Understanding-Object-Oriented-Programming
 * This includes SOLID principles, design patterns, encapsulation, inheritance, etc.
 * The `librarian` tool fetches this context at runtime, ensuring reviews are grounded
 * in documented best practices rather than generic AI knowledge.
 * 
 * ## Environment Variables Required:
 * - AMP_API_KEY: API key for Amp AI service
 * - GITHUB_TOKEN: Token for posting comments to the PR
 * - PR_NUMBER: The pull request number
 * - REPO_NAME: Repository in format "owner/repo"
 * - BASE_SHA: Base commit SHA for diff comparison
 * - HEAD_SHA: Head commit SHA for diff comparison
 */

import { execute } from '@sourcegraph/amp-sdk';
import { execSync } from 'child_process';

/**
 * Posts a comment to the pull request using the GitHub API.
 * 
 * @param {string} prNumber - The PR number to comment on
 * @param {string} comment - The markdown comment body to post
 * @returns {Promise<object>} - The GitHub API response
 */
async function postComment(prNumber, comment) {
  const [owner, repo] = process.env.REPO_NAME.split('/');
  const token = process.env.GITHUB_TOKEN;

  const url = `https://api.github.com/repos/${owner}/${repo}/issues/${prNumber}/comments`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Accept': 'application/vnd.github.v3+json',
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'User-Agent': 'Amp-PR-Review-Bot',
    },
    body: JSON.stringify({
      body: String(comment),
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to post comment: ${response.status} - ${errorText}`);
  }

  return response.json();
}

/**
 * Extracts the git diff summary between base and head commits.
 * 
 * Uses git commands to get:
 * - A stat summary showing files changed and lines added/removed
 * - A list of all changed file names
 * 
 * @returns {Promise<{diff: string, filesChanged: string[]}>}
 */
async function getDiffSummary() {
  try {
    const baseSha = process.env.BASE_SHA;
    const headSha = process.env.HEAD_SHA;
    
    // Get a summary of changes (files, insertions, deletions)
    const diff = execSync(`git diff ${baseSha}..${headSha} --stat`, { encoding: 'utf-8' });
    
    // Get list of changed files for targeted review
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

/**
 * Main function that orchestrates the PR review process.
 * 
 * Flow:
 * 1. Validates required environment variables
 * 2. Extracts diff information from the PR
 * 3. Constructs a prompt that instructs Amp to:
 *    - Use the `librarian` tool to fetch OOP guidelines from external repo
 *    - Review code against those OOP principles
 *    - Include references to which guidelines were applied
 * 4. Streams the Amp response and captures the final result
 * 5. Posts the review as a PR comment
 */
async function reviewPullRequest() {
  console.log('🤖 Starting Amp PR Review...');

  const prNumber = process.env.PR_NUMBER;
  
  // Validate API key is present
  if (!process.env.AMP_API_KEY) {
    console.error('❌ AMP_API_KEY is not set');
    process.exit(1);
  }

  // Get the changes in this PR
  const { diff, filesChanged } = await getDiffSummary();

  console.log(`📝 Files changed: ${filesChanged.length}`);
  console.log(`Files: ${filesChanged.join(', ')}`);

  /**
   * The prompt instructs Amp to:
   * 
   * 1. USE LIBRARIAN TOOL: Fetch OOP context from external GitHub repo
   *    This ensures reviews are based on documented principles, not just AI training data
   * 
   * 2. REVIEW CRITERIA: Apply OOP principles (SOLID, design patterns, etc.)
   *    from the fetched context
   * 
   * 3. STRUCTURED OUTPUT: Provide assessment, bugs, quality observations,
   *    security concerns, and suggestions
   * 
   * 4. REFERENCES SECTION: Cite which OOP principles were applied
   *    This provides transparency and educational value
   */
  const prompt = `
You are a code review bot. Review this pull request and provide constructive feedback.

**IMPORTANT**: Before reviewing, use the librarian tool to fetch OOP best practices and guidelines from:
- Repository: github.com/ma-px/Understanding-Object-Oriented-Programming
- Query: "Fetch all OOP principles, SOLID principles, design patterns, and best practices from this repository to use as review criteria"

Use the OOP guidelines from that repository as the primary criteria for evaluating code quality.

**Files Changed:**
${filesChanged.join('\n')}

**Diff Summary:**
${diff}

Please review the changes and provide:
1. Overall assessment of the changes
2. Any potential bugs or issues
3. Code quality observations based on OOP principles from the reference repository (SOLID, design patterns, encapsulation, inheritance, polymorphism, abstraction)
4. Security concerns if any
5. Suggestions for improvement aligned with OOP best practices
6. Positive feedback on what was done well

Format your response in markdown. Be concise but thorough. Focus on the most important issues first.
Use git diff to get the full changes if needed.

At the end of your review, include a "📚 References" section that lists which specific OOP principles or guidelines from the Understanding-Object-Oriented-Programming repository were applied during this review, with links to the relevant sections if available.
`;

  let reviewResult = '';

  try {
    /**
     * Execute the Amp agent with the review prompt.
     * 
     * - dangerouslyAllowAll: Allows all tool permissions (needed for librarian, git, etc.)
     * - cwd: Sets working directory so Amp can access repo files
     * 
     * The execute() function streams messages as the agent works:
     * - 'assistant': Agent is processing
     * - 'result': Final output (success or error)
     */
    for await (const message of execute({
      prompt,
      options: {
        dangerouslyAllowAll: true,
        cwd: process.cwd(),
      },
    })) {
      if (message.type === 'assistant') {
        console.log('🔄 Amp is analyzing...');
      } else if (message.type === 'result') {
        if (message.is_error) {
          console.error('❌ Amp Review Failed:', message.error);
          reviewResult = `## ❌ Review Failed\n\n${message.error}`;
        } else {
          console.log('✅ Amp Review Completed');
          console.log('Result type:', typeof message.result);
          console.log('Result preview:', message.result ? String(message.result).substring(0, 200) : 'empty');
          reviewResult = message.result;
        }
        break;
      }
    }

    // Format and post the review comment
    const resultText = typeof reviewResult === 'string' ? reviewResult : JSON.stringify(reviewResult);
    const fullComment = `## 🤖 Amp AI Code Review\n\n${resultText}\n\n---\n*Powered by [Amp AI](https://ampcode.com)*`;
    
    console.log('Posting comment with length:', fullComment.length);
    await postComment(prNumber, fullComment);
    console.log('✅ Review posted to PR successfully');

  } catch (error) {
    console.error('❌ An unexpected error occurred:', error);
    
    // Attempt to post error message to PR so reviewers are aware
    try {
      await postComment(
        prNumber,
        `## ❌ Amp AI Code Review Failed\n\nAn error occurred while reviewing this PR:\n\`\`\`\n${error.message}\n\`\`\``
      );
    } catch (commentError) {
      console.error('Failed to post error comment:', commentError);
    }
    
    process.exit(1);
  }
}

// Run the review
reviewPullRequest();
