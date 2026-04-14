# DPMB Tram Trips - Architecture Overview

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                         Your Browser                             │
│  (Chrome, Firefox, Safari, Edge, or mobile browser)             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          React Frontend Application                      │  │
│  │  • Line list sidebar                                     │  │
│  │  • Trip details display                                  │  │
│  │  • Statistics dashboard                                  │  │
│  │  • Responsive styling (CSS Grid)                        │  │
│  └────────┬─────────────────────────────────────┬───────────┘  │
│           │ HTTP GET Requests                  │               │
│           │ JSON Responses                      │               │
│           ▼                                     ▼               │
└─────────────────────────────────────────────────────────────────┘
              │                                       │
              │ Port 3001                            │ Port 3001
              ▼                                       ▼
    ┌──────────────────────┐        ┌──────────────────────┐
    │   Node.js Server     │        │   Python Server      │
    │   (server.js)        │        │  (server_python.py)  │
    │                      │        │                      │
    │  Express Framework   │    OR  │   Flask Framework    │
    │  CORS enabled        │        │   CORS enabled       │
    └────────┬─────────────┘        └────────┬─────────────┘
             │                               │
             │ Reads & Processes             │
             │ Trip Files                    │
             │                               │
             ▼                               ▼
        ┌─────────────────────────────────────────┐
        │  File System Data Processing            │
        │  (tripDataProcessor.js / server_python)│
        │                                         │
        │  1. Read all .txt files                │
        │  2. Parse timestamps, events           │
        │  3. Extract destination, vehicle       │
        │  4. Group by line and trip             │
        │  5. Cache in memory                    │
        │  6. Sort by start time                 │
        └────────┬───────────────────────────────┘
                 │
                 │ Reads from
                 │
                 ▼
        ┌─────────────────────────────────────────┐
        │  Log Files Directory                    │
        │  G:\Suli\DPMB-bot\logs\2026-04-14\    │
        │                                         │
        │  00101.txt (Line 1, Trip 1)            │
        │  01207.txt (Line 12, Trip 7)           │
        │  02501.txt (Line 25, Trip 1)           │
        │  03901.txt (Line 39, Trip 1)           │
        │  ... (hundreds more)                   │
        │                                         │
        │  Each file contains:                   │
        │  YYYY-MM-DD HH:MM:SS | START | ...    │
        │  YYYY-MM-DD HH:MM:SS | END   | ...    │
        └─────────────────────────────────────────┘
```

---

## Data Flow

### 1. Server Startup
```
Start Server
    ↓
Load environment variables (LOGS_DIR, PORT)
    ↓
Initialize Express/Flask app with CORS
    ↓
Scan directory for all .txt files
    ↓
Parse each file:
  • Read contents
  • Extract START/END events
  • Parse timestamps, destination, vehicle
  • Group into trips
    ↓
Store in memory cache (organized by line)
    ↓
Server ready to handle requests
    ↓
Listen on http://localhost:3001
```

### 2. User Opens Browser
```
Open http://localhost:3001
    ↓
Load index.html from server
    ↓
React loads from CDN (React 18)
    ↓
React app loads styles.css
    ↓
React app calls /api/lines
    ↓
Server responds with all lines and trip counts
    ↓
React renders line list in sidebar
    ↓
Auto-select first line and load its trips
```

### 3. User Clicks a Line
```
Click line number (e.g., "12")
    ↓
React calls /api/lines/12/trips
    ↓
Server queries cached data for line 12
    ↓
Returns all trips for line 12 as JSON
    ↓
React renders trip cards with:
  • Start time
  • End time
  • Duration (calculated)
  • Destination
  • Vehicle number
```

---

## API Structure

### Available Endpoints

#### GET /api/lines
Returns all available lines
```javascript
Response:
{
  "success": true,
  "data": [
    {"lineNum": 1, "tripCount": 24},
    {"lineNum": 2, "tripCount": 18},
    ...
  ],
  "timestamp": "2026-04-14T12:34:56.789Z"
}
```

#### GET /api/lines/:lineNum/trips
Returns trips for specific line
```javascript
Response:
{
  "success": true,
  "line": 12,
  "trips": [
    {
      "tripId": 7,
      "startTime": "2026-04-14 15:23:46",
      "endTime": "2026-04-14 16:42:31",
      "destination": "Okrouhlice",
      "lines": ["12"],
      "vehicle": "4501"
    },
    ...
  ],
  "count": 15,
  "timestamp": "2026-04-14T12:34:56.789Z"
}
```

#### GET /api/stats
Returns overall statistics
```javascript
Response:
{
  "success": true,
  "stats": {
    "totalLines": 45,
    "totalTrips": 8324,
    "lastUpdated": "2026-04-14T12:34:56.789Z"
  }
}
```

---

## File Parsing Logic

### Filename Parsing
```
Filename: 02501.txt

Extract with regex: /^(\d{3})(\d{2})\.txt$/

Group 1: 025 → Line number: 25
Group 2: 01 → Trip number: 1

Result: Line 25, Trip 1
```

### Content Parsing
```
Line: "2026-04-14 15:35:33 | START | Jármű: 3303 | Vonal: 38 | Cél: Preslova"

Extract with regex: /^([\d\-\s:]+)\s*\|\s*(START|END)\s*\|(.*)$/

Group 1: 2026-04-14 15:35:33 → startTime
Group 2: START → eventType
Group 3: "Jármű: 3303 | Vonal: 38 | Cél: Preslova" → details

