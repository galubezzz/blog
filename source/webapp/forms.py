from django import forms
from .models import Article, Comment, Rate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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


# class RatingForm(forms.ModelForm):
#     # def clean(self):
#     #     rate = self.instance
#     #     user = rate.user
#     #     article = rate.article
#     #
#     #     objects = Rate.objects.filter(user=user, article=article)
#     #
#     #     if len(objects) > 0:
#     #         msg = "User can rate article only once"
#     #         self._errors["article"] = self.error_class([msg])
#     #         raise ValidationError(msg)
#     #
#     #     return super().clean()
#
#     class Meta:
#         model = Rate
#         fields = ['rate']
