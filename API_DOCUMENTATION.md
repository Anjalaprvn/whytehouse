# WhyteHouse API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication

All API endpoints (except authentication endpoints) require JWT authentication with OTP verification.

### Authentication Flow

#### Step 1: Request OTP

**Endpoint:** `POST /api/auth/request-otp/`

**Request Body:**
```json
{
  "email": "admin@example.com",
  "password": "your_password"
}
```

**Success Response (200):**
```json
{
  "message": "OTP sent to your registered email",
  "email": "admin@example.com",
  "user_id": 1
}
```

**Error Responses:**
- `400`: Email and password are required
- `401`: Invalid email or password
- `500`: Failed to send OTP

**Note:** OTP is valid for 5 minutes. Save the `user_id` for the next step.

---

#### Step 2: Verify OTP and Get Tokens

**Endpoint:** `POST /api/auth/verify-otp/`

**Request Body:**
```json
{
  "user_id": 1,
  "otp": "123456"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User"
  }
}
```

**Error Responses:**
- `400`: user_id and otp are required / OTP expired or not found
- `401`: Invalid OTP
- `404`: User not found

**Tokens:**
- `access`: Use this token for API requests (valid for 1 hour)
- `refresh`: Use this to get a new access token (valid for 7 days)

---

#### Step 3: Resend OTP (Optional)

**Endpoint:** `POST /api/auth/resend-otp/`

**Request Body:**
```json
{
  "user_id": 1
}
```

**Success Response (200):**
```json
{
  "message": "OTP resent to your registered email",
  "email": "admin@example.com"
}
```

---

#### Step 4: Refresh Access Token

**Endpoint:** `POST /api/auth/refresh/`

**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Success Response (200):**
```json
{
  "access": "new_access_token",
  "refresh": "new_refresh_token"
}
```

---

### Using the Access Token

Include the access token in the Authorization header for all API requests:

```
Authorization: Bearer your_access_token
```

