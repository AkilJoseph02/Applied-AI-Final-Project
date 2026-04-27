# Music Recommender System Diagrams

This directory contains visual documentation of the music recommender system with RAG (Retrieval-Augmented Generation) integration.

## Files

### Markdown Files (for VS Code/GitHub viewing)
### 1. `system_architecture_diagram.md`
**Complete System Architecture**
- Shows the entire music recommender system flow
- From user input through data loading, RAG scoring, to final recommendations
- Includes all components: UI, data layer, recommendation engine, RAG system, and output

### 2. `rag_system_diagram.md`
**RAG System Deep Dive**
- Detailed view of the RAG (Retrieval-Augmented Generation) components
- Shows how the thesaurus lookup works with API and local fallback
- Illustrates scoring logic for exact vs. similar matches
- Includes technical implementation details

### Mermaid Files (for mermaid.live)
### 3. `system_architecture_diagram.mmd`
**Complete System Architecture** (mermaid.live compatible)
- Raw Mermaid markup for the full system diagram
- Ready to paste into [mermaid.live](https://mermaid.live/)

### 4. `rag_system_diagram.mmd`
**RAG System Deep Dive** (mermaid.live compatible)
- Raw Mermaid markup for the RAG system diagram
- Ready to paste into [mermaid.live](https://mermaid.live/)

## How to View the Diagrams

### Option 1: VS Code/GitHub (Markdown files)
1. **VS Code**: Open the `.md` files - diagrams render automatically
2. **GitHub**: Diagrams display when viewing the `.md` files online

### Option 2: Mermaid.live (Raw Mermaid files)
1. Go to [mermaid.live](https://mermaid.live/)
2. Open either `.mmd` file and copy the entire content
3. Paste into the mermaid.live editor
4. The diagram will render instantly

### Option 3: Other Mermaid Viewers
- **Mermaid CLI**: `mmdc -i diagram.mmd -o diagram.png`
- **VS Code Extensions**: Install "Mermaid Preview" extension
- **Online Tools**: Any Mermaid.js compatible renderer

## System Overview

The music recommender uses a RAG-enhanced scoring system that:

- **Exact Matching**: Full points for direct keyword matches
- **Semantic Matching**: Reduced points for thesaurus-similar terms
- **Dual Source**: Online Datamuse API + curated local thesaurus
- **Caching**: Performance optimization for repeated queries
- **Fallback**: Works offline with local thesaurus

### Scoring Examples

| Match Type | Genre Points | Mood Points | Example |
|------------|-------------|-------------|---------|
| Exact Match | +2.0 | +1.0 | "pop" matches "pop" |
| RAG Similar | +1.5 | +0.8 | "chill" matches "relaxed" |
| No Match | +0.0 | +0.0 | "pop" vs "metal" |

## RAG Benefits

1. **Flexible User Input**: Accepts colloquial terms ("chill", "mellow")
2. **Semantic Understanding**: Recognizes related concepts
3. **Offline Capability**: Works without internet connection
4. **Performance**: Caches results to reduce API calls
5. **Reliability**: Graceful degradation when API unavailable

## Technical Details

- **API**: Datamuse API for synonym lookup
- **Fallback**: Curated music-specific thesaurus
- **Caching**: In-memory dictionary with TTL considerations
- **Rate Limiting**: 0.1s delay between API calls
- **Timeout**: 3-second API timeout
- **Language**: Python with Mermaid.js diagrams