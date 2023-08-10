from flask import Flask, request, url_for, session, redirect,render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import random
import os
from datetime import date

app = Flask(__name__)

app.secret_key=os.environ['cookie_env']
app.config['SESSIONS_COOKIE_NAME'] ='my cookie'
TOKEN_INFO = "token_info"

client_id=os.environ['client_id_env']
client_secret=os.environ['client_secret_env']

@app.route('/')
def pre_login_page():
    session.pop("token_info", None)
    return render_template('home3.html')


@app.route('/login')
def login():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True,
        client_id=client_id,
        client_secret=client_secret)
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect(url_for("login"))

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        print(auth_url)
        return redirect(auth_url)

    sp = spotipy.Spotify(auth_manager=auth_manager)
    return redirect(url_for("services"))



@app.route('/logout')
def sign_out():
    session.pop("token_info", None)
    return redirect("/")

@app.route('/redirect')
def redirectPage():
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/services')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):

        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)


@app.route('/services')
def services():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'
    return render_template('services3.html',profile_name=profile_name, profile_photo_url=profile_photo_url)








@app.route('/pre_anything_playlist')
def pre_anything_playlist():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'


    return render_template('pre_anything_playlist3.html',profile_name=profile_name, profile_photo_url=profile_photo_url)


@app.route('/anything_playlist', methods=['GET', 'POST'])
def anything_playlist():
    if request.method == 'POST':
        input_text = request.form['input_text']
        cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
            cache_handler=cache_handler,
            redirect_uri=url_for('login', _external=True),
            show_dialog=True, client_id=client_id,
            client_secret=client_secret)
        if not auth_manager.validate_token(cache_handler.get_cached_token()):
            return redirect('/')

        sp = spotipy.Spotify(auth_manager=auth_manager)

        search_list_for_any_playlist_string = sp.search(q=input_text,type='playlist')#['playlists']['items'][0]['name']
        total_items = search_list_for_any_playlist_string['playlists']['total']
        search_list_for_any_playlist=[]
        anything_playlist = []

        user_profile = sp.current_user()
        profile_name = user_profile['display_name']
        profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'

        if total_items >4 :
         search_list_for_any_playlist.append(search_list_for_any_playlist_string['playlists']['items'][0]['id'])
         search_list_for_any_playlist.append(search_list_for_any_playlist_string['playlists']['items'][1]['id'])
         search_list_for_any_playlist.append(search_list_for_any_playlist_string['playlists']['items'][2]['id'])
         search_list_for_any_playlist.append(search_list_for_any_playlist_string['playlists']['items'][3]['id'])
        else:
            for x in range (0,total_items):
                search_list_for_any_playlist.append(search_list_for_any_playlist_string['playlists']['items'][x]['id'])
        for y in search_list_for_any_playlist :
            playlist_any_songs_string = sp.playlist_items(additional_types=["track"],playlist_id=y)
            for x in range(10):
                if playlist_any_songs_string['items'][x]['track']['uri'] not in anything_playlist:
                    anything_playlist.append(
                        playlist_any_songs_string['items'][x]['track']['uri'])
            if x == 2:
                seed_artist=[]
                seed_artist.append(playlist_any_songs_string1['items'][x]['track']['album']['artists'][0][
                     'id'])
                any_playlist_tracks_string_from_recommendations = sp.recommendations(
                      seed_artists=seed_artist, limit=5)
                for x in range(0,5):
                    anything_playlist.append(any_playlist_tracks_string_from_recommendations['tracks'][x]['id'])

        sp.user_playlist_create(user=sp.current_user()['id'], public=False, name=input_text, description='Generated using mood.music ---> https://thecodeworks.in/mood.music/')
        new_playlist_id_anything = sp.user_playlists(user=sp.current_user()['id'])['items'][0]['id']
        sp.playlist_add_items(playlist_id=new_playlist_id_anything, items=anything_playlist,position=0)
        time.sleep(2)
        return render_template('anything_playlist3.html', playlist_id1_anything=new_playlist_id_anything,profile_name=profile_name, profile_photo_url=profile_photo_url)
    else:
        # Handle GET request for the route
        return redirect("/anything_playlist")



@app.route('/pre_you_playlist')
def pre_you_playlist():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'
#################################################################

    return render_template('pre_you_playlist.html',profile_name=profile_name, profile_photo_url=profile_photo_url)


@app.route("/about")
def about():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'
    return render_template("about3.html",profile_name=profile_name, profile_photo_url=profile_photo_url)

@app.route("/privacy")
def privacy():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'
    return render_template("privacy3.html",profile_name=profile_name, profile_photo_url=profile_photo_url)




