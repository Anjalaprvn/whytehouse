# Dashboard API Guide

## Endpoint

```
GET /api/dashboard/
```

**Authentication Required:** Yes (Bearer Token)

---

## Description

Returns comprehensive dashboard statistics including:
- Total counts (invoices, vouchers, customers, leads, etc.)
- Profit statistics
- Average feedback rating
- Package and property counts
- Upcoming bookings (next 3)
- Recent invoices (last 5)
- Recent leads (last 5)

---

## Request

### Postman Setup:

```
Method: GET
URL: http://127.0.0.1:8000/api/dashboard/
```

### Headers:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

### Body:
```
(No body required for GET request)
```

---

## Response

### Success Response (200 OK):

```json
{
  "statistics": {
    "total_bookings": 0,
    "total_vouchers": 5,
    "total_invoices": 15,
    "total_profit": 50000.00,
    "new_leads": 6,
    "total_customers": 6,
    "avg_feedback_rating": 3.9,
    "total_blogs": 3,
    "international_packages": 10,
    "domestic_packages": 8,
    "hospitality_properties": 8
  },
  "upcoming_bookings": [
    {
      "id": 1,
      "invoice_no": "INV001",
      "customer_name": "John Doe",
      "resort_name": "Paradise Resort",
      "checkin_date": "2026-05-01",
      "checkout_date": "2026-05-05",
      "total": 47500.0,
      "nights": 4,
      "rooms": 1
    },
    {
      "id": 2,
      "invoice_no": "INV002",
      "customer_name": "Jane Smith",
      "resort_name": "Beach View Resort",
      "checkin_date": "2026-05-10",
      "checkout_date": "2026-05-15",
      "total": 65000.0,
      "nights": 5,
      "rooms": 2
    }
  ],
  "recent_invoices": [
    {
      "id": 15,
      "invoice_no": "INV015",
      "customer_name": "Test Customer",
      "invoice_date": "2026-04-16",
      "created_at": "2026-04-16T11:30:00Z",
      "total": 35000.0,
      "received": 10000.0,
      "pending": 25000.0
    },
    {
      "id": 14,
      "invoice_no": "INV014",
      "customer_name": "Another Customer",
      "invoice_date": "2026-04-15",
      "created_at": "2026-04-15T10:00:00Z",
      "total": 42000.0,
      "received": 42000.0,
      "pending": 0.0
    }
  ],
  "recent_leads": [
    {
      "id": 5,
      "full_name": "Anjala",
      "mobile_number": "5445555555",
      "place": "Mumbai",
      "enquiry_type": "package",
      "status": "new",
      "is_viewed": false,
      "created_at": "2026-04-16T09:00:00Z"
    },
    {
      "id": 4,
      "full_name": "nandini",
      "mobile_number": "1234565654",
      "place": "Delhi",
      "enquiry_type": "package",
      "status": "new",
      "is_viewed": false,
      "created_at": "2026-04-15T14:30:00Z"
    },
    {
      "id": 3,
      "full_name": "lohugvf",
      "mobile_number": "1234565654",
      "place": "Bangalore",
      "enquiry_type": "package",
      "status": "contacted",
      "is_viewed": true,
      "created_at": "2026-04-14T11:00:00Z"
    }
  ]
}
```

---

## Response Fields

### Statistics Object:

| Field | Type | Description |
|-------|------|-------------|
| `total_bookings` | integer | Total number of bookings (currently 0, add if you have booking model) |
| `total_vouchers` | integer | Total number of vouchers created |
| `total_invoices` | integer | Total number of invoices |
| `total_profit` | float | Sum of all profits from invoices |
| `new_leads` | integer | Number of leads created in last 30 days |
| `total_customers` | integer | Total number of customers |
| `avg_feedback_rating` | float | Average rating from all feedbacks (0-5) |
| `total_blogs` | integer | Total number of blog posts |
| `international_packages` | integer | Number of international travel packages |
| `domestic_packages` | integer | Number of domestic travel packages |
| `hospitality_properties` | integer | Total number of properties |

