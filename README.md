# Precast Concrete Block Comparison Web App - Backend

This repository contains the backend implementation of the web application designed for comparing different sections of retaining walls using precast concrete blocks. The application generates reports on costs, materials, and CO2 emissions based on various block configurations. Customers can use the app to generate detailed reports for their own projects or businesses.

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Useful Links](#useful-links)
- [Contact](#contact)

## Overview

The backend is built using Django and Django Rest Framework (DRF). It provides API endpoints for managing user accounts, block comparisons, projects, and reports. The backend handles user authentication, report generation, and database interactions, ensuring a smooth experience for the client-side application.

## Technologies Used

- **Python** - Main programming language
- **Django 5.1.1** - Web framework
- **Django Rest Framework 3.15.2** - For building the API
- **PostgreSQL** - Database for storing user, project, and report data
- **Djoser 2.2.3** - For user authentication and management
- **SimpleJWT 5.3.1** - JWT-based authentication
- **CORS Headers 4.4.0** - To manage cross-origin requests
- **Pytest 8.3.2** - For unit testing
- **Python-dotenv 1.0.1** - For managing environment variables

## Setup and Installation

To get the backend running locally, follow the steps below:

### 1. Clone the repository

```bash
git clone git@github.com:ItalianCookieMonster/section_comparison_tool_back.git
cd repo-name
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate  # For Windows use `env\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory and add the following variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1
DATABASE_URL=postgres://username:password@localhost:5432/your-db-name
```

### 5. Database Setup

Ensure PostgreSQL is installed and running. Run the following commands to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Running the Project

To run the backend locally, use the following command:

```bash
python manage.py runserver
```

The server will be available at `http://127.0.0.1:8000/`.

## API Documentation

API endpoints are structured as follows:
- **/api/auth/**: Authentication-related endpoints (login, registration, password reset)
- **/api/projects/**: CRUD operations for projects
- **/api/blocks/**: Block data and comparisons
- **/api/reports/**: Report generation for projects

More detailed API documentation can be found in the project’s Postman collection or Swagger documentation (coming soon).

## Testing

Unit tests are handled using `pytest`. To run tests, use the following command:

```bash
pytest
```

For test coverage, run:

```bash
pytest --cov=.
```

## Useful Links

- [Database Schema]((https://drawsql.app/teams/valentina-5/diagrams/section-comparison-tool)) 
- [Figma Design](https://www.figma.com/design/mV7H0yoqPbrsKBMeVzv3vH/Wireframe-BlockCalculator?node-id=23-6674&t=ZMFFcyeQMrXhfIZ9-1) 
- [Flowchart](https://drive.google.com/file/d/15my32Zdf100SE88YOFgBbZMQrayNrGWT/view?usp=sharing)

## Contact

For inquiries, reach out via [LinkedIn]([https://linkedin.com/in/your-linkedin-profile](https://www.linkedin.com/in/valentinatoni/)).
