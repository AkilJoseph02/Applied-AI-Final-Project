# RAG-Enhanced Music Recommender System

## Overview

This document describes the Retrieval-Augmented Generation (RAG) system integrated into your music recommender. The RAG system uses online and offline thesaurus data to find semantically similar genres and moods, enabling more flexible and intelligent recommendations.

## How It Works

### Scoring System with Thesaurus Integration

The recommender now uses a two-tier scoring system:

#### Exact Matches (Direct Alignment)
- **Genre Match**: +2.0 points
- **Mood Match**: +1.0 point

#### Thesaurus-Based Similar Matches (Semantic Alignment)
- **Similar Genre**: +1.5 points (found via thesaurus)
- **Similar Mood**: +0.8 points (found via thesaurus)

### Example Scenario

If a user prefers the **"country"** genre, the system will:
1. Give +2.0 points to songs labeled "country"
2. Give +1.5 points to songs labeled with genres like "western", "americana", "folk-country", or "country-pop" (found via thesaurus)

Similarly, if a user prefers the **"chill"** mood:
1. Give +1.0 point to songs labeled "chill"
2. Give +0.8 points to songs labeled "relaxed", "peaceful", "lounge", or "laid-back"

## Implementation Details

### Architecture

The RAG system consists of three main components:

#### 1. **Datamuse API Integration (Primary)**
```python
fetch_synonyms_from_thesaurus(word: str) -> Set[str]
```
- Queries the free Datamuse API for synonyms and related words
- Uses endpoint: `https://api.datamuse.com/words?rel_syn={word}&max=10`
- Includes rate limiting (0.1 second delay between calls) to respect API limits
- Caches results to avoid repeated API calls

#### 2. **Local Fallback Thesaurus (Secondary)**
```python
_LOCAL_THESAURUS = {
    "mood": {"synonym1", "synonym2", ...},
    "genre": {"synonym1", "synonym2", ...}
}
```
- Curated dictionary of mood and genre synonyms
- Used when the online API is unavailable or times out
- Ensures system reliability even without internet connectivity

#### 3. **Similarity Detection**
```python
is_genre_or_mood_similar(user_term: str, song_term: str) -> bool
```
- Checks bidirectional similarity (A→B and B→A)
- Returns True if terms are synonymous via thesaurus
- Excludes exact matches (handled separately in scoring)

### Data Flow

```
User Profile (mood: "chill", genre: "country")
        ↓
load_songs() [Load 20 songs from CSV]
        ↓
For each song:
  1. Check exact genre match → +2.0 or check similar → +1.5
  2. Check exact mood match → +1.0 or check similar → +0.8
  3. Check energy match → +(1.0 - |target - song|)
  4. Check acousticness preference
        ↓
Score each song
        ↓
Sort by score (descending)
        ↓
Return top K recommendations
```

## Usage

### Basic Usage

```python
from recommender import load_songs, recommend_songs

# Load songs
songs = load_songs("data/songs.csv")

# Create user preference profile
user_prefs = {
    "genre": "country",        # Will match "country" AND "western", "americana", etc.
    "mood": "chill",           # Will match "chill" AND "relaxed", "peaceful", etc.
    "energy": 0.6,             # 0.0 (calm) to 1.0 (energetic)
    "likes_acoustic": True     # True or False
}

# Get top 5 recommendations
recommendations = recommend_songs(user_prefs, songs, k=5)

# Display results
for song, score, explanation in recommendations:
    print(f"{song['title']} - Score: {score:.2f}")
    print(f"Because: {explanation}")
```

### Testing the RAG System

Run the included test scripts:

```bash
# Test basic thesaurus functionality
python test_minimal.py

# Test with sample songs
python quick_test.py

# Full demonstration with multiple profiles
python demo_rag_final.py
```

## Benefits of RAG Integration

