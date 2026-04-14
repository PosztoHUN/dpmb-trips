const fs = require('fs-extra');
const path = require('path');

// Global cache for processed data
let dataCache = {
  lines: {},
  allTrips: [],
  lastUpdated: null
};

/**
 * Parse a trip file and extract start time, end time, start location, end location, destination
 */
function parseTripsLog(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.trim().split('\n');
    
    const trips = [];
    let currentTrip = null;

    for (const line of lines) {
      const match = line.match(/^([\d\-\s:]+)\s*\|\s*(START|END)\s*\|(.*)$/);
      if (!match) continue;

      const timestamp = match[1].trim();
      const eventType = match[2];
      const details = match[3];

      // Parse direction/destination from details
      let destination = '';
      let lineNum = '';
      let vehicle = '';

      const lineParts = details.split('|');
      for (const part of lineParts) {
        if (part.includes('Cél:')) {
          destination = part.split('Cél:')[1].trim();
        }
        if (part.includes('Vonal:')) {
          lineNum = part.split('Vonal:')[1].trim();
        }
        if (part.includes('Jármű:')) {
          vehicle = part.split('Jármű:')[1].trim();
        }
      }

      if (eventType === 'START') {
        currentTrip = {
          startTime: timestamp,
          endTime: null,
          destination: destination,
          line: lineNum,
          vehicle: vehicle,
          segments: [lineNum]
        };
      } else if (eventType === 'END' && currentTrip) {
        currentTrip.endTime = timestamp;
        
        // Add to trips if both start and end exist
        if (currentTrip.startTime && currentTrip.endTime) {
          trips.push(currentTrip);
        }
        currentTrip = null;
      }
    }

    return trips;
  } catch (error) {
    console.error(`Error parsing file ${filePath}:`, error);
    return [];
  }
}

/**
 * Process all trip files and build a searchable data structure
 */
function processAllTripsFromDirectory(logsDir) {
  const lines = {};
  const allTrips = [];

  try {
    const files = fs.readdirSync(logsDir);
    
    files.forEach(file => {
      if (!file.endsWith('.txt') || file === 'placeholder.txt') return;

      // Parse filename: XXXXX.txt where XXX = line, XX = trip
      const match = file.match(/^(\d{3})(\d{2})\.txt$/);
      if (!match) return;

      const lineNum = parseInt(match[1]);
      const tripNum = parseInt(match[2]);
      
      const filePath = path.join(logsDir, file);
      const trips = parseTripsLog(filePath);

      if (trips.length > 0) {
        // Organize by line
        if (!lines[lineNum]) {
          lines[lineNum] = [];
        }

        trips.forEach(trip => {
          trip.lineId = lineNum;
          trip.tripId = tripNum;
          trip.filename = file;
          lines[lineNum].push(trip);
          allTrips.push(trip);
        });
      }
    });

    // Sort trips within each line by start time
    Object.keys(lines).forEach(lineNum => {
      lines[lineNum].sort((a, b) => 
        new Date(a.startTime) - new Date(b.startTime)
      );
    });

    dataCache = {
      lines: lines,
      allTrips: allTrips,
      lastUpdated: new Date()
    };

    console.log(`Processed ${Object.keys(lines).length} lines with ${allTrips.length} total trips`);
    return dataCache;
  } catch (error) {
    console.error('Error processing trips directory:', error);
    return dataCache;
  }
}

/**
 * Get all available lines
 */
function getLines() {
  return Object.keys(dataCache.lines)
    .map(num => ({
      lineNum: parseInt(num),
      tripCount: dataCache.lines[num].length
    }))
    .sort((a, b) => a.lineNum - b.lineNum);
}

/**
 * Get trips for a specific line
 */
function getTripsForLine(lineNum) {
  const trips = dataCache.lines[lineNum];
  if (!trips) return [];
  
  return trips.map(trip => ({
    tripId: trip.tripId,
    filename: trip.filename,
    startTime: trip.startTime,
    endTime: trip.endTime,
    destination: trip.destination,
    lines: trip.segments,
    vehicle: trip.vehicle
  }));
}

module.exports = {
  processAllTripsFromDirectory,
  getLines,
  getTripsForLine,
  getCache: () => dataCache
};
