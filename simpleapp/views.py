from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from datetime import datetime

class ProductsList(ListView):
    model=Product
    ordering='name'
    template_name = 'product.html'
    context_object_name = 'products'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['time_now']=datetime.utcnow()
        context['next_sale']=None

        return context


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'products'