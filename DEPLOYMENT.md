# Vercel Deployment Setup

This project is now configured for automatic deployment to Vercel using GitHub Actions.

## ✅ Completed Setup

1. **Branches Merged**: All feature branches have been merged to main
2. **Vercel Configuration**: Added `vercel.json` for optimal deployment settings
3. **Build Script**: Created `build_files.sh` for proper Django deployment
4. **Django Settings**: Updated for multi-platform compatibility

## 🔧 Required Configuration

To complete the Vercel deployment setup, you need to add environment variables in your Vercel dashboard:

### Step 1: Create Vercel Project

1. **Create Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Import GitHub Repository**: 
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import your GitHub repository

### Step 2: Configure Environment Variables

In your Vercel project dashboard, go to **Settings > Environment Variables** and add:

**Required Variables:**
- `SECRET_KEY`: Your Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your Vercel domain (e.g., `your-app.vercel.app`)

**Optional Variables:**
- `DATABASE_URL`: If using external database
- `POSTGRES_URL`: If using Vercel Postgres

### Step 3: Deploy

Once configured, Vercel will automatically deploy when you:
- Push to `main` branch → Production deployment
- Push to any other branch → Preview deployment

## � Common Deployment Issues & Solutions

### Issue 1: Build Timeout
**Error**: "Build exceeded maximum duration"
**Solution**: 
```bash
# In vercel.json, increase build timeout
{
  "builds": [{
    "src": "build_files.sh",
    "use": "@vercel/static-build",
    "config": { "maxDuration": 300 }
  }]
}
```

### Issue 2: Static Files Not Found
**Error**: "Static files returning 404"
**Solution**: Ensure `vercel.json` routes are correct:
```json
{
  "routes": [
    { "src": "/static/(.*)", "dest": "/static/$1" },
    { "src": "/(.*)", "dest": "requirements_lab/wsgi.py" }
  ]
}
```

### Issue 3: Database Connection
**Error**: "Database connection failed"
**Solution**: 
- Use SQLite for simple deployments (default)
- Or set up Vercel Postgres in your project dashboard
- Add `DATABASE_URL` environment variable if using external DB

### Issue 4: Module Import Errors
**Error**: "No module named 'requirements_lab'"
**Solution**: Verify your project structure and WSGI configuration

### Issue 5: ALLOWED_HOSTS Error
**Error**: "DisallowedHost"
**Solution**: 
- Set `ALLOWED_HOSTS` environment variable
- Or let Django auto-detect from `VERCEL_URL`

## 🔍 Debugging Deployment

1. **Check Build Logs**: View detailed logs in Vercel dashboard
2. **Test Locally**: Run `python debug_django.py` to test Django setup
3. **Verify Configuration**: Run `python quick_compatibility_check.py`
4. **Check Requirements**: Ensure all packages are in `requirements.txt`