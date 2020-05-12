from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
# Create your views here.
from .models import Shop


class ShopLoginView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "shops/login.html"


class AlertView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "shop/alert.html"


class badgeView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "shop/badge.html"


class buttonView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "shop/button.html"


class calendarView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "shops/index.html"


class cardView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "shop/card.html"


class chartView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "admin/card.html"
