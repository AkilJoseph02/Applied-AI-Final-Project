# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0** 
Answer: Recommend-From-A-Friend 


---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

Answer: The recommeder is mostly for people that have a specific preference for music to find more music they can enjoy. Probably won't help someone branch out of their norms, though. If a person likes high energy songs (often done in pop), then it can be assumed that the user is energetic. If a profile prefers relaxed and calm music, the user is a more laid back person.

Mostly done for classroom exploration.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.
Answer: If a song's genre matches with a profile's favorite genre, then the song gets 2 points. If the mood matches, the songs gets 1 point. The difference between a profile's preferred energy and a song's energy is subtracted by 1 to get the points for energy. If a profile mentions that the user like acoustics in their music, then the song will get point based on the amount of acoustics it has. If the user DOESN'T like acoustics, the song will lose points based on the amount of accoustics it has.

Compared to the initial design, the song's artist is NEVER used or referenced. Still could be useful in recommedation.
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  
Answer: There are 20 songs in the catalog, with the following genres: Pop, Lofi, Rock, Ambient, Jazz, Electronic, Classical, Folk, Hip-Hop, Blues, Reggae, Soul, and Metal. Following Moods: Intense, Happy, Moody, Sad, Romantic, Relaxed, and Aggressive. Missing EDM and Dubstep as genres.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

Answer: Recommmending songs that match a profile's favorite genre and mood. Correctly calculated the amount of points a song recommedation would receive based on the energy and acousticness.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Answer: Dataset doesn't contain any rock songs, so the first test mostly focused on recommending songs that lacked accoustics had high energy. If moods and genres dont match at all for a profile, energy and accoustics will be the only defining characteristics for a recommedation.

Issues when it comes to dealing with moods that are synomymous with each other. For example, most would think that relaxed and calm mean the same thing, so profiles that list "calm" as their preferred mood for songs would still have song labeled as "relaxes" recommended to them. However, the current implementation doesn't take synonyms into account. So a song labeled as "relaxing" would NOT get recommended.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.
Answers: I checked for the following profiles:
    1. Regular profile that liked happy, acoustic, high energy pop songs
    2. High Energy + Sad Mood
    3. Low Energy + Intense Mood (Contradictory energy and mood)
    4. Acoustic Preference + High Energy (Edge Case: Acoustic songs are often mellow)
    5. Non-Acoustic Preference + Low Energy (Edge Case: Non-acoustic songs are often energetic)
    6. Extreme Energy Mismatch (Adversarial: Very high energy with calm mood)
    7. No Genre/Mood Matches (Edge Case: Rare or nonexistent preferences)

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Answer: Think up a way to factor in the artists behind the songs (If a profile has a favorite artist, the recommeder would not only recommend other songs from said artist, but also determine the genre said artist often dabbles in and recommend other artist if they indulge in similar genres or have similar moods). Figure out how check for moods and genres that are similar/synomymous with each other (ex: pop/chart/popular for genre and relaxed/calm for moods).

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Answer: There are alot more factors involved when it comes to accurately and efficiently recommending songs to people of either vague or specific tastes.
