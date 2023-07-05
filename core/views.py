from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404

class HomeView(TemplateView):
    template_name="home.html"

class DevelopmentView(TemplateView):
    template_name="errors/error403.html"
    
