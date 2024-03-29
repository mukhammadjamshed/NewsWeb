from django import forms
from .models import Contact, CommentModel


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class SubscriptionForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    email = forms.EmailField()
class CommentForm(forms.ModelForm):


    class Meta:
        model = CommentModel
        fields = ['body']