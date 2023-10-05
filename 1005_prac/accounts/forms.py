from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    nickname = forms.CharField(max_length=30, required=True,
                               help_text='필요 시 닉네임을 지정하세요.')
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('nickname', )