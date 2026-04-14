# DPMB Tram Trips Website - Complete Setup Guide

Welcome! This is a modern web application for tracking tram trips in Brno. Below is everything you need to get started.

## 🚀 Quick Start (Choose One Option)

### Option 1: Node.js Backend (Recommended)

**Pros:** Better performance, good for scaling  
**Cons:** Requires Node.js installation

```powershell
# 1. Install Node.js from https://nodejs.org (v18 LTS recommended)
#    Download installer and check "Add to PATH"

# 2. Install dependencies
cd g:\Suli\dpmb-trips
npm run install:all

# 3. Start server
npm start

# 4. Open browser
https://localhost:3001
```

**Detailed guide:** See [SETUP.md](SETUP.md)

---

### Option 2: Python Backend (Faster Setup)

**Pros:** Minimal setup, single file deployment  
**Cons:** Requires Python installation

```powershell
# 1. Install Python from https://www.python.org (3.7+)
#    Check "Add Python to PATH" during installation

# 2. Install dependencies
cd g:\Suli\dpmb-trips\backend
pip install -r requirements.txt

# 3. Start server
python server_python.py

# 4. Open browser
http://localhost:3001
```

**Detailed guide:** See [backend/PYTHON_BACKEND.md](backend/PYTHON_BACKEND.md)

---

## ✅ Verification

After starting the server, you should see:

1. **Terminal Output:**
   ```
   DPMB Trips backend server running on http://localhost:3001
   Processed XX lines with XXXX total trips
   ```

2. **Browser at http://localhost:3001:**
   - Statistics showing lines and trip counts
   - Left sidebar with list of tram lines
   - Main panel showing trips when you click a line

3. **Each trip should show:**
   - ⏱️ Start and end times
   - 📍 Destination/direction
   - 🚗 Vehicle number (optional)
   - 🚊 Lines involved

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference for commands
- **[README.md](README.md)** - Full documentation and API reference
- **[SETUP.md](SETUP.md)** - Detailed Node.js setup troubleshooting
- **[backend/PYTHON_BACKEND.md](backend/PYTHON_BACKEND.md)** - Python setup guide

---

## 🏗️ Project Structure

```
dpmb-trips/
├── backend/
│   ├── server.js               # Node.js server (Express)
│   ├── server_python.py        # Python server (Flask)
│   ├── tripDataProcessor.js    # Trip data parsing (Node.js)
│   ├── package.json            # Npm dependencies
│   └── requirements.txt         # Python dependencies
│
├── frontend/
│   ├── index.html              # Main page
│   ├── app.js                  # React application
│   └── styles.css              # Styling
│
├── README.md                   # Full documentation
├── SETUP.md                    # Setup troubleshooting
├── QUICKSTART.md              # Quick reference
└── package.json               # Root npm config
```

---

## 🔍 Data Format

**Files are located at:**
```
G:\Suli\DPMB-bot\logs\2026-04-14\
```

**Filename format:** `XXXXX.txt`
- First 3 digits: Tram line (001 = line 1, 038 = line 38, 050 = line 50)
- Last 2 digits: Trip number (01-99)
- Example: `02501.txt` = line 25, first trip

**File content:**
```
2026-04-14 15:23:46 | START | Vehicle: 3303 | Direction: 38 | Location: {...}
2026-04-14 15:35:33 | START | Jármű: 3303 | Vonal: 38 | Cél: Preslova
2026-04-14 16:03:42 | END   | Jármű: 3303 | Vonal: 38 | Cél: Preslova
```

---

## 🌐 API Endpoints

Once the server is running:

### Get All Lines
```
GET http://localhost:3001/api/lines
```
Returns all available tram lines with trip counts.

### Get Trips for a Line
```
GET http://localhost:3001/api/lines/1/trips
```
Returns all trips for line 1.

### Get Statistics
```
GET http://localhost:3001/api/stats
```
Returns total lines and trips.

---

## ⚙️ Configuration

### Change Port
```powershell
# Node.js
$env:PORT = "3000"
npm start

# Python
$env:PORT = "3000"
python backend/server_python.py
```

### Change Log Directory
```powershell
# Node.js
$env:LOGS_DIR = "G:\Custom\Path\to\logs"
npm start

# Python
$env:LOGS_DIR = "G:\Custom\Path\to\logs"
python backend/server_python.py
```

