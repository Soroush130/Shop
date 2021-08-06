from django import forms
from shop_account.models import UserAccount, Profile


class LoginUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterUserForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        is_exists_email = UserAccount.objects.filter(email=email).exists()
        if is_exists_email:
            raise forms.ValidationError("چنین ایمیلی قبلا ثبت شده است")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['email', 'name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'f_name', 'l_name', 'address', 'avatar_image']

