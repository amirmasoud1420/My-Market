from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    rate = forms.IntegerField(
        required=False,
        validators=[rate_validator],
    )

    class Meta:
        model = Comment
        fields = ['comment', 'rate']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