1. **Flexible User Preferences**: Users can use colloquial terms ("chill", "mellow", "groovy") without exact matches
2. **Semantic Understanding**: System understands mood/genre relationships (e.g., "calm" and "peaceful" are similar)
3. **Reduced Cold-Start Problem**: New or rare genres/moods can find similar songs
4. **Graceful Degradation**: Falls back to local thesaurus if online API is unavailable
5. **Reduced Points for Approximations**: Thesaurus matches score slightly lower than exact matches, maintaining preference for exact user preferences

## Thesaurus Data Sources

### Online (Primary)
- **Service**: Datamuse API
- **Endpoint**: `https://api.datamuse.com/words?rel_syn={word}`
- **Features**: Free, no authentication, comprehensive synonym database
- **Rate Limit**: Reasonable for this use case (0.1s minimum between calls)

### Local (Fallback)
Curated mappings for music-specific moods and genres:

**Sample Mood Mappings:**
- chill ↔ relaxed, peaceful, lounge, laid-back, mellow
- happy ↔ cheerful, upbeat, joyful, bright, positive
- romantic ↔ intimate, sensual, sweet, dreamy, sentimental

**Sample Genre Mappings:**
- country ↔ western, americana, folk-country, country-pop
- rock ↔ alternative, indie, punk, classic rock
- electronic ↔ edm, synth, techno, house

## Error Handling

The system is robust against API failures:

```python
try:
    # Try online Datamuse API
    response = requests.get(url, timeout=3)
except requests.exceptions.Timeout:
    # Fall back to local thesaurus
    use_local_thesaurus()
except Exception:
    # Gracefully handle any error
    use_local_thesaurus()
```

## Performance Considerations

- **API Calls**: Cached after first fetch to avoid repeated requests
- **Rate Limiting**: 0.1 second minimum delay between API calls
- **Timeout**: 3-second timeout per API call to prevent hanging
- **Local Fallback**: Instant lookup with no network dependency

## Limitations

1. **Thesaurus Coverage**: Not all possible moods/genres are mapped
   - Solution: Can extend `_LOCAL_THESAURUS` with more mappings

2. **Context Sensitivity**: Thesaurus doesn't understand context
   - Example: "cool" in music means different things than temperature cool
   - Mitigation: Local thesaurus uses music-specific synonyms

3. **Single Language**: Currently only supports English terms
   - Future: Could add multilingual support

4. **No User Feedback**: Doesn't learn from user preferences over time
   - Future: Could track which thesaurus matches users like

## Future Improvements

1. **Add User Feedback Loop**: Learn which thesaurus matches users prefer
2. **Expand Local Thesaurus**: Add more music-specific mood/genre synonyms
3. **Implement Semantic Similarity**: Use word embeddings (Word2Vec, BERT) for more accurate similarity
4. **Multi-Language Support**: Extend to Spanish, French, etc.
5. **Artist Similarity**: Find similar artists using same RAG approach
6. **Nested Genres**: Handle compound genres ("indie pop", "country rock", "folk metal")

## Technical Specifications

- **Language**: Python 3.7+
- **Dependencies**: `requests` (for API calls)
- **API**: Datamuse API (free, public)
- **Cache**: In-memory dictionary
- **Response Time**: ~0.1-0.5 seconds per recommendation (with API calls)

## Files Modified

1. **src/recommender.py**
   - Added: `fetch_synonyms_from_thesaurus()`
   - Added: `is_genre_or_mood_similar()`
   - Added: `_LOCAL_THESAURUS` dictionary
   - Modified: `score_song()` to use thesaurus matching
   - Modified: `is_genre_or_mood_similar()` helper

2. **requirements.txt**
   - Added: `requests` library

## Testing Results

✓ Datamuse API Integration Working
✓ Local Fallback Thesaurus Working
✓ Bidirectional Similarity Matching Working
✓ Scoring with Reduced Points Working
✓ Caching and Rate Limiting Working

---

**Last Updated**: April 2026
**RAG System Version**: 1.0
