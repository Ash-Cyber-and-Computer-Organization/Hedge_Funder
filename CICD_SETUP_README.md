# HedgeFunder CI/CD Pipeline Setup

This document explains how to set up and use the GitHub Actions CI/CD pipeline for the HedgeFunder trading system.

## 🚀 Pipeline Overview

The CI/CD pipeline includes the following jobs:

1. **Frontend**: Build, test, and deploy React app to Vercel
2. **Backend**: Build, test, and deploy Python API to Docker Hub
3. **N8N**: Export and commit n8n workflows
4. **Security**: Vulnerability scanning with Trivy
5. **Lint**: Code linting and formatting

## 📋 Prerequisites

### Required Secrets in GitHub Repository

Add these secrets to your GitHub repository settings:

```bash
# Vercel Deployment
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_vercel_org_id
VERCEL_PROJECT_ID=your_vercel_project_id

# Docker Hub
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_password

# N8N (Optional)
N8N_API_KEY=your_n8n_api_key

# Render Deployment (Optional)
RENDER_DEPLOY_HOOK=your_render_deploy_hook_url
```

### API Keys for Full Functionality

Add these to your `.env` file for enhanced news aggregation:

```bash
# Required
FINNHUB_API_KEY=your_finnhub_api_key

# Optional (for more news sources)
NEWSAPI_KEY=your_newsapi_key
ALPHA_VANTAGE_API_KEY=your_alphavantage_key
```

## 🛠️ Local Development Setup

### Using Docker Compose (Recommended)

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
python n8n_minimal_api.py

# Frontend
cd frontend
npm install
npm run dev
```

## 🔧 Pipeline Configuration

### Trigger Conditions

The pipeline runs on:
- Push to `main` branch
- Pull requests to `main` branch

### Job Dependencies

- All jobs run in parallel
- Security and lint jobs run on all branches
- Deployment jobs only run on `main` branch

## 📊 Pipeline Features

### Frontend Job
- ✅ Node.js 18 setup
- ✅ Dependency installation
- ✅ Test execution (if tests exist)
- ✅ Production build
- ✅ Vercel deployment

### Backend Job
- ✅ Python 3.11 setup
- ✅ Dependency installation
- ✅ Test execution
- ✅ Docker image build
- ✅ Docker Hub push
- ✅ Render deployment (optional)

### Security Job
- ✅ Vulnerability scanning with Trivy
- ✅ SARIF report generation
- ✅ GitHub Security tab integration

### Linting Job
- ✅ ESLint for JavaScript/React
- ✅ Prettier for code formatting
- ✅ Flake8 for Python
- ✅ Black for Python formatting

## 🚨 Troubleshooting

### Common Issues

1. **Vercel Deployment Fails**
   - Check `VERCEL_TOKEN` is valid
   - Verify `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID`
   - Ensure frontend build succeeds locally

2. **Docker Build Fails**
   - Check `backend/Dockerfile` syntax
   - Verify all dependencies in `requirements.txt`
   - Test build locally: `docker build ./backend`

3. **Tests Fail**
   - Run tests locally first
   - Check environment variables
   - Verify API keys are set

4. **N8N Export Fails**
   - Verify `N8N_API_KEY` is correct
   - Check n8n instance URL
   - Ensure n8n is accessible from GitHub Actions

### Debugging Pipeline

```bash
# View workflow logs in GitHub Actions
# Go to Actions tab → Select workflow → View logs

# Test locally before pushing
cd backend && python -m pytest
cd frontend && npm run build
```

## 🔒 Security Considerations

- All secrets are encrypted in GitHub
- Trivy scans for vulnerabilities
- Dependencies are pinned for reproducibility
- Code is linted and formatted automatically

## 📈 Monitoring & Alerts

- Pipeline status visible in GitHub Actions
- Security vulnerabilities reported to Security tab
- Deployment status notifications (if configured)

## 🎯 Best Practices

1. **Always test locally first**
2. **Keep dependencies updated**
3. **Use semantic versioning**
4. **Review PRs before merging**
5. **Monitor security alerts**

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Vercel Deployment Guide](https://vercel.com/docs)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Trivy Security Scanner](https://aquasecurity.github.io/trivy/)

---

## 🚀 Quick Start

1. **Set up secrets** in GitHub repository
2. **Add API keys** to `.env` file
3. **Push to main branch** to trigger pipeline
4. **Monitor deployment** in Actions tab

The pipeline will automatically build, test, and deploy your HedgeFunder application! 🎉
