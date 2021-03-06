# -*- encoding: utf-8 -*-
from django import forms

from apps.article.models import Tag, Article, ArticleTag
from apps.dashboard.widgets import DatetimePickerInput, multiple_widget_generator
from apps.gallery.widgets import SingleImageInput


class TagForm(forms.ModelForm):

    class Meta(object):
        model = Tag
        fields = ['name', 'slug']


class ArticleForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('name'),
        label=u'Tags',
        help_text=u'Legg til kategori',
        required=False
    )

    class Meta(object):
        """
        Add fields that should have DTP activated in the datetimepicker_fields list
        """

        model = Article
        exclude = ['old_image']

        # Fields should be a mapping between field name and an attribute dictionary
        img_fields = [('image', {'id': 'responsive-image-id'})]
        dtp_fields = [('published_date', {})]
        widgetlist = [
            (DatetimePickerInput, dtp_fields),
            (SingleImageInput, img_fields)
        ]

        # Multiple widget generator merges results from regular widget_generator into a single widget dict
        widgets = multiple_widget_generator(widgetlist)
