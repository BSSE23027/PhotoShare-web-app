# PhotoShare

A social photo-sharing web application built with Django and PostgreSQL that enables authenticated users to upload, view, and share photos within a private community. The platform provides secure user authentication, personalized profiles, and a responsive gallery experience optimized for desktop and mobile devices.

## Features

* User registration and authentication
* Secure login and session management
* Photo upload and sharing
* Responsive photo gallery interface
* Photo captions and descriptions
* User profile management
* Private community access (authenticated users only)
* PostgreSQL database integration
* Responsive design using Bootstrap
* Cloud deployment on PythonAnywhere

## Technology Stack

### Backend

* Django
* Python
* PostgreSQL

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

### Deployment

* PythonAnywhere

## System Architecture

The application follows Django's Model-View-Template (MVT) architecture:

* **Models:** Manage users, photos, and related metadata.
* **Views:** Handle user requests, authentication, uploads, and gallery rendering.
* **Templates:** Provide a responsive user interface using Bootstrap.
* **Database:** PostgreSQL stores user accounts, photo information, and application data.

## Key Functionalities

### User Authentication

* User registration
* Login and logout
* Session management
* Access control for authenticated users

### Photo Management

* Upload photos
* Add captions and descriptions
* View shared photos
* Browse community gallery

### User Profiles

* Personalized user accounts
* Profile information management
* User-specific photo collections

## Installation

### Prerequisites

* Python 3.x
* PostgreSQL
* pip

### Clone Repository

```bash
git clone https://github.com/your-username/photoshare.git
cd photoshare
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database

Update the PostgreSQL database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database_name',
        'USER': 'database_user',
        'PASSWORD': 'database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

## Deployment

The application was deployed on PythonAnywhere using:

* Django web framework
* PostgreSQL database
* WSGI configuration
* Static file management

## Learning Outcomes

This project provided practical experience with:

* Full-stack web development using Django
* Authentication and authorization systems
* Database design and management with PostgreSQL
* Responsive UI development using Bootstrap
* Deployment and hosting on PythonAnywhere
* Secure session handling
* MVC/MVT application architecture

## Future Improvements

* Photo likes and reactions
* Comment system
* User following functionality
* Image optimization and compression
* Search and filtering features
* REST API integration
* Cloud storage for media files

## Author

Developed as part of academic and personal learning in Software Engineering, focusing on backend development, database management, and web application deployment.
