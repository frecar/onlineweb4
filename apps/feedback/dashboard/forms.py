# -*- coding: utf-8 -*-
from django import forms

from apps.feedback.models import Feedback
from apps.feedback.models import TextQuestion
from apps.feedback.models import RatingQuestion
from apps.feedback.models import MultipleChoiceRelation

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        exclude = ('author',)


class TextQuestionForm(forms.ModelForm):

	class Meta:
		model = TextQuestion
		exclude = ('feedback',)

class RatingQuestionForm(forms.ModelForm):

	class Meta:
		model = RatingQuestion
		exclude = ('feedback',)


class MultipleChoiceQuestionForm(forms.ModelForm):

	class Meta:
		model = MultipleChoiceRelation
		exclude = ('feedback',)
