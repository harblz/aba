from django import template


register = template.Library()


@register.filter(name="minutes")
def duration_minutes(duration):
    return int(duration.total_seconds() / 60)
