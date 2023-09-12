from django.shortcuts import render, HttpResponseRedirect
from core.form import signUpForm, ArticleForm, ContactForms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import PostArticle
from twilio.rest import Client


# Create your views here.

def homeone(request):
    x = request.user.is_authenticated
    article = PostArticle.objects.all()
    return render(request,'core/homeone.html',{'isauth':x,'articles':article})


#login page

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                psswd=fm.cleaned_data['password']
                profile=authenticate(username=uname, password=psswd)
                if profile is not None:
                    login(request,profile)
                    messages.success(request,'Login Successfully')
                    return HttpResponseRedirect('/profile/')

        else:
            fm=AuthenticationForm()
    else:
        return HttpResponseRedirect('/profile/')
    return render(request,'core/login.html',{'form':fm})

#signup page
def user_signup(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=signUpForm(request.POST)
            if fm.is_valid():
                messages.success(request,'Account Successfully created!!')
                fm.save()
                fm=signUpForm()
               
        else:
            fm=signUpForm()
        return render(request,'core/signup.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')


#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


#about
def about(request):
    x = request.user.is_authenticated
    return render(request,'core/about.html',{'isauth':x})

#contact
def user_contact(request):
    if request.method=='POST':
        fm=ContactForms(request.POST)
        if fm.is_valid():
            nm=fm.cleaned_data['name']
            em=fm.cleaned_data['email']
            sj=fm.cleaned_data['subject']
            msg=fm.cleaned_data['message']
            x = f"Name: {nm}\n\nEmail: {em}\n\nSubject: {sj}\n\nMessage: {msg}"
            account_sid = 'AC161b7a452e96ad3b39612559898708ba'
            auth_token = '2db4c9bf1550f50ee5bd4d41598a196d'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=x,
            to='whatsapp:+919939212017'
            )
            print(x)
                    
    else:
        print("Ye GET request se aaya hai")
    x = request.user.is_authenticated
    fm=ContactForms()
    return render(request,'core/contact.html',{'isauth':x,'form':fm})
    
#profile

def user_profile(request):
    if request.user.is_authenticated:
        user=request.user
        full_name=user.get_full_name()
        article = PostArticle.objects.filter(authorusername=user)
        return render(request, 'core/profile.html', {'username':user,'full_name':full_name,'articles':article})
    else:
        return HttpResponseRedirect('/login/')

#addarticle
def add_article(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=ArticleForm(request.POST)
            if fm.is_valid():
                title=fm.cleaned_data['title']
                desc=fm.cleaned_data['desc']
                articleContent=fm.cleaned_data['articleContent']
                pst=PostArticle(title=title,desc=desc,articleContent=articleContent,authorusername=request.user)
                pst.save()
                fm=ArticleForm()  
        else:
            fm=ArticleForm()       

        return render(request, 'core/addarticle.html',{'form':fm,'isauth':request.user.is_authenticated})
    else:
        return HttpResponseRedirect('/login/')

#update article
def update_article(request,uid):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=ArticleForm(request.POST)
            if fm.is_valid():
                title=fm.cleaned_data['title']
                desc=fm.cleaned_data['desc']
                articleContent=fm.cleaned_data['articleContent']
                Toupdate=PostArticle.objects.get(pk=uid)
                Toupdate.title=title
                Toupdate.desc=desc
                Toupdate.articleContent=articleContent
                Toupdate.save()
                fm=ArticleForm()  
        else:
            fm=ArticleForm()       

        return render(request, 'core/updatearticle.html',{'form':fm,'isauth':request.user.is_authenticated})
    else:
        return HttpResponseRedirect('/login/')


#delete data

def delete_article(request,uid):
    if request.method=='POST':
        pi=PostArticle.objects.get(pk=uid)
        pi.delete()
        return HttpResponseRedirect('/profile/')


#show article
def show_article(request,uid):
    if request.user.is_authenticated:
        article = PostArticle.objects.get(pk=uid)
        return render(request,'core/showarticle.html',{'articles':article,'isauth':request.user.is_authenticated})
    else:
        article = PostArticle.objects.get(pk=uid)
        return render(request,'core/showarticle.html',{'articles':article})

#play article

from django.shortcuts import render
from django.http import HttpResponse
from gtts import gTTS
import tempfile
import os

def article_audio(request, article_id):
    article = PostArticle.objects.get(pk=article_id)
    text = article.articleContent
    tts = gTTS(text)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    temp_file.close()
    response = HttpResponse(content_type='audio/mpeg')
    response['Content-Disposition'] = f'attachment; filename="article_audio.mp3"'
    with open(temp_file.name, 'rb') as audio_file:
        response.write(audio_file.read())
    os.remove(temp_file.name)
    return response

