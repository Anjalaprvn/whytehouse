# Travel Package & Destination API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

---

## 🎯 Travel Packages API

### Endpoints

#### 1. List All Packages
```
GET /api/packages/
```

**Query Parameters:**
- `category` - Filter by category (Domestic/International)
- `active` - Filter by active status (true/false)
- `destination` - Filter by destination ID
- `country` - Filter by country name
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter
- `search` - Search in name, location, country, description, itinerary

**Example:**
```bash
# Get all active international packages
GET /api/packages/?category=International&active=true

# Get packages between price range
GET /api/packages/?min_price=10000&max_price=50000

# Search packages
GET /api/packages/?search=Goa
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Goa Beach Paradise",
    "category": "Domestic",
    "destination_name": "Goa",
    "location": "Goa",
    "country": "India",
    "price": "15000.00",
    "duration": "3 Days 2 Nights",
    "image": "/media/travel_packages/goa.jpg",
    "image_url": "http://127.0.0.1:8000/media/travel_packages/goa.jpg",
    "active": true,
    "created_at": "2026-02-28T10:30:00Z"
  }
]
```

---

#### 2. Get Package Details
```
GET /api/packages/{id}/
```

**Response:**
```json
{
  "id": 1,
  "name": "Goa Beach Paradise",
  "category": "Domestic",
  "destination": 5,
  "destination_details": {
    "id": 5,
    "name": "Goa",
    "country": "India",
    "category": "Domestic",
    "description": "Beautiful beaches and nightlife",
    "image": "/media/destinations/goa.jpg",
    "image_url": "http://127.0.0.1:8000/media/destinations/goa.jpg",
    "is_popular": true,
    "created_at": "2026-02-28T10:00:00Z",
    "package_count": 3
  },
  "location": "Goa",
  "country": "India",
  "price": "15000.00",
  "duration": "3 Days 2 Nights",
  "description": "Enjoy the sun, sand, and sea...",
  "image": "/media/travel_packages/goa.jpg",
  "image_url": "http://127.0.0.1:8000/media/travel_packages/goa.jpg",
  "active": true,
  "itinerary": "Day 1: Arrival...\nDay 2: Beach hopping...",
  "inclusions": "Hotel, Breakfast, Transfers",
  "exclusions": "Lunch, Dinner, Personal expenses",
  "meta_title": "Goa Beach Paradise - 3D/2N",
  "meta_description": "Best Goa beach package...",
  "story_main_image": "/media/package_stories/goa_main.jpg",
  "story_main_image_url": "http://127.0.0.1:8000/media/package_stories/goa_main.jpg",
  "story_side_image1": "/media/package_stories/goa_side1.jpg",
  "story_side_image1_url": "http://127.0.0.1:8000/media/package_stories/goa_side1.jpg",
  "story_side_image2": "/media/package_stories/goa_side2.jpg",
  "story_side_image2_url": "http://127.0.0.1:8000/media/package_stories/goa_side2.jpg",
  "created_at": "2026-02-28T10:30:00Z"
}
```

---

#### 3. Create Package
```
POST /api/packages/
```

**Request Body:**
```json
{
  "name": "Kerala Backwaters",
  "category": "Domestic",
  "destination": 3,
  "location": "Alleppey",
  "country": "India",
  "price": "20000.00",
  "duration": "4 Days 3 Nights",
  "description": "Experience the serene backwaters...",
  "active": true,
  "itinerary": "Day 1: Arrival...",
  "inclusions": "Houseboat, Meals, Guide",
  "exclusions": "Airfare, Personal expenses"
}
```

---

#### 4. Update Package
```
PUT /api/packages/{id}/
PATCH /api/packages/{id}/
```

---

#### 5. Delete Package
```
DELETE /api/packages/{id}/
```

---

#### 6. Get Package Summary
```
GET /api/packages/summary/
```

**Response:**
```json
{
  "total": 25,
  "active_count": 20,
  "inactive_count": 5,
  "domestic_count": 12,
  "international_count": 13
}
```

---

#### 7. Get Featured Packages
```
GET /api/packages/featured/
```

Returns first 6 active packages.

---

#### 8. Get Packages by Category
```
GET /api/packages/by_category/
```

