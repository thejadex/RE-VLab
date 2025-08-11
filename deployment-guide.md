# RE VLab Deployment Guide

## 🚀 Hosting Options for Your Project

Your RE VLab project is a hybrid Django + Next.js application. Here are the best deployment strategies:

## Option 1: Railway (Recommended - Easiest)

### Why Railway?
- Automatically detects both Django and Next.js
- Built-in database (PostgreSQL)
- Easy environment variables setup
- Custom domain support
- Great free tier

### Steps:
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Initialize:**
   ```bash
   railway login
   railway init
   ```

3. **Deploy:**
   ```bash
   railway up
   ```

4. **Set Environment Variables:**
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-domain.railway.app`
   - `DATABASE_URL` (automatically provided)

### Cost: Free tier with generous limits

---

## Option 2: Render (Great Free Alternative)

### Setup:
1. **Backend (Django):**
   - Connect GitHub repo to Render
   - Create new "Web Service"
   - Build command: `pip install -r requirements.txt`
   - Start command: `python manage.py runserver 0.0.0.0:$PORT`

2. **Frontend (Next.js):**
   - Create new "Static Site"
   - Build command: `npm run build`
   - Publish directory: `.next`

3. **Database:**
   - Add PostgreSQL addon
   - Update Django settings

### Cost: Free tier available

---

## Option 3: Vercel + Railway Database

### Steps:
1. **Frontend on Vercel:**
   ```bash
   npm install -g vercel
   vercel --prod
   ```

2. **Backend on Railway:**
   - Deploy Django backend separately
   - Use Railway for database

3. **Connect Frontend to Backend:**
   - Update API endpoints in Next.js
   - Configure CORS in Django

---

## Option 4: DigitalOcean App Platform

### Features:
- One-click deployment
- Auto-scaling
- Built-in monitoring
- Custom domains

### Cost: Starting at $5/month

---

## Option 5: Heroku (Classic Choice)

### Setup:
1. **Install Heroku CLI**
2. **Create Procfile:**
   ```
   web: python manage.py runserver 0.0.0.0:$PORT
   ```
3. **Deploy:**
   ```bash
   git push heroku main
   ```

### Note: Heroku no longer has a free tier

---

## Quick Start with Railway (Recommended)

1. **Prepare your project:**
   ```bash
   # Add to requirements.txt
   echo "gunicorn==21.2.0" >> requirements.txt
   echo "whitenoise==6.6.0" >> requirements.txt
   ```

2. **Update Django settings for production:**
   ```python
   # In settings.py
   import os
   
   DEBUG = os.environ.get('DEBUG', 'False') == 'True'
   ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
   
   # Static files
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   
   # Database
   if os.environ.get('DATABASE_URL'):
       import dj_database_url
       DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'))
   ```

3. **Create railway.json:**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn requirements_lab.wsgi:application"
     }
   }
   ```

4. **Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

Your app will be live at: `https://your-project.railway.app`

## 🔒 Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Set up proper CORS headers
- [ ] Use a production database (PostgreSQL recommended)

## 📝 Environment Variables Needed

```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://...
```

## 🎯 Next Steps After Deployment

1. **Custom Domain:** Most platforms allow custom domain setup
2. **SSL Certificate:** Usually automatic with hosting providers
3. **Monitoring:** Set up error tracking (Sentry recommended)
4. **Backups:** Configure database backups
5. **CI/CD:** Set up automatic deployments from Git

Choose the option that best fits your needs and budget. Railway is recommended for beginners due to its simplicity and generous free tier.
