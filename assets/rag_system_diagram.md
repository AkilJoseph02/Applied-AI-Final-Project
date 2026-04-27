# RAG System Architecture - Detailed Implementation

```mermaid
graph TD
    %% Main Flow
    A[User Input] --> B[main.py]
    B --> C[load_songs()]
    C --> D[recommend_songs()]
    D --> E[score_song() for each song]
    E --> F[RAG-Enhanced Scoring]

    %% RAG System Focus
    F --> G{Genre Matching}
    F --> H{Mood Matching}

    G --> I[Exact Match?]
    I -->|Yes| J[+2.0 points]
    I -->|No| K[is_genre_or_mood_similar()]

    H --> L[Exact Match?]
    L -->|Yes| M[+1.0 points]
    L -->|No| N[is_genre_or_mood_similar()]

    K --> O[fetch_synonyms_from_thesaurus()]
    N --> O

    %% RAG Implementation Details
    O --> P{API Available?}
    P -->|Yes| Q[Datamuse API Call]
    Q --> R[https://api.datamuse.com/words?rel_syn=word]
    R --> S[Parse JSON Response]
    S --> T[Extract Synonyms]
    T --> U[Cache Results]

    P -->|No| V[Local Thesaurus Fallback]
    V --> W[_LOCAL_THESAURUS Dictionary]
    W --> X[Music-Specific Synonyms]
    X --> Y[Cache Results]

    U --> Z[Return Synonym Set]
    Y --> Z

    Z --> AA{Is song_term in synonyms?}
    AA -->|Yes| AB[Similar Match Found]
    AA -->|No| AC[No Similarity]

    AB --> AD{Genre or Mood?}
    AD -->|Genre| AE[+1.5 points]
    AD -->|Mood| AF[+0.8 points]

    AC --> AG[+0.0 points]

    %% Scoring Completion
    J --> AH[Total Score Calculation]
    AE --> AH
    AF --> AH
    AG --> AH

    AH --> AI[Generate Explanation]
    AI --> AJ[Sort & Return Top K]

    %% Styling
    classDef ragCore fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef apiCall fill:#e8f5e8,stroke:#2e7d32
    classDef localFallback fill:#fce4ec,stroke:#c2185b
    classDef scoring fill:#e1f5fe,stroke:#0277bd

    class O,P,Q,R,S,T,U ragCore
    class V,W,X,Y localFallback
    class G,H,I,J,K,L,M,N,AA,AB,AC,AD,AE,AF,AG,AH,AI,AJ scoring
```

## RAG System Deep Dive

This diagram provides a detailed view of the RAG (Retrieval-Augmented Generation) system implementation within the music recommender.

### RAG Architecture Overview:

The RAG system enhances the basic keyword matching by finding semantically similar genres and moods using a thesaurus approach.

### Core Functions:

#### 1. `is_genre_or_mood_similar(user_term, song_term)`
- Checks if two terms are similar via thesaurus lookup
- Returns `False` for exact matches (handled separately)
- Returns `True` if terms are found in each other's synonym sets

#### 2. `fetch_synonyms_from_thesaurus(word)`
- **Primary**: Queries Datamuse API for synonyms
- **Fallback**: Uses local curated thesaurus
- **Caching**: Results cached to avoid repeated calls
- **Rate Limiting**: 0.1s delay between API calls

### Data Sources:

#### Online API (Primary):
- **Service**: Datamuse API
- **Endpoint**: `https://api.datamuse.com/words?rel_syn={word}&max=10`
- **Response**: JSON with synonym words
- **Timeout**: 3 seconds
- **Caching**: In-memory dictionary

#### Local Thesaurus (Fallback):
```python
_LOCAL_THESAURUS = {
    "chill": {"relaxed", "lounge", "laid-back", "mellow", "calm", "peaceful"},
    "country": {"western", "folk", "americana", "country-pop", "blue-grass"},
    # ... more curated music-specific synonyms
}
```

### Scoring Logic:

| Match Type | Genre Points | Mood Points | Example |
|------------|-------------|-------------|---------|
| Exact Match | +2.0 | +1.0 | "pop" → "pop" |
| RAG Similar | +1.5 | +0.8 | "chill" → "relaxed" |
| No Match | +0.0 | +0.0 | "pop" → "metal" |

### Flow Explanation:

1. **Input**: User preferences (genre/mood) and song attributes
2. **Exact Check**: Direct string comparison
3. **RAG Lookup**: If no exact match, query thesaurus
4. **API Priority**: Try online API first, fall back to local
5. **Similarity Check**: See if song term exists in user term's synonyms
6. **Scoring**: Apply reduced points for similar matches
7. **Caching**: Store results for future lookups

### Performance Features:

- **Caching**: `_thesaurus_cache` dictionary prevents repeated API calls
- **Rate Limiting**: `_api_call_delay` prevents API abuse
- **Timeout Handling**: API calls timeout after 3 seconds
- **Graceful Fallback**: System works without internet
- **Bidirectional Search**: Checks both term directions

### Example Scenarios:

#### Scenario 1: User likes "chill" mood
- Exact match: "chill" song → +1.0 points
- RAG match: "relaxed" song → +0.8 points (found via thesaurus)
- No match: "aggressive" song → +0.0 points

#### Scenario 2: User likes "country" genre
- Exact match: "country" song → +2.0 points
- RAG match: "western" song → +1.5 points (found via thesaurus)
- No match: "electronic" song → +0.0 points

### Benefits:

1. **Semantic Understanding**: Recognizes related terms
2. **Flexible Matching**: Users can use colloquial terms
3. **Offline Capability**: Works without internet
4. **Performance**: Caching reduces API calls
5. **Reliability**: Local fallback ensures functionality

### Technical Implementation:

- **Language**: Python 3.7+
- **Dependencies**: `requests` for API calls
- **Caching**: In-memory dictionary
- **Threading**: Single-threaded with rate limiting
- **Error Handling**: Graceful API failure handling