@app.route('/getYouPlaylist')
def getYouPlaylist():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'
#####################################################
    follow_len=len(sp.current_user_followed_artists(limit=50)['artists']['items'])
    top_len=len(sp.current_user_top_artists(limit=50)['items'])
    saved_len=len(sp.current_user_saved_tracks(limit=50)['items'])
    follow_control=1
    top_control=1
    saved_control=1
    if follow_len == 0:
        follow_control=0
    if top_len == 0:
        top_control = 0
    if saved_len == 0:
        saved_control = 0


################################### FOLLOWED ARTISTS LIST ##############################
    follow_artists_string = sp.current_user_followed_artists(limit=50)
    list_of_user_followed_artists = []
    if follow_control == 1:
        for x in range (0,follow_len):
            list_of_user_followed_artists.append(follow_artists_string['artists']['items'][x]['uri'])
#######################################################################################

################################### TOP ARTISTS LIST ##############################
    top_artists_string = sp.current_user_top_artists(limit=50)
    list_of_user_top_artists = []
    if top_control == 1:
        for x in range(0, top_len):
            list_of_user_top_artists.append(top_artists_string['items'][x]['uri'])
###################################################################################
############################# YOU PLAYLIST AVG VALUES GENERATOR ##########################

    list_of_seed_artists_for_you_playlist = []
    list_of_user_saved_tracks_string = sp.current_user_saved_tracks(limit=50)
    list_of_user_saved_tracks_id=[]
    if saved_control == 1:
        for x in range(0,saved_len):
            list_of_user_saved_tracks_id.append(list_of_user_saved_tracks_string['items'][x]['track']['artists'][0]['uri'])
        for x in random.choices(list_of_user_saved_tracks_id, k=5):
            list_of_seed_artists_for_you_playlist.append(x)
############################################################################################
    you_Playlist = []

############################ SONG GENERATION FROM TOP AND FOLLOWED ARTISTS #################

    list_of_artists_top_and_followed_for_you_playlist = []
    if follow_control == 1 and top_control == 1 and saved_control == 1:
        for x in random.choices(list_of_user_top_artists,k=2):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        for x in random.choices(list_of_user_followed_artists,k=3):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
    elif follow_control == 1 and top_control == 0 and saved_control == 1:
        for x in random.choices(list_of_user_followed_artists,k=5):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
    elif follow_control == 0 and top_control == 1 and saved_control == 1:
        for x in random.choices(list_of_user_top_artists,k=5):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
    elif follow_control == 0 and top_control == 0 and saved_control == 1:
        list_of_artists_top_and_followed_for_you_playlist = list_of_seed_artists_for_you_playlist
    elif follow_control == 1 and top_control == 1 and saved_control == 0:
        for x in random.choices(list_of_user_top_artists,k=2):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        for x in random.choices(list_of_user_followed_artists,k=3):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        list_of_seed_artists_for_you_playlist = list_of_artists_top_and_followed_for_you_playlist
    elif follow_control == 1 and top_control == 0 and saved_control == 0:
        for x in random.choices(list_of_user_followed_artists,k=5):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        list_of_seed_artists_for_you_playlist = list_of_artists_top_and_followed_for_you_playlist
    elif follow_control == 0 and top_control == 1 and saved_control == 0:
        for x in random.choices(list_of_user_top_artists,k=5):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        list_of_seed_artists_for_you_playlist = list_of_artists_top_and_followed_for_you_playlist
    elif follow_control == 0 and top_control == 0 and saved_control == 0:
        print("huh")
        sp.current_user_follow_playlist(playlist_id="37i9dQZEVXbNG2KDcFcKOF")
        return render_template('no_data3.html', playlist_id1="37i9dQZEVXbNG2KDcFcKOF", profile_name=profile_name,
                               profile_photo_url=profile_photo_url)
    else:
        print("what")


    list_of_top_artists_songs_for_you_playlist = []
    for x in list_of_artists_top_and_followed_for_you_playlist:
        len_top_songs1=len(sp.artist_top_tracks(artist_id=x)['tracks'])
        if len_top_songs1 < 3:
            continue
        list_of_top_artists_songs_for_you_playlist.append(sp.artist_top_tracks(artist_id=x)['tracks'][random.randint(0,len_top_songs1-1)]['uri'])

