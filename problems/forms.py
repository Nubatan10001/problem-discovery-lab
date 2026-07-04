from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ConversationMessage, ProblemIdea


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='メールアドレス', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProblemIdeaForm(forms.ModelForm):
    class Meta:
        model = ProblemIdea
        fields = ['raw_memo', 'category', 'status']
        widgets = {
            'raw_memo': forms.Textarea(attrs={
                'rows': 7,
                'placeholder': '例: 会議後に議事録を書くのが面倒だった。誰かが自動で要点を整理してくれたら助かる。',
            }),
            'category': forms.TextInput(attrs={'placeholder': '例: 業務効率化、教育、研究、生活'}),
        }


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']
        labels = {'content': 'AIへの返信'}
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'AIからの質問に答えてください。分かる範囲の短い返答で大丈夫です。',
            })
        }
