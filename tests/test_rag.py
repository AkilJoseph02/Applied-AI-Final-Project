#!/usr/bin/env python
"""Quick test of RAG thesaurus functionality"""

import sys
sys.path.insert(0, 'src')

from recommender import fetch_synonyms_from_thesaurus, is_genre_or_mood_similar

print("Testing RAG Thesaurus Integration\n" + "="*50)

# Test 1: Fetch synonyms for 'chill'
print("\nTest 1: Fetching synonyms for 'chill'...")
chill_synonyms = fetch_synonyms_from_thesaurus('chill')
print(f"Synonyms for 'chill': {chill_synonyms}")

# Test 2: Check if 'relaxed' is similar to 'chill'
print("\nTest 2: Is 'relaxed' similar to 'chill'?")
is_similar = is_genre_or_mood_similar('chill', 'relaxed')
print(f"Result: {is_similar}")

# Test 3: Check if 'lounge' is similar to 'chill'
print("\nTest 3: Is 'lounge' similar to 'chill'?")
is_similar = is_genre_or_mood_similar('chill', 'lounge')
print(f"Result: {is_similar}")

# Test 4: Fetch synonyms for 'country'
print("\nTest 4: Fetching synonyms for 'country' (genre)...")
country_synonyms = fetch_synonyms_from_thesaurus('country')
print(f"Synonyms for 'country': {country_synonyms}")

# Test 5: Check if 'western' is similar to 'country'
print("\nTest 5: Is 'western' similar to 'country'?")
is_similar = is_genre_or_mood_similar('country', 'western')
print(f"Result: {is_similar}")

print("\n" + "="*50)
print("RAG Thesaurus tests complete!")
