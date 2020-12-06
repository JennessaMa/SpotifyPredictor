import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import configparser

const NUM_FEATURES = 11

#AUTHENTICATION PROCESS
cid = "6cf836da1edc44bf9d696846615b1083"
secret = "71176dc8eef847d08b3efa4ddaea6566"
username = "jennessa.ma"
redirect_uri = "https://www.google.ca/"
scope = 'user-library-read playlist-read-private'

token = spotipy.SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope, cache_path=".cache-jennessa.ma", username=username)
sp = spotipy.Spotify(auth_manager=token)

#------------------------------------------------------------------------------#

#HELPER FUNCTIONS
#passes in 2 arrays containing audio features of 2 songs
#returns a similarity value
def getDotProd(vector1, vector2):
    product = 1;
    for i in range(NUM_FEATURES):
        product += (vector1[i] * vector2[i])
    return product

#passes in a list of uris
#returns a dictionary that maps a uri key to an array of features {song_uri : [features]}
def getAudioFeatures(uri_list):
    artists = []
    tracks = []
    danceability = []
    energy = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []

    for uri in uri_list:
        features = sp.audio_features(uri)
        track = sp.track(uri)
        tracks.append(track["name"])
        artists.append(track["album"]["artists"][0]["name"])
        for f in features:
            danceability.append(f['danceability'])
            energy.append(f['energy'])
            key.append(f['key'])
            loudness.append(f['loudness'])
            mode.append(f['mode'])
            speechiness.append(f['speechiness'])
            acousticness.append(f['acousticness'])
            instrumentalness.append(f['instrumentalness'])
            liveness.append(f['liveness'])
            valence.append(f['valence'])
            tempo.append(f['tempo'])

    return {"danceability": danceability, "energy": energy, "key": key, "loudness": loudness, "mode": mode, "speechiness": speechiness,
            "acousticness": acousticness, "instrumentalness": instrumentalness, "liveness": liveness, "valence" : valence, "tempo": tempo}
#------------------------------------------------------------------------------#

#RETRIEVING NECESSARY PLAYLISTS
results = sp.user_playlists("jennessa.ma")
#lists out my playlists
for i, item in enumerate(results['items']):
    print("%d %s" % (i, item['name']))

currents_uri = "spotify:playlist:0FuxVY5atFaK4wH1aNBcxT"
top_songs_uri = "spotify:playlist:37i9dQZF1ELXs5U1shc3bl"
#top_songs_uri = results['items'][2]['uri']

currents = sp.playlist(currents_uri)
top_songs = sp.playlist(top_songs_uri)
missed_hits = sp.playlist("spotify:playlist:37i9dQZF1EOf3ucP0DhFZL")
daily_mix1 = sp.playlist("spotify:playlist:37i9dQZF1E379IN8ESLjEh")

current_tracks = currents["tracks"]["items"]
top_songs_tracks = top_songs["tracks"]["items"]
missed_hits_tracks = missed_hits["tracks"]["items"]
daily_mix_tracks = daily_mix1["tracks"]["items"]

#get the song namne and its uri to extract data from
# print(current_tracks[0]["track"]["uri"])
# print(current_tracks[0]["track"]["name"])

num_top_tracks = len(top_songs_tracks)
top_songs_uris = []
for i in range(num_top_tracks):
    top_songs_uris.append(top_songs_tracks[i]["track"]["uri"])

num_missed_hits = len(missed_hits_tracks)
missed_hits_uris = []
for i in range(num_missed_hits):
    missed_hits_uris.append(missed_hits_tracks[i]["track"]["uri"])

num_daily_tracks = len(daily_mix_tracks)
daily_mix_uris = []
for i in range(num_daily_tracks):
    daily_mix_uris.append(daily_mix_tracks[i]["track"]["uri"])

test_uris = missed_hits_uris + daily_mix_uris

test_songs_dict = getAudioFeatures(test_uris)
top_songs_dict = getAudioFeatures(top_songs_uri[:80])



# avg_dance = sum(danceability) / num_top_tracks
# avg_energy = sum(energy) / num_top_tracks
# avg_key = sum(key) / num_top_tracks
# avg_loudness = sum(loudness) / num_top_tracks
# avg_mode = sum(mode) / num_top_tracks
# avg_speech = sum(speechiness) / num_top_tracks
# avg_acoust = sum(acousticness) / num_top_tracks
# avg_instr = sum(instrumentalness) / num_top_tracks
# avg_live = sum(liveness) / num_top_tracks
# avg_val = sum(valence) / num_top_tracks
# avg_tempo = sum(tempo) / num_top_tracks
#
# print("average danceability: " + str(avg_dance))
# print("average energy: " + str(avg_energy))
# print("average loudness: " + str(avg_loudness))
# print("average sppechiness: " + str(avg_speech))
# print("average acousticness: " + str(avg_acoust))
# print("average instrumentalness: " + str(avg_instr))
# print("average liveness: " + str(avg_live))
# print("average valence: " + str(avg_val))
# print("average tempo: " + str(avg_tempo))
