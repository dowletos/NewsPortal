from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from datetime import datetime

class NewsList(ListView):
    model=Post
    ordering='-post_ID'
    template_name = 'news.html'
    context_object_name = 'Post'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['time_now']=datetime.utcnow()
        context['next_sale']=None

        return context


class NewsListDetailed(DetailView):
    model=Post
    ordering='post_ID'
    template_name = 'news_detailed.html'
    context_object_name = 'Post'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['time_now']=datetime.utcnow()
        context['next_sale']=None

        return context
