// app/api/readme/generate/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { SFNClient, StartExecutionCommand } from '@aws-sdk/client-sfn';

const sfnClient = new SFNClient({
  region: 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

export async function POST(request: NextRequest) {
  try {
    const { github_url } = await request.json();

    if (!github_url) {
      return NextResponse.json(
        { error: 'GitHub URL is required' },
        { status: 400 }
      );
    }

    // Validate GitHub URL
    const githubRegex = /^https:\/\/github\.com\/[\w\-\.]+\/[\w\-\.]+\/?$/;
    if (!githubRegex.test(github_url)) {
      return NextResponse.json(
        { error: 'Invalid GitHub URL format' },
        { status: 400 }
      );
    }

    // Start Step Functions execution
    const command = new StartExecutionCommand({
      stateMachineArn: 'arn:aws:states:us-east-1:695221387268:stateMachine:complete-readme-generator-workflow',
      input: JSON.stringify({ github_url }),
    });

    const result = await sfnClient.send(command);

    return NextResponse.json({
      success: true,
      execution_arn: result.executionArn,
      message: 'README generation started',
    });
  } catch (error) {
    console.error('README generation failed:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// app/api/readme/status/[executionArn]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { SFNClient, DescribeExecutionCommand } from '@aws-sdk/client-sfn';

export async function GET(
  request: NextRequest,
  { params }: { params: { executionArn: string } }
) {
  try {
    const executionArn = decodeURIComponent(params.executionArn);

    const command = new DescribeExecutionCommand({
      executionArn,
    });

    const result = await sfnClient.send(command);

    return NextResponse.json({
      status: result.status,
      output: result.output ? JSON.parse(result.output) : null,
      error: result.error,
    });
  } catch (error) {
    console.error('Status check failed:', error);
    return NextResponse.json(
      { error: 'Failed to check status' },
      { status: 500 }
    );
  }
}

// app/api/readme/download/[owner]/[repo]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({
  region: 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

export async function GET(
  request: NextRequest,
  { params }: { params: { owner: string; repo: string } }
) {
  try {
    const { owner, repo } = params;
    const key = `generated-readmes/${owner}/${repo}.md`;

    const command = new GetObjectCommand({
      Bucket: 'smart-readme-lambda-31641',
      Key: key,
    });

    const result = await s3Client.send(command);
    const readme_content = await result.Body?.transformToString();

    if (!readme_content) {
      return NextResponse.json(
        { error: 'README not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      readme_content,
      s3_url: `https://smart-readme-lambda-31641.s3.amazonaws.com/${key}`,
      owner,
      repo,
    });
  } catch (error) {
    console.error('README fetch failed:', error);
    return NextResponse.json(
      { error: 'Failed to fetch README' },
      { status: 500 }
    );
  }
}
