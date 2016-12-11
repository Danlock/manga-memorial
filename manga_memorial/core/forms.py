import re
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from . import models

User = get_user_model()

#Custom widgets
class ListTextWidget(forms.TextInput):
  def __init__(self, data_list, name, *args, **kwargs):
    super(ListTextWidget, self).__init__(*args, **kwargs)
    self._name = name
    self._list = data_list
    self.attrs.update({'list': 'list__{}'.format(self._name)})

  def render(self, name, value, attrs=None):
    text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
    data_list = '<datalist id="list__{}">'.format(self._name,self._name)
    for item in self._list:
      data_list += '<option value="{}">{}</option>'.format(item[0], item[1])
    data_list += '</datalist>'
    return '<div id="div_list__{}">'.format(self._name) + text_html + data_list + '</div>'


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
  # manga = forms.CharField(widget=ListTextWidget(attrs=dict(required=True, max_length=2048), data_list=models.MangaList.getMangaListForAutocomplete(), name="manga_list"), label=_("Manga"))
  manga = forms.ChoiceField(required=True, label=_("Manga"),choices=models.MangaList.getMangaListForAutocomplete())
  release = forms.CharField(required=False,widget=forms.TextInput(attrs=dict(required=False, max_length=128)), label=_("Chapter"))

  def clean_manga(self):
    mangas = models.MangaList.getMangaList()
    if self.cleaned_data['manga'] not in mangas:
      raise forms.ValidationError(_("That manga does not exist on mangaupdates.com."))
    else:
      return self.cleaned_data['manga']

class ProfileForm(forms.Form):
  email = forms.EmailField(widget=forms.TextInput(attrs=dict(max_length=128)), label=_("Email"))
  notifications = forms.ChoiceField(choices=models.User.frequency_choices, label=_("Notification Frequency"))

  def clean_email(self):
    if ('email' not in self.cleaned_data):
      self.cleaned_data['email'] = ""
    return self.cleaned_data['email']