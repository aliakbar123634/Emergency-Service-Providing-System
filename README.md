# 🚑 Emergency Service Providing System (Backend)

A **production-ready Django REST API** for an emergency service platform where users can request services (e.g., plumber, electrician), providers can accept jobs, and payments are securely handled via a wallet system.

---

## 🔥 Live API

👉 https://emergency-service-providing-system-production.up.railway.app/

---

## 🧠 System Overview

This project simulates a **real-world service marketplace backend**, focusing on secure transactions, role-based access control, and scalable architecture.

---

## 🔄 System Flow

* User registers and authenticates using JWT
* User creates a service request
* Providers browse and accept requests
* User makes payment via wallet
* Platform deducts a **15% service fee automatically**
* Provider completes the service
* User submits a review and rating

---

## ⚡ Key Technical Highlights

* **Atomic Transactions** → Prevents double-spending and ensures data consistency
* **Role-Based Permissions** → Fine-grained access control for users, providers, and admins
* **Modular Architecture** → Decoupled apps (accounts, payments, requests, reviews, etc.)
* **Decimal-Based Calculations** → Financial accuracy in payment processing
* **RESTful API Design** → Built with DRF ViewSets, serializers, and routers
* **Production Deployment** → Live on Railway with PostgreSQL

---

## 🚀 Core Features

### 👤 Authentication & Security

* JWT authentication (login & refresh)
* Email verification system
* Forgot / reset password workflow
* Secure password change

---

### 🧾 Service Management

* Service category management
* Provider service profiles
* Activate / deactivate services
* Fetch providers per service

---

### 📍 Service Requests

* Create and manage service requests
* Track request lifecycle (**pending → accepted → completed**)
* Update and delete requests

---

### 💳 Wallet & Payment System (Core Feature)

* Wallet-based payment processing
* Automatic **15% platform fee deduction**
* Atomic database transactions for safe balance updates
* Transaction history tracking
* Payment status management

---

### ⭐ Reviews & Ratings

* Users can rate and review providers
* Full CRUD support for reviews

---

### 🔔 Notifications (API Ready)

* Notification CRUD APIs implemented
* Designed for future integration with **FCM / WebSockets**

---

## 🛠️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Authentication:** JWT (SimpleJWT)
* **Database:** PostgreSQL (Railway)
* **Deployment:** Railway
* **Static Files:** WhiteNoise
* **Image Handling:** Pillow

---

## ⚙️ Local Setup

```bash
git clone https://github.com/your-username/Emergency-Service-Providing-System.git
cd Emergency-Service-Providing-System

python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate

pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@host:port/dbname

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@example.com
EMAIL_HOST_PASSWORD=your-email-password

ALLOWED_HOSTS=localhost,127.0.0.1
```

> In production, set `DEBUG=False` and use Railway’s `DATABASE_URL`.

---

## 🧱 Run Locally

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 🚀 Deployment (Railway)

Deployed using Railway with PostgreSQL.

### Start Command

```bash
python manage.py migrate && gunicorn main.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 📡 API Overview

### 🔐 Auth

* POST `/api/token/`
* POST `/api/token/refresh/`
* POST `/send-verification-email/`
* POST `/verify-email/`
* POST `/forgot-password/`
* POST `/reset-password/`
* POST `/change-password/`

### 🧾 Services

* GET / POST `/service/`
* PATCH / DELETE `/service/{id}/`

### 📍 Requests

* GET / POST `/requests/`
* PATCH / DELETE `/requests/{id}/`

### 💳 Payments

* POST `/payments/pay/`
* GET `/payments/{id}/detail/`
* GET `/wallet/`

### ⭐ Reviews

* CRUD `/review/`

### 🔔 Notifications

* CRUD `/notification/`

---

## 🧠 Engineering Decisions

* Used transactions to guarantee consistency in wallet operations
* Separated concerns using modular Django apps
* Used JWT instead of session auth for scalability
* Designed APIs to be frontend-independent

---

## 📚 Learnings & Experience

* Built a **production-style backend system**
* Implemented **secure financial logic with atomic transactions**
* Learned **cloud deployment (Railway + PostgreSQL)**
* Structured scalable APIs using DRF best practices

---

## 📌 Future Improvements

* 📍 Location-based provider matching (Google Maps API)
* 💬 Real-time chat system (Django Channels)
* 🔔 Push notifications (Firebase Cloud Messaging)
* 📊 Admin analytics dashboard
* 📄 API documentation (Swagger / Redoc)

---

## 👨‍💻 Author

**Muhammad Ali AKBAR**
Backend Developer (Django / DRF)

---

## ⭐ Final Note

This project demonstrates a **real-world backend system** with production-level concepts including authentication, service workflows, and secure payment handling.
