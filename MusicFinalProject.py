import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import configparser
import math

#CONSTANTS
NUM_FEATURES = 11
NUM_SONGS = 79
THRESHOLD = 0.9966892120292986 #taken from a song I decided was really good in the "missed hits"

#AUTHENTICATION PROCESS
cid = #[REDACTED]
secret = #[REDACTED]
username = "jennessa.ma"
redirect_uri = "https://www.google.ca/"
scope = 'user-library-read playlist-read-private'

token = spotipy.SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope, cache_path=".cache-jennessa.ma", username=username)
sp = spotipy.Spotify(auth_manager=token)

#------------------------------------------------------------------------------#

#HELPER FUNCTIONS
#passes in 2 arrays containing audio features of 2 songs
#returns a similarity value
def getDotProd(song1, song2):
    product = 1;
    for i in range(NUM_FEATURES):
        temp = song1[i] * song2[i]
        product += (song1[i] * song2[i])
    return product

#get the magnitude of a vector
def getMagnitude(song1):
    sum = 0
    for i in range(NUM_FEATURES):
        sum += (song1[i] * song1[i])
    return math.sqrt(sum)

#equation for cosine similarity used in content-based filtering
# = ratio between dot product and magnitudes multiplied
# will return a value between 0 and 1, with 1 being the most similar to each other
def getSimilarity(song1, song2):
    numerator = getDotProd(song1, song2)
    denominator = getMagnitude(song1) * getMagnitude(song2)
    return numerator / denominator

def getAvgSimilarity(song1_uri, song1_vector, cmpr_dict):
    sum = 0
    for uri_key in cmpr_dict:
        if (song1_uri == uri_key):
            pass
        else:
            sum += getSimilarity(song1_vector, cmpr_dict[uri_key])
    return sum / NUM_SONGS

#passes in a list of uris
#returns a dictionary that maps a uri key to an array of features {song_uri : [features]}
def getAudioFeatures(uri_list):
    dict = {}
    for uri in uri_list:
        features = sp.audio_features(uri)[0]
        if features is None:
            continue
        dict[uri] = list(features.values())[:11] #only need necessary parameters
    return dict

#print the most similar songs given a dictionary of test songs and a dictionary of good songs
def printMostSimilar(top_songs_dict, test_songs_dict):
    most_similar = []
    print("MOST SIMILAR SONGS AND THEIR SIMILARITY SCORES")
    test_iter = iter(test_songs_dict)
    for i in range(NUM_SONGS):
        test_uri = next(test_iter)
        avg = getAvgSimilarity(test_uri, test_songs_dict[test_uri], top_songs_dict)
        if (avg >= THRESHOLD):
            most_similar.append(test_uri)
            print(sp.track(test_uri)["name"] + ": " + str(avg))
    return most_similar

def analyze(uris):
    genre_dict = {}
    for uri in uris:
        track = sp.track(uri)
        artist = sp.artist(track["artists"][0]["uri"])
        genres = artist["genres"]
        for genre in genres:
            if (genre in genre_dict):
                genre_dict[genre] += 1
            else:
                genre_dict[genre] = 1
    genre_dict = sorted(genre_dict.items(), key = lambda x : x[1], reverse = True)
    print("-----------------------------------------------")
    popular = [pair[0] for pair in genre_dict][:4]
    print("THE MOST POPULAR GENRES WERE: " + str(popular))
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

#get the song name and its uri to extract data from
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

#------------------------------------------------------------------------------#

#CALL HELPER FUNCTIONS ON RETRIEVED DATA
test_songs_dict = getAudioFeatures(test_uris)
top_songs_dict = getAudioFeatures(top_songs_uris[:79])

# test_track = sp.track(next(iter(test_songs_dict)))
# artist = sp.artist(test_track["artists"][0]["uri"])
# print(artist["genres"])
most_similar_uris = printMostSimilar(top_songs_dict, test_songs_dict)
analyze(most_similar_uris)
