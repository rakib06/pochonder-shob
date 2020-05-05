from django.shortcuts import render
from .models import Item


def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "shop.html", context)


def products(request):
    context = {
        'items': Items.objects.all()
    }
    return render(request, 'products.html', context)


def checkout(request):
    return render(request, "checkout.html")


def home(request):
    context = {
        'items': Items.objects.all()
    }
    return render(request, "home.html", context)
