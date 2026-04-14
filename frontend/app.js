// DPMB Tram Trips Frontend Application
const { useState, useEffect, useCallback } = React;

// API Base URL
const API_BASE = 'http://localhost:3001/api';

// Main Application Component
function App() {
  const [lines, setLines] = useState([]);
  const [selectedLine, setSelectedLine] = useState(null);
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  // Load all lines on mount
  useEffect(() => {
    fetchLines();
    fetchStats();
  }, []);

  // Fetch all available lines
  const fetchLines = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE}/lines`);
      if (response.data.success) {
        setLines(response.data.data);
        // Auto-select first line
        if (response.data.data.length > 0) {
          setSelectedLine(response.data.data[0].lineNum);
        }
      }
    } catch (err) {
      setError('Failed to load lines: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch trips for selected line
  useEffect(() => {
    if (selectedLine !== null) {
      fetchTripsForLine(selectedLine);
    }
  }, [selectedLine]);

  const fetchTripsForLine = useCallback(async (lineNum) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE}/lines/${lineNum}/trips`);
      if (response.data.success) {
        setTrips(response.data.trips);
      }
    } catch (err) {
      setError('Failed to load trips: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch statistics
  const fetchStats = useCallback(async () => {
    try {
      const response = await axios.get(`${API_BASE}/stats`);
      if (response.data.success) {
        setStats(response.data.stats);
      }
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  }, []);

  return (
    <div className="app">
      {/* Header */}
      <div className="header">
        <div className="container">
          <h1>🚊 DPMB Public Transport</h1>
          <p>Real-time tracking for trams, buses, trolleybuses in Brno</p>
        </div>
      </div>

      {/* Main Container */}
      <div className="container">
        {/* Statistics Bar */}
        {stats && (
          <div className="stats-bar">
            <div className="stat-card">
              <div className="stat-value">{stats.totalLines}</div>
              <div className="stat-label">Lines (All Types)</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{stats.totalTrips}</div>
              <div className="stat-label">Total Trips</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{trips.length}</div>
              <div className="stat-label">Selected Line Trips</div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && <div className="error-message">❌ {error}</div>}

        {/* Main Content */}
        <div className="main-content">
          {/* Sidebar - Lines List */}
          <div className="sidebar">
            <div className="sidebar-title">📍 All Lines</div>
            <div className="lines-list">
              {lines.map(line => (
                <div
                  key={line.lineNum}
                  className={`line-item ${selectedLine === line.lineNum ? 'active' : ''}`}
                  onClick={() => setSelectedLine(line.lineNum)}
                >
                  <span className="line-number">{line.lineNum}</span>
                  <span className="trip-count">{line.tripCount}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Main Panel - Trips Display */}
          <div className="main-panel">
            <div className="panel-header">
              🚋 Line {selectedLine} - Trips
            </div>

            <div className="panel-content">
              {loading ? (
                <div className="loading">Loading trips...</div>
              ) : trips.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-state-icon">🚫</div>
                  <p>No trips found for this line</p>
                </div>
              ) : (
                <div className="trips-container">
                  {trips.map((trip, index) => (
                    <TripCard key={index} trip={trip} />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Trip Card Component
function TripCard({ trip }) {
  const formatTime = (dateString) => {
    return dateString.split(' ')[1] || dateString;
  };

  const getDuration = (start, end) => {
    try {
      const startDate = new Date(`2026-04-14 ${formatTime(start)}`);
      const endDate = new Date(`2026-04-14 ${formatTime(end)}`);
      const minutes = Math.round((endDate - startDate) / 60000);
      return `${minutes} min`;
    } catch {
      return 'N/A';
    }
  };

  return (
    <div className="trip-card">
      <div className="trip-header">
        <div>
          <div className="trip-time">
            ⏱️ {formatTime(trip.startTime)} - {formatTime(trip.endTime)}
          </div>
          <div style={{ fontSize: '0.85rem', color: '#999', marginTop: '4px' }}>
            Duration: {getDuration(trip.startTime, trip.endTime)}
          </div>
        </div>
        {trip.vehicle && (
          <div className="trip-vehicle">
            Vehicle: {trip.vehicle}
          </div>
        )}
      </div>

      {trip.destination && (
        <div className="trip-destination">
          📍 {trip.destination}
        </div>
      )}

      <div className="trip-details">
        <div className="trip-detail-item">
          <span className="trip-detail-label">Start:</span>
          <span className="trip-detail-value">{formatTime(trip.startTime)}</span>
        </div>
        <div className="trip-detail-item">
          <span className="trip-detail-label">End:</span>
          <span className="trip-detail-value">{formatTime(trip.endTime)}</span>
        </div>
      </div>

      {trip.lines && trip.lines.length > 0 && (
        <div className="trip-lines">
          <div className="trip-lines-label">Lines involved:</div>
          <div className="trip-lines-items">
            {trip.lines.map((line, idx) => (
              <span key={idx} className="line-badge">
                Line {line}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Render the app to DOM
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
