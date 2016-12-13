import re
from dal import autocomplete
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from . import models

User = get_user_model()

#Custom Form Widgets
class MangaChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

#Custom Forms
class RegistrationForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=128)), label=_("Username"))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=128, render_value=False)), label=_("Password"))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=128, render_value=False)), label=_("Password (again)"))
  email = forms.EmailField(required=False,widget=forms.TextInput(attrs=dict(max_length=128)), label=_("Email (optional)"))
  
  def clean_username(self):
    try:
      user = User.objects.get(username=self.cleaned_data['username'])
    except User.DoesNotExist:
      return self.cleaned_data['username']
    raise forms.ValidationError(_("The username already exists. Please try another one."))

  def clean_email(self):
    if ('email' not in self.cleaned_data):
      self.cleaned_data['email'] = ""
    return self.cleaned_data['email']

  def clean(self):
    if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
      if self.cleaned_data['password1'] != self.cleaned_data['password2']:
        raise forms.ValidationError(_("The two password fields did not match."))
      return self.cleaned_data

class BookmarkForm(forms.Form):
  manga = MangaChoiceField(widget=autocomplete.ModelSelect2(url='manga-autocomplete',attrs={'data-minimum-input-length': 3,'data-placeholder': 'Manga title here...'}), queryset=models.Manga.objects.all())
  release = forms.CharField(required=False, widget=forms.TextInput(attrs=dict(required=False, max_length=128, placeholder='Current chapter here...')), label=_("Chapter"))


class ProfileForm(forms.Form):
  email = forms.EmailField(widget=forms.TextInput(attrs=dict(max_length=128)), label=_("Email"))
  notifications = forms.ChoiceField(choices=models.User.frequency_choices, label=_("Notification Frequency"))

  def clean_email(self):
    if ('email' not in self.cleaned_data):
      self.cleaned_data['email'] = ""
    return self.cleaned_data['email']