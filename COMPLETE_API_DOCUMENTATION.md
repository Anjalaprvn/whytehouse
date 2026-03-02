# Complete API Documentation - Whyte House

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
Currently, all endpoints are open. Add authentication as needed.

---

## 📚 Table of Contents
1. [Travel Packages API](#travel-packages-api)
2. [Destinations API](#destinations-api)
3. [Customers API](#customers-api)
4. [Invoices API](#invoices-api)
5. [Vouchers API](#vouchers-api)
6. [Resorts API](#resorts-api)
7. [Meals API](#meals-api)
8. [Accounts API](#accounts-api)
9. [Employees API](#employees-api)
10. [Inquiries API](#inquiries-api)
11. [Leads API](#leads-api)
12. [Blogs API](#blogs-api)
13. [Properties API](#properties-api)

---

## 🎯 Travel Packages API

**Base Endpoint:** `/api/packages/`

### List Packages
```
GET /api/packages/
```

**Filters:**
- `category` - Domestic/International
- `active` - true/false
- `destination` - Destination ID
- `country` - Country name
- `min_price` - Minimum price
- `max_price` - Maximum price
- `search` - Search query

**Example:**
```bash
GET /api/packages/?category=International&active=true&max_price=50000
```

### Get Package Details
```
GET /api/packages/{id}/
```

### Create Package
```
POST /api/packages/
Content-Type: application/json

{
  "name": "Goa Beach Paradise",
  "category": "Domestic",
  "destination": 1,
  "location": "Goa",
  "country": "India",
  "price": "15000.00",
  "duration": "3 Days 2 Nights",
  "description": "Beautiful beach package",
  "active": true
}
```

### Update Package
```
PUT /api/packages/{id}/
PATCH /api/packages/{id}/
```

### Delete Package
```
DELETE /api/packages/{id}/
```

### Custom Actions
```
GET /api/packages/summary/          # Get statistics
GET /api/packages/featured/         # Get featured packages
GET /api/packages/by_category/      # Get packages by category
```

---

## 🌍 Destinations API

**Base Endpoint:** `/api/destinations/`

### List Destinations
```
GET /api/destinations/
```

**Filters:**
- `category` - Domestic/International
- `is_popular` - true/false
- `search` - Search query

### Get Destination Details
```
GET /api/destinations/{id}/
```

### Create Destination
```
POST /api/destinations/
Content-Type: application/json

{
  "name": "Bali",
  "country": "Indonesia",
  "category": "International",
  "description": "Island paradise",
  "is_popular": true
}
```

### Custom Actions
```
GET /api/destinations/summary/              # Get statistics
GET /api/destinations/{id}/packages/        # Get packages for destination
```

---

## 👥 Customers API

**Base Endpoint:** `/api/customers/`

### List Customers
```
GET /api/customers/
```

**Filters:**
- `customer_type` - Individual/Corporate/Government
- `search` - Search query

### Get Customer Details
```
GET /api/customers/{id}/
```

### Create Customer
```
POST /api/customers/
Content-Type: application/json

{
  "customer_type": "Individual",
  "salutation": "Mr",
  "first_name": "John",
  "last_name": "Doe",
  "display_name": "John Doe",
  "place": "Mumbai",
  "contact_number": "9876543210",
  "same_as_whatsapp": true,
  "whatsapp_number": "9876543210"
}
```

### Custom Actions
```
GET /api/customers/summary/     # Get statistics
```

---

## 🧾 Invoices API

**Base Endpoint:** `/api/invoices/`

### List Invoices
```
GET /api/invoices/
```

**Filters:**
- `customer` - Customer ID
- `resort` - Resort ID
- `sales_person` - Employee ID
- `payment_mode` - Payment mode
- `date_from` - Start date (YYYY-MM-DD)
- `date_to` - End date (YYYY-MM-DD)
- `search` - Search query

**Example:**
```bash
GET /api/invoices/?date_from=2026-01-01&date_to=2026-12-31&resort=5
```

### Get Invoice Details
```
GET /api/invoices/{id}/
```

### Create Invoice
```
POST /api/invoices/
Content-Type: application/json

{
  "customer": 1,
  "invoice_no": "INV-2026-001",
  "resort": 2,
  "check_in_date": "2026-03-15",
  "check_out_date": "2026-03-18",
  "number_of_nights": 3,
  "number_of_adults": 2,
  "number_of_children": 1,
  "meal": 1,
  "room_type": "Deluxe",
  "room_rate": "5000.00",
  "meal_cost": "1500.00",
  "other_charges": "500.00",
  "discount": "200.00",
  "total_amount": "20800.00",
  "paid_amount": "10000.00",
  "pending_amount": "10800.00",
  "payment_mode": "Cash",
  "account": 1,
  "sales_person": 3
}
```

### Custom Actions
```
GET /api/invoices/summary/      # Get financial statistics
GET /api/invoices/pending/      # Get invoices with pending amount
```

---

## 🎫 Vouchers API

**Base Endpoint:** `/api/vouchers/`

### List Vouchers
```
GET /api/vouchers/
```

**Filters:**
- `customer` - Customer ID
- `resort` - Resort ID
- `check_in_date` - Check-in date (YYYY-MM-DD)
- `check_out_date` - Check-out date (YYYY-MM-DD)
- `search` - Search query

### Get Voucher Details
```
GET /api/vouchers/{id}/
```

### Create Voucher
```
POST /api/vouchers/
Content-Type: application/json

{
  "customer": 1,
  "voucher_no": "VCH-2026-001",
  "resort": 2,
  "check_in_date": "2026-03-15",
  "check_out_date": "2026-03-18",
  "number_of_nights": 3,
  "number_of_adults": 2,
  "number_of_children": 1,
  "meal": 1,
  "room_type": "Deluxe",
  "special_requests": "Sea view room",
  "total_amount": "18000.00"
}
```

### Custom Actions
```
GET /api/vouchers/summary/      # Get statistics
```

---

## 🏨 Resorts API

**Base Endpoint:** `/api/resorts/`

### List Resorts
```
GET /api/resorts/
```

**Filters:**
- `status` - Active/Inactive
- `location` - Location name
- `search` - Search query

### Get Resort Details
```
GET /api/resorts/{id}/
```

### Create Resort
```
POST /api/resorts/
Content-Type: application/json

{
  "resort_name": "Paradise Beach Resort",
  "location": "Goa",
  "contact_person": "Manager Name",
  "contact_number": "9876543210",
  "email": "resort@example.com",
  "price_per_night": "5000.00",
  "amenities": "Pool, Spa, Restaurant, WiFi",
  "status": "Active"
}
```

### Custom Actions
```
GET /api/resorts/summary/       # Get statistics
```

---

## 🍽️ Meals API

**Base Endpoint:** `/api/meals/`

### List Meals
```
GET /api/meals/
```

**Filters:**
- `status` - Available/Unavailable
- `search` - Search query

### Get Meal Details
```
GET /api/meals/{id}/
```

### Create Meal
```
POST /api/meals/
Content-Type: application/json

{
  "meal_plan": "Full Board (FB)",
  "description": "Breakfast, Lunch, and Dinner included",
  "price_per_person": "1500.00",
  "status": "Available"
}
```

### Custom Actions
```
GET /api/meals/summary/         # Get statistics
```

---

## 💰 Accounts API

**Base Endpoint:** `/api/accounts/`

### List Accounts
```
GET /api/accounts/
```

**Filters:**
- `account_type` - savings/current/business
- `status` - Active/Inactive
- `search` - Search query

### Get Account Details
```
GET /api/accounts/{id}/
```

### Create Account
```
POST /api/accounts/
Content-Type: application/json

{
  "account_name": "Business Account",
  "account_type": "business",
  "bank_name": "HDFC Bank",
  "branch": "Mumbai Main",
  "account_number": "1234567890",
  "ifsc_code": "HDFC0001234",
  "balance": "100000.00",
  "status": "Active"
}
```

### Custom Actions
```
GET /api/accounts/summary/      # Get statistics with total balance
```

---

## 👨‍💼 Employees API

**Base Endpoint:** `/api/employees/`

### List Employees
```
GET /api/employees/
```

**Filters:**
- `status` - Active/Inactive
- `role` - Role name
- `search` - Search query

### Get Employee Details
```
GET /api/employees/{id}/
```

### Create Employee
```
POST /api/employees/
Content-Type: application/json

{
  "name": "John Smith",
  "role": "Sales Manager",
  "email": "john@example.com",
  "phone": "9876543210",
  "address": "Mumbai, India",
  "date_of_joining": "2026-01-15",
  "salary": "50000.00",
  "status": "Active"
}
```

### Custom Actions
```
GET /api/employees/summary/     # Get statistics
```

---

## 📧 Inquiries API

**Base Endpoint:** `/api/inquiries/`

### List Inquiries
```
GET /api/inquiries/
```

**Filters:**
- `status` - New/Contacted/Converted/Closed
- `search` - Search query

### Get Inquiry Details
```
GET /api/inquiries/{id}/
```

### Create Inquiry
```
POST /api/inquiries/
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "9876543210",
  "package": "Goa Beach Package",
  "message": "Interested in booking for March",
  "status": "New"
}
```

### Custom Actions
```
GET /api/inquiries/summary/     # Get statistics by status
```

---

## 📞 Leads API

**Base Endpoint:** `/api/leads/`

### List Leads
```
GET /api/leads/
```

**Filters:**
- `type` - General/International/Domestic
- `source` - Source name
- `new` - true (for "Enquire Now" leads)
- `search` - Search query

### Get Lead Details
```
GET /api/leads/{id}/
```

### Create Lead
```
POST /api/leads/
Content-Type: application/json

{
  "full_name": "John Doe",
  "mobile_number": "9876543210",
  "place": "Mumbai",
  "source": "Website",
  "enquiry_type": "International",
  "remarks": "Interested in Bali package"
}
```

### Custom Actions
```
GET /api/leads/summary/         # Get statistics by type
```

---

## 📝 Blogs API

**Base Endpoint:** `/api/blogs/`

### List Blogs
```
GET /api/blogs/
```

**Filters:**
- `status` - draft/published/scheduled
- `search` - Search query

### Get Blog Details
```
GET /api/blogs/{id}/
```

### Create Blog
```
POST /api/blogs/
Content-Type: application/json

{
  "title": "Top 10 Beaches in Goa",
  "slug": "top-10-beaches-goa",
  "excerpt": "Discover the best beaches...",
  "content": "Full blog content here...",
  "status": "published",
  "author_name": "Travel Writer",
  "author_summary": "Expert travel blogger",
  "reading_time": 5,
  "publish_date": "2026-03-01",
  "hashtags": "goa, beaches, travel",
  "tags": "goa, beaches, travel"
}
```

### Custom Actions
```
GET /api/blogs/summary/         # Get statistics by status
```

---

## 🏠 Properties API

**Base Endpoint:** `/api/properties/`

### List Properties
```
GET /api/properties/
```

**Filters:**
- `property_type` - hotel/resort/villa/apartment
- `location` - Location name
- `search` - Search query

### Get Property Details
```
GET /api/properties/{id}/
```

### Create Property
```
POST /api/properties/
Content-Type: application/json

{
  "name": "Luxury Beach Villa",
  "property_type": "villa",
  "location": "Goa",
  "website": "https://example.com",
  "address": "Calangute Beach, Goa",
  "summary": "Luxury beachfront villa",
  "owner_name": "Owner Name",
  "owner_contact": "9876543210",
  "amenities": "Pool, WiFi, Kitchen, AC"
}
```

---

## 🔍 Common Response Format

### Success Response
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2",
  ...
}
```

### List Response
```json
[
  {
    "id": 1,
    "field1": "value1"
  },
  {
    "id": 2,
    "field1": "value2"
  }
]
```

### Error Response
```json
{
  "detail": "Error message"
}
```

---

## 📊 Summary Endpoints

All major resources have a `/summary/` endpoint:

```bash
GET /api/packages/summary/
GET /api/destinations/summary/
GET /api/customers/summary/
GET /api/invoices/summary/
GET /api/vouchers/summary/
GET /api/resorts/summary/
GET /api/meals/summary/
GET /api/accounts/summary/
GET /api/employees/summary/
GET /api/inquiries/summary/
GET /api/leads/summary/
GET /api/blogs/summary/
```

---

## 🚀 Quick Start Examples

### JavaScript/Fetch
```javascript
// Get all packages
fetch('http://127.0.0.1:8000/api/packages/')
  .then(res => res.json())
  .then(data => console.log(data));

// Create customer
fetch('http://127.0.0.1:8000/api/customers/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    first_name: 'John',
    last_name: 'Doe',
    display_name: 'John Doe',
    contact_number: '9876543210',
    customer_type: 'Individual'
  })
}).then(res => res.json());
```

### Python/Requests
```python
import requests

# Get invoices
response = requests.get('http://127.0.0.1:8000/api/invoices/')
invoices = response.json()

# Create resort
data = {
    'resort_name': 'Beach Resort',
    'location': 'Goa',
    'price_per_night': '5000.00',
    'status': 'Active'
}
response = requests.post('http://127.0.0.1:8000/api/resorts/', json=data)
```

### cURL
```bash
# Get all customers
curl http://127.0.0.1:8000/api/customers/

# Create employee
curl -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "role": "Manager",
    "email": "john@example.com",
    "phone": "9876543210",
    "status": "Active"
  }'
```

---

## ✅ All APIs are Live!

Browse the interactive API documentation at:
```
http://127.0.0.1:8000/api/
```

All endpoints support:
- ✅ GET (List & Detail)
- ✅ POST (Create)
- ✅ PUT/PATCH (Update)
- ✅ DELETE (Remove)
- ✅ Custom Actions (summary, etc.)
- ✅ Filtering & Search
- ✅ Django REST Framework Browsable API
