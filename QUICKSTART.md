# Quick Start Guide

## Installation (Windows)

1. Open PowerShell in the `g:\Suli\dpmb-trips` directory

2. Install all dependencies:
```powershell
npm run install:all
```

3. Start the server:
```powershell
npm start
```

4. Open your browser and navigate to:
```
http://localhost:3001
```

## What You'll See

- **Left Sidebar**: List of all tram lines (1, 2, 5, 6, 7, 8, etc.)
- **Main Panel**: Trips for the selected line showing:
  - ⏱️ Departure and arrival times
  - 📍 Destination/direction
  - 🚋 Vehicle number
  - Trip duration

- **Top Stats**: Overview statistics

## Common Commands

```powershell
# Install dependencies
npm run install:all

# Start the server
npm start

# Run with auto-reload (for development)
npm run dev:backend

# Use different port
$env:PORT = "3000"; npm start

# Use different log directory
$env:LOGS_DIR = "C:\Path\To\Logs"; npm start
```

## Features

✅ Browse all tram lines  
✅ View trips for each line  
✅ See start/end times and destinations  
✅ Track vehicle numbers  
✅ Handle line changes (like 38→39)  
✅ Responsive design for mobile & desktop  
✅ Real-time data loading  

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Need Help?

1. Check that Node.js is installed: `node --version`
2. Verify npm works: `npm --version`
3. Ensure log files exist at: `G:\Suli\DPMB-bot\logs\2026-04-14`
4. Check browser console (F12) for errors
