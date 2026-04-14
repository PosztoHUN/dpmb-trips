# Python Backend for DPMB Tram Trips

## Setup (Python Alternative)

If you prefer to use Python instead of Node.js, follow these steps:

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Check if Python is installed:**
```powershell
python --version
pip --version
```

Should show Python 3.7+ and pip version.

If not installed, download from: https://www.python.org/

2. **Install dependencies:**
```powershell
cd g:\Suli\dpmb-trips\backend
pip install -r requirements.txt
```

3. **Start the server:**
```powershell
python server_python.py
```

Expected output:
```
Loading trips from: G:\Suli\DPMB-bot\logs\2026-04-14
Processed XX lines with XXXX total trips
DPMB Trips backend server running on http://localhost:3001
```

4. **Open in browser:**
```
http://localhost:3001
```

### Configuration (Python)

**Use different port:**
```powershell
$env:PORT = "3000"
python server_python.py
```

**Use different log directory:**
```powershell
$env:LOGS_DIR = "G:\Path\To\Logs"
python server_python.py
```

**Debug mode:**
```powershell
$env:DEBUG = "1"
python server_python.py
```

### Advantages of Python Backend

- Single file deployment
- No build step required
- Simpler data processing
- Built-in Flask server
- Same API as Node.js version

### Disadvantages

- Slightly slower than Node.js (for this use case, not noticeable)
- Less suitable for very high traffic
- Requires Python installation

---

## Troubleshooting (Python)

### "ModuleNotFoundError: No module named 'flask'"

Install missing package:
```powershell
pip install Flask Flask-CORS
```

### "Port 3001 is already in use"

```powershell
$env:PORT = "3002"
python server_python.py
```

### "Cannot find path..."

Update LOGS_DIR:
```powershell
$env:LOGS_DIR = "C:\Your\Actual\Path"
python server_python.py
```

---

## Comparison

| Feature | Node.js | Python |
|---------|---------|--------|
| Setup Time | Medium | Fast |
| Performance | Fast | Good |
| Dependencies | Many | Few |
| File Size | Larger | Smaller |
| Deployment | Easier | Simple |
| Development | Good | Good |
| Scalability | Better | Good |

---

## Which One to Choose?

**Choose Node.js if:**
- You're planning to scale or add features
- You want better async performance
- You're familiar with Node.js/JavaScript

**Choose Python if:**
- You have Python already installed
- You want minimal setup
- You prefer Python syntax
- Faster initial setup

Both versions have the same API and frontend, so you can easily switch between them.
