#!/usr/bin/env python
"""Demonstration of RAG Thesaurus Integration"""

import sys
sys.path.insert(0, 'src')
from recommender import load_songs, score_song

# Load songs
songs = load_songs('data/songs.csv')
print("="*70)
print("RAG THESAURUS INTEGRATION - DEMONSTRATION")
print("="*70)
print(f"\nDataset: {len(songs)} songs loaded\n")

# Test 1: User prefers 'chill' mood
print("TEST 1: User Prefers 'CHILL' Mood")
print("-" * 70)

user_prefs_chill = {
    'genre': 'pop',
    'mood': 'chill',
    'energy': 0.4,
    'likes_acoustic': True
}

print(f"User Profile: {user_prefs_chill}\n")

# Score all songs and get top recommendations
scores = []
for song in songs:
    score, reasoning = score_song(user_prefs_chill, song)
    scores.append((song, score, reasoning))

scores.sort(key=lambda x: x[1], reverse=True)

print("Top 5 Recommendations:\n")
for i, (song, score, reasoning) in enumerate(scores[:5], 1):
    print(f"{i}. {song['title']} ({song['genre']}/{song['mood']}) - Score: {score:.2f}")
    # Show which points came from mood matching
    if 'exact mood' in reasoning:
        print(f"   ✓ EXACT MOOD MATCH (+1.0 points)")
    elif 'similar mood' in reasoning:
        print(f"   ✓ THESAURUS MOOD MATCH (+0.8 points)")
    # Show which points came from genre matching
    if 'exact genre' in reasoning:
        print(f"   ✓ EXACT GENRE MATCH (+2.0 points)")
    elif 'similar genre' in reasoning:
        print(f"   ✓ THESAURUS GENRE MATCH (+1.5 points)")
    print()

# Test 2: User prefers 'peaceful' mood  
print("\nTEST 2: User Prefers 'PEACEFUL' Mood")
print("-" * 70)

user_prefs_peaceful = {
    'genre': 'ambient',
    'mood': 'peaceful',
    'energy': 0.3,
    'likes_acoustic': True
}

print(f"User Profile: {user_prefs_peaceful}\n")

# Score all songs and get top recommendations
scores2 = []
for song in songs:
    score, reasoning = score_song(user_prefs_peaceful, song)
    scores2.append((song, score, reasoning))

scores2.sort(key=lambda x: x[1], reverse=True)

print("Top 5 Recommendations:\n")
for i, (song, score, reasoning) in enumerate(scores2[:5], 1):
    print(f"{i}. {song['title']} ({song['genre']}/{song['mood']}) - Score: {score:.2f}")
    # Show which points came from mood matching
    if 'exact mood' in reasoning:
        print(f"   ✓ EXACT MOOD MATCH (+1.0 points)")
    elif 'similar mood' in reasoning:
        print(f"   ✓ THESAURUS MOOD MATCH (+0.8 points)")
    # Show which points came from genre matching
    if 'exact genre' in reasoning:
        print(f"   ✓ EXACT GENRE MATCH (+2.0 points)")
    elif 'similar genre' in reasoning:
        print(f"   ✓ THESAURUS GENRE MATCH (+1.5 points)")
    print()

print("="*70)
print("SUMMARY:")
print("- Exact matches: +2.0 (genre) / +1.0 (mood)")
print("- Thesaurus matches: +1.5 (genre) / +0.8 (mood)")
print("- Thesaurus data from Datamuse API with local fallback")
print("="*70)