**Example:**
```bash
curl -X GET http://localhost:8000/api/customers/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## API Endpoints

### 1. Customers API
**Base:** `/api/customers/`

**Operations:**
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer (full)
- `PATCH /api/customers/{id}/` - Update customer (partial)
- `DELETE /api/customers/{id}/` - Delete customer

**Search:** `?search=john` (searches: first_name, last_name, display_name, contact_number, email)

**Ordering:** `?ordering=-created_at` (fields: id, created_at, updated_at)

**Example Request:**
```json
{
  "customer_type": "individual",
  "salutation": "Mr",
  "first_name": "John",
  "last_name": "Doe",
  "display_name": "John Doe",
  "place": "Mumbai",
  "contact_number": "9876543210",
  "email": "john@example.com",
  "same_as_whatsapp": true,
  "whatsapp_number": "9876543210",
  "work_number": "",
  "gst_number": ""
}
```

---

### 2. Resorts API
**Base:** `/api/resorts/`

**Operations:** Same as Customers (GET, POST, PUT, PATCH, DELETE)

**Search:** `?search=resort_name` (searches: resort_name, resort_place, city, state, mobile, email)

**Example Request:**
```json
{
  "resort_name": "Paradise Resort",
  "resort_place": "Goa",
  "mobile": "9876543210",
  "email": "info@paradiseresort.com",
  "cc_emails": "manager@paradiseresort.com",
  "location_map_link": "https://maps.google.com/..."
}
```

---

### 3. Meals API
**Base:** `/api/meals/`

**Operations:** Same as above

**Search:** `?search=breakfast` (searches: name, description)

**Example Request:**
```json
{
  "name": "Full Board",
  "description": "Breakfast, Lunch, and Dinner included",
  "included_meals": ["breakfast", "lunch", "dinner"]
}
```

---

### 4. Accounts API
**Base:** `/api/accounts/`

**Operations:** Same as above

**Search:** `?search=account_name` (searches: account_name, account_number, bank_name, branch_name, ifsc_code)

**Example Request:**
```json
{
  "account_name": "WhyteHouse Business Account",
  "account_number": "1234567890",
  "bank_name": "HDFC Bank",
  "branch_name": "Mumbai Main",
  "ifsc_code": "HDFC0001234",
  "account_type": "current"
}
```

---

### 5. Invoices API
**Base:** `/api/invoices/`

**Operations:** Same as above

**Search:** `?search=INV001` (searches: invoice_no, room_type, meals_plan, notes)

**Ordering:** `?ordering=-invoice_date` (fields: id, invoice_date, checkin_date, checkout_date, created_at, updated_at, total)

**Auto-calculated fields:** `pax_total`, `total`, `pending`, `profit`

**Example Request:**
```json
{
  "customer": 1,
  "sales_person": 1,
  "resort": 1,
  "invoice_date": "2026-04-16",
  "checkin_date": "2026-05-01",
  "checkout_date": "2026-05-05",
  "checkin_time": "14:00",
  "checkout_time": "11:00",
  "adults": 2,
  "children": 1,
  "pax_notes": "1 child is 5 years old",
  "nights": 4,
  "room_type": "Deluxe",
  "rooms": 1,
  "meals_plan": "Full Board",
  "bank_account": 1,
  "package_price": 25000,
  "tax": 2500,
  "resort_price": 20000,
  "received": 10000,
  "notes": "Early check-in requested"
}
```

---

### 6. Vouchers API
**Base:** `/api/vouchers/`

**Operations:** Same as above

**Search:** `?search=VCH001` (searches: voucher_no, room_type, meals_plan, notes)

**Ordering:** `?ordering=-voucher_date`

**Auto-calculated fields:** `pax_total`, `total_amount`, `pending`, `from_whytehouse`, `profit`

**Example Request:**
```json
{
  "customer": 1,
  "sales_person": 1,
  "resort": 1,
  "voucher_date": "2026-04-16",
  "checkin_date": "2026-05-01",
  "checkout_date": "2026-05-05",
  "checkin_time": "14:00",
  "checkout_time": "11:00",
  "adults": 2,
  "children": 1,
  "pax_notes": "1 child is 5 years old",
  "nights": 4,
  "room_type": "Deluxe",
  "no_of_rooms": 1,
  "meals_plan": 1,
  "bank_account": 1,
  "package_price": 25000,
  "resort_price": 20000,
  "received": 10000,
  "note_for_resort": "Please arrange early check-in",
  "note_for_guest": "Enjoy your stay!"
}
```

---

### 7. Leads/Enquiries API
**Base:** `/api/leads/`

**Operations:** Same as above

**Search:** `?search=john` (searches: full_name, mobile_number, alternate_number, place, email, package_name, property_name, source, enquiry_type, status, remarks)

**Ordering:** `?ordering=-created_at`

**Example Request:**
```json
{
  "full_name": "John Doe",
  "mobile_number": "9876543210",
  "alternate_number": "",
  "place": "Mumbai",
  "email": "john@example.com",
  "message": "Interested in Goa package for 4 nights",
  "package": 1,
  "package_name": "Goa Beach Paradise",
  "property_name": "",
  "source": "website",
  "enquiry_type": "package",
  "status": "new",
  "is_viewed": false,
  "remarks": "",
  "employee": null
}
```

---

### 8. Properties API
**Base:** `/api/properties/`

**Operations:** Same as above

**Search:** `?search=hotel` (searches: name, property_type, location, owner_name, owner_contact, summary)

**Example Request:**
```json
{
  "name": "Beach View Hotel",
  "property_type": "hotel",
  "location": "Goa",
  "website": "https://beachview.com",
  "address": "Calangute Beach, Goa",
  "summary": "Luxury beachfront hotel",
  "owner_name": "Mr. Smith",
  "owner_contact": "9876543210",
  "amenities": ["wifi", "pool", "spa"],
  "image": null,
  "is_active": true
}
```

---

### 9. Feedbacks API
**Base:** `/api/feedbacks/`

**Operations:** Same as above

**Search:** `?search=john` (searches: name, email, mobile_number, feedback_type, feedback)

**Ordering:** `?ordering=-rating`

**Example Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "mobile_number": "9876543210",
  "feedback_type": "review",
  "rating": 5,
  "feedback": "Excellent service and amazing experience!",
  "featured": false
}
```

---

### 10. Blogs API
**Base:** `/api/blogs/`

**Operations:** Same as above

**Search:** `?search=goa` (searches: title, slug, excerpt, content, author_name, hashtags, tags, status)

**Ordering:** `?ordering=-publish_date`

**Example Request:**
```json
{
  "title": "Top 10 Places to Visit in Goa",
  "slug": "top-10-places-goa",
  "excerpt": "Discover the best beaches and attractions in Goa",
  "content": "Full blog content here...",
  "status": "published",
  "category": "travel",
  "package_id": "GOA001",
  "author_name": "Travel Expert",
  "author_summary": "10 years of travel experience",
  "reading_time": 5,
  "publish_date": "2026-04-16",
  "featured_image": null,
  "hashtags": "#Goa #Travel #Beach",
  "tags": "goa, beach, travel"
}
```

