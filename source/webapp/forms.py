from django import forms
from .models import Article, Comment
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    def clean(self):
        if not self.cleaned_data['text'] and not self.cleaned_data['image']:
            raise forms.ValidationError('Хотя бы одно из полей "Текст" и "Картинка" должно быть заполнено.')
        return super().clean()

    class Meta:
        model = Article
        fields = ['title', 'text', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
