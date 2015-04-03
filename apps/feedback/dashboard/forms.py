# -*- coding: utf-8 -*-
from django import forms

from apps.feedback.models import Feedback
from apps.feedback.models import TextQuestion

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        exclude = ('author',)


class TextQuestionForm(forms.ModelForm):

	class Meta:
		model = TextQuestion
		exclude = ('feedback',)