---

### 11. Destinations API
**Base:** `/api/destinations/`

**Operations:** Same as above

**Search:** `?search=goa` (searches: name, country, category, description)

**Ordering:** `?ordering=packages_start_from`

**Example Request:**
```json
{
  "name": "Goa",
  "country": "India",
  "category": "beach",
  "description": "Beautiful beaches and vibrant nightlife",
  "packages_start_from": 15000,
  "image": null,
  "map_image": null,
  "is_popular": true,
  "is_active": true
}
```

---

### 12. Employees API
**Base:** `/api/employees/`

**Operations:** Same as above

**Search:** `?search=john` (searches: name, email, phone, role, department, status)

**Ordering:** `?ordering=-join_date`

**Example Request:**
```json
{
  "name": "John Doe",
  "email": "john@whytehouse.com",
  "phone": "9876543210",
  "role": "Sales Manager",
  "department": "Sales",
  "join_date": "2026-01-01",
  "salary": 50000,
  "status": "active",
  "profile_picture": null
}
```

---

### 13. Travel Packages API
**Base:** `/api/packages/`

**Operations:** Same as above

**Search:** `?search=goa` (searches: package_id, name, category, destination, location, country, description, price_type, meta_title, meta_description)

**Ordering:** `?ordering=price`

**Example Request:**
```json
{
  "package_id": "GOA001",
  "name": "Goa Beach Paradise",
  "category": "domestic",
  "destination": "Goa",
  "location": "North Goa",
  "country": "India",
  "price": 25000,
  "adult_price": 25000,
  "price_type": "per_person",
  "duration": "4 Nights / 5 Days",
  "description": "Experience the best of Goa beaches",
  "image": null,
  "active": true,
  "itinerary": "Day 1: Arrival...",
  "inclusions": "Hotel, Meals, Transport",
  "exclusions": "Airfare, Personal expenses",
  "meta_title": "Goa Beach Package",
  "meta_description": "Best Goa beach package deals",
  "story_main_image": null,
  "story_side_image1": null,
  "story_side_image2": null
}
```

---

## Common Query Parameters

### Pagination
```
?page=1&page_size=10
```

### Search
```
?search=keyword
```

### Ordering
```
?ordering=-created_at  (descending)
?ordering=created_at   (ascending)
```

### Filtering (if implemented)
```
?status=active
?category=domestic
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 400 Bad Request
```json
{
  "field_name": ["This field is required."]
}
```

---

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Start the server:
```bash
python manage.py runserver
```

---

## Testing with cURL

### Step 1: Request OTP
```bash
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "your_password"}'
```

### Step 2: Verify OTP and Get Tokens
```bash
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "otp": "123456"}'
```

### Step 3: Use Access Token
```bash
curl -X GET http://localhost:8000/api/customers/ \
  -H "Authorization: Bearer your_access_token"
```

### Create Lead with Token
```bash
curl -X POST http://localhost:8000/api/leads/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "mobile_number": "9876543210",
    "email": "john@example.com",
    "message": "Interested in Goa package",
    "source": "website",
    "enquiry_type": "package"
  }'
```

---

## Postman Testing Guide

### 1. Request OTP
- Method: `POST`
- URL: `http://localhost:8000/api/auth/request-otp/`
- Body (JSON):
```json
{
  "email": "your_admin_email@example.com",
  "password": "your_password"
}
```
- Save the `user_id` from response

### 2. Check Email for OTP
- Check your email inbox for the 6-digit OTP
- OTP is valid for 5 minutes

### 3. Verify OTP
- Method: `POST`
- URL: `http://localhost:8000/api/auth/verify-otp/`
- Body (JSON):
```json
{
  "user_id": 1,
  "otp": "123456"
}
```
- Save the `access` token from response

### 4. Test Protected Endpoint
- Method: `GET`
- URL: `http://localhost:8000/api/leads/`
- Headers:
  - Key: `Authorization`
  - Value: `Bearer your_access_token_here`

### 5. Create/Update Data
- Method: `POST`
- URL: `http://localhost:8000/api/leads/`
- Headers:
  - Key: `Authorization`
  - Value: `Bearer your_access_token_here`
  - Key: `Content-Type`
  - Value: `application/json`
- Body (JSON):
```json
{
  "full_name": "Test User",
  "mobile_number": "9876543210",
  "email": "test@example.com",
  "message": "Test enquiry",
  "source": "api",
  "enquiry_type": "package"
}
```