###########################################################################################
######################### RELATED ARTISTS ################################################
    list_of_top_related_artists_songs_for_you_playlist = []
    for x in list_of_artists_top_and_followed_for_you_playlist:
       len_top_artists1=len(sp.artist_related_artists(x)['artists'])
       if len_top_artists1 < 3:
            continue
       temp_related_artist_id = sp.artist_related_artists(x)['artists'][random.randint(0,len_top_artists1-1)]['id']
       len_top_related1=len((sp.artist_top_tracks(artist_id=temp_related_artist_id)['tracks']))
       if len_top_related1 < 3:
          continue
       list_of_top_related_artists_songs_for_you_playlist.append(sp.artist_top_tracks(artist_id=temp_related_artist_id)['tracks'][random.randint(0,len_top_related1-1)]['uri'])


    print(sp.current_user()['id'])
    you_playlist_tracks_string_from_recommendations =sp.recommendations(seed_artists=list_of_seed_artists_for_you_playlist,seed_tracks=[],limit=20)

    for x in range(0, 19):
        you_Playlist.append(you_playlist_tracks_string_from_recommendations['tracks'][x]['id'])
    for x in list_of_top_artists_songs_for_you_playlist:
        you_Playlist.append(x)
    for x in list_of_top_related_artists_songs_for_you_playlist:
        you_Playlist.append(x)


    sp.user_playlist_create(user=sp.current_user()['id'], public=False, name="You Playlist "+str(date.today()), description='Generated using mood.music ---> https://thecodeworks.in/mood.music/')
    new_playlist_id = sp.user_playlists(user=sp.current_user()['id'])['items'][0]['id']
    print(you_Playlist)
    sp.playlist_add_items(playlist_id=new_playlist_id, items=you_Playlist, position=0)

    time.sleep(2)
    return render_template('you_playlist3.html', playlist_id1=new_playlist_id,profile_name=profile_name, profile_photo_url=profile_photo_url)

@app.route("/pre_mood_playlist")
def pre_mood_playlist():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'
    return render_template("pre_mood_playlist3.html",profile_name=profile_name, profile_photo_url=profile_photo_url)
    #print(sp.recommendations(seed_artists=['4AK6F7OLvEQ5QYCBNiQWHq'],target_danceability=0.2))
    #return "hfbdf"

