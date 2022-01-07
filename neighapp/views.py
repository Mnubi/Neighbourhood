from os import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http  import HttpResponse

# Create your views here.
def welcome(request):
    return HttpResponse('Welcome to the Moringa Tribune')

# created view for homepage
@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    if profile is None:
        profile = Profile.objects.filter(
            user_id=current_user.id).first()  # get profile
        posts = Post.objects.filter(user_id=current_user.id)
        # get all locations
        locations = Location.objects.all()
        neighbourhood = Neighbourhood.objects.all()   
        businesses = Business.objects.filter(user_id=current_user.id)
        contacts = Contact.objects.filter(user_id=current_user.id)
        return render(request, "profile.html", {"danger": "Update Profile by selecting Your Neighbourhood name to continue 😥!!", "locations": locations, "neighbourhood": neighbourhood, "businesses": businesses, "contacts": contacts, "posts": posts})
    else:
        neighbourhood = profile.neighbourhood
        # get all posts in the neighbourhood of the user ordered by date
        posts = Post.objects.filter(neighbourhood=neighbourhood).order_by("-created_at")
        return render(request, 'index.html', {'posts': posts})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(
        user_id=current_user.id).first()  # get profile
    posts = Post.objects.filter(user_id=current_user.id)
    locations = Location.objects.all()
    neighbourhood = Neighbourhood.objects.all()
    businesses = Business.objects.filter(user_id=current_user.id)
    contacts = Contact.objects.filter(user_id=current_user.id)

    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'locations': locations, 'neighbourhood': neighbourhood, 'categories': category, 'businesses': businesses, 'contacts': contacts})
