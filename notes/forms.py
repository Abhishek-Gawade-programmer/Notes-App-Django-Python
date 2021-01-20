from django import forms
from .models import Note,Note_Password
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()
	class Meta:
		model=User
		fields=['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
	email=forms.EmailField()

	class Meta:
		model=User
		fields=('username','email')

class NoteForm(forms.ModelForm):
	class Meta:
		exclude=['author','category']
		model = Note

class Note_PasswordForm(forms.ModelForm):
    class Meta:
        model = Note_Password
        
        fields = ('password',)
        widgets={
        'password':forms.PasswordInput(),
        }


class Note_Change_PasswordForm(forms.Form):
	password=forms.CharField(widget=forms.PasswordInput,label='Enter Your <b>Old</b> Password')
	password1= forms.CharField(widget=forms.PasswordInput,label='Enter Your <b style="color: red">New</b> Password')

class Note_Confirm_PasswordForm(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput,label="Enter Your Note's Password")

class Share_the_PostForm(forms.Form):
	email=forms.EmailField(label="Enter The Email To Whoom Share",help_text='A valid email address, please.')
	subject=forms.CharField(label="Enter The Subject For Email")
	content=forms.CharField(widget=forms.Textarea,label="Enter The Message You Want To Send")
	

   
    
    


    
    
        


    