from os import name
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeDoneView
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.http  import HttpResponse
from django.contrib.auth.models import User
from .form import BusinessForm, PostForm, ProfileForm, UpdateProfileForm, NeighbourhoodForm
from .models import Profile,Neighbourhood,Post,Business,Location


# Create your views here.
def welcome(request):
    return HttpResponse('Welcome to the Moringa Tribune')

# created view for homepage
# @login_required(login_url='/accounts/login/')
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

    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'locations': locations, 'neighbourhoods': neighbourhood, 'businesses': businesses, 'contacts': contacts})


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
        return render(request, "index.html", {"locations": locations, "neighbourhoods": neighbourhood, "businesses": businesses, "contacts": contacts, "posts": posts})
    else:
        neighbourhood = Neighbourhood.objects.all()
        # get all posts in the neighbourhood of the user ordered by date
        posts = Post.objects.filter(neighbourhood=neighbourhood).order_by("-timestamp")
        return render(request, 'index.html', {'posts': posts})


@login_required(login_url='/accounts/login/')
def update_profile(request,id):
    Profile.objects.get_or_create(user=request.user)
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


def posts(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    posts = Post.objects.filter(user_id=current_user.id)
    if profile is None:
        profile = Profile.objects.filter(
            user_id=current_user.id).first() 
        posts = Post.objects.filter(user_id=current_user.id)
        
        locations = Location.objects.all()
        neighbourhood = Neighbourhood.objects.all()
        
        businesses = Business.objects.filter(user_id=current_user.id)
        
        return render(request, "profile.html", {"danger": "Update Profile ", "locations": locations, "neighbourhood": neighbourhood,  "businesses": businesses,"posts": posts})
    else:
        neighbourhood = profile.neighbourhood
        posts = Post.objects.filter(user_id=current_user.id)
        return render(request, "alert.html", {"posts": posts})

login_required(login_url="/accounts/login/")
def create_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.neighbourhood = neighbourhood
            post.user=current_user
            post.save()
            return redirect('/posts')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

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


def join_neighbourhood(request, id):
    neighbourhood = get_object_or_404(Neighbourhood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('index')

def leave_neighbourhood(request, id):
    neighbourhood = get_object_or_404(Neighbourhood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('index')

@login_required(login_url="/accounts/login/")
# alerts page
def alerts(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    locations = Location.objects.all()
    neighbourhood = Neighbourhood.objects.all()
    businesses = Business.objects.filter(user_id=current_user.id)
    contacts = Contact.objects.filter(user_id=current_user.id)
    
    return render(request, "alert.html", {"locations": locations, "neighbourhood": neighbourhood, "businesses": businesses, "contacts": contacts, "posts": posts})
    

@login_required(login_url='/accounts/login/')
def business(request):
    current_user = request.user
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user

            business.save()

        return redirect('index')

    else:
        form = BusinessForm()
    return render(request, 'business.html', {"form": form})

@login_required(login_url="/accounts/login/")
def create_business(request):
    current_user = request.user
    if request.method == "POST":
        
        form=BusinessForm(request.POST,request.FILES)

        if form.is_valid():
            business=form.save(commit=False)
            business.user=current_user
            business.hood= neighbourhood
            business.save()
        return HttpResponseRedirect('/businesses')
    else:
        form=BusinessForm()
    return render (request,'business_form.html', {'form': form, 'profile': profile})

@login_required(login_url="/accounts/login/")
def businesses(request):
    current_user = request.user
    businesses = Business.objects.all().order_by('-id')
    
    profile = Profile.objects.filter(user_id=current_user.id).first()

    if profile is None:
        profile = Profile.objects.filter(
            user_id=current_user.id).first()
        
        locations = Location.objects.all()
        neighborhood = Neighbourhood.objects.all()
        
        businesses = Business.objects.all().order_by('-id')
        
        return render(request, "profile.html", {"danger": "Update Profile", "locations": locations, "neighborhood": neighborhood, "businesses": businesses})
    else:
        neighborhood = profile.neighbourhood
        businesses = Business.objects.all().order_by('-id')
        return render(request, "business.html", {"businesses": businesses}) 

@login_required(login_url="/accounts/login/")
def search(request):
    if 'search_term' in request.GET and request.GET["search_term"]:
        search_term = request.GET.get("search_term")
        searched_hood = Neighbourhood.objects.filter(name__icontains=search_term)
        message = f"Search For: {search_term}"

        return render(request, "search.html", {"message": message, "hood": searched_hood})
    else:
        message = "You haven't searched for any term"
        return render(request, "search.html", {"message": message})
