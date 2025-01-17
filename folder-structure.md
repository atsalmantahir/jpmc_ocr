/project-root
│
├── /api                    # Flask backend API (previously 'server')
│   ├── /src                # Main application logic (formerly 'app')
│   │   ├── /models         # Database models (SQLAlchemy models, Pydantic schemas)
│   │   ├── /routes         # API routes (views or controllers)
│   │   ├── /services       # Business logic (e.g., authentication, user management)
│   │   ├── /utils          # Utility functions (logging, error handling)
│   │   ├── /config         # Configuration files (API settings, database settings)
│   │   ├── /migrations     # Database migrations (Flask-Migrate)
│   │   └── __init__.py     # Initialize Flask app
│   ├── /venv               # Virtual environment for backend dependencies
│   ├── /requirements.txt   # Flask dependencies
│   ├── /run.py             # Entry point to run the Flask application
│   └── /swagger.json       # Swagger JSON definition (optional)
│
├── /client                 # React frontend (Admin and User Panels)
│   └── ...
├── /docker                 # Docker-related files (if using Docker)
├── /docs                   # Documentation (API docs, how to run the app, etc.)
└── /tests                  # Unit and integration tests
