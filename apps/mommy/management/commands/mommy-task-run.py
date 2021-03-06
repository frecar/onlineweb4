from django.core.management.base import BaseCommand, CommandError
from apps import mommy

class Command(BaseCommand):
    args = 'name of job'
    help = 'run a job'

    def print_job_names(self):
        possible_jobs = []
        for task, _ in mommy.schedule.tasks.iteritems():
            possible_jobs.append(task.__name__)
        print "possible jobs:" + str(possible_jobs)

    def handle(self, *args, **options):
        mommy.autodiscover()

        if(len(args) == 0):
            self.print_job_names()
            return

        # run shit
        do_name = args[0]
        for task, _ in mommy.schedule.tasks.iteritems():
            if(task.__name__ == do_name):
                task.run()
                return
        print "could not find job:" + do_name
