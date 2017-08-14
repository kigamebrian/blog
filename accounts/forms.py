from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from.models import About,UserProfile


class RegistrationForm(UserCreationForm):
	email =forms.EmailField(required=True)
	class Meta:
		model =User
		fields =('username','first_name','last_name','email','password1','password2')




	def  e(self,commit=True):
		user =super(RegistrationForm,self).save(commit=False)
		user.first_name=self.cleaned_data['first_name']
		user.last_name=self.cleaned_data['last_name']
		user.email=self.cleaned_data['email']
		password1=self.cleaned_data['password1']

		if commit: 
			user.save()

		return user

class EditProfileForm(forms.ModelForm):
	class Meta:

		model=UserProfile

		fields=(
			'email',
			'username',
			'first_name',
			'last_name',
			'email',
			'description',
			'city',
			'phone',
			'website',
			'image',
			

			
			)

class About(forms.ModelForm):
	class Meta:
		model= About
		
		fields=(
		"mission",
		"about",
		
		)

TOPIC_CHOICES = (
	('general', 'General enquiry'),
	('bug', 'Bug report'),
	('suggestion', 'Suggestion'),
	('complain',"complain report"),
	('comment',"comment something about us"),
	)
class ContactForm(forms.Form):
	topic = forms.ChoiceField(choices=TOPIC_CHOICES)
	message = forms.CharField(widget=forms.Textarea)
	sender = forms.EmailField(required=False)

	def clean_message(self):
		message = self.cleaned_data.get('message', '')
		num_words = len(message.split())
		if num_words < 4:
			raise forms.ValidationError("Not enough words!")
		return message