# Harmonica Tabs Project

A modern web application for browsing and managing harmonica tabs. Built with Flask and designed to provide an intuitive interface for harmonica players to find and share tablature.

## Features

- **🔍 Advanced Search**: Search by artist, song, or genre with filters for difficulty, harp type, and key
- **📊 Smart Sorting**: Sort tabs by artist, song title, difficulty, key, or date added
- **👤 User Management**: Registration, login, and role-based access (admin, editor, viewer)
- **⭐ Favorites System**: Save and organize your favorite tabs
- **📝 Tab Management**: Add, edit, and delete tabs (admin/editor roles)
- **🔒 Security**: CSRF protection, input validation, and secure password handling
- **📱 Responsive Design**: Mobile-friendly interface using Bootstrap 5

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd harmonica_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   ```

6. **Create search indexes** (optional but recommended for performance)
   ```bash
   python scripts/create_indexes.py
   ```

7. **Run the application**
   ```bash
   python run.py
   ```

Visit `http://127.0.0.1:5000` in your browser.

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/harmonica_tabs.db

# Development Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### Production Deployment

For production deployment:

1. **Use a production database** (PostgreSQL recommended):
   ```bash
   DATABASE_URL=postgresql://username:password@localhost/harmonica_tabs
   ```

2. **Set production variables**:
   ```bash
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=your-very-secure-secret-key
   ```

3. **Use a production WSGI server** (like Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
   ```

## Project Structure

```
harmonica_project/
├── app/                    # Main application package
│   ├── __init__.py         # Application factory
│   ├── models.py           # Database models
│   ├── routes.py           # Main application routes
│   ├── forms.py            # WTForms classes
│   ├── auth.py             # Authentication routes
│   ├── decorators.py       # Custom decorators
│   ├── templates/          # Jinja2 templates
│   └── static/            # CSS, JS, images
├── database/               # Database files
├── scripts/               # Utility scripts
├── config.py              # Configuration
├── run.py                # Application runner
├── init_db.py            # Database initialization
├── requirements.txt       # Python dependencies
└── .env.example          # Environment template
```

## User Roles

- **Viewer**: Browse and search tabs, save favorites
- **Editor**: All viewer permissions + add/edit tabs
- **Admin**: All permissions + user management

## API Endpoints

### Public Routes
- `GET /` - Homepage with tab listings
- `GET /search` - Search tabs with filters
- `GET /tab/<id>` - View specific tab

### Authentication Routes
- `GET /auth/login` - Login page
- `GET /auth/register` - Registration page
- `POST /auth/login` - Login submission
- `POST /auth/register` - Registration submission
- `GET /auth/logout` - Logout

### Protected Routes
- `GET /favorites` - User's favorite tabs
- `GET /profile` - User profile
- `POST /change_password` - Change password
- `GET|POST /add-tab` - Add new tab (editor+)
- `GET|POST /edit-tab/<id>` - Edit tab (editor+)
- `POST /delete-tab/<id>` - Delete tab (admin only)

## Database Schema

### Tables
- **users**: User accounts and authentication
- **tabs**: Harmonica tab information
- **favorites**: Many-to-many relationship between users and tabs

### Search Indexes
Performance indexes on:
- `tabs.artist` (case-insensitive)
- `tabs.song` (case-insensitive)  
- `tabs.genre` (case-insensitive)

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Code Style
This project follows PEP 8 guidelines. Use:
```bash
pip install flake8
flake8 app/
```

### Adding New Features

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Make your changes
3. Test thoroughly
4. Commit with descriptive messages
5. Push and create pull request

## Troubleshooting

### Common Issues

**Database errors**: Ensure database directory exists and is writable
```bash
mkdir -p database
chmod 755 database
```

**Import errors**: Check virtual environment activation
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Permission errors**: Check file permissions, especially on database files

### Logging

The application includes comprehensive logging. Check logs for:
- Database connection issues
- Authentication failures
- Form validation errors
- Performance bottlenecks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure code follows project style
5. Submit a pull request with clear description

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Support

For questions, issues, or contributions:
- Create an issue in the repository
- Check existing documentation first
- Provide detailed error reports with environment details

