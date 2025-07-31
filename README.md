# 🎬 Online Cinema – Authentication & Profile API

This project is a part of an **Online Cinema Platform**, focusing on user registration, authentication, profile management, password reset, and email communication. Built with **FastAPI**, **SQLAlchemy**, **Alembic**, and **Celery**.

---

## ✅ Features Implemented

### 1. **User Authentication**
- Email-based registration with hashed password storage
- Account activation via token sent to email
- JWT access and refresh token issuance

### 2. **Profile Management**
- Get and update user profile via protected endpoints
- Profile data includes: full name, bio, birth date

### 3. **Password Reset**
- Request password reset via email
- Reset password using a secure token

### 4. **Token System**
- Issue and refresh JWT tokens
- Store and verify refresh tokens
- One-time password reset tokens

### 5. **Email Integration**
- Asynchronous email delivery using Celery & FastAPI-Mail
- Activation and password reset emails

### 6. **Database Migrations**
- Alembic used for schema versioning
- Initial schema includes: users, profiles, tokens, groups

### 7. **Middleware**
- Custom middleware for CORS and logging

---

## 🗂️ Project Structure

