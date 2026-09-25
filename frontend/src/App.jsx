import { useState, useEffect, useRef } from 'react';
import { Search, Film, User, Clapperboard, PlayCircle, AlertCircle } from 'lucide-react';

function App() {
  const [movies, setMovies] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const wrapperRef = useRef(null);

  useEffect(() => {
    // Fetch initial list of movies
    fetch('http://localhost:5000/api/movies')
      .then(res => res.json())
      .then(data => setMovies(data.movies))
      .catch(err => console.error("Failed to fetch movies:", err));
      
    // Handle click outside for suggestions
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSearch = async (titleToSearch = searchQuery) => {
    if (!titleToSearch.trim()) return;
    
    setSearchQuery(titleToSearch);
    setShowSuggestions(false);
    setLoading(true);
    setError(null);
    setRecommendations([]);

    try {
      const response = await fetch(`http://localhost:5000/api/recommend?title=${encodeURIComponent(titleToSearch)}`);
      const data = await response.json();

      if (data.error) {
        setError(data.error);
      } else {
        setRecommendations(data.recommendations);
      }
    } catch (err) {
      setError("Failed to connect to the recommendation server. Make sure it's running.");
    } finally {
      setLoading(false);
    }
  };

  const filteredMovies = movies.filter(movie => 
    movie.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="app-container">
      <header className="header">
        <h1>Kollywood Recommender</h1>
        <p>Discover your next favorite Tamil movie based on what you already love.</p>
      </header>

      <div className="search-container">
        <div className="search-input-wrapper" ref={wrapperRef}>
          <Search className="search-icon" size={20} />
          <input
            type="text"
            className="search-input"
            placeholder="Type a movie you like (e.g., Vikram, 96)..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setShowSuggestions(true);
            }}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            onFocus={() => setShowSuggestions(true)}
          />
          
          {showSuggestions && searchQuery && filteredMovies.length > 0 && (
            <div className="suggestions-container">
              {filteredMovies.slice(0, 5).map((movie, index) => (
                <div 
                  key={index} 
                  className="suggestion-item"
                  onClick={() => handleSearch(movie.title)}
                >
                  <span className="suggestion-title">{movie.title}</span>
                  <span className="suggestion-genre">{movie.genres}</span>
                </div>
              ))}
            </div>
          )}
        </div>
        <button 
          className="search-button"
          onClick={() => handleSearch()}
          disabled={!searchQuery.trim() || loading}
        >
          Discover
        </button>
      </div>

      {error && (
        <div className="error-message">
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      {loading && (
        <div className="loader-container">
          <div className="loader"></div>
          <p>Analyzing film features...</p>
        </div>
      )}

      {recommendations.length > 0 && (
        <div>
          <h2 className="section-title">
            <PlayCircle size={28} color="var(--primary-color)" />
            Recommended for you
          </h2>
          <div className="movie-grid">
            {recommendations.map((movie, index) => (
              <div key={index} className="movie-card" style={{ animationDelay: `${index * 0.1}s` }}>
                <h3 className="movie-title">{movie.title}</h3>
                
                <div className="movie-meta">
                  <div className="meta-item">
                    <Film size={16} />
                    <span>{movie.genres}</span>
                  </div>
                  <div className="meta-item">
                    <Clapperboard size={16} />
                    <span>Dir: {movie.director}</span>
                  </div>
                  <div className="meta-item">
                    <User size={16} />
                    <span>Starring: {movie.lead_actor}</span>
                  </div>
                </div>
                
                <p className="movie-desc">{movie.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
