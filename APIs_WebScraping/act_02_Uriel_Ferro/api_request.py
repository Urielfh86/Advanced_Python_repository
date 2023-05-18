import requests
import json
from collections import Counter # La utilizo para contar la cantidad de apariciones de un género en una lista y crear un diccionario con esa información
import urllib.request # La utilizo para leer lo que hay en la URL de la imágen de la portada de la Playlist y poder guardarla en disco

class Api_Request():

    __success_code = 200

    def __init__(self, token, func_get_token):
        self.__token = token
        self.__func_get_token = func_get_token
        self.__base_url = 'https://api.spotify.com/v1/'

        self.__headers = {
        "Authorization" : f'Bearer {self.__token}',
        "Accept" : "application/json"
        }

        self.__params = {
            "limit" : 10
        }

        self.__artists = None
        self.__top_10_artists = list()
        self.__top_5_genres = list()
        self.__songs_list = list()
        self.__playlist_id = None
        self.__playlist_followers = None

        self.__tempo_avg = None
        self.__acousticness_avg = None
        self.__danceability_avg = None
        self.__energy_avg = None
        self.__instrumentalness_avg = None
        self.__liveness_avg = None
        self.__loudness_avg = None
        self.__valence_avg = None

    def get_user_info_from_spotify(self):
        self.__get_top_10_artists()
        self.__get_top_5_genres()
        self.__get_top_10_tracks_with_artists()

        pre_json_dict_user = self.__generate_pre_json_user()
        self.__save_json("data_user_spotify.json", "del usuario", pre_json_dict_user)

    def print_user_info_from_spotify(self):
        self.__print_top_10_artists()
        self.__print_top_5_genres()
        self.__print_top_10_tracks()

    def __get_top_10_artists(self):
        self.__token = self.__func_get_token()

        endpoint = "me/top/artists"

        response = requests.get(self.__base_url + endpoint, params = self.__params, headers = self.__headers)

        if response.status_code == Api_Request.__success_code:
            data = response.json()
            self.__artists = data["items"]
            
            for artist in self.__artists:
                self.__top_10_artists.append(artist["name"])
        else:
            print("\nError al obtener la información solicitada sobre el top 10 de artistas y top 5 géneros.")
            print(f"{response.json()}")

    def __get_top_5_genres(self):
        self.__token = self.__func_get_token()

        genres_list = list()

        for artist in self.__artists:
            genres_list.extend(artist["genres"])

        genres_count = dict(Counter(genres_list))

        genres_count = dict(sorted(genres_count.items(), key = lambda item: item[1], reverse = True))

        self.__top_5_genres = list(genres_count.keys())[:5]

    def __get_top_10_tracks_with_artists(self):
        self.__token = self.__func_get_token()
        
        endpoint = "me/top/tracks"

        response = requests.get(self.__base_url + endpoint, params = self.__params, headers = self.__headers)

        if response.status_code == Api_Request.__success_code:
            data = response.json()
            tracks = data["items"]

            for track in tracks:
                song = dict()
                song["name"] = track["name"]
                song["artist"] = track["artists"][0]["name"]
                self.__songs_list.append(song)
        else:
            print("\nError al obtener la información solicitada sobre el top 10 de canciones mas escuchadas.")
            print(f"{response.json()}") 

    def get_info_playlist(self):
        self.__token = self.__func_get_token()

        self.__playlist_id = "37i9dQZF1DWWGFQLoP9qlv"
        endpoint = f"playlists/{self.__playlist_id}"

        response = requests.get(self.__base_url + endpoint, headers = self.__headers)

        if response.status_code == Api_Request.__success_code:
            data = response.json()
        else:
            print("\nError al obtener la información solicitada sobre la playlist.")
            print(f"{response.json()}")

        self.__save_cover_image_playlist(data)
        self.__get_playlist_followers(data)
        self.__get_avg_params_from_playlist_tracks()

        pre_json_dict_playlist = self.__generate_pre_json_playlist()
        self.__save_json("data_playlist_spotify.json", "de la Playlist", pre_json_dict_playlist)

    def print_info_playlist(self):
        self.__print_playlist_followers()
        self.__print_avg_params_of_all_tracks_playlist()
    
    def __save_cover_image_playlist(self, data):
        url_image = data["images"][0]["url"]
            
        try:
            with urllib.request.urlopen(url_image) as image:
                image_file = image.read()
                with open("portada_playlist.jpg", "wb") as file:
                        file.write(image_file)
            print("\nLa imágen de la portada de la playlist ha sido guardada con éxito!")
        except:
            print("Ocurrió un error y no se pudo guardar la imágen de la portada!")

    def __get_playlist_followers(self, data):
        self.__playlist_followers = data["followers"]["total"]

    def __get_avg_params_from_playlist_tracks(self):
        self.__token = self.__func_get_token()
        
        tempo = list()
        acousticness = list()
        danceability = list()
        energy = list()
        instrumentalness = list()
        liveness = list()
        loudness = list()
        valence = list()

        endpoint = f"playlists/{self.__playlist_id}/tracks"

        response = requests.get(self.__base_url + endpoint, headers = self.__headers)

        track_ids = []
        track_ids_str = ""

        if response.status_code == Api_Request.__success_code:
            data = response.json()

            for track in data["items"]:
                track_id = track['track']['id']
                track_ids.append(track_id)
        else:
            print("\nError al obtener la información solicitada sobre los IDs de las canciones de la playlist.")
            print(f"{response.json()}")  

        track_ids_str = ",".join(track_ids)

        endpoint = "audio-features"

        params = {
            "ids" : track_ids_str 
        }

        response = requests.get(self.__base_url + endpoint, params = params, headers = self.__headers)

        if response.status_code == Api_Request.__success_code:
            data = response.json()
            
            for track in data["audio_features"]:
                tempo.append(track["tempo"])
                acousticness.append(track["acousticness"])
                danceability.append(track["danceability"])
                energy.append(track["energy"])
                instrumentalness.append(track["instrumentalness"])
                liveness.append(track["liveness"])
                loudness.append(track["loudness"])
                valence.append(track["valence"])

        self.__tempo_avg = self.__average(tempo)
        self.__acousticness_avg = self.__average(acousticness)
        self.__danceability_avg = self.__average(danceability)
        self.__energy_avg = self.__average(energy)
        self.__instrumentalness_avg = self.__average(instrumentalness)
        self.__liveness_avg = self.__average(liveness)
        self.__loudness_avg = self.__average(loudness)
        self.__valence_avg = self.__average(valence)

    def __save_json(self, file_name, type_json, file_to_save):
        try:
            with open(f"{file_name}", "w") as file:
                json.dump(file_to_save, file)
            print(f"\nLa información {type_json} ha sido guardada en un archivo JSON de forma exitosa!")
        except:
            print(f"\nOcurrió un ERROR y la información {type_json} no pudo ser guardada en un JSON!")

    def __average(self, lista):
        return (sum(lista) / len(lista))

    def __generate_pre_json_user(self):
        key_artists = "user_top_10_artists"
        key_genres = "user_top_5_genres"
        key_tracks = "user_top_10_tracks"
        pre_json_dict_user = {key_artists : self.__top_10_artists, key_genres : self.__top_5_genres, key_tracks : self.__songs_list}
        return pre_json_dict_user

    def __generate_pre_json_playlist(self):
        key_followers = "number_of_followers"
        key_params = "average_params"

        dict_params = {
            "tempo" : self.__tempo_avg, 
            "acousticness" : self.__acousticness_avg,
            "danceability" : self.__danceability_avg,
            "energy" : self.__energy_avg,
            "instrumentalness" : self.__instrumentalness_avg,
            "liveness" : self.__liveness_avg,
            "loudness" : self.__loudness_avg,
            "valence" : self.__valence_avg
            }

        pre_json_dict_playlist = {key_followers : self.__playlist_followers, key_params : dict_params}

        return pre_json_dict_playlist

    def __print_top_10_artists(self):
        print("\nLos 10 artistas más escuchados por el usuario son: ")
        for artist in self.__top_10_artists:
            print(artist)

    def __print_top_5_genres(self):
        print(f"\nLos 5 generos más escuchados por el usuario son:")
        for genre in self.__top_5_genres:
            print(genre)

    def __print_top_10_tracks(self):
        print("\nLas 10 cancionas más escuchadas por el usuario y sus artistas son: ")
        for track in self.__songs_list:
            print(track["name"] + " ---> " + track["artist"])

    def __print_playlist_followers(self):
        print(f"\nLa playlist tiene {self.__playlist_followers} seguidores.")

    def __print_avg_params_of_all_tracks_playlist(self):
        print("\nPromedio de los parametros de todas las canciones de la playlist:")
        print(f'Tempo (BPM) promedio: {self.__tempo_avg}')
        print(f'Acousticness promedio: {self.__acousticness_avg}')
        print(f'Danceability promedio: {self.__danceability_avg}')
        print(f'Energy promedio: {self.__energy_avg}')
        print(f'Instrumentalness promedio: {self.__instrumentalness_avg}')
        print(f'Liveness promedio: {self.__liveness_avg}')
        print(f'Loudness promedio: {self.__loudness_avg}')
        print(f'Valence promedio: {self.__valence_avg}')

