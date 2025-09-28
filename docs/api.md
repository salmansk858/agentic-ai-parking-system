# API Reference

## Overview

The Agentic AI Frictionless Parking System provides a RESTful API for intelligent parking management. All endpoints return JSON responses and use HTTP status codes for error handling.

## Base URL

```
Local Development: http://localhost:8000
Production: https://api.parking-ai.example.com
```

## Authentication

Currently uses API key authentication. Include your API key in the header:

```bash
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health Check

#### GET /
Check system health and status.

**Response:**
```json
{
  "service": "Agentic AI Frictionless Parking System",
  "status": "running", 
  "version": "1.0.0",
  "agents_loaded": 7
}
```

### Agent Management

#### GET /agents
List all available agents in the system.

**Response:**
```json
{
  "agents": [
    "interaction",
    "informative_search", 
    "on_route_guidance",
    "access",
    "micro_routing",
    "on_spot",
    "departure"
  ],
  "total": 7
}
```

### User Profiles

#### GET /profiles
Get all available user profiles based on research.

**Response:**
```json
{
  "profiles": {
    "commuter_saver": {
      "name": "Commuter Saver",
      "description": "Drives an EV on a tight budget..."
    },
    "efficient_multitasker": {
      "name": "Efficient Multitasker", 
      "description": "Values time over money..."
    }
  }
}
```

### Parking Search

#### POST /parking/search
Search for optimal parking spots using multi-agent system.

**Request Body:**
```json
{
  "destination": "Toronto City Hall",
  "user_profile": "green_professional",
  "constraints": {
    "ev_charging": "required",
    "max_price": 5.0,
    "accessibility": "preferred"
  },
  "preferences": {
    "walking_distance": 300,
    "rating_priority": "high"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "results": {
    "workflow": "find_parking",
    "user_preferences": {
      "profile_type": "green_professional",
      "preferences": {
        "ev_charging": "fast_required",
        "reliability": "critical"
      }
    },
    "search_results": {
      "status": "success", 
      "results": [
        {
          "name": "Green P Carpark 36",
          "address": "110 Queen St W, Toronto",
          "coordinates": {"lat": 43.6517, "lng": -79.3844},
          "walk_distance": "87m",
          "price": "CA$4.00 per half-hour",
          "ev_charging": true,
          "accessibility": true,
          "rating": 4.2,
          "booking_url": "https://..."
        }
      ],
      "total_found": 3
    }
  }
}
```

### Navigation

#### POST /navigation/start
Start navigation to selected parking destination.

**Request Body:**
```json
{
  "destination": {
    "name": "Green P Carpark 36",
    "address": "110 Queen St W, Toronto", 
    "coordinates": {"lat": 43.6517, "lng": -79.3844}
  },
  "current_location": {
    "lat": 43.6426,
    "lng": -79.3871
  }
}
```

**Response:**
```json
{
  "status": "success",
  "navigation": {
    "destination": {...},
    "eta": "12 minutes",
    "distance": "3.2 km", 
    "route": "via University Ave",
    "traffic_status": "light",
    "weather": "clear"
  }
}
```

### Feedback

#### POST /feedback
Submit user feedback for system learning.

**Request Body:**
```json
{
  "session_id": "sess_123456",
  "rating": 5,
  "comments": "Great parking recommendation!"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Thank you for your feedback!",
  "feedback_id": "fb_789012"
}
```

### System Metrics

#### GET /system/metrics
Get system performance and configuration metrics.

**Response:**
```json
{
  "model_config": {
    "model": "gpt-4o-mini",
    "temperature": 0.2,
    "max_tokens": 150,
    "top_p": 0.8
  },
  "agents_status": {
    "interaction": "active",
    "informative_search": "active"
  },
  "performance_optimizations": {
    "entropy_setting": "low",
    "verbosity": "short", 
    "prompt_specificity": "medium",
    "chain_of_thought": "enabled"
  }
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Invalid or missing API key
- `404 Not Found` - Endpoint not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

**Error Response Format:**
```json
{
  "status": "error",
  "error": "Description of the error",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error details"
  }
}
```

## Rate Limiting

- **Development**: 100 requests per minute
- **Production**: 1000 requests per minute
- **Enterprise**: Custom limits available

Rate limit headers included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95  
X-RateLimit-Reset: 1640995200
```

## SDK Examples

### Python

```python
from src.runner import ParkingSystem

# Initialize system
system = ParkingSystem()

# Find parking
result = await system.find_parking(
    destination="Toronto City Hall",
    user_profile="commuter_saver"
)

# Navigate to selected spot
if result['search_results']['results']:
    selected = result['search_results']['results'][0]
    navigation = await system.navigate_to_parking(selected)
```

### cURL

```bash
# Search for parking
curl -X POST "http://localhost:8000/parking/search" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Toronto City Hall",
    "user_profile": "green_professional"
  }'

# Start navigation
curl -X POST "http://localhost:8000/navigation/start" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": {
      "name": "Green P Carpark 36",
      "coordinates": {"lat": 43.6517, "lng": -79.3844}
    }
  }'
```

### JavaScript

```javascript
// Search for parking
const searchResponse = await fetch('/parking/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    destination: 'Toronto City Hall',
    user_profile: 'efficient_multitasker',
    constraints: {
      ev_charging: 'required',
      max_price: 6.0
    }
  })
});

const searchResult = await searchResponse.json();
console.log('Found parking options:', searchResult.results);
```

## API Versioning

The API uses URL versioning:
- `/v1/parking/search` - Version 1 (current)
- `/v2/parking/search` - Version 2 (future)

Current version: `v1`

For the latest API changes, see our [changelog](CHANGELOG.md).
