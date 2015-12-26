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
        #db = _mysql.connect(host=options['host'],user=options['username'],
        #          passwd=options['password'],db=options['database'])
        #db.query('select * from smplog_rant;')
        #r = db.use_result()
        #art = r.fetch_row()
        db = MySQLdb.connect(host=options['host'],user=options['username'],
                     passwd=options['password'],db=options['database'])
        c = db.cursor()
        #c.execute("""SELECT spam, eggs, sausage FROM breakfast
        #  WHERE price < %s""", (max_price,))
        c.execute('select * from smplog_rant;')
        art = c.fetchone()

        print art
        newart = Article()
        newart.published = art[1]
        newart.publish_from = art[1]
        newart.title = art[4]
        print newart.__dict__
        #for poll_id in options['poll_id']:
        #    try:
        #        poll = Poll.objects.get(pk=poll_id)
        #    except Poll.DoesNotExist:
        #        raise CommandError('Poll "%s" does not exist' % poll_id)

        #    poll.opened = False
        #    poll.save()

        #    self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
