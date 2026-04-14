# DPMB Tram Trips Website 🚊

A modern web application for tracking tram trips in Brno. View available tram lines and their scheduled trips with detailed information about destinations, times, and vehicles.

## Features

✨ **Line Management**
- Display all available tram lines
- Show trip counts for each line
- Sticky sidebar for easy navigation

📅 **Trip Details**
- Start and end times for each trip
- Trip duration calculation
- Vehicle information
- Destination/direction information
- Lines involved in each trip (handles line changes like 38→39)

📊 **Statistics**
- Total number of lines
- Total trips across all lines
- Today's trips count

🎨 **Modern UI**
- Responsive design (mobile, tablet, desktop)
- Similar to Hungarian transport tracking sites
- Clean and intuitive navigation
- Real-time data loading

## Project Structure

```
dpmb-trips/
├── backend/                 # Node.js/Express server
│   ├── server.js           # Main Express server
│   ├── tripDataProcessor.js # Data parsing and processing
│   ├── package.json
│   └── data-processor/     # Data processing utilities
├── frontend/               # React frontend
│   ├── index.html         # Main HTML file
│   ├── app.js             # React application
│   ├── styles.css         # Styling
│   └── package.json
└── package.json           # Root package configuration
```

## Data Format

Trip files are located at: `G:\Suli\DPMB-bot\logs\YYYY-MM-DD`

**Filename Format**: `XXXXX.txt`
- First 3 digits: Tram line number (e.g., `001` = line 1, `038` = line 38)
- Last 2 digits: Trip number (e.g., `01` = first trip)
- Example: `01207.txt` = line 12, trip 7

**File Content**: Each file contains log entries with formats:
```
2026-04-14 15:23:46 | START | Vehicle: 3303 | Direction: 38 | Location: {...}
2026-04-14 15:35:33 | START | Jármű: 3303 | Vonal: 38 | Cél: Preslova
2026-04-14 16:03:42 | END   | Jármű: 3303 | Vonal: 38 | Cél: Preslova
```

## Installation

### Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)

### Setup Steps

1. **Install dependencies:**
```bash
npm run install:all
```

2. **Start the server:**
```bash
npm start
```

The application will be available at: `http://localhost:3001`

### Development Mode

For development with auto-reload:
```bash
npm run dev:backend
```

## API Endpoints

### Get All Lines
```
GET /api/lines
```
Returns all available tram lines with trip counts.

**Response:**
```json
{
  "success": true,
  "data": [
    { "lineNum": 1, "tripCount": 24 },
    { "lineNum": 2, "tripCount": 18 }
  ],
  "timestamp": "2026-04-14T12:00:00.000Z"
}
```

### Get Trips for a Line
```
GET /api/lines/:lineNum/trips
```
Returns all trips for a specific line.

**Response:**
```json
{
  "success": true,
  "line": 1,
  "trips": [
    {
      "tripId": 1,
      "startTime": "2026-04-14 15:23:46",
      "endTime": "2026-04-14 16:42:31",
      "destination": "Řečkovice",
      "lines": ["1"],
      "vehicle": "1088"
    }
  ],
  "count": 24,
  "timestamp": "2026-04-14T12:00:00.000Z"
}
```

### Get Statistics
```
GET /api/stats
```
Returns overall statistics.

**Response:**
```json
{
  "success": true,
  "stats": {
    "totalLines": 45,
    "totalTrips": 8324,
    "lastUpdated": "2026-04-14T12:00:00.000Z"
  }
}
```

## Configuration

### Custom Log Directory

By default, the application loads data from: `G:\Suli\DPMB-bot\logs\2026-04-14`

To use a different directory, set the `LOGS_DIR` environment variable:

```bash
set LOGS_DIR=G:\Path\To\Your\Logs
npm start
```

Or on Unix/Linux:
```bash
LOGS_DIR=/path/to/logs npm start
```

### Port Configuration

By default, the server runs on port `3001`.

To use a different port, set the `PORT` environment variable:

```bash
set PORT=3000
npm start
```

## Technologies Used

**Backend:**
- Node.js
- Express.js
- CORS middleware
- fs-extra for file operations

**Frontend:**
- React 18
- Axios for HTTP requests
- CSS3 for styling
- Responsive design with CSS Grid

**Data Processing:**
- File parsing and regex pattern matching
- In-memory caching
- Real-time data filtering

## Features & Inspiration

The UI design is inspired by:
- https://holajarmu.hu/szeged/history/vehicles?line=4&day=2026-04-14
- https://online.winmenetrend.hu/futar/history/lines
- https://online.winmenetrend.hu/futar/history/lines/3010?date=2026-04-14

## Usage Example

1. Open http://localhost:3001 in your browser
2. The application loads with statistics showing total lines and trips
3. Click on any tram line number in the left sidebar to view its trips
4. View detailed information for each trip:
   - Departure time, arrival time, and duration
   - Destination/direction
   - Vehicle number
   - Lines involved (useful for trips that change lines)

## Troubleshooting

### Port already in use
If port 3001 is already in use:
```bash
set PORT=3002
npm start
```

### Data not loading
- Verify the log directory path exists
- Check that the date folder matches (default: 2026-04-14)
- Ensure files follow the XXXXX.txt naming format

### Frontend not displaying
- Clear browser cache (Ctrl+Shift+Del)
- Ensure backend server is running (check http://localhost:3001/api/stats)
- Check browser console for errors

## Future Enhancements

- [ ] Real-time vehicle tracking with GPS
- [ ] Historical data visualization
- [ ] Trip planner/route finder
- [ ] Notifications for delays
- [ ] Multiple date support
- [ ] Export trip data to CSV/PDF
- [ ] Database integration for persistence
- [ ] User preferences and saved routes
- [ ] Mobile app

## License

MIT License - Feel free to use and modify

## Support

For issues or questions, check the troubleshooting section or review the API documentation above.
