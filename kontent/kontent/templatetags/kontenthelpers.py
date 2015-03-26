from django import template
register = template.Library()


@register.filter(name='prettydate')
def prettydate(datetime):
    #return datetime.strftime('We are the %d, %b %Y')
    if datetime:
        return datetime.strftime('%A, %d %B %Y')
    else:
        return 'Unknown'


@register.filter(name='simpledate')
def simpledate(datetime):
    if datetime:
        return datetime.strftime('%Y-%M-%d')
    else:
        return 'Unknown'


@register.filter(name='timestamp')
def timestamp(datetime):
    if datetime:
        return datetime.strftime('%H:%M:%S')
    else:
        return 'Unknown'


@register.filter(name='isodate')
def isodate(datetime):
    if datetime:
        return datetime.strftime('%Y-%M-%dT%H:%M:%S%z')
    else:
        return 'Unknown'
