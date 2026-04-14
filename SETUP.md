# DPMB Tram Trips - Setup & Installation Guide

## 🔧 Prerequisites

This project requires **Node.js** and **npm**. Choose one of the options below:

### Option A: Node.js Installation (Recommended)

#### Windows:
1. Download Node.js LTS from: https://nodejs.org/
2. Run the installer (.msi file)
3. During installation, check "Add to PATH" ✓
4. Complete installation
5. Verify installation by opening PowerShell and running:
```powershell
node --version
npm --version
```

Should show:
```
v18.x.x (or higher)
9.x.x (or higher)
```

#### If Node.js is already installed but npm isn't recognized:

**Step 1: Find Node.js Installation Path**

In PowerShell, run:
```powershell
where node
```

Example output: `C:\Program Files\nodejs\node.exe`

**Step 2: Add to Windows PATH**

1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", click "New"
5. Variable name: `NODEJS_HOME`
6. Variable value: `C:\Program Files\nodejs` (or your path from Step 1)
7. Click OK
8. Find "Path" variable, click Edit
9. Click "New" and add: `%NODEJS_HOME%`
10. Click OK, OK, OK
11. Restart PowerShell and verify:
```powershell
npm --version
```

---

### Option B: Python Alternative Backend

If you prefer not to install Node.js, I can create a Python-based backend instead.

---

## 📦 Installation Steps (Node.js)

### Step 1: Navigate to Project Directory

Open PowerShell and run:
```powershell
cd g:\Suli\dpmb-trips
```

### Step 2: Install Dependencies

```powershell
npm run install:all
```

This will install:
- **Backend**: Express, CORS, fs-extra
- **Frontend**: React, Axios

Alternatively, install separately:
```powershell
# Backend
cd backend
npm install
cd ..

# Frontend (optional - it's loaded via CDN)
cd frontend
npm install
cd ..
```

### Step 3: Start the Server

```powershell
npm start
```

Expected output:
```
DPMB Trips backend server running on http://localhost:3001
API available at http://localhost:3001/api
Loaded XX lines with XXXX total trips
```

### Step 4: Open in Browser

Visit: http://localhost:3001

---

## 🚀 Usage

### Running the Server

**Normal mode:**
```powershell
npm start
```

**Development mode with auto-reload (requires nodemon):**
```powershell
npm run dev:backend
```

**Using different port:**
```powershell
$env:PORT = "3000"
npm start
```

**Using different log directory:**
```powershell
$env:LOGS_DIR = "G:\Path\To\Your\Logs"
npm start
```

---

## 🐛 Troubleshooting

### Error: "npm: The term 'npm' is not recognized"

**Solution:**
1. Reinstall Node.js from https://nodejs.org/
2. Make sure to check "Add to PATH" during installation
3. Restart PowerShell after installation
4. Verify: `npm --version`

### Error: "Port 3001 is already in use"

**Solution:**
```powershell
$env:PORT = "3002"
npm start
```

Or find and kill the process using port 3001:
```powershell
netstat -ano | findstr :3001
taskkill /PID <PID> /F
```

### Error: "Cannot find path 'G:\Suli\DPMB-bot\logs\2026-04-14'"

**Solution:**
- Update the log directory path in your command:
```powershell
$env:LOGS_DIR = "G:\Your\Actual\Path"
npm start
```

### Frontend not loading / Blank page

1. Check backend is running: http://localhost:3001/api/stats
2. Check browser console (F12) for errors
3. Try clearing cache: `Ctrl + Shift + Del`
4. Restart backend and browser

### No trip data displaying

1. Verify log files exist: `G:\Suli\DPMB-bot\logs\2026-04-14`
2. Check file naming: Should be like `00101.txt`, `01207.txt`, etc.
3. Check backend console for parsing errors

---

## 📋 Project Structure

```
g:\Suli\dpmb-trips\
├── backend/                    # Node.js server
│   ├── server.js              # Express server
│   ├── tripDataProcessor.js   # Data parsing
│   ├── package.json           # Dependencies
│   └── node_modules/          # Installed packages (created after npm install)
│
├── frontend/                   # React application
│   ├── index.html            # Main page
│   ├── app.js                # React component
│   ├── styles.css            # Styling
│   └── package.json
│
├── package.json              # Root configuration
├── README.md                 # Full documentation
├── QUICKSTART.md            # Quick reference
└── SETUP.md                 # This file
```

---

## 🌐 Accessing the Application

Once the server is running:

- **Frontend:** http://localhost:3001
- **API - All lines:** http://localhost:3001/api/lines
- **API - Line 1 trips:** http://localhost:3001/api/lines/1/trips
- **API - Statistics:** http://localhost:3001/api/stats

---

## 💾 Data Format

Trip files:
- Location: `G:\Suli\DPMB-bot\logs\2026-04-14\`
- Naming: `XXXXX.txt` (first 3 digits = line, last 2 = trip)
- Example: `01207.txt` = Line 12, Trip 7

---

## 📞 Support

If you encounter any issues:

1. Check the browser console (F12 → Console tab)
2. Check the PowerShell output in the terminal
3. Verify all prerequisites are installed
4. Try restarting the server
5. Check file paths and permissions

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Node.js installed: `node --version` shows v14+
- [ ] npm installed: `npm --version` shows 6+
- [ ] Dependencies installed: `g:\Suli\dpmb-trips\backend\node_modules` exists
- [ ] Server starts with `npm start`
- [ ] Browser opens http://localhost:3001 successfully
- [ ] Sidebar shows tram lines (1, 2, 5, etc.)
- [ ] Clicking a line shows trips
- [ ] Trip details are visible

---

## 🎯 Next Steps

1. **Verify Setup Works:**
   - Run `npm start`
   - Open http://localhost:3001
   - Click on line 1
   - Should see trips with times and destinations

2. **Optional Enhancements:**
   - Deploy to web server
   - Add database support
   - Enable real-time updates
   - Mobile app development

3. **For Developers:**
   - Backend API: `backend/server.js`
   - Frontend component: `frontend/app.js`
   - Data processor: `backend/tripDataProcessor.js`

Good luck! 🚊
