import sys
sys.path.insert(0, 'src')
from recommender import load_songs, score_song

songs = load_songs('data/songs.csv')
print(f'Loaded {len(songs)} songs')

user_prefs = {'genre': 'pop', 'mood': 'relaxed', 'energy': 0.5, 'likes_acoustic': True}
song = songs[0]
score, reasoning = score_song(user_prefs, song)
print(f'Song: {song["title"]}')
print(f'Score: {score}')
print(f'Reasoning:\n{reasoning}')
