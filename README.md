# 🛒 Django E-Commerce Platform

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

A **full-featured e-commerce web application** built with **Django** and **Django REST Framework**, featuring **OTP-based authentication**, **cart & order management**, **shipping system**, and **payment gateway integration** with **eSewa** and **PayPal**.  

This project demonstrates real-world web development workflows, including secure REST APIs, dynamic cart/order processing, and payment verification.

---

## 🚀 Features

### 🔐 Authentication
- User registration with **OTP email verification**
- Secure login & logout
- Profile management with contact info and bio

### 🛍 Product Management
- Product listing & detailed view
- Category filtering & search
- Featured & trending products
- Related product suggestions

### 🛒 Cart System
- Add / Remove products via REST API
- Update product quantity
- Real-time cart total calculation
- Authenticated user-specific carts

### 📦 Order & Checkout
- Create order from cart or **Buy Now**
- Select shipping options
- Assign delivery addresses
- Full **order lifecycle**:
  - `PENDING` → `PAID` → `SHIPPED` → `DELIVERED` → `CANCELLED` → `DELETED`

### 💳 Payment Integration
- **eSewa** payment gateway
- **PayPal** integration
- Payment success & failure handling
- Automatic order number & invoice generation
- Email confirmation after successful payment

### 👤 User Dashboard
- View **recent orders** and order details
- Update profile information
- Manage multiple addresses
- Set **default shipping preference**

### 🔌 REST API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products/` | GET | List all products |
| `/api/cart/add_remove/` | POST | Add or remove product in cart |
| `/api/cart/update_quantity/` | POST | Update quantity of cart item |
| `/api/order/update_shipping/` | POST | Update shipping option for order |
| `/api/order/update_address/` | POST | Update order delivery address |
| `/api/order/cancel/` | POST | Cancel an order |
| `/api/order/delete/` | POST | Delete an order |
| `/api/profile/update_shipping/` | POST | Update user shipping preference |
| `/api/profile/update_address/` | POST | Set default address |

---

## 🛠 Tech Stack

- **Backend:** Python, Django, Django REST Framework  
- **Database:** SQLite / PostgreSQL  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **Payment Gateways:** eSewa, PayPal  
- **Others:** Email notifications, OTP verification, shortuuid for order IDs

---

## 💡 Project Highlights

- Clean and modular **Django project structure**
- **Secure APIs** with authentication
- Complete **order lifecycle handling**
- **Payment verification** with signature validation
- **Email notifications** for order confirmation
- Production-ready and **scalable architecture**

---

## 📂 Project Structure (Simplified)

