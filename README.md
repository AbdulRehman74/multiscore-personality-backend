# Multiscore Personality App Backend

A FastAPI-based backend service for a comprehensive personality assessment application. The application provides a quiz-based personality evaluation system with scoring algorithms and result interpretation.

## Features

- **Personality Quiz System**: Dynamic question shuffling with seeded randomization
- **Advanced Scoring Algorithm**: Multi-dimensional personality trait calculation
- **Result Interpretation**: Detailed personality profile generation with dominant traits
- **RESTful API**: Well-documented endpoints with automatic OpenAPI documentation
- **Database Integration**: PostgreSQL with SQLAlchemy ORM (currently disabled in deployment)
- **Authentication System**: JWT-based user authentication (currently disabled in deployment)
- **Payment Processing**: Stripe integration for premium features (currently disabled in deployment)
- **Email Services**: SendGrid integration for notifications (currently disabled in deployment)
- **Error Monitoring**: Sentry integration for production monitoring
- **Admin Interface**: SQLAdmin for database management
- **CORS Support**: Configured for frontend integration

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.10
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Authentication**: JWT (JSON Web Tokens)
- **Payments**: Stripe
- **Email**: SendGrid
- **Monitoring**: Sentry
- **Admin Panel**: SQLAdmin
- **Deployment**: Docker 

## Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- PostgreSQL (for full functionality)
- Git
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Using Poetry (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd multiscore-personality-backend
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

   **Note:** If you encounter issues with the above command, try:
   ```bash
   poetry install --no-root
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

4. **Environment Configuration:**
   - Copy `.env.example` to `.env`
   - Fill in all required environment variables (see Environment Variables section)

5. **Run the application:**
   ```bash
   # Development
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Production
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Option 2: Using Docker

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd multiscore-personality-backend
   ```

2. **Environment Configuration:**
   - Copy `.env.example` to `.env`
   - Fill in all required environment variables (see Environment Variables section)

3. **Build and run with Docker:**
   ```bash
   # Build the Docker image
   docker build -t multiscore-personality-backend .

   # Run the container
   docker run -p 8000:8000 --env-file .env multiscore-personality-backend
   ```

   **Note:** The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## API Endpoints

### Core Quiz Endpoints
- `GET /api/v1/questions` - Retrieve shuffled quiz questions
- `POST /api/v1/score` - Calculate personality scores from responses

### Additional Features (Currently Disabled)
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/payment/create-session` - Create Stripe payment session
- `POST /api/v1/stripe/webhook` - Handle Stripe webhooks

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Application Settings
APP_NAME=Multiscore Personality App
VERSION=1.0.0
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (Required for full functionality)
POSTGRES_DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# File Paths
QUESTIONS_FILE=app/static/questions.json

# External Services (Required for full functionality)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG...
SENDGRID_URL=https://api.sendgrid.com/v3/mail/send
FRONTEND_DOMAIN=https://your-frontend-domain.com

# Monitoring (Optional)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_RELEASE=1.0.0
```

## Project Structure

```
multiscore-personality-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── admin.py                # SQLAdmin configuration
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── questions.py    # Quiz questions endpoint
│   │       ├── scoring.py      # Scoring calculation endpoint
│   │       ├── decision_tree.py
│   │       ├── payment.py      # Payment endpoints
│   │       └── stripe_webhook.py # Stripe webhook handler
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Application configuration
│   │   ├── database.py         # Database connection
│   │   ├── auth.py             # Authentication utilities
│   │   ├── scoring.py          # Scoring algorithms
│   │   ├── stripe_service.py   # Stripe integration
│   │   ├── email.py            # Email services
│   │   ├── response.py         # Response utilities
│   │   └── utils.py            # Utility functions
│   ├── models/
│   │   ├── __init__.py
│   │   ├── basemodels.py       # Base SQLAlchemy models
│   │   ├── user.py             # User model
│   │   ├── question.py         # Question model
│   │   └── scoring.py          # Scoring request/response models
│   └── static/
│       ├── questions.json      # Quiz questions data
│       └── results.json        # Personality results data
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_questions.py
│   └── test_scoring.py
├── Dockerfile
├── Procfile
├── pyproject.toml
├── requirements.txt
├── runtime.txt
└── README.md
```

## Deployment

The application supports multiple deployment options:

### Docker Deployment
```bash
# Build the image
docker build -t multiscore-personality-backend .

# Run the container
docker run -p 8000:8000 --env-file .env multiscore-personality-backend
```

## Current Deployment Status

**Active Features:**
- Personality quiz functionality
- Question shuffling and randomization
- Scoring algorithm and result generation
- API documentation

**Disabled Features (Present in Code but Not Active):**
- User authentication and registration
- Database operations
- Stripe payment processing
- Email notifications
- Admin panel

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary software. All rights reserved.

## Support

For support and questions, please contact the development team.

## Version History

- **v1.0.0**: Initial release with core quiz functionality
  - Personality assessment quiz
  - Scoring algorithm implementation
  - API documentation
  - Basic deployment configuration
