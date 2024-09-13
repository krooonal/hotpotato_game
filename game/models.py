from django.db import models

# game/models.py
import json
import os
from django.conf import settings
from datetime import datetime

GAME_DATA_FILE = os.path.join(settings.BASE_DIR, 'game_data.json')

class GameData:
    def __init__(self):
        self.load_data()

    def load_data(self):
        if os.path.exists(GAME_DATA_FILE):
            with open(GAME_DATA_FILE, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {"games": []}

    def save_data(self):
        with open(GAME_DATA_FILE, 'w') as file:
            json.dump(self.data, file, indent=4)

    def create_game(self, user_email):
        game_id = len(self.data['games']) + 1
        new_game = {
            "game_id": game_id,
            "users": [user_email],
            "current_user": user_email,
            "streak": 1,
            "created_at": datetime.now().isoformat(),
            "last_passed": datetime.now().isoformat()
        }
        self.data['games'].append(new_game)
        self.save_data()
        return new_game

    def pass_potato(self, game_id, current_user, new_user):
        game = next((g for g in self.data['games'] if g['game_id'] == game_id), None)
        if game:
            if new_user in game['users']:
                return {"error": f"{new_user} has already held the potato."}
            game['users'].append(new_user)
            game['current_user'] = new_user
            game['streak'] += 1
            game['last_passed'] = datetime.now().isoformat()
            self.save_data()
            return {"success": True, "new_user": new_user}
        return {"error": "Game not found."}