@app.route("/mood_playlist", methods=["POST"])
def mood_playlist():
    danceability = float(request.form['danceability'])
    acousticness = float(request.form['acousticness'])
    speechiness = float(request.form['speechiness'])
    valence = float(request.form['valence'])
    popularity = int(request.form['popularity'])
    tempo = float(request.form['tempo'])
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'
    #####################################################
    follow_len = len(sp.current_user_followed_artists(limit=50)['artists']['items'])
    top_len = len(sp.current_user_top_artists(limit=50)['items'])
    saved_len = len(sp.current_user_saved_tracks(limit=50)['items'])
    follow_control = 1
    top_control = 1
    saved_control = 1
    if follow_len == 0:
        follow_control = 0
    if top_len == 0:
        top_control = 0
    if saved_len == 0:
        saved_control = 0

    ################################### FOLLOWED ARTISTS LIST ##############################
    follow_artists_string = sp.current_user_followed_artists(limit=50)
    list_of_user_followed_artists = []
    if follow_control == 1:
        for x in range(0, follow_len):
            list_of_user_followed_artists.append(follow_artists_string['artists']['items'][x]['uri'])
    #######################################################################################

    ################################### TOP ARTISTS LIST ##############################
    top_artists_string = sp.current_user_top_artists(limit=50)
    list_of_user_top_artists = []
    if top_control == 1:
        for x in range(0, top_len):
            list_of_user_top_artists.append(top_artists_string['items'][x]['uri'])
    ###################################################################################
    ############################# YOU PLAYLIST AVG VALUES GENERATOR ##########################

    list_of_seed_artists_for_you_playlist = []
    list_of_user_saved_tracks_string = sp.current_user_saved_tracks(limit=50)
    list_of_user_saved_tracks_id = []
    if saved_control == 1:
        for x in range(0, saved_len):
            list_of_user_saved_tracks_id.append(
                list_of_user_saved_tracks_string['items'][x]['track']['artists'][0]['uri'])
        for x in random.choices(list_of_user_saved_tracks_id, k=5):
            list_of_seed_artists_for_you_playlist.append(x)
    ############################################################################################
    mood_Playlist = []

    ############################ SONG GENERATION FROM TOP AND FOLLOWED ARTISTS #################

    list_of_artists_top_and_followed_for_you_playlist = []
    if follow_control == 1 and top_control == 1 and saved_control == 1:
        for x in random.choices(list_of_user_top_artists, k=2):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        for x in random.choices(list_of_user_followed_artists, k=3):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
    elif follow_control == 1 and top_control == 0 and saved_control == 1:
        for x in random.choices(list_of_user_followed_artists, k=5):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
    elif follow_control == 0 and top_control == 1 and saved_control == 1:
        for x in random.choices(list_of_user_top_artists, k=5):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
    elif follow_control == 0 and top_control == 0 and saved_control == 1:
        list_of_artists_top_and_followed_for_you_playlist = list_of_seed_artists_for_you_playlist
    elif follow_control == 1 and top_control == 1 and saved_control == 0:
        for x in random.choices(list_of_user_top_artists, k=2):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        for x in random.choices(list_of_user_followed_artists, k=3):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        list_of_seed_artists_for_you_playlist = list_of_artists_top_and_followed_for_you_playlist
    elif follow_control == 1 and top_control == 0 and saved_control == 0:
        for x in random.choices(list_of_user_followed_artists, k=5):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        list_of_seed_artists_for_you_playlist = list_of_artists_top_and_followed_for_you_playlist
    elif follow_control == 0 and top_control == 1 and saved_control == 0:
        for x in random.choices(list_of_user_top_artists, k=5):
            list_of_artists_top_and_followed_for_you_playlist.append(x)
        list_of_seed_artists_for_you_playlist = list_of_artists_top_and_followed_for_you_playlist
    elif follow_control == 0 and top_control == 0 and saved_control == 0:
        print("huh")
        sp.current_user_follow_playlist(playlist_id="37i9dQZEVXbNG2KDcFcKOF")
        return render_template('no_data3.html', playlist_id1="37i9dQZEVXbNG2KDcFcKOF", profile_name=profile_name,
                               profile_photo_url=profile_photo_url)
    else:
        print("what")



    ###########################################################################################
    ######################### RELATED ARTISTS ###############################################

    mood_playlist_recommendations = sp.recommendations(
        seed_artists=list_of_seed_artists_for_you_playlist, seed_tracks=[], limit=10,target_acousticness=acousticness,target_danceability=danceability,
    target_speechiness=speechiness,target_valence=valence,target_popularity=popularity,target_tempo=tempo)

    for x in range(0, 10):
        mood_Playlist.append(mood_playlist_recommendations['tracks'][x]['id'])

    mood_playlist_recommendations = sp.recommendations(
        seed_artists=list_of_artists_top_and_followed_for_you_playlist, seed_tracks=[], limit=10,target_acousticness=acousticness,target_danceability=danceability,
    target_speechiness=speechiness,target_valence=valence,target_popularity=popularity,target_tempo=tempo)

    for x in range(0, 10):
        mood_Playlist.append(mood_playlist_recommendations['tracks'][x]['id'])


    sp.user_playlist_create(user=sp.current_user()['id'], public=False, name="Mood Playlist "+str(date.today()), description='Generated using mood.music ---> https://thecodeworks.in/mood.music/')
    new_playlist_id = sp.user_playlists(user=sp.current_user()['id'])['items'][0]['id']
    sp.playlist_add_items(playlist_id=new_playlist_id, items=mood_Playlist, position=0)

    time.sleep(2)

    return render_template('mood_playlist3.html', playlist_id1=new_playlist_id, profile_name=profile_name,
                           profile_photo_url=profile_photo_url)


