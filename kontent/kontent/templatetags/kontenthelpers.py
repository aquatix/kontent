from django import template
register = template.Library()


@register.filter(name='prettydate')
def prettydate(datetime):
    #return datetime.strftime('We are the %d, %b %Y')
    return datetime.strftime('%A, %d %B %Y')


@register.filter(name='timestamp')
def timestamp(datetime):
    return datetime.strftime('%H:%M')


@register.filter(name='isodate')
def isodate(datetime):
    return datetime.strftime('%Y-%M-%dT%H:%M:%S%z')
