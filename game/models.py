from django.db import models

# game/models.py
import json
import os
from django.conf import settings
from datetime import datetime
from django.core.mail import send_mail

GAME_DATA_FILE = os.path.join(settings.BASE_DIR, 'game_data.json')

def send_streak_report(email, streak_length, held_users, average_streak, max_streak):
    send_mail(
        subject="Hot Potato Game Ended",
        message=f"The game ended with a streak of {streak_length} users.\n" +
                f"Participants: {', '.join([user for user in held_users])}\n" +
                f"Average streak length: {average_streak}\n" +
                f"Max streak length: {max_streak}",
        from_email='noreply@krooonal.com',
        recipient_list=[email],
        html_message=f"The game ended with a streak of <b>{streak_length}</b> users.\n" +
                f"Participants: {', '.join([user for user in held_users])}\n" +
                f"Average streak length: <b>{average_streak}</b>\n" +
                f"Max streak length: <b>{max_streak}</b>",
    )

class GameData:
    def __init__(self):
        self.load_data()

    def load_data(self):
        if os.path.exists(GAME_DATA_FILE):
            with open(GAME_DATA_FILE, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {
                "stats": {
                    "average_streak_length": 0.0,
                    "max_streak_length": 0,
                    "total_games": 0
                },
                "games": []
            }

    def save_data(self):
        with open(GAME_DATA_FILE, 'w') as file:
            json.dump(self.data, file, indent=4)

    def create_game(self, user_email):
        game_id = len(self.data['games']) + 1
        new_game = {
            "game_id": str(game_id),
            "users": [user_email],
            "current_user": user_email,
            "streak": 1,
            "created_at": datetime.now().isoformat(),
            "last_passed": datetime.now().isoformat(),
            "time_limit": 24*3600
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

    def end_game(self):
        for game in self.data['games']:
            difference = datetime.now() - datetime.fromisoformat(game['last_passed'])
            if difference.total_seconds() <= game['time_limit']:
                continue

            # Get the users who held the potato in the game
            held_users = game['users']
            streak_length = len(held_users)

            # Update average streak and max streak
            num_games = self.data['stats']['total_games']
            current_avg = self.data['stats']['average_streak_length']
            new_avg = current_avg + (streak_length - current_avg) / (num_games + 1)
            self.data['stats']['average_streak_length'] = new_avg
            current_max = self.data['stats']['max_streak_length']
            if streak_length > current_max:
                current_max = streak_length
                self.data['stats']['max_streak_length'] = streak_length

            # Send streak report to users
            for user in held_users:
                send_streak_report(user, streak_length,
                                   held_users, new_avg, current_max)

            self.data['games'].remove(game)
        self.save_data()
