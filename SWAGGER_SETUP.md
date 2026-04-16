# Swagger/OpenAPI Documentation Setup

## Installation

1. Install the required package:
```bash
pip install drf-spectacular
```

2. Run migrations (if any):
```bash
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

---

## Access Swagger Documentation

### 🎯 Swagger UI (Interactive API Documentation)
```
http://127.0.0.1:8000/api/docs/
```
- Interactive UI to test all API endpoints
- Try out requests directly from the browser
- See request/response examples
- Authorize with JWT tokens

### 📚 ReDoc (Alternative Documentation View)
```
http://127.0.0.1:8000/api/redoc/
```
- Clean, readable documentation
- Better for reading and understanding APIs
- No interactive testing

### 📄 OpenAPI Schema (JSON/YAML)
```
http://127.0.0.1:8000/api/schema/
```
- Raw OpenAPI 3.0 schema
- Can be imported into Postman, Insomnia, etc.

---

## How to Use Swagger UI

### Step 1: Open Swagger UI
Navigate to: `http://127.0.0.1:8000/api/docs/`

### Step 2: Test Authentication (No Token Required)

1. **Expand "Authentication" section**
2. **Click on "POST /api/auth/request-otp/"**
3. **Click "Try it out"**
4. **Enter your credentials:**
```json
{
  "email": "admin@example.com",
  "password": "your_password"
}
```
5. **Click "Execute"**
6. **Copy the `user_id` from response**
7. **Check your email for OTP**

### Step 3: Verify OTP

1. **Click on "POST /api/auth/verify-otp/"**
2. **Click "Try it out"**
3. **Enter:**
```json
{
  "user_id": 1,
  "otp": "123456"
}
```
4. **Click "Execute"**
5. **Copy the `access` token from response**

### Step 4: Authorize Swagger

1. **Click the "Authorize" button** (🔒 icon at top right)
2. **In the "Bearer" field, enter:**
```
Bearer YOUR_ACCESS_TOKEN_HERE
```
Example:
```
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
3. **Click "Authorize"**
4. **Click "Close"**

### Step 5: Test Protected Endpoints

Now you can test any endpoint:

1. **Expand any section** (Customers, Leads, etc.)
2. **Click on any endpoint** (GET, POST, etc.)
3. **Click "Try it out"**
4. **Fill in the request body (if needed)**
5. **Click "Execute"**
6. **See the response below**

---

## Available API Sections in Swagger

### 🔐 Authentication
- Request OTP
- Verify OTP
- Resend OTP
- Refresh Token

### 👥 Customers
- List, Create, Read, Update, Delete customers

### 🏨 Resorts
- Manage resort properties

### 🍽️ Meals
- Manage meal plans

### 💳 Accounts
- Manage bank accounts

### 📄 Invoices
- Create and manage invoices

### 🎟️ Vouchers
- Create and manage vouchers

### 📞 Leads
- Manage customer enquiries and leads

### 🏢 Properties
- Manage hospitality properties

### ⭐ Feedbacks
- Customer feedback and reviews

### 📝 Blogs
- Blog post management

### 🌍 Destinations
- Travel destination information

### 👔 Employees
- Employee management

### ✈️ Packages
- Travel package management

---

## Features

✅ **Interactive Testing** - Test all endpoints directly from browser  
✅ **Authentication Support** - Built-in JWT token authorization  
✅ **Request Examples** - See example requests for each endpoint  
✅ **Response Examples** - See example responses with status codes  
✅ **Schema Validation** - Automatic request/response validation  
✅ **Search & Filter** - Search through all endpoints  
✅ **Try It Out** - Execute real API calls  
✅ **Download Schema** - Export OpenAPI schema for other tools  

---

## Import to Postman

1. Go to: `http://127.0.0.1:8000/api/schema/`
2. Copy the entire JSON response
3. Open Postman
4. Click "Import" → "Raw text"
5. Paste the JSON
6. Click "Import"
7. All endpoints will be imported as a collection!

---

## Troubleshooting

### Swagger UI not loading?
- Make sure server is running: `python manage.py runserver`
- Check if `drf-spectacular` is installed: `pip list | grep drf-spectacular`
- Clear browser cache and reload

### Authorization not working?
- Make sure you clicked "Authorize" button
- Token format must be: `Bearer YOUR_TOKEN` (with space)
- Token must be the `access` token, not `refresh` token
- Check if token is expired (valid for 1 hour)

### Endpoints not showing?
- Make sure all apps are in `INSTALLED_APPS`
- Restart the server after configuration changes
- Check for any errors in console

---

## Quick Links

- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **ReDoc:** http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema:** http://127.0.0.1:8000/api/schema/
- **API Base:** http://127.0.0.1:8000/api/

---

## Next Steps

1. Install package: `pip install drf-spectacular`
2. Start server: `python manage.py runserver`
3. Open Swagger: http://127.0.0.1:8000/api/docs/
4. Test authentication endpoints
5. Authorize with JWT token
6. Test all other endpoints

Enjoy your fully documented API! 🎉