@app.route("/stats")
def stats():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-follow-read,user-follow-modify,user-read-recently-played,user-modify-playback-state,user-library-read,user-read-currently-playing,user-top-read,playlist-modify-private,playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-read-private",
        cache_handler=cache_handler,
        redirect_uri=url_for('login', _external=True),
        show_dialog=True, client_id=client_id,
        client_secret=client_secret)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)

    user_profile = sp.current_user()
    profile_name = user_profile['display_name']
    profile_photo_url = user_profile['images'][0]['url'] if user_profile['images'] else 'static/profile3.png'

    list_of_top_songs_medium=[]
    list_of_top_songs_short=[]
    pop_medium=0
    pop_short=0
    ac_medium=0
    ac_short=0
    da_medium=0
    da_short=0
    en_short=0
    en_medium=0
    in_short=0
    in_medium=0
    te_short=0
    te_medium=0
    va_short=0
    va_medium=0
    list_of_top_songs_string=sp.current_user_top_tracks(limit=50,time_range="short_term")
    top_len= len(list_of_top_songs_string['items'])
    if top_len == 0:
        return render_template('no_data3.html', playlist_id1="37i9dQZEVXbNG2KDcFcKOF", profile_name=profile_name,
                               profile_photo_url=profile_photo_url)
    for x in range(0,top_len):
        list_of_top_songs_short.append(list_of_top_songs_string['items'][x]['id'])
        pop_short = pop_short + int(list_of_top_songs_string['items'][x]['popularity'])
    pop_short = pop_short/top_len
    short_features_string = sp.audio_features(list_of_top_songs_short)
    for x in range(0, top_len):
        ac_short = ac_short + short_features_string[x]['acousticness']
        da_short = da_short + short_features_string[x]['danceability']
        en_short = en_short + short_features_string[x]['energy']
        in_short = in_short + short_features_string[x]['instrumentalness']
        te_short = te_short + short_features_string[x]['tempo']
        va_short = va_short + short_features_string[x]['valence']
    ac_short = ac_short / top_len
    da_short = da_short / top_len
    en_short = en_short / top_len
    in_short = in_short / top_len
    te_short = te_short / top_len
    va_short = va_short / top_len


    list_of_top_songs_string=sp.current_user_top_tracks(limit=50,time_range="medium_term")
    top_len= len(list_of_top_songs_string['items'])
    if top_len != 0:
        for x in range(0,top_len):
            list_of_top_songs_medium.append(list_of_top_songs_string['items'][x]['id'])
            pop_medium = pop_medium + int(list_of_top_songs_string['items'][x]['popularity'])
        pop_medium = pop_medium/top_len
        medium_features_string = sp.audio_features(list_of_top_songs_medium)
        for x in range(0,top_len):
           ac_medium = ac_medium + medium_features_string[x]['acousticness']
           da_medium = da_medium + medium_features_string[x]['danceability']
           en_medium = en_medium + medium_features_string[x]['energy']
           in_medium = in_medium + medium_features_string[x]['instrumentalness']
           te_medium = te_medium + medium_features_string[x]['tempo']
           va_medium = va_medium + medium_features_string[x]['valence']
        ac_medium = ac_medium/top_len
        da_medium = da_medium/top_len
        en_medium = en_medium/top_len
        in_medium = in_medium/top_len
        te_medium = te_medium/top_len
        va_medium = va_medium/ top_len

        if pop_short >= pop_medium:
            pl_text="The type of music you've been listening to is getting more popular,from " + str(round(pop_medium))+"% to "+str(round(pop_short))+"%"
        else:
            pl_text="You've started listening to more newer music ,from " + str(round(pop_medium))+"% to "+str(round(pop_short))+"%"
        if ac_short >= ac_medium:
            ac_text="The type of music you've been listening to is getting more acoustic,from " + str(round(ac_medium*100))+"% to "+str(round(ac_short*100))+"%"
        else:
            ac_text="You've started listening to more techno music ,from an acoustic " + str(round(ac_medium*100))+"% to "+str(round(ac_short*100))+"%"

        if da_short >= da_medium:
            da_text="More dance energy in your music from " + str(round(da_medium*100))+"% to "+str(round(da_short*100))+"%"
        else:
            da_text="Less dance, more chill in your music " + str(round(da_medium*100))+"% to "+str(round(da_short*100))+"%"

        if en_short >= en_medium:
            en_text="The type of music you've been listening to is getting more energetic,from " + str(round(en_medium*100))+"% to "+str(round(en_short*100))+"%"
        else:
            en_text="You've started listening to more low key music ,from energy " + str(round(en_medium*100))+"% to "+str(round(en_short*100))+"%"

        if in_short >= in_medium:
            in_text="The type of music you've been listening to is getting more instrumental from " + str(round(in_medium*100))+"% to "+str(round(in_short*100))+"%"
        else:
            in_text="You've started listening to less instrumental music from " + str(round(in_medium*100))+"% to "+str(round(in_short*100))+"%"

        if te_short >= te_medium:
            te_text="You've been listening to more high tempo songs ,from " + str(round(te_medium))+" to "+str(round(te_short))
        else:
            te_text="You've started listening to slower, calmer music ,from tempo " + str(round(te_medium))+" to "+str(round(te_short))

        if va_short >= va_medium:
            va_text="The type of music you've been listening to is getting more uplifting,from " + str(round(va_medium*100))+"% to "+str(round(va_short*100)) +"%"
        else:
            va_text="You've started listening to more down key music ,from " + str(round(va_medium*100))+"% to "+str(round(va_short*100)) +"%"


    return render_template("stats3.html",pl_text=pl_text,ac_text=ac_text,da_text=da_text,en_text=en_text,in_text=in_text,te_text=te_text,va_text=va_text,profile_name=profile_name,profile_photo_url=profile_photo_url)
if __name__ == "__main__":
 app.run()




