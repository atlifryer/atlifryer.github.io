# predictions/templatetags/custom_filters.py

from django import template
from predictions.models import Game
from django.db.models.functions import TruncDay

register = template.Library()

@register.filter
def capitalize_first(value):
    return value[0].upper() + value[1:] if value else value

@register.filter
def get_unique_dates(games):
    return games.annotate(date=TruncDay('game_date')).order_by('date').values_list('date', flat=True).distinct()

@register.filter(name='matches_date')
def matches_date(day, game_date):
    formatted_day = day.strftime('%Y-%m-%d')
    return formatted_day == game_date

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)