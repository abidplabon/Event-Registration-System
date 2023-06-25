from django.shortcuts import render,HttpResponseRedirect
from App_Login.forms import CreateNewUser
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse,reverse_lazy
from App_Login.models import UserProfile,Follow
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from App_Login.forms import EditProfile
from App_Posts.forms import PostForm

from App_Posts.forms import PostForm
from django.contrib.auth.models import User

# Create your views here.

def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile= UserProfile(user = user) #making relation with the model "user" one to one field
            user_profile.save()
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request,'App_Login/signup.html',context={'title':'Signup Form Here','form':form})

def login_page(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)    #store the post request in the data variable
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)    #matching with database
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('App_Posts:home'))
    return render(request,'App_login/login.html',context={'title':'Login Page','form':form})

@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user) #fetch the requested user
    form = EditProfile(instance=current_user)   #modified changes will be kept here for future login

    if request.method == "POST":
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))

    return render(request,'App_Login/profile.html',context={'title':'Edit Profile Page','form':form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))

@login_required
def profile(request):
    form = PostForm()       #initiating the form by calling it in a variable
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request,'App_Login/user.html',context={'title':'User Profile','form':form})


@login_required
def user(request,username):
    user_other = User.objects.get(username=username) #matches the username of the <a> tag
    already_followed = Follow.objects.filter(follower=request.user,following=user_other)
    if user == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request,'App_Login/user_other.html',context={'user_other':user_other,'already_followed':already_followed})


@login_required
def follow(request,username):
    following_user = User.objects.get(username=username)   #Follow button click who do follow so username
    follower_user  = request.user                          #Who will follow like others
    already_followed = Follow.objects.filter(follower=follower_user,following=following_user) # get all name list form the database
    if not already_followed:
        followed_user = Follow(follower=follower_user,following=following_user) #follow na korle follow te click korle username ta add hobe
        followed_user.save()
    return HttpResponseRedirect(reverse('App_Login:user',kwargs={'username':username})) #kwargs for passing parameter

@login_required
def unfollow(request,username):
    following_user = User.objects.get(username=username)  # Follow button click who do follow so username
    follower_user = request.user  # Who will follow like others
    already_followed = Follow.objects.filter(follower=follower_user,
                                             following=following_user)  # get all name list form the database
    already_followed.delete()
    return HttpResponseRedirect(
        reverse('App_Login:user', kwargs={'username': username}))  # kwargs for passing parameter
