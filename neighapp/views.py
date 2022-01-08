from os import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.http  import HttpResponse
from django.contrib.auth.models import User
from .form import BusinessForm, PostForm, ProfileForm, UpdateProfileForm, NeighbourhoodForm
from .models import Profile,Neighbourhood,Post,Business,Location


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

@login_required(login_url='/accounts/login/')
def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id = user)
    form = UpdateProfileForm(instance=profile)
    if request.method == "POST":
            form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():  
                
                profile = form.save(commit=False)
                profile.save()
                return redirect('profile') 
            
    return render(request, 'update_profile.html', {"form":form})

@login_required(login_url='/accounts/login/')
def neighbourhood(request):
    
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.admin = request.user

            neighbourhood.save()

        return redirect('index')

    else:
        form = NeighbourhoodForm()
    return render(request, 'neighbourhood.html', {"form": form})

@login_required(login_url='/accounts/login/')
def post(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user

            post.save()

        return redirect('index')

    else:
        form = PostForm()
    return render(request, 'post.html', {"form": form})

@login_required(login_url="/accounts/login/")
def contacts(request):
    current_user = request.user
    # get current user neighbourhood
    profile = Profile.objects.filter(user_id=current_user.id).first()
    # check if user has neighbourhood
    if profile is None:
        profile = Profile.objects.filter(
            user_id=current_user.id).first()  # get profile
        posts = Post.objects.filter(user_id=current_user.id)
        # get all locations
        locations = Location.objects.all()
        neighbourhood = Neighbourhood.objects.all()
        businesses = Business.objects.filter(user_id=current_user.id)
        contacts = Contact.objects.filter(user_id=current_user.id)
        # redirect to profile with error message
        return render(request, "contacts.html", {"locations": locations, "neighbourhood": neighbourhood, "businesses": businesses, "contacts": contacts, "posts": posts})
    else:
        neighbourhood = profile.neighbourhood
        # get all contacts where the neighbourhood is the same as the user neighbourhood
        contacts = Contact.objects.filter(
            neighbourhood=profile.neighbourhood).order_by("-created_at")
        return render(request, "contacts.html", {"contacts": contacts, "neighbourhood": profile.neighbourhood})