import csv
import requests
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from functools import lru_cache
import time

# Global cache for thesaurus lookups to avoid repeated API calls
_thesaurus_cache: Dict[str, Set[str]] = {}

# Ratios for API throttling to respect rate limits
_last_api_call: float = 0
_api_call_delay: float = 0.1  # Minimum delay between API calls in seconds

# Local fallback thesaurus for moods and genres (when API is unavailable)
# This ensures the system works even without internet connectivity
_LOCAL_THESAURUS = {
    # Moods
    "chill": {"relaxed", "lounge", "laid-back", "mellow", "calm", "peaceful"},
    "relaxed": {"chill", "calm", "peaceful", "laid-back", "mellow", "lounge"},
    "calm": {"peaceful", "serene", "tranquil", "relaxed", "mellow", "quiet"},
    "peaceful": {"calm", "serene", "tranquil", "relaxing", "soothing", "quiet"},
    "happy": {"cheerful", "upbeat", "joyful", "bright", "positive", "energetic"},
    "sad": {"melancholic", "sorrowful", "blue", "gloomy", "mournful", "down"},
    "intense": {"energetic", "powerful", "aggressive", "high-energy", "fierce", "passionate"},
    "romantic": {"intimate", "sensual", "sweet", "dreamy", "sentimental", "love"},
    # Genres\n    "pop": {"chart", "popular", "mainstream", "dance-pop", "synth-pop"},
    "country": {"western", "folk", "americana", "country-pop", "blue-grass", "folk-country"},
    "rock": {"alternative", "hard rock", "indie", "punk", "classic rock", "rock-n-roll"},
    "jazz": {"bebop", "smooth jazz", "fusion", "swing", "cool jazz", "modal"},
    "electronic": {"edm", "synth", "techno", "house", "electro", "ambient-electronic"},
    "acoustic": {"unplugged", "folk", "singer-songwriter", "acoustic-pop"},
    "lofi": {"chill-hop", "lo-fi", "ambient", "indie", "experimental"},
    "classical": {"orchestral", "symphony", "chamber", "baroque", "romantic"},
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def fetch_synonyms_from_thesaurus(word: str) -> Set[str]:
    """
    Fetches synonyms and related words for a given word.
    
    Implementation uses Retrieval-Augmented Generation (RAG) with a two-tier approach:
    1. Primary: Datamuse API for comprehensive online thesaurus data
    2. Fallback: Local curated thesaurus for offline/reliable operation
    
    Args:
        word: The word to find synonyms for (genre or mood)
    
    Returns:
        Set of related words/synonyms
    """
    global _last_api_call
    
    word_lower = word.lower().strip()
    
    # Check cache first
    if word_lower in _thesaurus_cache:
        return _thesaurus_cache[word_lower]
    
    synonyms = set()
    
    # Try online API first (Datamuse)
    try:
        # Rate limiting: ensure minimum delay between API calls
        time.sleep(max(0, _api_call_delay - (time.time() - _last_api_call)))
        _last_api_call = time.time()
        
        # Query Datamuse API for related words (synonyms and similar terms)
        url = f"https://api.datamuse.com/words?rel_syn={word_lower}&max=10"
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            # Extract the 'word' field from each result
            for item in data:
                if 'word' in item:
                    synonyms.add(item['word'].lower())
        
        if synonyms:
            _thesaurus_cache[word_lower] = synonyms
            return synonyms
    
    except requests.exceptions.Timeout:
        pass  # Fall through to local thesaurus
    except Exception as e:
        pass  # Fall through to local thesaurus
    
    # Fallback to local curated thesaurus
    if word_lower in _LOCAL_THESAURUS:
        synonyms = _LOCAL_THESAURUS[word_lower].copy()
    
    # Cache the result (whether from API or local)
    _thesaurus_cache[word_lower] = synonyms
    return synonyms

def is_genre_or_mood_similar(user_term: str, song_term: str) -> bool:
    """
    Checks if two genre/mood terms are similar using thesaurus data.
    
    Args:
        user_term: User's preferred genre/mood
        song_term: Song's genre/mood
    
    Returns:
        True if terms are similar, False otherwise
    """
    user_term = user_term.lower().strip()
    song_term = song_term.lower().strip()
    
    # First check for exact match
    if user_term == song_term:
        return False  # Exact matches handled separately
    
    # Check if song_term is a synonym of user_term
    user_synonyms = fetch_synonyms_from_thesaurus(user_term)
    if song_term in user_synonyms:
        return True
    
    # Check if user_term is a synonym of song_term (bidirectional)
    song_synonyms = fetch_synonyms_from_thesaurus(song_term)
    if user_term in song_synonyms:
        return True
    
    return False

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            song = {}
            for key, value in row.items():
                # Try to convert to int first, then float, otherwise keep as string
                try:
                    if '.' in value:
                        song[key] = float(value)
                    else:
                        song[key] = int(value)
                except ValueError:
                    song[key] = value
            songs.append(song)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Calculate scores for all songs
    scored_songs = [(song, score, reasoning) for song in songs 
                   for score, reasoning in [score_song(user_prefs, song)]]
    
    # Sort by score in descending order and take top k
    top_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]
    
    return top_songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a song based on user preferences with RAG-enhanced thesaurus support.
    Similar genres/moods found via thesaurus receive reduced points.
    Required by tests/test_recommender.py
    """
    score = 0.0
    reasoning = ""
    
    user_genre = user_prefs.get('genre', '').lower().strip()
    song_genre = song.get('genre', '').lower().strip()
    
    # Genre match with RAG support: +2.0 for exact, +1.5 for similar
    if song_genre == user_genre:
        score += 2.0
        reasoning += f"+2.0 for exact genre match ({song['genre']})\n"
    elif is_genre_or_mood_similar(user_genre, song_genre):
        score += 1.5
        reasoning += f"+1.5 for similar genre ({song_genre} is similar to {user_prefs.get('genre')})\n"
    else:
        reasoning += f"+0.0 genre mismatch (user: {user_prefs.get('genre')}, song: {song.get('genre')})\n"
    
    user_mood = user_prefs.get('mood', '').lower().strip()
    song_mood = song.get('mood', '').lower().strip()
    
    # Mood match with RAG support: +1.0 for exact, +0.8 for similar
    if song_mood == user_mood:
        score += 1.0
        reasoning += f"+1.0 for exact mood match ({song['mood']})\n"
    elif is_genre_or_mood_similar(user_mood, song_mood):
        score += 0.8
        reasoning += f"+0.8 for similar mood ({song_mood} is similar to {user_prefs.get('mood')})\n"
    else:
        reasoning += f"+0.0 mood mismatch (user: {user_prefs.get('mood')}, song: {song.get('mood')})\n"
    
    # Energy match: +(1.0 - abs(target_energy - song_energy))
    target_energy = user_prefs.get('energy', 0.5)
    song_energy = song.get('energy', 0.5)
    energy_score = 1.0 - abs(target_energy - song_energy)
    score += energy_score
    reasoning += f"+{energy_score:.2f} for energy match (target: {target_energy}, song: {song_energy})\n"
    
    # Acousticness match
    song_acousticness = song.get('acousticness', 0.5)
    if user_prefs.get('likes_acoustic', False):
        score += song_acousticness
        reasoning += f"+{song_acousticness:.2f} for acousticness (user likes acoustic)\n"
    else:
        acoustic_score = 1.0 - song_acousticness
        score += acoustic_score
        reasoning += f"+{acoustic_score:.2f} for low acousticness (user dislikes acoustic)\n"
    
    reasoning = reasoning.rstrip('\n')
    return score, reasoning
