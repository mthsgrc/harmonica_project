# Render.com Deployment Checklist

## ✅ Pre-Deployment Tests (Completed)

- [x] Production dependencies installed (psycopg2-binary, gunicorn)
- [x] App factory works with environment configuration
- [x] Health check endpoint responds correctly
- [x] Gunicorn configuration is valid
- [x] Migration script ready for use

## 🚀 Deployment Steps

### 1. Commit Changes
```bash
git add .
git commit -m "Add Render.com deployment configuration"
git push origin main
```

### 2. Create Render Account & Services
- [ ] Sign up at render.com
- [ ] Connect GitHub repository
- [ ] Create PostgreSQL database (Free tier)
- [ ] Create web service (auto-detected from render.yaml)

### 3. Configure Environment Variables
In Render web service dashboard:
- [ ] Set DATABASE_URL (from PostgreSQL service)
- [ ] Set SECRET_KEY (generate secure random string)
- [ ] Set FLASK_ENV=production
- [ ] Set FLASK_DEBUG=False

### 4. Initialize Database
After deployment completes:
- [ ] Access Render Shell for web service
- [ ] Run: `python init_db.py`
- [ ] Run: `python scripts/migrate_to_postgres.py` (if migrating data)
- [ ] Run: `python scripts/migrate_to_postgres.py create-admin`

### 5. Test Application
- [ ] Visit your-app.onrender.com
- [ ] Test homepage loads
- [ ] Test search functionality
- [ ] Test user registration/login
- [ ] Test admin panel (username: admin, password: admin123)

## 🔧 Generate Secure SECRET_KEY

Use this command to generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```

## 📊 Expected Render Configuration

### Web Service
- **Runtime**: Python 3.9
- **Build**: `pip install -r requirements.txt`
- **Start**: `gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"`
- **Health Check**: `/health`

### PostgreSQL Database
- **Plan**: Free (256MB RAM, 10GB storage)
- **Connection**: SSL enabled
- **Backups**: Automatic

## 🚨 Troubleshooting Quick Reference

### Build Fails
- Check requirements.txt format
- Verify Python version compatibility
- Review build logs

### Database Connection Issues
- Verify DATABASE_URL format
- Check PostgreSQL service status
- Test connection manually

### Health Check Fails
- Visit `/health` endpoint
- Check application logs
- Verify database connectivity

## 🎯 Success Indicators

✅ Web service builds and deploys successfully  
✅ Health check returns status 200  
✅ Database tables created  
✅ Application loads in browser  
✅ User registration/login works  
✅ Admin panel accessible  

## 📝 Post-Deployment

- [ ] Monitor application logs
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring alerts
- [ ] Test all features thoroughly
- [ ] Document any issues

## 🆘 Support Resources

- [Render Documentation](https://render.com/docs)
- [Flask on Render Guide](https://render.com/docs/deploy-flask)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

**Ready to deploy!** 🚀
