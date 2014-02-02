# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger("mommy")

from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.contenttypes.models import ContentType


from django.template import Context
from django.template.loader import get_template


from apps.mommy import Task, schedule
from apps.feedback.models import FeedbackRelation
from apps.events.models import Event, AttendanceEvent, Attendee


class MailEventWrapper(object):
    """
    A simple wrapper around FeedbackRelation that assumes that the related
    object is an Event.

    This wrapper sends mails to users.
    """
    def __init__(self, fbr):
        self.fbr = fbr
        self.admin_email = fbr.admin_email
        self.url = fbr.get_absolute_url()
        self.results_url = fbr.get_absolute_url() + "results"

        self.lazy_user_emails = [user.email for user in fbr.lazy_users]

        self.title = fbr.title
        self.object_id = fbr.object_id
        self.content_type = fbr.content_type
        self.dotkom_mail = "dotkom@online.ntnu.no"
        self.give_marks = fbr.give_marks

        if(fbr.start_date):
            self.start_date = fbr.start_date.strftime("%d. %B").encode("utf-8")
        else:
            self.start_date = ""

    def send_marks(self):
        """
        Send email to lazy users that they have received a mark.
        """
        if(self.give_marks):
            logger.debug(u"sending marks mail for %s, (%s %s)" %
                    (self.title, self.object_id, self.content_type))

            plaintext = get_template('feedback_marks_mail.txt')
            d = Context({
                    'admin_mail': self.admin_mail
                })

            body = plaintext.render(d)
            logger.debug("to: %s\n body:%s", self.lazy_user_emails, body)
            EmailMessage(subject, body, self.admin_mail, [], lazy_user_emails).send()

    def send_feedback(self, last_warning=False):
        """
        Mail to users
        """
        logger.debug(u"Sending reminder emails for %s, last_warning=%s, (%s %s)" %
                (self.title, last_warning, self.object_id, self.content_type))

        plaintext = get_template('feedback_mail.txt')

        d = Context({
                'title': self.title,
                'start_date': self.start_date,
                'deadline': deadline,
                'admin_mail': self.admin_mail
            })

        body = plaintext.render(d)
        logger.debug("to: %s\n body:%s", self.lazy_user_emails, body)


        EmailMessage(subject, body, self.admin_mail, [], self.lazy_user_emails).send()

    def send_feedback_admin(self):
        """
        Mail to admins, when feedback starts
        """
        plaintext = get_template('feedback_admin_mail.txt')
        d = Context({
                'title': self.title,
                'link': self.link(results=True)
            })
        body = plaintext.render(d)
        logger.debug("to: %s\n body:%s", self.lazy_user_emails, body)
        EmailMessage(subject, body, "dotkom@online.ntnu.no", [], self.admin_mail).send()

    def send_feedback_admin_results(self, lazy_user_emails):
        """
        Mail to admins when feedback ends
        """
        logger.debug(u"Sending results email for %s, (%s %s)" %
                (self.title, self.object_id, self.content_type))

        plaintext = get_template('feedback_results_mail.txt')
        d = Context({
                'title': self.title,
                'link': self.link(results=True)
            })

        body = plaintext.render(d)
        logger.debug("to: %s\n body:%s", self.lazy_user_emails, body)
        EmailMessage(subject, body, "dotkom@online.ntnu.no", [], self.admin_mail).send()


class EventFeedback(Task):
    """
    Business logic for sending mails to users

    Sets marks and sends emails to various recipients
    """
    @staticmethod
    def run():
        logger.debug(u"Kjører EventFeedbackMail.run()")

        # collect all feedbacks for events
        event_type = ContentType.objects.get_for_model(Event)
        active_feedbacks = FeedbackRelation.objects.filter(active=True,
                content_type=event_type)

        for fbr in active_feedbacks:
            logger.debug(u"EventFeedbackMail.run() for %s, (%s %s)" %
                    (fbr.title, fbr.object_id, fbr.content_type))

            mailer = MailEventWrapper(fbr)

            # collect some dates
            locale.setlocale(locale.LC_ALL, "nb_NO.UTF-8")
            today = timezone.now().date()
            yesterday = today + datetime.timedelta(days=-1)
            deadline_diff = (feedback.deadline - today).days


            # skip it if already done.
            deadline_sendt = fbr.content_object.deadline_sendt
            if(deadline_sendt and deadline_diff <= deadline_sendt):
                logger.debug(u"EventFeedbackMail already done for %s, (%s %s)" %
                    (fbr.title, fbr.object_id, fbr.content_type))
                return

            # send and set marks
            if(deadline_diff < 0):
                logger.debug(u"Final deadline passed for %s, (%s %s)" %
                    (fbr.title, fbr.object_id, fbr.content_type))

                fbr.active = False
                fbr.save()

                EventFeedbackMail.give_marks(fbr)
                mailer.send_marks()

            # last warning
            elif(deadline_diff < 1):
                mailer.send_feedback_mail(last_warning=True)
                mailer.send_admin_results_mail()

            # send reminder mail
            elif(deadline_diff < 3 and fbr.gives_mark):
                logger.debug(u"Sending reminder emails for %s, (%s %s)" %
                        (fbr.title, fbr.object_id, fbr.content_type))
                mailer.send_feedback_mail()

            # send first notification mails
            elif(first_notification_date(fbr)):
                logger.debug(u"Sending first reminder emails for %s, (%s %s)" %
                        (fbr.title, fbr.object_id, fbr.content_type))
                mailer.send_feedback_mail()
                mailer.send_feedback_admin_mail()


    @staticmethod
    def give_marks(title, fbr):
        mark = Mark()
        mark.title = u"Manglende tilbakemelding på %s" % (title)
        mark.category = 4 #Missed feedback
        mark.description = u"Du har fått en prikk fordi du ikke har levert tilbakemelding."
        mark.save()

        for user in fbr.lazy_users:
            user_entry = UserEntry()
            user_entry.user = user
            user_entry.mark = mark
            user_entry.save()

    def send_first_notification(fbr):
        #The object that requires feedback doesnt have a start date
        if not fbr.start_date:
            yesterday = timezone.now().date() - datetime.timedelta(days=1)
            if feedback.created_date == yesterday.date():
                #Send the first notification the day after the feedback relation was created
                return True
        else:
            day_after_event = fbr.start_date.date() + datetime.timedelta(1)
            if day_after_event == datetime.datetime.date(timezone.now()):
                #Send the first notification the day after the event
                return True
        return False

schedule.register(EventFeedback, day_of_week='mon-sun', hour=8, minute=00)
