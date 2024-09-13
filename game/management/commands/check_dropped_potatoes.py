# game/management/commands/check_dropped_potatoes.py
from django.core.management.base import BaseCommand
from game.models import GameData

class Command(BaseCommand):
    help = 'Check for games where the potato was dropped'

    def handle(self, *args, **kwargs):
        game_data = GameData()
        game_data.end_game()

