#!/usr/bin/env python
"""Test RAG system with genre/mood similarity matching"""

import sys
sys.path.insert(0, 'src')

from recommender import load_songs, score_song, fetch_synonyms_from_thesaurus, is_genre_or_mood_similar

print("="*60)
print("RAG THESAURUS INTEGRATION TEST")
print("="*60)

# Load songs
songs = load_songs("data/songs.csv")
print(f"\nLoaded {len(songs)} songs from catalog\n")

# Test thesaurus similarity
print("TEST 1: Thesaurus Similarity Detection")
print("-" * 60)

print("\n1a. Testing mood similarity (chill vs relaxed):")
chill_syns = fetch_synonyms_from_thesaurus('chill')
print(f"   Synonyms for 'chill': {chill_syns if chill_syns else 'None found'}")

print("\n1b. Testing mood similarity (calm vs relaxed):")
calm_syns = fetch_synonyms_from_thesaurus('calm')
print(f"   Synonyms for 'calm': {calm_syns if calm_syns else 'None found'}")

print("\n1c. Testing genre similarity (country vs western):")
country_syns = fetch_synonyms_from_thesaurus('country')
print(f"   Synonyms for 'country': {country_syns if country_syns else 'None found'}")

# Test scoring with exact matches
print("\n\nTEST 2: Scoring Examples - Exact Matches")
print("-" * 60)

user_prefs_pop = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": True}
print(f"\nUser Profile: {user_prefs_pop}\n")

# Find songs that exactly match
exact_matches = [s for s in songs if s.get('genre', '').lower() == 'pop' and s.get('mood', '').lower() == 'happy']
print(f"Found {len(exact_matches)} songs with exact genre+mood match:\n")
for song in exact_matches[:3]:
    score, reasoning = score_song(user_prefs_pop, song)
    print(f"Song: {song['title']}")
    print(f"Score: {score:.2f}")
    print(f"Reasoning:\n{reasoning}\n")

# Test with moods that should find similar matches
print("\nTEST 3: Scoring with Similar Moods (Using Thesaurus)")
print("-" * 60)

user_prefs_relaxed = {"genre": "pop", "mood": "relaxed", "energy": 0.5, "likes_acoustic": True}
print(f"\nUser Profile: {user_prefs_relaxed}")
print("(Note: Looking for 'relaxed' mood - should find similar moods like 'peaceful', 'calm', etc.)\n")

# Score all songs and show top 5
all_scores = [(song, score, reasoning) for song in songs 
              for score, reasoning in [score_song(user_prefs_relaxed, song)]]
all_scores.sort(key=lambda x: x[1], reverse=True)

print("Top 5 recommendations:")
for i, (song, score, reasoning) in enumerate(all_scores[:5], 1):
    print(f"\n{i}. {song['title']} - Score: {score:.2f}")
    print(f"   Genre: {song.get('genre')} | Mood: {song.get('mood')}")
    if "similar" in reasoning:
        print(f"   ✓ HAS SIMILAR MATCH (Thesaurus Match!)")
    reasoning_lines = reasoning.split('\n')
    for line in reasoning_lines:
        if 'similar' in line or '+0.8' in line:
            print(f"   {line}")

print("\n" + "="*60)
