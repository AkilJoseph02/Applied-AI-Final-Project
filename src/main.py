"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded Songs: {len(songs)}")

    #Input your user preferences here for testing
    user_prefs = {"genre": "", "mood": "", "energy": 0, "likes_acoustic": False}

    user_prefs["genre"] = input("Enter preferred genre (e.g., pop, rock, jazz): ").strip()
    user_prefs["mood"] = input("Enter preferred mood (e.g., happy, relaxed, energetic): ").strip()

    energy_answered = False
    while (not energy_answered):
        user_prefs["energy"] = float(input("Enter preferred energy level (0.0 to 1.0): ").strip())
        if 0.0 <= user_prefs["energy"] <= 1.0:
            energy_answered = True
        else:
            print("Please enter a valid energy level between 0.0 and 1.0.")
    
    accoustic_answered = False
    while (not accoustic_answered):
        acoustic_pref = input("Do you like acoustic songs? (yes/no): ").strip().lower()
        if acoustic_pref in ['yes']:
            user_prefs["likes_acoustic"] = True
            accoustic_answered = True
        elif acoustic_pref in ['no']:
            user_prefs["likes_acoustic"] = False
            accoustic_answered = True
        else:
            print("Please answer 'yes' or 'no' for acoustic preference.")

    recommend_num = int(input("How many recommendations would you like? (e.g., 5): ").strip())

    recommendations = recommend_songs(user_prefs, songs, k=recommend_num)


    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: \n{explanation}")
        print()

if __name__ == "__main__":
    main()
