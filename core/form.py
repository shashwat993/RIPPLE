from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import PostArticle



class signUpForm(UserCreationForm):
    mobileno = forms.IntegerField(label="Mobile Number")
    class Meta:
        model = User
        fields=['username','first_name','last_name','email','mobileno']
        labels={'email':'Email'}


class ArticleForm(forms.ModelForm):
    class Meta:
        model=PostArticle
        fields=["title","desc","articleContent"]
        labels={'title':"Title",'desc':"Description",'articleContent':"Write Article"}
        widgets={'title':forms.Textarea(attrs={'placeholder':"Add title of your Article",'rows':1}),
                'desc':forms.Textarea(attrs={'placeholder':"Add description of your Article",'rows':2}),
                'articleContent':forms.Textarea(attrs={'placeholder':"Write your Article",'rows':8}),
          }




class ContactForms(forms.Form):
    name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})
    )
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'})
    )
    message = forms.CharField(
        max_length=300,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 3})
    )
