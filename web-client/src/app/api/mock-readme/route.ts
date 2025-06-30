import { NextResponse } from 'next/server';

const SAMPLE_README = `# 🚀 Smart ReadmeGen Demo Project

> AI-powered repository analysis and README generation using AWS Lambda and Amazon Bedrock

[![AWS](https://img.shields.io/badge/AWS-Lambda-orange)](https://aws.amazon.com/lambda/)
[![Bedrock](https://img.shields.io/badge/Amazon-Bedrock-blue)](https://aws.amazon.com/bedrock/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9-blue)](https://typescriptlang.org)
[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

This is a demonstration project showcasing the Smart ReadmeGen AI system. The project demonstrates how artificial intelligence can analyze code repositories and generate comprehensive, professional documentation automatically.

### Key Features

- **🤖 AI-Powered Analysis**: Uses Claude Sonnet 4 for deep code understanding
- **📊 Comprehensive Structure**: Generates 12-section professional README structure  
- **🏗️ Serverless Architecture**: Built on AWS Lambda with S3 storage
- **🔄 Multi-Stage Pipeline**: Analysis → Storage → Generation workflow
- **📈 Production Ready**: Includes monitoring, alerts, and error handling
- **🎯 High Accuracy**: 99%+ accuracy in project type and framework detection

## 🏛️ Architecture

\`\`\`
GitHub Repository → Lambda Analyzer → S3 Storage → Lambda Generator → README
                        ↓               ↓              ↓
                  Bedrock Claude    JSON Structure   Markdown Output
\`\`\`

### Components

1. **Analyzer Lambda**: Repository analysis and JSON generation
2. **Generator Lambda**: README markdown generation from JSON  
3. **Bedrock Service**: AI model integration
4. **S3 Storage**: Intermediate JSON storage with organized key structure
5. **CloudWatch Monitoring**: Performance and error tracking

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- AWS Account with appropriate permissions
- GitHub Personal Access Token

### Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/example-user/smart-readmegen-demo.git
cd smart-readmegen-demo

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev
\`\`\`

### Configuration

\`\`\`bash
# Environment Variables
GITHUB_TOKEN=your_github_token
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0
NEXT_PUBLIC_API_URL=https://your-api-gateway-url
\`\`\`

## 📖 Usage

### Basic Usage

\`\`\`typescript
import { ReadmeGenerator } from './lib/readme-generator';

const generator = new ReadmeGenerator({
  githubToken: process.env.GITHUB_TOKEN,
  awsRegion: 'us-east-1'
});

// Generate README for a repository
const result = await generator.generate('https://github.com/user/repo');
console.log(result.readmeContent);
\`\`\`

### Advanced Configuration

\`\`\`typescript
const generator = new ReadmeGenerator({
  githubToken: process.env.GITHUB_TOKEN,
  awsRegion: 'us-east-1',
  options: {
    includeCodeExamples: true,
    generateBadges: true,
    includeContributing: true,
    customSections: ['deployment', 'monitoring']
  }
});
\`\`\`

## 🧪 API Reference

### Generate README

\`\`\`http
POST /api/generate
Content-Type: application/json

{
  "githubUrl": "https://github.com/user/repo",
  "options": {
    "includeExamples": true,
    "generateBadges": true
  }
}
\`\`\`

**Response:**

\`\`\`json
{
  "success": true,
  "data": {
    "readmeContent": "# Generated README...",
    "analysis": {
      "projectType": "Web Application",
      "primaryLanguage": "TypeScript",
      "frameworks": ["React", "Next.js"],
      "confidence": 0.95
    },
    "processingTime": 28.5
  }
}
\`\`\`

## 🔧 Development

### Project Structure

\`\`\`
src/
├── app/                 # Next.js app directory
├── components/          # React components
├── lib/                # Utility libraries
├── hooks/              # Custom React hooks
├── types/              # TypeScript type definitions
└── utils/              # Helper functions
\`\`\`

### Running Tests

\`\`\`bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
\`\`\`

### Code Quality

\`\`\`bash
# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check
\`\`\`

## 🚀 Deployment

### Vercel Deployment

\`\`\`bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod
\`\`\`

### AWS Deployment

\`\`\`bash
# Deploy infrastructure
aws cloudformation deploy \\
  --template-file infrastructure/template.yaml \\
  --stack-name smart-readmegen-demo \\
  --capabilities CAPABILITY_IAM
\`\`\`

## 📊 Performance

- **Analysis Speed**: 25-30 seconds per repository
- **Accuracy**: 99%+ for project type detection  
- **Model**: Claude Sonnet 4 (highest accuracy)
- **Reliability**: 99.9% uptime with multi-region inference
- **Cost**: ~$0.10-0.50 per analysis (depending on repository size)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Process

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (\`git commit -m 'Add amazing feature'\`)
6. Push to the branch (\`git push origin feature/amazing-feature\`)
7. Open a Pull Request

### Code Standards

- Follow TypeScript best practices
- Write comprehensive tests
- Use conventional commit messages
- Ensure accessibility compliance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Amazon Bedrock** for providing powerful AI models
- **AWS Lambda** for serverless computing platform
- **Next.js** for the excellent React framework
- **Tailwind CSS** for utility-first styling
- **The Open Source Community** for inspiration and tools

## 📞 Support

- 📧 Email: support@smartreadmegen.com
- 💬 Discord: [Join our community](https://discord.gg/smartreadmegen)
- 📖 Documentation: [docs.smartreadmegen.com](https://docs.smartreadmegen.com)
- 🐛 Issues: [GitHub Issues](https://github.com/user/repo/issues)

---

**Built with ❤️ using AWS Serverless Technologies and AI**

*Generated by Smart ReadmeGen AI - Professional README generation in seconds*`;

export async function GET() {
  return NextResponse.json({
    content: SAMPLE_README,
    metadata: {
      repoName: 'smart-readmegen-demo',
      repoUrl: 'https://github.com/example-user/smart-readmegen-demo',
      owner: 'example-user',
      generatedAt: new Date().toISOString(),
      projectType: 'Web Application',
      primaryLanguage: 'TypeScript',
      frameworks: ['React', 'Next.js', 'Tailwind CSS'],
      confidence: 0.95,
      processingTime: 28.5
    }
  });
}
