#!/usr/bin/env python
"""Minimal RAG test - tests only the thesaurus API"""

import sys
sys.path.insert(0, 'src')

from recommender import fetch_synonyms_from_thesaurus, is_genre_or_mood_similar

print("Testing Datamuse API for Synonyms\n")

# Test 1: Direct API call
print("1. Fetching synonyms for 'relaxed'...")
try:
    synonyms = fetch_synonyms_from_thesaurus('relaxed')
    print(f"   Result: {list(synonyms)[:5]}")  # Show first 5
    print(f"   Total found: {len(synonyms)}")
except Exception as e:
    print(f"   Error: {e}")

print("\n2. Testing if 'calm' is similar to 'relaxed'...")
try:
    result = is_genre_or_mood_similar('relaxed', 'calm')
    print(f"   Result: {result}")
except Exception as e:
    print(f"   Error: {e}")

print("\n3. Testing if 'peaceful' is similar to 'calm'...")
try:
    result = is_genre_or_mood_similar('calm', 'peaceful')
    print(f"   Result: {result}")
except Exception as e:
    print(f"   Error: {e}")

print("\nTest complete!")
