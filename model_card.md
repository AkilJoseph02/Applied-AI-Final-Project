# Reflections:

## What are the limitations or biases in your system?
Runtime has been increased greatly due to fetching the API and parsing the info within the thesaurus. There could be biases within the thesaures (both online and local) that could affect the reliability of the genre/mood similarities.

## Could your AI be misused, and how would you prevent that?
AI needs more validation to make sure the results of the recommender are genuinely helpful for the user. Song catalogues weighted more towards a certain genre or mood could skew results, giving the user recommendations they're not into. Also, if the results from the RAG lookup are stored in an insecure, they could be used by malicious parties to study user behavior, so increased security is also a must.

## What surprised you while testing your AI's reliability?
Mostly when it comes to similarity testing. I'd figure moods like sad and contemplative would have a similarity, but the system considered it a mismatch. Also realized that if similarity matches are found, energy matches and acousticness will carry the recommendation. May cause issues if a catalogue shows a bias towards a genre or mood that the user isn't particularly fond of.

## Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.
AI created the suggestion of utilizing 2 libraries for the thesaures, an online one from Datamuse that will be used by default, and a local thesaurus in case the online one is unavailable. AI provided another layer of reliability was incredibly helpful and genius.

AI didn't give me a flawed suggestion, implementation of RAG was thankfully clean and robust with testing.