# Render.com Deployment Guide

This guide provides step-by-step instructions for deploying the Harmonica Tabs application to Render.com.

## Prerequisites

- Active Render.com account (free tier available)
- GitHub repository with your code
- Local development environment set up

## Phase 1: Local Preparation (Completed)

The following files have been prepared for deployment:

### 1. Production Dependencies
- `requirements.txt` updated with `psycopg2-binary` and `gunicorn`
- These are essential for PostgreSQL connectivity and production serving

### 2. Configuration Files
- `render.yaml` - Render service configuration
- `.env.example` - Environment variable template
- `config.py` - Environment-specific configurations

### 3. Database Migration
- `scripts/migrate_to_postgres.py` - SQLite to PostgreSQL migration script
- Health check endpoint added at `/health`

## Phase 2: Render Setup

### 1. Create Render Account
1. Visit [render.com](https://render.com)
2. Sign up with GitHub or email
3. Verify your email address

### 2. Connect GitHub Repository
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub account
4. Select your harmonica-tabs repository

### 3. Configure Web Service
Render will automatically detect your `render.yaml` file. The configuration includes:
- **Runtime**: Python 3.9
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"`
- **Health Check**: `/health` endpoint

### 4. Set Up PostgreSQL Database
1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Choose "Free" plan
4. Name: `harmonica-tabs-db`
5. Click "Create Database"

### 5. Configure Environment Variables
In your web service settings, add these environment variables:

```bash
# Required
DATABASE_URL=postgresql://username:password@host:5432/database_name
SECRET_KEY=your-very-secure-production-secret-key

# Production settings
FLASK_ENV=production
FLASK_DEBUG=False
```

**Important**: Get the `DATABASE_URL` from your PostgreSQL service dashboard.

## Phase 3: Deployment

### 1. Push Changes to GitHub
```bash
git add .
git commit -m "Add Render.com deployment configuration"
git push origin main
```

### 2. Trigger Render Build
1. Render will automatically start building when you push
2. Monitor the build log in Render dashboard
3. If build fails, check the logs for errors

### 3. Initialize Database
After successful deployment, run the database initialization:

```bash
# Option 1: Use Render Shell (recommended)
# In your web service dashboard, click "Shell" and run:
python init_db.py

# Option 2: Run migration script (if you have existing SQLite data)
python scripts/migrate_to_postgres.py

# Create admin user
python scripts/migrate_to_postgres.py create-admin
```

### 4. Test Application
1. Visit your Render URL (e.g., `https://harmonica-tabs.onrender.com`)
2. Test basic functionality:
   - Homepage loads
   - Search works
   - User registration/login
   - Admin panel access

## Phase 4: Post-Deployment

### 1. Monitor Application
- Check Render logs regularly
- Monitor database usage
- Set up alerts if needed

### 2. Custom Domain (Optional)
1. In your web service settings, click "Custom Domains"
2. Add your domain name
3. Update DNS records as instructed

### 3. Backup Strategy
- Enable automatic backups in PostgreSQL settings
- Regularly export data if needed

## Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check requirements.txt format
pip install -r requirements.txt

# Verify Python version compatibility
python --version  # Should be 3.9+
```

#### Database Connection Errors
```bash
# Verify DATABASE_URL format
# Should be: postgresql://user:pass@host:5432/dbname

# Test connection manually
python -c "import psycopg2; conn = psycopg2.connect('your-database-url'); print('Connected!')"
```

#### Health Check Failures
```bash
# Check health endpoint
curl https://your-app.onrender.com/health

# Should return: {"status": "healthy", "database": "connected", ...}
```

#### Static File Issues
- Ensure static files are in `app/static/` directory
- Check template paths for CSS/JS references

### Performance Optimization

#### Database Indexes
```bash
# Create performance indexes
python scripts/create_indexes.py
```

#### Caching
Consider adding Redis for session storage in production:
```bash
# Add to requirements.txt
redis
flask-session

# Set environment variables
REDIS_URL=redis://host:port
```

## Security Best Practices

1. **Strong SECRET_KEY**: Use a random, long string
2. **Database Security**: Use SSL connections (default on Render)
3. **Regular Updates**: Keep dependencies updated
4. **Monitor Logs**: Watch for suspicious activity

## Cost Management

### Free Tier Limits
- **Web Service**: 750 hours/month (sufficient for 24/7)
- **PostgreSQL**: 256MB RAM, 10GB storage
- **Bandwidth**: 100GB/month

### Optimization Tips
- Optimize database queries
- Use efficient pagination
- Monitor resource usage
- Consider caching for frequent queries

## Maintenance

### Regular Tasks
1. Update dependencies monthly
2. Monitor database size
3. Review logs weekly
4. Backup data regularly

### Updates and Deployments
```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Render automatically deploys changes
```

## Support

### Render Documentation
- [Render Docs](https://render.com/docs)
- [Flask Deployment Guide](https://render.com/docs/deploy-flask)

### Common Questions
- **How long does deployment take?**: Usually 2-5 minutes
- **Can I use a custom domain?**: Yes, on free tier
- **Is SSL included?**: Yes, automatic SSL certificates
- **How do I access logs?**: In Render dashboard under "Logs"

## Next Steps

After successful deployment:
1. Set up monitoring and alerts
2. Configure custom domain if desired
3. Implement backup strategies
4. Consider performance optimizations
5. Plan for scaling if needed

## Emergency Procedures

### If Application Goes Down
1. Check Render status page
2. Review deployment logs
3. Check environment variables
4. Restart service if needed
5. Contact Render support if issues persist

### Database Issues
1. Check PostgreSQL service status
2. Verify connection string
3. Run health check endpoint
4. Restore from backup if necessary
