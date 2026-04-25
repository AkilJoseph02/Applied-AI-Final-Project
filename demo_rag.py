#!/usr/bin/env python
"""Demonstration of RAG Thesaurus Integration in Music Recommender"""

import sys
sys.path.insert(0, 'src')

from recommender import load_songs, score_song

print("="*70)
print("RAG-ENHANCED MUSIC RECOMMENDER - THESAURUS DEMONSTRATION")
print("="*70)

# Load songs
songs = load_songs("data/songs.csv")
print(f"\nLoaded {len(songs)} songs from catalog\n")

print("EXAMPLE 1: User prefers 'relaxed' mood (using Thesaurus Matching)")
print("-" * 70)

user_prefs = {
    "genre": "pop",
    "mood": "relaxed",  # Using 'relaxed' instead of exact mood names
    "energy": 0.5,
    "likes_acoustic": True
}

print(f"User Preferences: {user_prefs}\n")

# Score all songs
scored_songs = []
for song in songs:
    score, reasoning = score_song(user_prefs, song)
    scored_songs.append((song, score, reasoning))

# Sort and show top 5
scored_songs.sort(key=lambda x: x[1], reverse=True)

print("Top 5 Recommendations:\n")
for i, (song, score, reasoning) in enumerate(scored_songs[:5], 1):
    print(f"{i}. {song['title']} - Score: {score:.2f}")
    print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
    print(f"   Explanation:")
    for line in reasoning.split('\n'):
        if line.strip():
            print(f"      {line}")
    # Highlight thesaurus matches
    if "similar" in reasoning:
        print("   ✓ Contains THESAURUS MATCH!")
    print()

print("\nEXAMPLE 2: User prefers 'country' genre (using Thesaurus Matching)")
print("-" * 70)

user_prefs2 = {
    "genre": "country",
    "mood": "happy",
    "energy": 0.7,
    "likes_acoustic": False
}

print(f"User Preferences: {user_prefs2}\n")

# Score all songs
scored_songs2 = []
for song in songs:
    score, reasoning = score_song(user_prefs2, song)
    scored_songs2.append((song, score, reasoning))

# Sort and show top 5
scored_songs2.sort(key=lambda x: x[1], reverse=True)

print("Top 5 Recommendations:\n")
for i, (song, score, reasoning) in enumerate(scored_songs2[:5], 1):
    print(f"{i}. {song['title']} - Score: {score:.2f}")
    print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
    print(f"   Explanation:")
    for line in reasoning.split('\n'):
        if line.strip():
            print(f"      {line}")
    # Highlight thesaurus matches
    if "similar" in reasoning:
        print("   ✓ Contains THESAURUS MATCH!")
    print()

print("="*70)
print("RAG System Summary:")
print("- Exact matches: +2.0 (genre) / +1.0 (mood)")
print("- Thesaurus matches: +1.5 (genre) / +0.8 (mood)")
print("- Thesaurus data sourced from Datamuse API with local fallback")
print("="*70)
