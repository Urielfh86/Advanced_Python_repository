from auth import Auth
from api_request import Api_Request

base_url = 'https://api.spotify.com/v1/'

auth = Auth()
auth.generate_token() # use it only for the first time
token = auth.get_token()

# Mi codigo hacia abajo

act_02 = Api_Request(token, auth.get_token)

act_02.get_user_info_from_spotify()
act_02.print_user_info_from_spotify()

act_02.get_info_playlist()
act_02.print_info_playlist()

