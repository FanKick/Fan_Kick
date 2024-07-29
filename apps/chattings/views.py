from django.shortcuts import redirect
import hashlib

# def get_hashed_id(request):
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         hashed_id = hashlib.sha256(str(user_id).encode()).hexdigest()[:10]
#         hashed_id_url = f'?user_hash={hashed_id}'
#     return hashed_id_url


def redirect_to_dm(request):
    if request.user.is_player:
        ip_port = 'http://192.168.0.8:9000/dm/player/'
        user_id = str(request.user.id)
        dm_url = ip_port + user_id
        return redirect(dm_url)

    else:
        ip_port = 'http://192.168.0.8:9000/dm/'
        user_id = str(request.user.id)
        dm_url = ip_port + user_id
        return redirect(dm_url)