# Flask Application Template

A production-ready Flask application template with modular design, robust error handling, and persistent storage.

## Features

- **Modular Architecture**
  - Blueprint-based route organization
  - Factory pattern for application creation
  - Separation of concerns in module structure

- **Robust Storage System**
  - Thread-safe persistent storage
  - JSON-based data persistence
  - In-memory caching for performance

- **Configuration Management**
  - Environment-specific configurations
  - Secure secret key handling
  - Environment variable integration

- **Error Handling & Logging**
  - Comprehensive error pages
  - Detailed logging system
  - Debug routes for testing

- **Modern Frontend**
  - Responsive design
  - Clean, modular CSS
  - Template inheritance
  - Flash messaging

## Project Structure

```
.
├── app/                    # Application package
│   ├── __init__.py        # Application factory
│   ├── routes/            # Route blueprints
│   │   └── __init__.py    # Route initialization
│   ├── models/            # Data models
│   │   └── __init__.py    # Model initialization
│   ├── templates/         # Jinja2 templates
│   │   ├── base.html      # Base template
│   │   └── index.html     # Index page
│   ├── static/            # Static assets
│   │   └── css/
│   │       └── styles.css # Central stylesheet
│   └── utils/             # Utility functions
│       └── __init__.py    # Utilities initialization
├── config/                # Configuration
│   └── config.py         # Config classes
├── storage/              # Data persistence
│   └── persistent.py     # Storage implementation
├── logs/                 # Application logs
│   ├── Progress.txt      # Development progress
│   └── Instructions.txt  # Setup instructions
├── requirements.txt      # Dependencies
└── run.py               # Application entry point
```

## Setup and Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env` (if provided)
   - Set required environment variables:
     - `FLASK_ENV`: development/testing/production
     - `SECRET_KEY`: Your secure secret key

4. Run the application:
   ```bash
   python run.py
   ```

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Write comprehensive docstrings
   - Keep functions focused and small

2. **Version Control**
   - Make atomic commits
   - Write descriptive commit messages
   - Use feature branches
   - Review code before merging

3. **Testing**
   - Write unit tests for new features
   - Ensure all tests pass before committing
   - Use the debug routes for testing
   - Monitor logs for issues

4. **Security**
   - Never commit sensitive data
   - Use environment variables for secrets
   - Keep dependencies updated
   - Follow Flask security best practices

## Production Deployment

1. Set `FLASK_ENV=production`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up proper logging
4. Configure a reverse proxy (e.g., Nginx)
5. Use HTTPS
6. Set a secure `SECRET_KEY`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 