# FHIR NLP Backend Service

## Overview

This Django backend accepts natural language queries about patients (e.g., “Show me all diabetic patients over 50”) and converts them into simulated FHIR API requests. It also returns example patient results.

## Requirements

- Python 3.10+
- Django 5.2+
- Django REST Framework
- spaCy (`en_core_web_sm`)
- django-cors-headers

```bash
Clone the repository:

git clone <your-repo-url>
cd backend_project

Install dependencies:

pip install django djangorestframework spacy django-cors-headers
python -m spacy download en_core_web_sm

Run the Backend

python manage.py migrate
python manage.py runserver
