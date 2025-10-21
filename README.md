
# GreatKart - Django E-Commerce Platform

## Project Description
**GreatKart** is a full-featured, scalable e-commerce platform built with Django. This full-stack web application provides a complete online shopping experience with modern web technologies. The platform supports user accounts, shopping carts, product categories, promotional coupons, wishlists, blog functionality, and real-time notifications.

---

## Features

### User Management
- User registration and authentication  
- Profile management and order history  
- Password reset functionality  
- Secure login/logout system  

### Product Management
- Product browsing by categories and subcategories  
- Product details with images and descriptions  
- Inventory management  
- Product ratings and reviews  

### Shopping Experience
- Shopping cart with add/remove/update functionality  
- Secure checkout process  
- Order tracking and history  
- Wishlist management  

### Marketing & Engagement
- Coupon codes and discount system  
- Blog with categories and posts  
- Advertisement management  
- Email notifications for orders and promotions  
- Search functionality across products  

### Administrative Features
- Admin dashboard for store management  
- Order management system  
- User management  
- Content management for blogs and ads  

---

## Folder Structure

```
GreatKart/
├── accounts/              # User authentication, profiles, and registration
├── advertisement/         # Advertisement management system
├── blogs/                 # Blog posts and categories
├── carts/                 # Shopping cart logic and session management
├── category/              # Product category management
├── coupons/               # Coupon codes and discount logic
├── greatkart/             # Main Django project settings and configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── home/                  # Home page views and templates
├── media/                 # Uploaded media files (product images, user avatars)
├── notifications/         # Email and site notification system
├── orders/                # Order placement, tracking, and management
├── search/                # Search functionality implementation
├── static/                # Static files (CSS, JavaScript, images)
├── store/                 # Products and store management
├── templates/             # Django HTML templates
├── wishlist/              # Wishlist feature implementation
├── .gitignore             # Git ignore rules
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

---

## Installation Instructions

### Prerequisites
- Python 3.8 or higher  
- pip (Python package manager)  
- Git  

### Basic Workflow

**User Registration & Login**
1. Create a new user account via the registration page  
2. Verify email (if configured)  
3. Login to access personalized features  

**Product Management**
1. Browse products by categories  
2. Use search functionality to find specific items  
3. View product details and customer reviews  

**Shopping Cart & Checkout**
1. Add products to cart  
2. Apply coupon codes during checkout  
3. Complete order with secure payment process  

**Administrative Tasks**
1. Add new products and categories via admin panel  
2. Manage user accounts and orders  
3. Create blog posts and advertisements  
4. Configure coupon codes and discounts  

**Testing Email Notifications**
- Configure your email settings in `settings.py` to test:  
  - Order confirmation emails  
  - Password reset functionality  
  - Promotional notifications  

---