Parse details:
• "Jármů: 3303" → vehicle: "3303"
• "Vonal: 38" → line: "38"
• "Cél: Preslova" → destination: "Preslova"

Create trip object and cache it
```

---

## Memory Structure

### Cache Object
```javascript
data_cache = {
  lines: {
    1: [
      {
        startTime: "2026-04-14 15:23:46",
        endTime: "2026-04-14 16:42:31",
        destination: "Řečkovice",
        vehicle: "1088",
        segments: ["1"],
        tripId: 1,
        filename: "00101.txt"
      },
      // ... more trips for line 1
    ],
    2: [
      // ... trips for line 2
    ],
    // ... more lines
  },
  all_trips: [...all trips combined],
  last_updated: "2026-04-14T12:34:56.789Z"
}
```

---

## Component Structure (React Frontend)

```
App Component
├── useState: lines, selectedLine, trips, loading, error, stats
├── useEffect: Load lines and stats on mount
├── useEffect: Load trips when selectedLine changes
│
├── Header
│   └── Title and description
│
├── StatsBar
│   ├── Total lines stat
│   ├── Total trips stat
│   └── Today's trips stat
│
├── MainContent (Grid Layout)
│   │
│   ├── Sidebar
│   │   ├── "Lines" title
│   │   └── LineItem components (map over lines)
│   │       └── onClick: setSelectedLine
│   │
│   └── MainPanel
│       ├── Header: "Line X"
│       └── TripCard components (map over trips)
│           ├── Trip time range
│           ├── Destination
│           ├── Vehicle info
│           └── Lines involved
```

---

## Response Times

Typical response times (on local machine):

| Action | Time |
|--------|------|
| Server startup | 1-2 seconds |
| Load all lines | 50-100ms |
| Load line trips | 10-50ms |
| Display frontend | 100-500ms |
| User interaction | Instant |

---

## Scalability Considerations

**Current Setup (Good for ~1000 trips/day):**
- In-memory caching
- Single-threaded processing
- Local file reading

**For Larger Scale (~10,000+ trips/day):**
- Add database (SQLite, PostgreSQL)
- Implement pagination
- Add compression
- Use CDN for static files
- Horizontal scaling with load balancer

**For Real-time Updates:**
- WebSocket connections
- Server-sent events (SSE)
- Message queue (RabbitMQ, Redis)

---

## Security Notes

**Current Implementation:**
- No authentication required
- Read-only operations
- No database access
- Local file system only
- CORS enabled for all origins

**For Production:**
- Add authentication/authorization
- Restrict CORS to specific domains
- Use HTTPS
- Add rate limiting
- Validate all inputs
- Implement logging and monitoring

---

## Deployment Architecture

### Local Development
```
Your Computer
├── Frontend (React via CDN + local HTML/CSS/JS)
├── Backend (Express/Flask on localhost:3001)
└── Data (Log files on local drive)
```

### Single Server Deployment
```
Web Server
├── Frontend (Served by Express/Flask)
├── Backend (Express/Flask on port 3001)
└── Data (Log files mounted or synced)
```

### Production Deployment
```
                    ┌─────────────┐
                    │   Browser   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Cloudflare │ (CDN/Cache)
                    └──────┬──────┘
                           │
                    ┌──────▼──────────────┐
                    │  Load Balancer      │
                    └──────┬──────┬───────┘
                           │      │
            ┌──────────────┘      └──────────────┐
            │                                    │
     ┌──────▼─────┐                      ┌─────▼──────┐
     │ Web Server 1    │                      │ Web Server 2 │
     │ Express/Flask   │                  │ Express/Flask  │
     │ Instance A      │                  │ Instance B     │
     └──────┬─────┘                      └──────┬────────┘
            │                                     │
            └──────────────┬──────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Database   │ (Shared)
                    └─────────────┘
```

---

## Technology Choices

### Why React?
- Fast rendering with virtual DOM
- Component reusability
- Large community and ecosystem
- Easy to update in real-time

### Why Express/Flask?
- **Express:** Fast, Node.js ecosystem, excellent for APIs
- **Flask:** Simple, Python ecosystem, faster to set up

### Why File-based Data?
- No database setup needed
- Easy to understand and modify
- Good for small to medium datasets
- Easy to backup (just copy folder)

### Why In-Memory Cache?
- Very fast responses
- No database latency
- Good for this use case (static daily data)
- Reloads on server restart

---

## Error Handling Flow

```
Request
  │
  ├─► Try block
  │   ├─► Process request
  │   └─► Return success response
  │
  └─► Catch block
      ├─► Log error to console
      ├─► Return error JSON
      └─► HTTP 500 status
```

---

## Performance Optimization Tips

1. **Reduce Initial Load Time**
   - Cache API responses in browser localStorage
   - Lazy load trip details
   - Compress JavaScript and CSS

2. **Improve Server Performance**
   - Use pagination for large datasets
   - Implement database indexing
   - Add server-side caching headers

3. **Better UI/UX**
   - Virtual scrolling for long lists
   - Debounce line selection
   - Show loading skeleton screens

---

## Monitoring & Logging

**Currently Logs:**
- Server startup
- Lines processed count
- Trip count
- Errors (if any)

**Could Add:**
- Request logging (Express morgan middleware)
- Performance metrics
- Error tracking (Sentry)
- Analytics (GA, Mixpanel)

---

This architecture is simple, effective, and easy to understand. It can be extended with additional features as needed using the API as the foundation.
