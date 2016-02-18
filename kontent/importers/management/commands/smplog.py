from django.core.management.base import BaseCommand, CommandError
#import mysql.connector
#import _mysql
import MySQLdb
from kontent.models import Article

class Command(BaseCommand):
    help = 'Import the specified smplog instance'

    def add_arguments(self, parser):
        #parser.add_argument('host', nargs='+', type=str)
        parser.add_argument('host', type=str)
        parser.add_argument('database', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        self.stdout.write('host "%s"' % options['host'])
        self.stdout.write('database "%s"' % options['database'])
        self.stdout.write('username "%s"' % options['username'])
        self.stdout.write('password "%s"' % options['password'])

        db = MySQLdb.connect(host=options['host'],user=options['username'],
                     passwd=options['password'],db=options['database'])
        c = db.cursor()
        #  WHERE price < %s""", (max_price,))
        #messageid, date, user, ip, title, location, message, contenttype, commentsenabled, initiated, published, ispublic, modified, modifieddate from smplog_rant;')
        # 0         1     2     3   4      5         6        7            8                9          10         11        12        13
        c.execute('select messageid, date, user, ip, title, location, message, contenttype, commentsenabled, initiated, published, ispublic, modified, modifieddate from smplog_rant;')
        art = c.fetchone()
        artcounter = 0

        while art is not None:
            print art
            newart = Article()

            # Hardcoded for now
            #newart.sites
            newart.author_id = 1

            newart.published = art[1]
            newart.publish_from = art[1]
            if art[9]:
                newart.date_created = art[9]
            else:
                newart.date_created = art[1]
            newart.date_modified = art[13]
            newart.modified_times = art[12]

            newart.title = art[4]
            newart.body = art[6]
            newart.location = art[5]

            newart.comments_enabled = True
            if art[8] == 0:
                newart.comments_enabled = False

            newart.public = True
            if art[11] == 0:
                newart.public = False

            print newart.__dict__
            newart.save()
            artcounter += 1
            art = c.fetchone()
        #for poll_id in options['poll_id']:
        #    try:
        #        poll = Poll.objects.get(pk=poll_id)
        #    except Poll.DoesNotExist:
        #        raise CommandError('Poll "%s" does not exist' % poll_id)

        #    poll.opened = False
        #    poll.save()

        #    self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
        self.stdout.write(self.style.SUCCESS('Successfully imported %s articles from smplog blog from database "%s"' % artcounter, options['database']))
