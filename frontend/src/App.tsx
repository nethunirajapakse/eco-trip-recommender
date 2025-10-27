import React, { useState, useRef, useEffect } from 'react';
import { Mountain, Compass, Sparkles, MapPin, TrendingUp, Target, AlertCircle, CheckCircle2, Leaf, Camera, Bird, X, Loader2 } from 'lucide-react';
import './App.css'

interface RecommendedPlace {
  name: string;
  climate: string;
  region: string;
  difficulty: string;
  popularity: string;
  score: number;
  features?: string[];
}

interface ApiResponse {
  success: boolean;
  results?: RecommendedPlace[];
  error?: string;
}

interface ActivitiesApiResponse {
  success: boolean;
  activities?: string[];
  error?: string;
  count?: number;
}

const App = () => {
  const [allAvailableActivities, setAllAvailableActivities] = useState<string[]>([]);
  const [activitiesLoading, setActivitiesLoading] = useState<boolean>(true);
  const [activitiesFetchError, setActivitiesFetchError] = useState<string | null>(null); 
  const [selectedActivities, setSelectedActivities] = useState<string[]>(['hiking', 'photography']);
  const [activityInput, setActivityInput] = useState<string>('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const [climate, setClimate] = useState<string>('any');
  const [region, setRegion] = useState<string>('any');
  const [difficulty, setDifficulty] = useState<string>('any');
  const [popularity, setPopularity] = useState<string>('any');
  const [results, setResults] = useState<RecommendedPlace[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false); 
  const [recommendationError, setRecommendationError] = useState<string | null>(null); 

  const API_URL: string = 'http://localhost:5000/api';

  const climates: string[] = ["any", "dry zone", "cool highland", "wet zone"];
  const regions: string[] = [
    "any", "southeast sri lanka", "central sri lanka", "southern sri lanka",
    "northwest sri lanka", "north central sri lanka", "southwest sri lanka",
    "eastern sri lanka", "northern sri lanka", "south central sri lanka"
  ];
  const difficulties: string[] = ["any", "easy", "moderate", "hard"];
  const popularities: string[] = ["any", "high", "medium", "low"];

  useEffect(() => {
    const fetchActivities = async () => {
      setActivitiesLoading(true);
      setActivitiesFetchError(null);
      try {
        const response = await fetch(`${API_URL}/activities`);
        const data: ActivitiesApiResponse = await response.json();

        if (response.ok && data.success && data.activities) {
          setAllAvailableActivities(data.activities);
        } else {
          setActivitiesFetchError(data.error || 'Failed to fetch available activities.');
        }
      } catch (err: any) {
        setActivitiesFetchError('Unable to connect to the activities API. Make sure the Flask backend is running.');
        console.error('Error fetching activities:', err);
      } finally {
        setActivitiesLoading(false);
      }
    };

    fetchActivities();
  }, [API_URL]); 

  const handleActivityInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setActivityInput(value);

    const filteredSuggestions = allAvailableActivities.filter(
      (activity) =>
        activity.toLowerCase().includes(value.toLowerCase()) &&
        !selectedActivities.includes(activity)
    );
    setSuggestions(filteredSuggestions);
    setShowSuggestions(true);
  };

  const addActivity = (activity: string) => {
    if (!selectedActivities.includes(activity)) {
      setSelectedActivities([...selectedActivities, activity]);
      setActivityInput('')
      setSuggestions([]);
      setShowSuggestions(false);
    }
    inputRef.current?.focus();
  };

  const removeActivity = (activityToRemove: string) => {
    setSelectedActivities(selectedActivities.filter(activity => activity !== activityToRemove));
    inputRef.current?.focus();
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (inputRef.current && !inputRef.current.contains(event.target as Node)) {
        const suggestionList = document.getElementById('activity-suggestions');
        if (suggestionList && !suggestionList.contains(event.target as Node)) {
          setShowSuggestions(false);
        }
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleRecommend = async () => {
    if (selectedActivities.length === 0) {
      setRecommendationError('Please select at least one activity');
      return;
    }

    setLoading(true);
    setResults(null);
    setRecommendationError(null);

    try {
      const response = await fetch(`${API_URL}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          activities: selectedActivities,
          climate: climate,
          region: region,
          difficulty: difficulty,
          popularity: popularity
        })
      });

      const data: ApiResponse = await response.json();

      if (response.ok && data.success && data.results) {
        setResults(data.results);
      } else {
        setRecommendationError(data.error || 'Failed to get recommendations');
      }
    } catch (err: any) {
      setRecommendationError('Unable to connect to the recommendation API. Make sure the Flask backend is running on port 5000.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number): string => {
    if (score >= 80) return 'bg-emerald-600';
    if (score >= 60) return 'bg-teal-600';
    if (score >= 40) return 'bg-cyan-600';
    return 'bg-blue-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white py-16 px-4 shadow-xl">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Leaf className="w-12 h-12 animate-pulse" />
            <h1 className="text-5xl font-bold tracking-tight">CeylonWild</h1>
            <Leaf className="w-12 h-12 animate-pulse" />
          </div>
          <p className="text-center text-xl text-emerald-50 max-w-2xl mx-auto">
            Discover Sri Lanka's pristine eco-destinations through our intelligent expert system
          </p>
          <div className="flex justify-center gap-8 mt-8 text-sm flex-wrap">
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5" />
              <span>26+ Destinations</span>
            </div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5" />
              <span>AI-Powered Matching</span>
            </div>
            <div className="flex items-center gap-2">
              <Target className="w-5 h-5" />
              <span>Personalized Results</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Input Form */}
          <div className="md:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg p-8 space-y-6">
              <div className="flex items-center gap-3 mb-6">
                <Compass className="w-6 h-6 text-emerald-600" />
                <h2 className="text-2xl font-bold text-gray-800">Your Preferences</h2>
              </div>

              {/* Activities Input with Tags and Suggestions */}
              <div className="space-y-2 relative">
                <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
                  <Camera className="w-4 h-4" />
                  Activities
                  {activitiesLoading && <Loader2 className="w-4 h-4 animate-spin text-emerald-500" />}
                </label>
                {activitiesFetchError ? (
                  <div className="bg-red-50 border-2 border-red-200 rounded-lg p-3 text-sm text-red-700">
                    <AlertCircle className="inline-block w-4 h-4 mr-2" />
                    {activitiesFetchError}
                  </div>
                ) : (
                  <>
                    <div className="flex flex-wrap gap-2 p-2 border-2 border-gray-200 rounded-lg focus-within:border-emerald-500 transition-colors bg-white min-h-[48px]">
                      {selectedActivities.map((activity) => (
                        <span
                          key={activity}
                          className="inline-flex items-center bg-emerald-100 text-emerald-800 text-sm font-medium px-2.5 py-1 rounded-full"
                        >
                          {activity}
                          <button
                            type="button"
                            onClick={() => removeActivity(activity)}
                            className="ml-1.5 p-0.5 rounded-full hover:bg-emerald-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                          >
                            <X className="w-3 h-3 text-emerald-600" />
                          </button>
                        </span>
                      ))}
                      <input
                        ref={inputRef}
                        type="text"
                        value={activityInput}
                        onChange={handleActivityInputChange}
                        onFocus={() => {
                            setSuggestions(allAvailableActivities.filter(act => !selectedActivities.includes(act)));
                            setShowSuggestions(true);
                        }}
                        placeholder={selectedActivities.length === 0 ? "e.g., hiking, photography" : ""}
                        className="flex-grow min-w-[150px] outline-none bg-transparent"
                        disabled={activitiesLoading}
                      />
                    </div>

                    {showSuggestions && suggestions.length > 0 && (
                      <ul id="activity-suggestions" className="absolute z-10 w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto mt-1">
                        {suggestions.map((activity) => (
                          <li
                            key={activity}
                            onClick={() => addActivity(activity)}
                            className="px-4 py-2 hover:bg-emerald-50 cursor-pointer text-gray-800"
                          >
                            {activity.charAt(0).toUpperCase() + activity.slice(1)}
                          </li>
                        ))}
                      </ul>
                    )}
                    <p className="text-xs text-gray-500">Type to search or select from suggestions.</p>
                  </>
                )}
              </div>

              {/* Climate Selection */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
                  <Mountain className="w-4 h-4" />
                  Climate
                </label>
                <select
                  value={climate}
                  onChange={(e) => setClimate(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-emerald-500 focus:outline-none transition-colors bg-white"
                >
                  {climates.map(c => (
                    <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
                  ))}
                </select>
              </div>

              {/* Region Selection */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
                  <MapPin className="w-4 h-4" />
                  Region
                </label>
                <select
                  value={region}
                  onChange={(e) => setRegion(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-emerald-500 focus:outline-none transition-colors bg-white"
                >
                  {regions.map(r => (
                    <option key={r} value={r}>{r.charAt(0).toUpperCase() + r.slice(1).replace(/_/g, ' ')}</option>
                  ))}
                </select>
              </div>

              {/* Difficulty Selection */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
                  <TrendingUp className="w-4 h-4" />
                  Difficulty
                </label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-emerald-500 focus:outline-none transition-colors bg-white"
                >
                  {difficulties.map(d => (
                    <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
                  ))}
                </select>
              </div>

              {/* Popularity Selection */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
                  <Sparkles className="w-4 h-4" />
                  Popularity
                </label>
                <select
                  value={popularity}
                  onChange={(e) => setPopularity(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-emerald-500 focus:outline-none transition-colors bg-white"
                >
                  {popularities.map(p => (
                    <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
                  ))}
                </select>
              </div>

              {/* Error Message for Recommendations */}
              {recommendationError && (
                <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-red-800 font-semibold">Error</p>
                    <p className="text-red-700 text-sm">{recommendationError}</p>
                  </div>
                </div>
              )}

              {/* Submit Button */}
              <button
                onClick={handleRecommend}
                disabled={loading || activitiesLoading}
                className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 text-white py-4 rounded-lg font-semibold text-lg hover:from-emerald-700 hover:to-teal-700 transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing...
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    <Compass className="w-5 h-5" />
                    Find My Perfect Destination
                  </span>
                )}
              </button>
            </div>
          </div>

          {/* Info Card */}
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-2xl shadow-lg p-6 border-2 border-amber-200">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-6 h-6 text-amber-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-gray-800 mb-2">How It Works</h3>
                  <ul className="text-sm text-gray-700 space-y-2">
                    <li>• Enter your preferred activities</li>
                    <li>• Select your climate preferences</li>
                    <li>• Choose difficulty and popularity</li>
                    <li>• Our AI matches you with ideal spots</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl shadow-lg p-6 border-2 border-emerald-200">
              <div className="flex items-start gap-3">
                <Leaf className="w-6 h-6 text-emerald-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-gray-800 mb-2">Eco-Friendly</h3>
                  <p className="text-sm text-gray-700">
                    All destinations promote sustainable tourism and conservation efforts across Sri Lanka's pristine wilderness.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl shadow-lg p-6 border-2 border-blue-200">
              <div className="flex items-start gap-3">
                <Target className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-gray-800 mb-2">CLIPS Expert System</h3>
                  <p className="text-sm text-gray-700">
                    Powered by rule-based AI that matches your preferences with the perfect eco-destinations.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {results !== null && (
          <div className="mt-12 bg-white rounded-2xl shadow-lg p-8">
            {results.length > 0 ? (
              <>
                <div className="flex items-center gap-3 mb-6">
                  <CheckCircle2 className="w-7 h-7 text-emerald-600" />
                  <h2 className="text-2xl font-bold text-gray-800">Your Perfect Matches</h2>
                  <span className="ml-auto bg-emerald-100 text-emerald-800 px-4 py-1 rounded-full text-sm font-semibold">
                    {results.length} {results.length === 1 ? 'Result' : 'Results'}
                  </span>
                </div>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {results.map((place, index) => (
                    <div
                      key={index}
                      className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl p-6 border-2 border-emerald-200 hover:border-emerald-400 transition-all hover:shadow-xl transform hover:scale-[1.02]"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="font-bold text-lg text-gray-800 flex-1 pr-2">
                          {place.name}
                        </h3>
                        <div className={`${getScoreColor(place.score)} text-white px-3 py-1 rounded-full text-sm font-bold`}>
                          {place.score}
                        </div>
                      </div>
                      <div className="space-y-2 text-sm text-gray-700">
                        <p className="flex items-center gap-2">
                          <Mountain className="w-4 h-4 text-emerald-600" />
                          <span className="font-semibold">Climate:</span> {place.climate}
                        </p>
                        <p className="flex items-center gap-2">
                          <MapPin className="w-4 h-4 text-emerald-600" />
                          <span className="font-semibold">Region:</span> {place.region}
                        </p>
                        <p className="flex items-center gap-2">
                          <TrendingUp className="w-4 h-4 text-emerald-600" />
                          <span className="font-semibold">Difficulty:</span> {place.difficulty}
                        </p>
                        {place.features && place.features.length > 0 && (
                          <div className="mt-3">
                            <p className="font-semibold mb-2">Special Features:</p>
                            <div className="flex flex-wrap gap-1">
                              {place.features.slice(0, 3).map((feature, i) => (
                                <span
                                  key={i}
                                  className="bg-white px-2 py-1 rounded text-xs text-gray-600 border border-emerald-200"
                                >
                                  {feature}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
                <p className="text-center text-sm text-gray-500 mt-6">
                  💡 Higher scores indicate better matches with your preferences
                </p>
              </>
            ) : (
              <div className="text-center py-12">
                <AlertCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-700 mb-2">No Matches Found</h3>
                <p className="text-gray-500">Try adjusting your preferences to find more destinations</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-gray-800 text-gray-300 py-8 mt-16">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p className="text-sm">
            🌿 <span className="font-semibold">CeylonWild</span> — Sri Lanka's Eco-Tourism Expert System © 2025
          </p>
          <p className="text-xs mt-2 text-gray-400">
            Powered by CLIPS Expert System | Built for Conservation & Discovery
          </p>
        </div>
      </div>
    </div>
  );
};

export default App;
