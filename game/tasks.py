# game/tasks.py
from celery import shared_task
from .models import GameData
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Create a periodic task for every 10 minutes
schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.MINUTES,
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Check for dropped potatoes',
    task='game.tasks.check_for_dropped_potatoes',
)


@shared_task
def check_for_dropped_potatoes():
    game_data = GameData()
    game_data.end_game()


