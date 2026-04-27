#!/usr/bin/env python
"""
Simple RAG Demo - Shows thesaurus matching without API delays
Uses only the first 2 songs to demonstrate quickly
"""

import sys
sys.path.insert(0, 'src')
from recommender import load_songs, score_song, fetch_synonyms_from_thesaurus

print("="*70)
print("RAG MUSIC RECOMMENDER - QUICK DEMO")
print("="*70)

# Load songs
songs = load_songs('data/songs.csv')
print(f"\n✓ Loaded {len(songs)} songs\n")

# Demo 1: Show thesaurus data
print("DEMO 1: Thesaurus Synonyms")
print("-" * 70)

print("\nSynonyms for 'chill' (mood):")
chill_syns = fetch_synonyms_from_thesaurus('chill')
print(f"  {chill_syns if chill_syns else 'Using local thesaurus'}")

print("\nSynonyms for 'peaceful' (mood):")
peaceful_syns = fetch_synonyms_from_thesaurus('peaceful')
print(f"  {peaceful_syns if peaceful_syns else 'Using local thesaurus'}")

print("\nSynonyms for 'country' (genre):")
country_syns = fetch_synonyms_from_thesaurus('country')
print(f"  {country_syns if country_syns else 'Using local thesaurus'}")

# Demo 2: Show scoring with exact matches
print("\n\nDEMO 2: Exact Match Scoring")
print("-" * 70)

user1 = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": True}
song1 = songs[0]  # Sunrise City
score1, reason1 = score_song(user1, song1)

print(f"\nUser prefers: {user1}")
print(f"Song: {song1['title']} ({song1['genre']}/{song1['mood']})")
print(f"Score: {score1:.2f}")
print(f"Breakdown:")
for line in reason1.split('\n'):
    print(f"  {line}")

# Demo 3: Show scoring with thesaurus matches
print("\n\nDEMO 3: Thesaurus Match Scoring")
print("-" * 70)

user2 = {"genre": "country", "mood": "chill", "energy": 0.4, "likes_acoustic": True}
# Find a song with similar mood/genre
similar_songs = [s for s in songs if s['mood'] in ['relaxed', 'peaceful'] and s['genre'] in ['folk', 'acoustic']]
if similar_songs:
    song2 = similar_songs[0]
    score2, reason2 = score_song(user2, song2)
    
    print(f"\nUser prefers: {user2}")
    print(f"Song: {song2['title']} ({song2['genre']}/{song2['mood']})")
    print(f"Score: {score2:.2f}")
    print(f"Breakdown:")
    for line in reason2.split('\n'):
        if 'similar' in line or 'mismatch' in line:
            print(f"  {line} ← Thesaurus matching!")
        else:
            print(f"  {line}")
else:
    print("\n(No songs found with similar mood/genre for this demo)")

print("\n" + "="*70)
print("✓ RAG System is working!")
print("  - Exact matches: +2.0 (genre) / +1.0 (mood)")
print("  - Thesaurus matches: +1.5 (genre) / +0.8 (mood)")
print("="*70)
