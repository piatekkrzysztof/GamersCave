from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from GamersCave.models import Studio, GameRating


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(forms.Form):
    username = forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Hasla nie są zgodne")

    def clean_login(self):
        user_name=self.cleaned_data.get('login')
        user = User.objects.filter(username=user_name)
        if user:
            raise ValidationError("Podana nazwa użytkownika jest już zajęta")
        return user_name


class AddStudioForm(forms.Form):
    IS_ACTIVE = (
        (True, 'tak'),
        (False, 'nie'),
    )
    name = forms.CharField()
    is_active = forms.ChoiceField(choices=IS_ACTIVE)

class AddGameForm(forms.Form):

    name = forms.CharField()
    year=forms.IntegerField()
    description=forms.CharField(widget=forms.Textarea)
    studio = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['studio'].choices = [(studio.id, studio.name) for studio in Studio.objects.all()]

class AddArticleForm(forms.Form):
    title=forms.CharField(max_length=256)
    text=forms.CharField(widget=forms.Textarea)

class GameRatingForm(forms.Form):
    RATES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        (10, "10"),
    )
    rate = forms.ChoiceField(choices=RATES)
    reviews = forms.CharField(widget=forms.Textarea)


class Forum_postForm(forms.Form):
    title=forms.CharField(max_length=128)
    text=forms.CharField(widget=forms.Textarea)

class Post_answerForm(forms.Form):
    text=forms.CharField(widget=forms.Textarea)

# class Forum_post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=128)
#     text=models.TextField()
#     date= models.DateTimeField()
#
# class Post_answer(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField()
#     date = models.DateTimeField()

