from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter(name='display_time', expects_localtime=True)
def display_time(value):
    
    delta = timezone.now() - value
    delta_seconds = delta.total_seconds()
    seconds_per_hour = 3600
    seconds_per_min = 60
    
    if delta >= timedelta(hours=24):
        return value.strftime('%b %d')
    elif delta >= timedelta(hours=1):
        delta_hours = int(delta_seconds / seconds_per_hour)
        return "%dhours" %delta_hours
    elif delta >= timedelta(minutes=1):
        delta_mins = int(delta_seconds / seconds_per_min)
        return "%dmins" %delta_mins
    elif delta >= timedelta(seconds=1):
        return "%ds" %int(delta_seconds)
    else:
        return 'now'