from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CustomerForm(ModelForm):
	class Meta:
		model = Dashboard_user
		fields = '__all__'
		exclude = ['user']

# class OrderForm(ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = '__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

# class DataForm(ModelForm):
# 	class Meta:
# 		model = CompanyData
# 		fields = ['name', 'gender_code', 'aboriginal_peoples', 'visible_minorities', 'person_with_disabilities', 'position_category']

size_choices = (
	('small', 'small'),
	('medium', 'medium'),
	('large', 'large'),

)


class DataForm(forms.Form):

		company_name = forms.CharField()
		company_size = forms.ChoiceField(choices=size_choices, required=False)
		year_collected = forms.IntegerField(required=True)
		file = forms.FileField()

# class CompanySizeform(forms.Form):

# 		model = CompanySize
# 		fields = ['small', 'medium', 'large']
		

