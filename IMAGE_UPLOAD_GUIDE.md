# Image Upload Guide - WhyteHouse API

## Overview

The API now supports image uploads for:
- **Destinations**: `image`, `map_image`
- **Travel Packages**: `image`, `story_main_image`, `story_side_image1`, `story_side_image2`
- **Properties**: `image`

---

## How to Upload Images in Postman

### Step 1: Set Request Type
- Method: `POST` (for create) or `PATCH`/`PUT` (for update)
- URL: Your endpoint (e.g., `/api/destinations/add-domestic/`)

### Step 2: Set Authorization
- Go to **Authorization** tab
- Type: **Bearer Token**
- Token: Your access token

### Step 3: Set Body Type
- Go to **Body** tab
- Select **form-data** (NOT raw JSON)

### Step 4: Add Fields
For each field:
- Key: field name (e.g., `name`, `country`, `image`)
- Value: field value
- For image fields: Change type from "Text" to "File" in the dropdown next to the key

---

## Example 1: Add Destination with Images

**Endpoint:** `POST /api/destinations/add-domestic/`

**Body (form-data):**

| Key | Type | Value |
|-----|------|-------|
| name | Text | Kerala |
| country | Text | India |
| description | Text | God's own country |
| packages_start_from | Text | 15000.00 |
| is_popular | Text | true |
| is_active | Text | true |
| image | File | [Select image file] |
| map_image | File | [Select map image file] |

**Response:**
```json
{
  "id": 20,
  "name": "Kerala",
  "country": "India",
  "category": "Domestic",
  "description": "God's own country",
  "packages_start_from": "15000.00",
  "image": "/media/destinations/kerala.jpg",
  "map_image": "/media/destinations/maps/kerala_map.jpg",
  "is_popular": true,
  "is_active": true,
  "created_at": "2026-04-20T15:00:00Z"
}
```

---

## Example 2: Add Travel Package with Story Images

**Endpoint:** `POST /api/packages/add-domestic/`

**Body (form-data):**

| Key | Type | Value |
|-----|------|-------|
| destination | Text | 1 |
| name | Text | Goa Beach Paradise |
| location | Text | Goa |
| country | Text | India |
| price | Text | 15000.00 |
| adult_price | Text | 15000.00 |
| price_type | Text | Per Person |
| duration | Text | 3 Days / 2 Nights |
| description | Text | Enjoy pristine beaches |
| itinerary | Text | Day 1: Arrival\nDay 2: Beach\nDay 3: Checkout |
| inclusions | Text | Hotel, Breakfast, Transfers |
| exclusions | Text | Lunch, Dinner, Entry tickets |
| active | Text | true |
| image | File | [Select main package image] |
| story_main_image | File | [Select story main image] |
| story_side_image1 | File | [Select story side image 1] |
| story_side_image2 | File | [Select story side image 2] |

**Response:**
```json
{
  "id": 10,
  "package_id": "PKG010",
  "name": "Goa Beach Paradise",
  "category": "Domestic",
  "destination": 1,
  "location": "Goa",
  "country": "India",
  "price": "15000.00",
  "adult_price": "15000.00",
  "duration": "3 Days / 2 Nights",
  "image": "/media/travel_packages/goa_beach.jpg",
  "story_main_image": "/media/package_stories/goa_story_main.jpg",
  "story_side_image1": "/media/package_stories/goa_story_1.jpg",
  "story_side_image2": "/media/package_stories/goa_story_2.jpg",
  "created_at": "2026-04-20T15:30:00Z"
}
```

---

## Example 3: Update Package Images (PATCH)

**Endpoint:** `PATCH /api/packages/10/`

**Body (form-data):**

| Key | Type | Value |
|-----|------|-------|
| story_main_image | File | [Select new story main image] |
| story_side_image1 | File | [Select new story side image 1] |

**Note:** Only include fields you want to update. Other fields remain unchanged.

---

## Example 4: Update Destination Image

**Endpoint:** `PATCH /api/destinations/5/`

**Body (form-data):**

| Key | Type | Value |
|-----|------|-------|
| image | File | [Select new destination image] |
| is_popular | Text | true |

