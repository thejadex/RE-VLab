# Vercel Deployment Guide for RE VLab

This guide will help you deploy the RE VLab Django application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional): Install via `npm i -g vercel`
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### 1. Connect Repository to Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Select the repository containing RE VLab

### 2. Configure Build Settings

When importing, Vercel will ask for build settings:

- **Framework Preset**: Other
- **Build Command**: Leave empty (handled by vercel.json)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### 3. Environment Variables

Add these environment variables in your Vercel project settings:

```bash
# Required
DJANGO_SETTINGS_MODULE=requirements_lab.settings
SECRET_KEY=your-super-secret-key-generate-a-new-one
DEBUG=False

# Optional - Database (default uses SQLite)
DATABASE_URL=postgresql://user:password@host:port/database

# Security (recommended for production)
ALLOWED_HOSTS=.vercel.app
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https

# Vercel-specific
VERCEL=1
VERCEL_ENV=production
```

### 4. Deploy

1. Click "Deploy" in Vercel dashboard
2. Wait for the build to complete
3. Your app will be available at `https://your-project-name.vercel.app`

## Database Configuration

### Option 1: SQLite (Default)
- No additional setup required
- Data persists between deployments
- Suitable for development/small projects

### Option 2: External PostgreSQL
1. Set up a PostgreSQL database (e.g., Neon, Supabase, Railway)
2. Add `DATABASE_URL` environment variable
3. Run migrations on first deployment

### Option 3: Vercel Postgres
1. Enable Vercel Postgres in your project
2. Vercel will automatically set `POSTGRES_URL`
3. Update `settings.py` to use `POSTGRES_URL` if available

## Custom Domain (Optional)

1. Go to your Vercel project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## File Structure

Your project should have these Vercel-specific files:

```
RE-VLab/
├── vercel.json              # Vercel configuration
├── build_files.sh           # Build script
├── requirements.txt         # Python dependencies
├── .env.vercel.template     # Environment variables template
├── requirements_lab/
│   ├── wsgi.py             # Updated for Vercel
│   └── settings.py         # Updated with Vercel support
└── manage.py
```

## Troubleshooting

### Common Issues:

1. **Build Timeout**: Reduce dependencies or use a smaller Docker image
2. **Static Files Not Loading**: Check `STATIC_ROOT` and `STATICFILES_STORAGE` settings
3. **Database Connection**: Ensure `DATABASE_URL` is correctly formatted
4. **Secret Key**: Generate a new secret key for production

### Debug Deployment:

1. Check Vercel function logs in the dashboard
2. Use Vercel CLI: `vercel logs your-project-name`
3. Enable Django debug mode temporarily (not recommended for production)

## Security Considerations

1. **Never commit secrets**: Use environment variables
2. **Generate new SECRET_KEY**: Don't use the default development key
3. **Enable HTTPS**: Set `SECURE_SSL_REDIRECT=True`
4. **Database Security**: Use strong passwords and SSL connections

## Performance Tips

1. **Static Files**: Use Vercel's CDN for static files
2. **Database**: Choose a database close to your users
3. **Caching**: Implement Django caching for better performance
4. **Monitoring**: Use Vercel Analytics to monitor performance

## Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

### Vercel CLI Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Production deployment
vercel --prod
```

## Support

For issues specific to this Django application, check the main README.md.
For Vercel-specific issues, consult the [Vercel Documentation](https://vercel.com/docs).
