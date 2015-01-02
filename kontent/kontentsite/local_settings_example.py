DB_DATABASE = 'dbname'
DB_USERNAME = 'dbusername'
DB_PASSWORD = 'P4ssw0rd'
DB_HOSTNAME = 'localhost'

SITE_ID = 1

# Needed when using an external theme, like the dammIT theme:
import os
TEMPLATE_DIRS = (
    '/srv/projects/github/kontent-dammit/dammit', # dammIT theme
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kontent/templates/'), # default kontent theme
)


STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), "static"),
    '/srv/projects/github/kontent-dammit/dammit/static',
)
