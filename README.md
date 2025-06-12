# 🎓 Django Frontend Project with Tailwind & External API Integration
This is a Django frontend project that connects to an external backend API for data handling. The frontend is styled using Tailwind CSS and supports JWT token-based authentication with automatic token refreshing. It is modularized into four main Django apps: course, user, admin_panel, and theme

## 🚀 Features
### 🧠 Course App
- Display a list of available courses.
- View individual course details.
- Add a new course (via API integration).

### 👤 User App
- Register new users.
- Login using credentials to obtain JWT token.
- View and edit user profile.
- Logout functionality.
- Automatic token refresh using refresh token endpoint to keep sessions active without requiring re-login.

## 🛠️ Admin Panel App
- Configure base URLs for:
Course API
User API
- Dynamic integration with external backend services.

##🎨 Theme App
- Tailwind CSS integration.
- Shared components and templates to maintain a consistent look and feel.

