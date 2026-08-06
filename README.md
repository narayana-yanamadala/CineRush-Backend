# 🎬 CineRush - Movie Ticket Booking System

<p align="center">
  <img src="https://img.shields.io/badge/React.js-Frontend-blue?logo=react" />
  <img src="https://img.shields.io/badge/Django-Backend-green?logo=django" />
  <img src="https://img.shields.io/badge/DRF-REST%20API-red" />
  <img src="https://img.shields.io/badge/JWT-Authentication-orange" />
  <img src="https://img.shields.io/badge/Twilio-OTP%20Verification-red" />
  <img src="https://img.shields.io/badge/Status-Live-success" />
</p>

<p align="center">
  <b>A Full-Stack Movie Ticket Booking Platform built using React.js and Django REST Framework.</b>
</p>

<p align="center">
  Browse Movies • Book Seats • Generate Tickets • OTP Authentication
</p>

---

## 🌐 Live Demo

### 🎬 Frontend Application

🔗 https://cinerush-gamma.vercel.app/

### ⚙️ Backend API

🔗 http://127.0.0.1:8000/

---

## 📖 Project Overview

CineRush is a full-stack movie ticket booking application that enables users to browse movies, search and filter movie listings, select seats, book tickets, and manage booking history through a modern and responsive interface.

The platform incorporates secure JWT Authentication, OTP verification using Twilio Verify API, real-time seat booking workflow, and PDF ticket generation to provide a complete movie ticket booking experience.

---

## ✨ Features

### 🔐 Authentication & Security

* User Registration
* Secure Login System
* JWT Authentication
* Protected Routes
* OTP Verification using Twilio Verify API

### 🎥 Movie Management

* Browse Available Movies
* Movie Details Page
* Search Movies
* Filter Movies by Category
* Responsive Movie Catalog

### 🎟️ Ticket Booking

* Interactive Seat Selection
* Real-Time Seat Availability
* Ticket Booking Workflow
* Booking Confirmation
* Booking History Management

### 📄 Ticket Generation

* PDF Ticket Generation
* Downloadable Tickets
* Booking Summary
* Digital Ticket Storage

### 📱 Responsive UI

* Mobile-Friendly Design
* Reusable React Components
* Responsive Layout
* Smooth Navigation using React Router

---

## 🛠️ Technology Stack

### Frontend

* React.js
* Context API
* React Router DOM
* Bootstrap
* Axios

### Backend

* Django
* Django REST Framework (DRF)
* JWT Authentication
* Twilio Verify API

### Database

* SQLite

### Deployment

* Vercel (Frontend)
* Render (Backend)

---

## 🏗️ System Architecture

```text
User
 │
 ▼
React Frontend
 │
 ▼
Django REST API
 │
 ├── Authentication
 ├── OTP Verification
 ├── Movie Management
 ├── Booking Management
 └── Ticket Generation
 │
 ▼
SQLite Database
```

---

## 📂 Project Structure

```text
CineRush-MovieApp
│
├── movieapp/                  # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── context/
│   │   ├── routes/
│   │   └── services/
│
├── myproject/                 # Django Backend
│   ├── accounts/
│   ├── movies/
│   ├── bookings/
│   ├── myproject/
│   ├── manage.py
│   ├── requirements.txt
│   └── Procfile
│
└── README.md
```

---

## 🚀 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/narayana-yanamadala/CineRush-MovieApp.git

cd CineRush-MovieApp
```

### 2️⃣ Backend Setup

Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Apply Migrations

```bash
python manage.py migrate
```

Run Backend Server

```bash
python manage.py runserver
```

Backend runs at:

```text
http://127.0.0.1:8000/
```

---

### 3️⃣ Frontend Setup

Navigate to Frontend Directory

```bash
cd movieapp
```

Install Packages

```bash
npm install
```

Start Frontend

```bash
npm start
```

Frontend runs at:

```text
http://localhost:3000/
```

---

## 🔐 Environment Variables

Create a `.env` file inside the backend directory:

```env
SECRET_KEY=your_django_secret_key

TWILIO_ACCOUNT_SID=your_account_sid

TWILIO_AUTH_TOKEN=your_auth_token

TWILIO_VERIFY_SERVICE_SID=your_verify_service_sid
```

### Important

⚠️ Never commit `.env` files to GitHub.

⚠️ Keep API keys and credentials secure.

---

## 🎯 API Features

* User Registration API
* User Login API
* OTP Verification API
* Movie Listing API
* Movie Details API
* Seat Booking API
* Booking History API
* Ticket Generation API

---

## 📸 Screenshots

### Home Page

```text
Add Screenshot Here
```

### Movies Page

```text
Add Screenshot Here
```

### Seat Booking Page

```text
Add Screenshot Here
```

### Booking Confirmation Page

```text
Add Screenshot Here
```

---

## 🌟 Key Highlights

✔ Full-Stack Application Development

✔ React.js Frontend Development

✔ Django REST API Development

✔ JWT Authentication & Authorization

✔ OTP Verification using Twilio

✔ REST API Integration

✔ PDF Ticket Generation

✔ Responsive UI Design

✔ Production Deployment using Vercel & Render

---

## 🔮 Future Enhancements

* Online Payment Gateway Integration
* QR Code Ticket Verification
* Movie Reviews & Ratings
* Admin Dashboard
* Email Notifications
* Cloud Database Integration
* AI-Based Movie Recommendations

---

## 📈 Learning Outcomes

Through this project, I gained hands-on experience in:

* Frontend Development with React.js
* State Management using Context API
* Backend Development using Django REST Framework
* Authentication & Authorization
* OTP Verification Workflow
* API Integration
* Database Management
* Deployment & Production Hosting

---

## 👨‍💻 Developer

### Narayana Yanamadala

Aspiring Full-Stack Developer passionate about building scalable web applications using modern web technologies.

📧 Email: [narayanayy448@gmail.com](mailto:narayanayy448@gmail.com)

💻 GitHub: https://github.com/narayana-yanamadala

🔗 LinkedIn: https://www.linkedin.com/in/narayanayanamadala/

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

Your support motivates further development and improvements.

---

<p align="center">
  <b>🎬 CineRush — Book Movies. Choose Seats. Enjoy the Show.</b>
</p>
