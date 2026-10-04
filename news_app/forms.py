from django import forms
from .models import Contacts,Comment

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']