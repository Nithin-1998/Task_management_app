from django import forms
from.models import CustomUser
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email','password','file','images')