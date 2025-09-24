# Backend Deployment Guide

## Common Deployment Issues and Solutions

### 1. 500: INTERNAL_SERVER_ERROR

This error typically occurs due to:

1. **Missing Environment Variables**
2. **Dependency Issues**
3. **Model Initialization Failures**
4. **Import Errors**

### 2. Troubleshooting Steps

#### Check Vercel Logs
1. Go to your Vercel dashboard
2. Navigate to the deployment that's failing
3. Check the logs for specific error messages

#### Verify Environment Variables
1. In Vercel dashboard, go to your project settings
2. Navigate to "Environment Variables"
3. Ensure `GOOGLE_API_KEY` is set with your actual Google API key

#### Test Locally
Before deploying, test your application locally:
```bash
cd backend
python test_local.py
```

### 3. Deployment Checklist

- [ ] `GOOGLE_API_KEY` is set in Vercel environment variables
- [ ] All dependencies in `requirements.txt` are correctly specified
- [ ] `vercel.json` is properly configured
- [ ] No syntax errors in `app.py`
- [ ] Test locally before deploying

### 4. Common Fixes

#### If you see "ImportError" in logs:
1. Check that all required packages are in `requirements.txt`
2. Ensure version numbers are compatible

#### If you see "Model initialization failed":
1. Verify `GOOGLE_API_KEY` is correctly set
2. Check that the API key has access to the specified model

#### If you see "No module named 'X'":
1. Add the missing module to `requirements.txt`
2. Redeploy

### 5. Emergency Recovery

If your deployment continues to fail:

1. Simplify `requirements.txt` to minimal dependencies
2. Use a more specific Python runtime in `vercel.json`
3. Add more logging to identify the exact failure point
4. Consider using the lightweight version if size is an issue

### 6. Contact Support

If you continue to experience issues:
1. Save the complete error logs from Vercel
2. Check the Vercel status page for service issues
3. Review the Google Cloud AI Platform status for model availability