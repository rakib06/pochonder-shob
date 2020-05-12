from django.shortcuts import render
from .models import Item, Category, Brand
# for class based views
from django.views.generic import ListView, DetailView


def item_list(request):
    context = {
        'items': Item.objects.all(),
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
    }
    return render(request, "shop.html", context)


def products(request):
    context = {
        'items': Items.objects.all()
    }
    return render(request, 'products.html', context)


def checkout(request):
    return render(request, "checkout.html")


class HomeView(ListView):
    model = Item
    template_name = "shop.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-details.html'
    # template_name = 'product.html'
