from django.http.response import Http404
from django.shortcuts import render,reverse,redirect
from django.views.generic import CreateView,DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CustomUserCreationForm,UserUpdateForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib import messages
from recipe.models import UserFavourite
User=get_user_model()


class UserSignupView(CreateView):
    template_name="registration/signup.html"
    form_class=CustomUserCreationForm
    
    def form_valid(self,form):
        user_Email=form.data['email']
        send_mail(
            "test subject",
            "this is test email for signup",
            "admin@gecom.com",
            [user_Email],
        )
        messages.success(self.request, 'Account created!')
        return super(UserSignupView,self).form_valid(form)

    def get_success_url(self):
        return reverse("login")

class UserProfileView(LoginRequiredMixin ,DetailView):
    model=User
    template_name="users/profile.html"
    context_object_name="userprofile"
    slug_url_kwarg="username"
    slug_field="username"

    def get_context_data(self,**kwargs):
        context=super(UserProfileView,self).get_context_data(**kwargs)
        recipes=self.object.user_recipes.all()
        favourite_recipes=self.object.user_favourite.first()
        favourite_recipes=self.object.user_favourite.first().recipe.all() if favourite_recipes else None           
        context["recipes"]=recipes
        context["favourite_recipes"]=favourite_recipes
        return context

    

class UserProfileUpdateView(LoginRequiredMixin,UpdateView):
    template_name="users/user_update.html"
    model=User
    form_class=UserUpdateForm
    slug_url_kwarg="username"
    slug_field="username"
    
    def dispatch(self, request, *args, **kwargs):
        profile=self.get_object()
        if profile != self.request.user:
            raise Http404("Knock knock , Not you!")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('users:profile', kwargs={'username': self.request.user.username})
