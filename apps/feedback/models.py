#-*- coding: utf-8 -*-
'''
An anonymous customizable Feedback Schema application.

An Object is connected to a customizable Feedback through FeedbackRelation,
A Feedback can have many Questions.
An Answer is related to an Object and a Question.

This implementation is not very database friendly however, as it does
very many database lookups.
'''
import uuid

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from apps.authentication.models import OnlineUser as User
from apps.authentication.models import FIELD_OF_STUDY_CHOICES

class FeedbackRelation(models.Model):
    """
    A many to many relation between a Generic Object and a Feedback schema.
    """
    feedback = models.ForeignKey('Feedback')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    deadline = models.DateField()
    gives_mark = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # Keep a record of who has answered. (not /what/ they have answered)
    answered = models.ManyToManyField(
        User,
        related_name='feedbacks',
        blank=True,
        null=True)

    class Meta:
        unique_together = ('feedback', 'content_type', 'object_id')

    @property
    def questions(self):
        return self.feedback.questions

    @property
    def ratingquestion(self):
        return self.feedback.ratingquestions

    @property
    def description(self):
        return self.feedback.description

    @property
    def answers(self):
        """
        All answers related to this FeedbackRelation.
        It's a property of the FeedbackRelation, so that when we know
        the Feedback schema and the Object, we can easily get all the
        answers.

        NB!: When creating more Question types, add their answers here
        """
        answers = []
        answers.extend(self.field_of_study_answers.all())
        answers.extend(self.text_answers.all())
        answers.extend(self.rating_answers.all())
        return sorted(answers, key=lambda x: x.order)  # sort by order

    def answers_to_question(self, question):
        return question.answer.filter(feedback_relation=self)

    def __unicode__(self):
        return str(self.feedback_id) + ': ' + str(self.content_object)

    def get_absolute_url(self):
        """
        Returns the absolute URL to its `views.feedback`
        """
        return reverse("apps.feedback.views.feedback",
                       args=[self.content_type.app_label,
                             self.content_type.model,
                             self.object_id,
                             self.feedback.feedback_id])

    def can_answer(self, user):
        """
        Is the user in conent_object.feedback_users?
        if the conent_object does not have feedback_user, everyone can aswer.
        """
        if user in self.answered.all():
            return False

        if hasattr(self.content_object, "feedback_users"):
            feedback_users = self.content_object.feedback_users
            if user not in feedback_users:
                return False
        return True

    @property
    def lazy_users(self):
        """
        People that has not answered the feedback.
        """
        if hasattr(self.content_object, "feedback_users"):
            feedback_users = set(self.content_object.feedback_users)
            answered = set(self.answered.all())
            return feedback_users.difference(answered)
        return []

    @property
    def admin_mail(self):
        if hasattr(self.content_object, "feedback_mail"):
            return self.content_object.feedback_mail

    @property
    def title(self):
        if hasattr(self.content_object, "feedback_title"):
            return self.content_object.feedback_title

    @property
    def start_date(self):
        if hasattr(self.content_object, "feedback_date"):
            return self.content_object.feedback_date

    def save(self, *args, **kwargs):
        new_fbr = not self.pk
        super(FeedbackRelation, self).save(*args, **kwargs)
        if new_fbr:
            token = uuid.uuid4().hex
            rt = RegisterToken(fbr = self, token = token)
            rt.save()

class Feedback(models.Model):
    """
    A customizable Feedback schema.
    """
    feedback_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User)
    description = models.CharField(_(u'beskrivelse'), max_length=100)

    @property
    def ratingquestions(self):
        rating_question = []
        rating_question.extend(self.rating_questions.all())
        return rating_question

    @property
    def questions(self):
        """
        All questions related to this Feedback schema.
        All the different question types are grouped together in this
        property to easily get all the questions related to this
        Feedback schema.

        NB!: When creating more Question types, add them here.
        """
        questions = []
        questions.extend(self.text_questions.all())
        questions.extend(self.rating_questions.all())
        return sorted(questions, key=lambda x: x.order)  # sort by order

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _(u'tilbakemelding')
        verbose_name_plural = _(u'tilbakemeldinger')



class FieldOfStudyAnswer(models.Model):
    feedback_relation = models.ForeignKey(
        FeedbackRelation,
        related_name="field_of_study_answers")

    answer = models.SmallIntegerField(
        _(u'Studieretning'), choices = FIELD_OF_STUDY_CHOICES)

    def __unicode__(self):
        return self.get_answer_display()

class TextQuestion(models.Model):
    feedback = models.ForeignKey(
        Feedback,
        related_name='text_questions')

    order = models.SmallIntegerField(_(u'Rekkefølge'), default=10)

    label = models.CharField(_(u'Spørsmål'), blank=False, max_length=256)

    def __unicode__(self):
        return self.label


class TextAnswer(models.Model):
    question = models.ForeignKey(TextQuestion, related_name='answer')

    feedback_relation = models.ForeignKey(
        FeedbackRelation,
        related_name="text_answers")

    answer = models.TextField(_(u'svar'), blank=False)

    def __unicode__(self):
        return self.answer

    @property
    def order(self):
        return self.question.order


RATING_CHOICES = [(k, str(k)) for k in range(1, 7)]  # 1 to 6


class RatingQuestion(models.Model):
    feedback = models.ForeignKey(
        Feedback,
        related_name='rating_questions')

    order = models.SmallIntegerField(_(u'Rekkefølge'), default=20)

    label = models.CharField(_(u'Spørsmål'), blank=False, max_length=256)

    def __unicode__(self):
        return self.label


class RatingAnswer(models.Model):
    feedback_relation = models.ForeignKey(
        FeedbackRelation,
        related_name="rating_answers")

    answer = models.SmallIntegerField(
        _(u'karakter'),
        choices=RATING_CHOICES,
        default=0)

    question = models.ForeignKey(RatingQuestion, related_name='answer')

    def __unicode__(self):
        return self.get_answer_display()

    @property
    def order(self):
        return self.question.order

#For creating a link for others(companies) to see the results page
class RegisterToken(models.Model):
    fbr = models.ForeignKey(FeedbackRelation, related_name="Feedback_relation")
    token = models.CharField(_(u"token"), max_length=32)
    created = models.DateTimeField(_(u"opprettet dato"), editable=False, auto_now_add=True)

    @property
    def is_valid(self):
        return True

        #valid_period = datetime.timedelta(days=365)#1 year
        #now = timezone.now()
        #return now < self.created + valid_period
