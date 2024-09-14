from django.shortcuts import render

# game/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GameData
from django.core.mail import send_mail
import json

game_data = GameData()

def index(request):
    return JsonResponse({"game_id": "y"})

# @csrf_exempt
def start_game(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_email = body.get('user_email')
        new_game = game_data.create_game(user_email)
        game_id = new_game["game_id"]

        send_mail(
            subject='You have created a Hot Potato!',
            message=f'You have 24 hours to pass the hot potato.\n' +
            f'Pass the potato using ' +
            f'http://localhost:8080/passpotato.html?' +
            f'user={user_email}&gameId={game_id}',
            html_message=f'You have 24 hours to pass the hot potato.\n' +
            f'Pass the potato using ' +
            f'<a href=http://localhost:8080/passpotato.html?' +
            f'user={user_email}&gameId={game_id}>this link</a>',
            from_email='noreply@krooonal.com',
            recipient_list=[user_email]
        )
        return JsonResponse({"game_id": new_game["game_id"], "message": "Game started!"})
    else:
        return JsonResponse({"game_id": "x"})

# @csrf_exempt
def pass_potato(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        game_id = body.get('game_id')
        current_user = body.get('current_user')
        new_user = body.get('new_user')
        result = game_data.pass_potato(game_id, current_user, new_user)
        
        if "error" in result:
            return JsonResponse({"error": result["error"]})
        
        # Send email notification to the new user
        send_mail(
            subject='You have the Hot Potato!',
            message=f'{current_user} passed you a hot potato.\n' +
            f'You have 24 hours to pass the hot potato.\n' +
            f'Pass the potato using ' +
            f'http://localhost:8080/passpotato.html?' +
            f'user={new_user}&gameId={game_id}',
            html_message=f'{current_user} passed you a hot potato.\n' +
            f'You have 24 hours to pass the hot potato.\n' +
            f'Pass the potato using ' +
            f'<a href=http://localhost:8080/passpotato.html?' +
            f'user={new_user}&gameId={game_id}>this link</a>',
            from_email='noreply@krooonal.com',
            recipient_list=[new_user]
        )
        return JsonResponse({"message": f"Potato passed to {new_user}!"})