### Upcoming Bookings Array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Invoice ID |
| `invoice_no` | string | Invoice number |
| `customer_name` | string | Customer display name |
| `resort_name` | string | Resort name |
| `checkin_date` | date | Check-in date (YYYY-MM-DD) |
| `checkout_date` | date | Check-out date (YYYY-MM-DD) |
| `total` | float | Total invoice amount |
| `nights` | integer | Number of nights |
| `rooms` | integer | Number of rooms |

### Recent Invoices Array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Invoice ID |
| `invoice_no` | string | Invoice number |
| `customer_name` | string | Customer display name |
| `invoice_date` | date | Invoice date |
| `created_at` | datetime | Creation timestamp |
| `total` | float | Total amount |
| `received` | float | Amount received |
| `pending` | float | Pending amount |

### Recent Leads Array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Lead ID |
| `full_name` | string | Lead's full name |
| `mobile_number` | string | Contact number |
| `place` | string | Location |
| `enquiry_type` | string | Type of enquiry |
| `status` | string | Lead status (new, contacted, etc.) |
| `is_viewed` | boolean | Whether admin has viewed |
| `created_at` | datetime | Creation timestamp |

---

## Error Responses

### 401 Unauthorized (No Token):
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 401 Unauthorized (Invalid Token):
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

---

## Testing in Postman

### Step 1: Get Access Token
1. Request OTP: `POST /api/auth/request-otp/`
2. Verify OTP: `POST /api/auth/verify-otp/`
3. Copy the `access` token

### Step 2: Test Dashboard API
1. Method: `GET`
2. URL: `http://127.0.0.1:8000/api/dashboard/`
3. Headers:
   - `Authorization: Bearer YOUR_ACCESS_TOKEN`
4. Click "Send"

---

## Testing in Swagger UI

1. Go to: `http://127.0.0.1:8000/api/docs/`
2. Authenticate with JWT token (click "Authorize" button)
3. Find "Dashboard" section
4. Click on `GET /api/dashboard/`
5. Click "Try it out"
6. Click "Execute"
7. See the response below

---

## Use Cases

### Frontend Dashboard Display:
```javascript
// Fetch dashboard data
fetch('http://127.0.0.1:8000/api/dashboard/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  // Display statistics
  document.getElementById('total-invoices').textContent = data.statistics.total_invoices;
  document.getElementById('total-profit').textContent = `₹${data.statistics.total_profit}`;
  document.getElementById('new-leads').textContent = data.statistics.new_leads;
  document.getElementById('avg-rating').textContent = data.statistics.avg_feedback_rating;
  
  // Display upcoming bookings
  data.upcoming_bookings.forEach(booking => {
    // Render booking card
  });
  
  // Display recent invoices
  data.recent_invoices.forEach(invoice => {
    // Render invoice row
  });
  
  // Display recent leads
  data.recent_leads.forEach(lead => {
    // Render lead item
  });
});
```

### Mobile App:
```dart
// Flutter example
Future<DashboardData> fetchDashboard() async {
  final response = await http.get(
    Uri.parse('http://127.0.0.1:8000/api/dashboard/'),
    headers: {
      'Authorization': 'Bearer $accessToken',
      'Content-Type': 'application/json',
    },
  );
  
  if (response.statusCode == 200) {
    return DashboardData.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load dashboard');
  }
}
```

---

## Notes

- This endpoint requires authentication (JWT token)
- Data is calculated in real-time from the database
- New leads count includes leads from last 30 days
- Upcoming bookings shows next 3 bookings with future check-in dates
- Recent invoices and leads show last 5 items
- All monetary values are in float format
- Dates are in ISO 8601 format

---

## Quick Test Command (cURL)

```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

---

## Related Endpoints

- `GET /api/invoices/` - Get all invoices
- `GET /api/leads/` - Get all leads
- `GET /api/customers/` - Get all customers
- `GET /api/feedbacks/` - Get all feedbacks
- `GET /api/packages/` - Get all packages
- `GET /api/properties/` - Get all properties

---

Perfect for building:
- Admin dashboard web apps
- Mobile admin apps
- Desktop applications
- Analytics dashboards
- Reporting tools