---

## 🆘 Troubleshooting

### "Module not found" / "npm not found"
- Install Node.js or Python from the links above
- Restart PowerShell after installation
- Verify with: `node --version` or `python --version`

### "Port already in use"
```powershell
# Use different port
$env:PORT = "3002"
npm start  # or python server_python.py
```

### "No data loading"
1. Check that `G:\Suli\DPMB-bot\logs\2026-04-14` exists
2. Verify files exist: `dir G:\Suli\DPMB-bot\logs\2026-04-14\*.txt`
3. Check file naming: Should be like `00101.txt`, `02501.txt`, etc.

### "Frontend not creating"
1. Check browser console: `F12` → Console
2. Verify backend is running: Open `http://localhost:3001/api/stats`
3. Clear browser cache: `Ctrl + Shift + Del`

---

## 🎯 What You Can Do With This App

✅ **Browse all tram lines** - View the complete list  
✅ **Select a line** - Click any line number  
✅ **See trip details** - Departure time, arrival time, duration  
✅ **View destinations** - Where each trip goes  
✅ **Track vehicles** - Vehicle numbers for each trip  
✅ **Handle line changes** - Trips that change lines (e.g., 38→39)  
✅ **Responsive design** - Works on desktop, tablet, mobile  

---

## 📱 Browser Support

- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

---

## 🚀 Deployment

### Deploy Locally (Current Setup)
- Server runs on your machine
- Access via `http://localhost:3001`
- Limited to local network

### Deploy to Server
1. Copy entire folder to server
2. Install Node.js/Python on server
3. Run the start command
4. Configure with actual IP address

### Deploy to Cloud
- Host on AWS, Azure, Heroku, etc.
- More complex setup, good for production

---

## 💡 Features Inspiration

This site is inspired by:
- https://holajarmu.hu/szeged/history/vehicles?line=4&day=2026-04-14
- https://online.winmenetrend.hu/futar/history/lines
- https://online.winmenetrend.hu/futar/history/lines/3010?date=2026-04-14

---

## 📖 Next Steps

1. **Choose your backend:** Node.js or Python
2. **Install requirements:** Node.js or Python + dependencies
3. **Start the server:** See instructions above
4. **Open in browser:** `http://localhost:3001`
5. **Test functionality:** Click lines, view trips
6. **Customize:** Modify colors, add features, etc.

---

## 📞 Getting Help

1. **Check the docs:**
   - [README.md](README.md) - Full API documentation
   - [QUICKSTART.md](QUICKSTART.md) - Quick commands reference
   - [SETUP.md](SETUP.md) - Node.js troubleshooting
   - [backend/PYTHON_BACKEND.md](backend/PYTHON_BACKEND.md) - Python guide

2. **Check your setup:**
   - Verify prerequisites installed: `node --version` or `python --version`
   - Check log directory exists: `dir G:\Suli\DPMB-bot\logs\2026-04-14\`
   - Verify files exist: Should have .txt files in the logs directory

3. **Common issues:**
   - Module not found → Install dependencies
   - Port in use → Change PORT environment variable
   - No data → Check log directory path and permissions

---

## 🎓 Technology Stack

**Frontend:**
- React 18 (via CDN)
- CSS3 with Grid/Flexbox
- Responsive design
- Real-time data loading

**Backend - Node.js Option:**
- Express.js web framework
- CORS for cross-origin requests
- fs-extra for file operations
- Nodemon for development

**Backend - Python Option:**
- Flask web framework
- Flask-CORS extension
- Built-in development server
- Minimal dependencies

**Data Processing:**
- Regex pattern matching
- In-memory caching
- Real-time file reading
- Efficient sorting and filtering

---

## ✨ Features

- 🎨 **Modern UI** - Clean, responsive design
- ⚡ **Fast loading** - Real-time data processing
- 📊 **Statistics** - Total lines and trips overview
- 🔍 **Easy navigation** - Sticky sidebar for quick access
- 📱 **Mobile friendly** - Works on all devices
- 🔄 **API-based** - RESTful API for extensibility
- 🎯 **Zero database** - File-based data storage

---

Great! You're ready to start. Choose your backend option above and follow the instructions. Good luck! 🚊

---

**Last Updated:** 2026-04-14  
**Version:** 1.0  
**Status:** Ready to deploy
