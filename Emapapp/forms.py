from django import forms
from .models import *
from django.contrib.auth.models import User

class PostForm(forms.Form):
	login = forms.CharField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput)

class RegForm(forms.ModelForm):
	username = forms.CharField(max_length=100000)
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username','password', 'email', 'first_name', 'last_name',)

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']

class CForm(forms.ModelForm):
	date = forms.CharField(max_length=100000)
	time = forms.CharField(max_length=100)
	class Meta:
		model = Celebr
		fields = ('name','descript', 'adress', 'incoords','quantity','thing','kategory',)

class ChaForm(forms.Form):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)

class ImageUploadForm(forms.Form):
	image = forms.ImageField()

class CodeForm(forms.Form):
	code = forms.CharField(max_length=100000)

class UseForm(forms.Form):
	user = forms.CharField(max_length=1000)