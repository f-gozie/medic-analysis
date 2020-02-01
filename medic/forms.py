from django import forms
from django.contrib.auth.models import User
from medic.models import UserProfile, Ailment, Analysis


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('number',)

BG_CHOICES = (('A', 'a'), ('B', 'b'), ('AB', 'ab'), ('O', 'o'))
GENDER_CHOICES = (('Male', 'M'), ('Female', 'F'))

class AnalysisForm(forms.ModelForm):
	blood_group = forms.ChoiceField(widget=forms.RadioSelect, choices=BG_CHOICES)
	gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES)
	ailments = forms.ModelMultipleChoiceField(queryset=Ailment.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Analysis
		fields = ('blood_group', 'height', 'weight', 'gender', 'ailments',)