**Response:**
```json
{
  "domestic": [
    { "id": 1, "name": "Goa Beach", ... }
  ],
  "international": [
    { "id": 5, "name": "Dubai Luxury", ... }
  ]
}
```

---

## 🌍 Destinations API

### Endpoints

#### 1. List All Destinations
```
GET /api/destinations/
```

**Query Parameters:**
- `category` - Filter by category (Domestic/International)
- `is_popular` - Filter popular destinations (true/false)
- `search` - Search in name, country, description

**Example:**
```bash
# Get popular international destinations
GET /api/destinations/?category=International&is_popular=true

# Search destinations
GET /api/destinations/?search=Bali
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Bali",
    "country": "Indonesia",
    "category": "International",
    "description": "Island paradise with temples and beaches",
    "image": "/media/destinations/bali.jpg",
    "image_url": "http://127.0.0.1:8000/media/destinations/bali.jpg",
    "is_popular": true,
    "created_at": "2026-02-28T09:00:00Z",
    "package_count": 5
  }
]
```

---

#### 2. Get Destination Details
```
GET /api/destinations/{id}/
```

---

#### 3. Create Destination
```
POST /api/destinations/
```

**Request Body:**
```json
{
  "name": "Maldives",
  "country": "Maldives",
  "category": "International",
  "description": "Tropical paradise with crystal clear waters",
  "is_popular": true
}
```

---

#### 4. Update Destination
```
PUT /api/destinations/{id}/
PATCH /api/destinations/{id}/
```

---

#### 5. Delete Destination
```
DELETE /api/destinations/{id}/
```

---

#### 6. Get Destination Summary
```
GET /api/destinations/summary/
```

**Response:**
```json
{
  "total": 15,
  "domestic_count": 8,
  "international_count": 7,
  "popular_count": 5
}
```

---

#### 7. Get Packages for Destination
```
GET /api/destinations/{id}/packages/
```

Returns all active packages for a specific destination.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Bali Adventure",
    "category": "International",
    "destination_name": "Bali",
    "location": "Ubud, Bali",
    "country": "Indonesia",
    "price": "45000.00",
    "duration": "5 Days 4 Nights",
    "image_url": "http://127.0.0.1:8000/media/travel_packages/bali.jpg",
    "active": true
  }
]
```

---

## 📝 Usage Examples

### JavaScript/Fetch
```javascript
// Get all international packages
fetch('http://127.0.0.1:8000/api/packages/?category=International')
  .then(response => response.json())
  .then(data => console.log(data));

// Get package details
fetch('http://127.0.0.1:8000/api/packages/1/')
  .then(response => response.json())
  .then(data => console.log(data));

// Create new package
fetch('http://127.0.0.1:8000/api/packages/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'New Package',
    category: 'Domestic',
    price: '10000.00',
    // ... other fields
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python/Requests
```python
import requests

# Get all packages
response = requests.get('http://127.0.0.1:8000/api/packages/')
packages = response.json()

# Get package details
response = requests.get('http://127.0.0.1:8000/api/packages/1/')
package = response.json()

# Create package
data = {
    'name': 'New Package',
    'category': 'Domestic',
    'price': '10000.00',
    # ... other fields
}
response = requests.post('http://127.0.0.1:8000/api/packages/', json=data)
```

### cURL
```bash
# Get all packages
curl http://127.0.0.1:8000/api/packages/

# Get package details
curl http://127.0.0.1:8000/api/packages/1/

# Create package
curl -X POST http://127.0.0.1:8000/api/packages/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Package",
    "category": "Domestic",
    "price": "10000.00"
  }'
```

---

## 🔍 Filter Examples

```bash
# Active international packages under 50000
GET /api/packages/?category=International&active=true&max_price=50000

# Popular domestic destinations
GET /api/destinations/?category=Domestic&is_popular=true

# Search packages by keyword
GET /api/packages/?search=beach

# Get packages for specific destination
GET /api/destinations/5/packages/
```

---

## ✅ Status

All APIs are now live and ready to use at:
- **Packages**: `http://127.0.0.1:8000/api/packages/`
- **Destinations**: `http://127.0.0.1:8000/api/destinations/`

You can also browse the API using Django REST Framework's browsable API by visiting the URLs in your browser.
