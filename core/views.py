from django.shortcuts import render,redirect
import requests
import json
from pprint import pprint
from django.contrib import messages
from django.contrib.auth.models import User, auth
from core.models import Profile
from datetime import date
from django.contrib.auth.decorators import login_required

# Create your views here.

def news(country,interest):
  interests = interest.split('-')
  data = []
  for interest in interests:
    current_date = date.today()
    pprint(current_date)
    response = requests.get(f'https://newsapi.org/v2/everything?q={interest} {country}&from={current_date}&to={current_date}&sortBy=popularity&apiKey=a6f648fec53d4d1fbe57bb08798fdf69')
    resp = response.json()
    try:
      articles = resp['articles']
    except:
      articles = []
    
    
    i = 0
    if len(articles) != 0 or articles != None:
      for article in articles:
        if i >= 10:
          break
        title = article['title']
        excerpt = article['description']
        imageurl = article['urlToImage']
        link = article['url']
        obj = {
          'title':title,'excerpt':excerpt,'imageurl':imageurl,'link':link,'interest':interest
        }
        data.append(obj)
        i += 1
  return data    
  
def worldNews(interest):
  interests = interest.split('-')
  data = []
  for interest in interests:
    current_date = date.today()
    response = requests.get(f'https://newsapi.org/v2/everything?q={interest}&from={current_date}&to={current_date}&sortBy=popularity&apiKey=a6f648fec53d4d1fbe57bb08798fdf69')
    resp = response.json()
    try:
      articles = resp['articles']
    except:
      articles = []
    i = 0
    if len(articles) != 0 or articles != None:
      for article in articles:
        if i >= 10:
          break
        title = article['title']
        excerpt = article['description']
        imageurl = article['urlToImage']
        link = article['url']
        obj = {
          'title':title,'excerpt':excerpt,'imageurl':imageurl,'link':link,'interest':interest
        }
        data.append(obj)
        i += 1
  return data    
  
def searchNews(keyword):
  data = []
  current_date = date.today()
  response = requests.get(f'https://newsapi.org/v2/everything?q={keyword}&from={current_date}&to={current_date}&sortBy=popularity&apiKey=a6f648fec53d4d1fbe57bb08798fdf69')
  resp = response.json()
  try:
    articles = resp['articles']
  except:
    articles = []
  i = 0
  if len(articles) != 0 or articles != None:
    for article in articles:
      if i >= 10:
        break
      title = article['title']
      excerpt = article['description']
      imageurl = article['urlToImage']
      link = article['url']
      obj = {
        'title':title,'excerpt':excerpt,'imageurl':imageurl,'link':link,'interest':keyword
      }
      data.append(obj)
      i += 1
  return data    
  
  
@login_required(login_url='login')      
def index(request):
  user_model = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_model)
  interest = user_profile.interests
  country = user_profile.country
  data = news(country,interest)
  return render(request,'index.html',{'data':data})

@login_required(login_url='login')
def explore(request):
  user_model = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_model)
  interest = user_profile.interests

  data = worldNews(interest)
  
  return render(request,'explore.html',{'data':data})

@login_required(login_url='login')
def search(request):
  data = []
  if request.method == 'POST':
    keyword = request.POST['keyword']
    if keyword != " " or keyword != None:
     data = searchNews(keyword)
  
  return render(request,'search.html',{'data':data})
  
def register(request):
  if request.method == 'POST':
    username = request.POST['username']
    password  = request.POST['password']
    password2  = request.POST['password2']
        
    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.info(request, 'Username Taken')
        return redirect('register')
      else:
        user = User.objects.create_user(username=username,password=password)
        user.save()
        user_login = auth.authenticate(username=username,password=password)
        auth.login(request, user_login)
        user_model = User.objects.get(username=username)
        profile = Profile.objects.create(user=user_model)
        profile.save()
        return redirect('/interests')
    else:
      messages.info(request, 'Password does not match')
      return redirect('register')
   
  return render(request,'register.html') 
  
def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
        
        
    user = auth.authenticate(username=username,password=password)
        
    if user is not None:
      auth.login(request,user)
      return redirect('/')
    else:
      messages.info(request, 'Credentials Invalid')
      return redirect('login')
  return render(request,'login.html') 

@login_required(login_url='login')
def interest(request):
  if request.method == 'POST':
    country = request.POST['countries']
    interest = request.POST.getlist('tag')
    if len(interest) <= 7:
      messages.info(request, 'You should have more than seven field of interest')
      return redirect('/interests')
    interests = "-".join(interest)
    user_model = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_model)
    user_profile.country = country
    user_profile.interests = interests
    user_profile.save()
    return redirect('/')
  return render(request,'tag.html') 

@login_required(login_url='login')
def about(request):
  return render(request,'about.html')
  
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')