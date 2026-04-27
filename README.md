## Title and Summary: What your project does and why it matters.
Original Project is from Show 3: Music Recommender

Original Purpose: Given a user profile that composed of a Favorite Genre, Favorite Mood, Target Energy, and if the user liked acoustics: the Music Recommender would the top 5 songs out of a catalog of songs (songs.csv) that would most likely appeal to the user by how close the song's aspects are to the user's preferences.

Updated Project: Uses a RAG implementation in the genre/mood matching part of the music recommendation system. Will either use the Datamuse online API thesaurus or a local fallback thesaurus (depends if the Datamuse API is unavailable) to determine if the mood or genre of a song in the catalogue is synonymous with the mood/genre the user prefers. If so, because the match isn't exactly accurate, the recommeder will give reduced points (+1.5 instead of +2.0 for genre, +0.8 instead of +1.0 for mood). Now allows the user to create their own profile for the recommender to work on.

## Architecture Overview: A short explanation of your system diagram.
User gives their input in the terminal after executing Main.py (favorite genre/mood, if they like acoustics in their music, what's their preferred energy, how many songs they want recommended, etc). This input creates a profile for the user. Then, main.py loads up the catalogue located in data/songs.csv and calls on the recommendation function from the recommender.py file to score and rank each song up the number of song recommendations the user wants.

With the update to the system using RAG, if the recommender notices that a song's genre or mood matches with the user's preference based on their profile, it will give the song a number of points, +2 for genre match, +1 for mood match. Songs will get points based on the difference between their energy and the target energy on the profile, and the amount/lack of acoustics depending on if the user likes acoustics.

RAG becomes a part of the equation if there isn't an exact match for genres or moods. If so, the recommender will either use an online API (Datamuse) thesaurus or a local fallback thesaurus to determine if the song's genre or mood are somewhat similiar to the user's preferences. RAG parses through the thesaurus and returns a list of synonyms for the user's preferred genre or mood, and if any of those synonyms are the song's mood or genre, then give the song a reduced number of points in the recommendation system (+1.5 points for similar genres, +0.8 points for similar moods). If not, the mood/genre don't match and no points will be given for mood/genre mismatch.

After scoring every song within the songs.csv file, each with explanations for why they received/didn't receive points, rank them up to k places for the amount of song the user wanted recommended to them, highest to lowest.

## Setup Instructions: Step-by-step directions to run your code.
1. Install the required libraries labeled in requirements.txt using the following command:
pip install -r requirements.txt
2. Open terminal and change directory to "Applied-AI-Final-Project"
3. Run the code by using executing the following command in the console:
python src/main.py
4. Follow the instructions printed on the terminal to generate your user profile and specify how many songs you want recommended to you.
5. Wait a couple of seconds, implementing RAG for the similar genre/mood matches increased the runtime of the program (accessing the APIs, parsing the JSON, etc.)

## Sample Interactions: Include at least 2-3 examples of inputs and the resulting AI outputs to demonstrate the system is functional.


## Design Decisions: Why you built it this way, and what trade-offs you made.

## Testing Summary: What worked, what didn't, and what you learned.

## Reflection: What this project taught you about AI and problem-solving.

## Link to Loom Presentation:
