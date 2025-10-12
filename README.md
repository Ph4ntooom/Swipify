# Swipify: Discover Music, One Swipe at a Time

Swipify is a web application built to solve the problem of music discovery in an engaging and interactive way. While streaming services offer millions of tracks, finding new music that truly matches your taste can be challenging. Swipify tackles this with a "Tinder-for-music" interface, allowing users to actively teach the recommendation algorithm their preferences.

The system starts by analyzing a user's 50 most recently played songs and then uses a content-based filtering model to suggest new tracks. With every swipe, the user's taste profile is refined, leading to increasingly accurate and personalized recommendations.

## ✨ Core Features
*   **Tinder-Style Swipe Interface:** An intuitive and fun way to rate songs (Right = Like, Left = Dislike).
*   **Real-Time Recommendation Engine:** The algorithm adapts and refines its suggestions based on your immediate feedback.
*   **Personalized "Liked Songs" Playlist:** All the songs you swipe right on are automatically added to a custom playlist in your Spotify account.
*   **Mood-Based Filtering:** Discover music that matches your current vibe, with curated suggestions for "Happy," "Chill," or "Energetic" moods.

## 🛠️ Technology Stack
*   **Backend:** Python, Flask, Spotipy (Spotify API Client)
*   **Machine Learning:** Scikit-learn, Pandas, NumPy
*   **Frontend:** React.js
*   **Data Source:** Spotify Web API
