# SkillForge 

SkillForge is an e-commerce Django web application that allows users to browse, book, and review skill-based workshops. The platform supports secure payments via Stripe, authentication, and marketing integrations like a newsletter signup and Facebook page.

Live Site: Heroku Deployment Link

## Table of Contents

- Project Overview

- Business Model & Marketing Strategy

- User Stories

- Agile Methodology

- Features

- Database Schema

- Technologies Used

- Testing

- Deployment

- Credits

## Project Overview

- SkillForge is a workshop booking platform designed for learners and instructors. Users can:

- Register/login to manage bookings.

- Browse workshops, sessions, and reviews.

- Purchase workshop seats securely using Stripe.

- Subscribe to a newsletter for updates.

__Admin/staff can:__

- Add/edit workshops, sessions, and instructors.

- View bookings and manage categories.

## Business Model & Marketing Strategy 

__Business Model__

- Direct-to-Consumer (D2C) services: Customers purchase workshop seats directly.

- Digital transactions: Stripe handles secure payments.

- Scalable: Admins can add unlimited workshops/sessions.

__Marketing Strategy__

- Facebook Page: A real/mockup business page showcases workshops and builds community.

- Newsletter Signup: Users join a mailing list for promotions and updates.

- SEO: Sitemap, robots.txt, and descriptive meta tags implemented.

- Retention: Users receive confirmation of bookings and can leave reviews.

## User Stories

- As a user, I can create an account so I can book workshops.

- As a user, I can browse upcoming workshops so I can choose one to attend.

- As a user, I can pay securely online so I can confirm my booking.

- As a user, I can leave reviews so I can share my experience.

- As an admin, I can add/edit workshops so I can manage content without the admin panel.

- As an admin, I can see bookings so I know attendance numbers.

## Agile Methodology

- GitHub Projects board used to manage tasks.

- User stories broken into issues with acceptance criteria.

- Feature branches used for development (e.g., feature/checkout, feature/marketing).

- Frequent commits with meaningful messages.

- Screenshot of GitHub Projects board here

## Features

- Custom Models (Workshops, Sessions, Bookings, NewsletterSubscriber)
- CRUD functionality on frontend (workshops, sessions, reviews)
- Delete UI for reviews
- User authentication (login, signup, logout)
- Stripe checkout integration with seat decrement
- Newsletter signup form
- Facebook marketing page mockup
- robots.txt, sitemap.xml, and meta tags for SEO
- Custom 404 page
- Responsive design with global CSS

Screenshots of home, detail, checkout, auth pages here

## Database Schema

- WorkshopCategory → Workshops → Sessions → Bookings
- Reviews linked to Workshops
- NewsletterSubscriber standalone for marketing

erDiagram
  USER ||--|| INSTRUCTOR : "profile of"
  USER ||--o{ BOOKING : "makes"}
  USER ||--o{ REVIEW : "writes"}

  WORKSHOPCATEGORY ||--o{ WORKSHOP : "has many"}
  INSTRUCTOR ||--o{ WORKSHOP : "teaches"}
  WORKSHOP ||--o{ SESSION : "has many"}
  WORKSHOP ||--o{ REVIEW : "receives"}
  SESSION ||--o{ BOOKING : "booked by"}

  NEWSLETTERSUBSCRIBER {
    int id PK
    varchar email UNIQUE
    datetime created_at
  }

  USER {
    int id PK
    varchar username
    varchar email
    varchar password
    datetime date_joined
  }

  INSTRUCTOR {
    int id PK
    int user_id FK -> USER.id UNIQUE
    text bio
    url website
  }

  WORKSHOPCATEGORY {
    int id PK
    varchar name UNIQUE
    varchar slug UNIQUE
  }

  WORKSHOP {
    int id PK
    int category_id FK -> WORKSHOPCATEGORY.id
    int instructor_id FK -> INSTRUCTOR.id
    varchar title
    varchar slug UNIQUE
    varchar short_description
    text description
    decimal base_price
    varchar image
    bool is_active
    datetime created
  }

  SESSION {
    int id PK
    int workshop_id FK -> WORKSHOP.id
    datetime starts_at
    datetime ends_at
    int capacity
    int seats_sold
    varchar location
  }

  BOOKING {
    int id PK
    int user_id FK -> USER.id
    int session_id FK -> SESSION.id
    int quantity
    decimal unit_price
    decimal total
    varchar stripe_pi
    bool paid
    datetime created
  }

  REVIEW {
    int id PK
    int workshop_id FK -> WORKSHOP.id
    int user_id FK -> USER.id
    smallint rating (1..5)
    text comment
    datetime created
    UNIQUE(workshop_id,user_id)
  }


## Technologies Used

- Backend: Django, Python

- Database: PostgreSQL (Heroku)

- Frontend: HTML, CSS, Bootstrap 5

- Payments: Stripe API

- Auth: Django-allauth

- Deployment: Heroku, Gunicorn, WhiteNoise

- Other: dj-database-url, python-dotenv, Pillow

## Testing
__Code Validation__

- HTML/CSS validated with W3C.

- Python checked with PEP8 (flake8).

__Functional Testing__

- Authentication: login/logout/signup/reset tested.

- Workshops: CRUD verified.

- Booking flow: Seat decrement after payment confirmed.

- Newsletter: Valid/invalid email submissions tested.

- Stripe: Test cards used successfully.

__Responsiveness__

- Tested on Chrome.

__Automated Tests__

- Basic unit tests for models (e.g., slug generation, seat availability) and booking flow.

- Screenshots of testing evidence here

## Deployment
__Local Development__

- Clone repo

- Create venv & install requirements:

- pip install -r requirements.txt

- Add .env with keys:
SECRET_KEY=yourkey
DEBUG=1
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
ALLOWED_HOSTS=localhost,127.0.0.1,.gitpod.io
CSRF_TRUSTED_ORIGINS=https://*.gitpod.io,http://localhost


- Run server:

- python manage.py runserver 0.0.0.0:8000

__Heroku Deployment__

- Push to GitHub.

- Connect Heroku app → GitHub repo.

- Set config vars (SECRET_KEY, STRIPE_*, etc).

- Add Postgres addon.

- Deploy branch.

- Run python manage.py migrate via Heroku CLI.

## Credits

- Stripe API docs.

- Bootstrap 5.

- Django & django-allauth documentation.

- Code Institute template guidance.