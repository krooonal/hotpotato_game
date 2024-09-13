from django.shortcuts import render

# game/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GameData
from django.core.mail import send_mail
import json

game_data = GameData()

@csrf_exempt
def start_game(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_email = body.get('user_email')
        new_game = game_data.create_game(user_email)
        return JsonResponse({"game_id": new_game["game_id"], "message": "Game started!"})

@csrf_exempt
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
            'You have the Hot Potato!',
            f'You have 24 hours to pass the hot potato.',
            'noreply@yourdomain.com',
            [new_user]
        )
        return JsonResponse({"message": f"Potato passed to {new_user}!"})

