import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="", # Add your id and secret
    client_secret="",
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-modify-public"
))

# Function to create a new playlist
def create_playlist(sp, playlist_name, description=""):
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=description)
    return playlist["id"]

# Function to search for a song and return the best match
def search_song(sp, song_title):
    results = sp.search(q=song_title, limit=1, type='track')
    tracks = results['tracks']['items']
    return tracks[0]['id'] if tracks else None

# Function to add a list of song IDs to a playlist
def add_songs_to_playlist(sp, playlist_id, song_ids):
    # Break the song_ids list into chunks of 100
    for i in range(0, len(song_ids), 100):
        chunk = song_ids[i:i + 100]
        sp.playlist_add_items(playlist_id, chunk)
        
# Main function
def main():
    # Load song list from file
    with open("songs.txt", "r") as file:
        song_titles = [line.strip() for line in file if line.strip()]
    
    # Create a new playlist
    playlist_id = create_playlist(sp, "My Playlist from Text File", description="Auto-generated playlist")
    
    # Search for each song and collect track IDs
    song_ids = []
    for title in song_titles:
        track_id = search_song(sp, title)
        if track_id:
            song_ids.append(track_id)
        else:
            print(f"Song '{title}' not found on Spotify.")
    
    # Add found songs to the playlist
    if song_ids:
        add_songs_to_playlist(sp, playlist_id, song_ids)
        print("Playlist created and songs added successfully!")
    else:
        print("No songs found to add.")

if __name__ == "__main__":
    main()

