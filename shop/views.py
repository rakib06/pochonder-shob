from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
# Create your views here.
from .models import Shop
from django.contrib.auth.decorators import login_required


from django.conf import settings
from django.core.files.storage import FileSystemStorage

'''
def shop_profile(request):
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ShopForm()

    return render(request, 'shop/shop_from.html', {
        'form': form
    })

'''


def home(request):
    pass


def products(request):
    pass


def orders(request):
    pass


def customer(request):
    pass


class ShopProfile(ListView):
    model = Shop
    template_name = "store/shop_form.html"


class cardView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "shop/card.html"


class chartView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "admin/card.html"


def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = ExampleModel.objects.get(pk=course_id)
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')


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


class IndexView(ListView):
    model = Shop
    # template_name = "shop/login.html"
    template_name = "store/main.html"
