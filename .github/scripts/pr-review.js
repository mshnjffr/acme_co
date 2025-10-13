import { execute } from '@sourcegraph/the-orb-is-awake';
import { execSync } from 'child_process';
import https from 'https';

async function postComment(prNumber, comment) {
  const [owner, repo] = process.env.REPO_NAME.split('/');
  const token = process.env.GITHUB_TOKEN;

  // Ensure comment is a plain string
  const commentBody = String(comment);
  
  const data = JSON.stringify({
    body: commentBody,
  });

  const options = {
    hostname: 'api.github.com',
    port: 443,
    path: `/repos/${owner}/${repo}/issues/${prNumber}/comments`,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length,
      'Authorization': `token ${token}`,
      'User-Agent': 'Amp-PR-Review-Bot',
    },
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(responseData));
        } else {
          reject(new Error(`Failed to post comment: ${res.statusCode} - ${responseData}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.write(data);
    req.end();
  });
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

**Files Changed:**
${filesChanged.join('\n')}

**Diff Summary:**
${diff}

Please review the changes and provide:
1. Overall assessment of the changes
2. Any potential bugs or issues
3. Code quality observations (following SOLID principles, DRY, KISS)
4. Security concerns if any
5. Suggestions for improvement
6. Positive feedback on what was done well

Format your response in markdown. Be concise but thorough. Focus on the most important issues first.
Use git diff to get the full changes if needed.
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
