import { execute } from '@sourcegraph/amp-sdk';
import { execSync } from 'child_process';

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

async function getDiffSummary() {
  try {
    const baseSha = process.env.BASE_SHA;
    const headSha = process.env.HEAD_SHA;
    
    const diff = execSync(`git diff ${baseSha}..${headSha} --stat`, { encoding: 'utf-8' });
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

async function reviewPullRequest() {
  console.log('🤖 Starting Amp PR Review...');

  const prNumber = process.env.PR_NUMBER;
  
  if (!process.env.AMP_API_KEY) {
    console.error('❌ AMP_API_KEY is not set');
    process.exit(1);
  }

  const { diff, filesChanged } = await getDiffSummary();

  console.log(`📝 Files changed: ${filesChanged.length}`);
  console.log(`Files: ${filesChanged.join(', ')}`);

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

    // Post the review as a comment
    // Ensure reviewResult is a string and sanitize it
    const resultText = typeof reviewResult === 'string' ? reviewResult : JSON.stringify(reviewResult);
    const fullComment = `## 🤖 Amp AI Code Review\n\n${resultText}\n\n---\n*Powered by [Amp AI](https://ampcode.com)*`;
    
    console.log('Posting comment with length:', fullComment.length);
    await postComment(prNumber, fullComment);
    console.log('✅ Review posted to PR successfully');

  } catch (error) {
    console.error('❌ An unexpected error occurred:', error);
    
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

reviewPullRequest();
