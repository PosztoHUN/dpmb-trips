require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const tripProcessor = require('./tripDataProcessor');

const app = express();
const PORT = process.env.PORT || 3001;

// Get logs directory with fallback
// For Railway: /data/logs
// For local: G:\Suli\DPMB-bot\logs\2026-04-14
const getLogsDir = () => {
  if (process.env.LOGS_DIR) {
    return process.env.LOGS_DIR;
  }
  // Check if on Railway (Linux environment)
  if (process.platform === 'linux') {
    return '/data/logs';
  }
  // Default for Windows development
  return 'G:\\Suli\\DPMB-bot\\logs\\2026-04-14';
};

const logsDir = getLogsDir();

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true
}));
app.use(express.json());

// Serve static files from frontend (but not directories with index files)
app.use(express.static(path.join(__dirname, '../frontend'), {
  index: false  // We'll handle index.html manually in the fallback
}));

// Initialize data on startup
console.log(`Loading all public transport lines from: ${logsDir}`);
console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
tripProcessor.processAllTripsFromDirectory(logsDir);

// API Routes

/**
 * GET /api/lines
 * Returns all available public transport lines (trams, buses, trolleybuses) with trip counts
 */
app.get('/api/lines', (req, res) => {
  try {
    const lines = tripProcessor.getLines();
    res.json({
      success: true,
      data: lines,
      timestamp: new Date(),
      note: 'Includes all transport types: trams, buses, trolleybuses, etc.'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/lines/:lineNum/trips
 * Returns all trips for a specific public transport line
 */
app.get('/api/lines/:lineNum/trips', (req, res) => {
  try {
    const lineNum = parseInt(req.params.lineNum);
    const trips = tripProcessor.getTripsForLine(lineNum);
    
    res.json({
      success: true,
      line: lineNum,
      trips: trips,
      count: trips.length,
      timestamp: new Date()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/stats
 * Returns overall statistics
 */
app.get('/api/stats', (req, res) => {
  try {
    const cache = tripProcessor.getCache();
    res.json({
      success: true,
      stats: {
        totalLines: Object.keys(cache.lines).length,
        totalTrips: cache.allTrips.length,
        lastUpdated: cache.lastUpdated
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /health
 * Health check endpoint for Railway/deployment
 */
app.get('/health', (req, res) => {
  try {
    const cache = tripProcessor.getCache();
    const isHealthy = cache.lines && Object.keys(cache.lines).length > 0;
    
    res.json({
      status: isHealthy ? 'healthy' : 'initializing',
      lines: Object.keys(cache.lines).length,
      trips: cache.allTrips.length,
      dataLoaded: isHealthy,
      timestamp: new Date()
    });
  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      error: error.message
    });
  }
});

// Fallback to React app (serves index.html for SPA routing and root path)
app.get('*', (req, res) => {
  const indexPath = path.join(__dirname, '../frontend/index.html');
  res.sendFile(indexPath, (err) => {
    if (err) {
      console.error('Error serving index.html:', err.message);
      res.status(404).json({
        success: false,
        error: 'Application not found'
      });
    }
  });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    error: 'Internal server error',
    message: err.message
  });
});

app.listen(PORT, () => {
  console.log('========================================');
  console.log('🚊 DPMB Public Transport Server');
  console.log('========================================');
  console.log(`✓ Server running on port ${PORT}`);
  console.log(`✓ Frontend: http://localhost:${PORT}`);
  console.log(`✓ API: http://localhost:${PORT}/api`);
  console.log(`✓ Health: http://localhost:${PORT}/health`);
  console.log(`✓ Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`✓ Logs: ${logsDir}`);
  console.log('========================================');
});
