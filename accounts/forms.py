from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','username','email','password']

    def clean(self):
        cleaned_data = super(RegistrationForm , self ).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match!'
            )
    def __init__(self, *args , **kwargs):
        super(RegistrationForm,self).__init__(*args , **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Foulen'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Fouleni'
        self.fields['username'].widget.attrs['placeholder'] = 'Foulen123'
        self.fields['email'].widget.attrs['placeholder'] = 'Foulen@****.com'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'