---

## Example 5: Add Property with Image

**Endpoint:** `POST /api/properties/`

**Body (form-data):**

| Key | Type | Value |
|-----|------|-------|
| name | Text | Beach Resort |
| property_type | Text | resort |
| location | Text | Goa |
| address | Text | Beach Road, Calangute |
| summary | Text | Luxury beachfront resort |
| owner_name | Text | John Doe |
| owner_contact | Text | 9876543210 |
| amenities | Text | Pool, Spa, WiFi, Restaurant |
| is_active | Text | true |
| image | File | [Select resort image] |

---

## Image Fields Summary

### Destination Model
- `image` - Main destination image
- `map_image` - Map/location image

### Travel Package Model
- `image` - Main package image
- `story_main_image` - Main story/traveller image
- `story_side_image1` - Story side image 1
- `story_side_image2` - Story side image 2

### Property Model
- `image` - Property image

---

## Important Notes

1. **Content-Type**: When using form-data, Postman automatically sets `Content-Type: multipart/form-data`

2. **File Size**: Ensure images are reasonable size (recommended < 5MB per image)

3. **File Formats**: Supported formats: JPG, JPEG, PNG, GIF, WEBP

4. **Optional Fields**: All image fields are optional. You can create/update without images.

5. **Updating Images**: Use PATCH to update only specific fields including images

6. **Multiple Images**: You can upload multiple images in a single request (e.g., all 4 package images at once)

7. **Image URLs**: Response includes full image paths (e.g., `/media/destinations/kerala.jpg`)

8. **Access Images**: Images are accessible at `http://127.0.0.1:8000/media/destinations/kerala.jpg`

---

## Postman Tips

### Setting File Type
1. In Body → form-data
2. Hover over the key field
3. Click the dropdown that appears on the right
4. Select "File" instead of "Text"
5. Click "Select Files" button that appears in the Value column

### Bulk Upload
You can add multiple fields at once:
- Add all text fields first
- Then add all file fields
- Submit the request

### Testing
1. Create with images
2. GET the resource to verify image URLs
3. Access image URL in browser to confirm upload

---

## Common Errors

### Error: "The submitted data was not a file"
- **Cause**: Field type is set to "Text" instead of "File"
- **Solution**: Change dropdown from "Text" to "File"

### Error: "Unsupported media type"
- **Cause**: Using raw JSON instead of form-data
- **Solution**: Switch Body type to "form-data"

### Error: "This field is required"
- **Cause**: Missing required text fields
- **Solution**: Ensure all required fields are included (name, country, etc.)

---

## cURL Examples

### Add Destination with Image
```bash
curl -X POST http://127.0.0.1:8000/api/destinations/add-domestic/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "name=Kerala" \
  -F "country=India" \
  -F "description=God's own country" \
  -F "packages_start_from=15000.00" \
  -F "is_popular=true" \
  -F "is_active=true" \
  -F "image=@/path/to/kerala.jpg" \
  -F "map_image=@/path/to/kerala_map.jpg"
```

### Add Package with Story Images
```bash
curl -X POST http://127.0.0.1:8000/api/packages/add-domestic/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "destination=1" \
  -F "name=Goa Beach Paradise" \
  -F "location=Goa" \
  -F "country=India" \
  -F "price=15000.00" \
  -F "duration=3 Days / 2 Nights" \
  -F "description=Beach vacation" \
  -F "image=@/path/to/package.jpg" \
  -F "story_main_image=@/path/to/story_main.jpg" \
  -F "story_side_image1=@/path/to/story1.jpg" \
  -F "story_side_image2=@/path/to/story2.jpg"
```

### Update Package Image (PATCH)
```bash
curl -X PATCH http://127.0.0.1:8000/api/packages/10/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "story_main_image=@/path/to/new_story.jpg"
```

---

## Summary

✅ Use **form-data** in Postman Body tab
✅ Set image fields to **File** type
✅ Include **Bearer token** in Authorization
✅ All image fields are **optional**
✅ Works with POST, PUT, and PATCH methods
✅ Supports multiple images in single request
