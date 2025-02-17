from django.core.files.images import get_image_dimensions
from django.db.models import Q
from django.views.generic import ListView
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView
from django.shortcuts import redirect
from django.utils import timezone
from .forms import ItemForm, ShopForm, CheckoutForm, CouponForm, RefundForm, PaymentForm, CreateProductForm
from .models import Item, RootCat, OrderItem, Order, Address, Refund, UserProfile, Slider, Shop, Category, Offer, Area
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

context = dict()


def home_view(request):
    global context
    markets = Area.objects.all().order_by('-updated_at')
    shops = Shop.objects.all().order_by('-updated_at')
    # items = Item.objects.all().order_by('-updated_at')[:10]
    top = Item.objects.all().order_by('-created_at')[:5]
    new = Item.objects.all().order_by('created_at')[:5]
    # temp
    latest = Item.objects.all().order_by('category')[:5]

    slider = Slider.objects.all()
    slider = random.sample(list(slider), len(slider))
    cats_all = Category.objects.all().order_by('name')
    cats = Category.objects.all()
    try:
        cats = random.sample(list(cats), 5)
    except:
        cats = random.sample(list(cats), len(cats))
    cats_nav = cats[:5]
    root_cat = RootCat.objects.all()
    root_cat = random.sample(list(root_cat), len(root_cat))
    cat_items = {}

    for cat in cats:

        content1 = Item.objects.filter(category=cat)
        for item in content1:
            print(len(item.title))

        content = sorted(content1, key=lambda x: len(x.title), reverse=False)

        try:

            content = random.sample(list(content), 4)
            content = sorted(content, key=lambda x: len(
                x.title), reverse=False)
        except:
            if (len(content) < 6):
                content = random.sample(list(content), len(content))
                content = sorted(content, key=lambda x: len(
                    x.title), reverse=False)

            else:
                content = random.sample(list(content), len(content))
                content = sorted(content, key=lambda x: len(
                    x.title), reverse=False)
        if cat.name not in cat_items.keys():

            if len(content) > 0:
                cat_items[str(cat.name)] = content

    '''
    we want to show item using paginator
    '''

    cat_items_t = tuple(cat_items)

    page = request.GET.get('page', 1)
    paginator = Paginator(cat_items_t, 2)
    try:
        cat_items1 = paginator.page(page)
    except PageNotAnInteger:
        cat_items1 = paginator.page(1)
    except EmptyPage:
        cat_items1 = paginator.page(paginator.num_pages)
    print(cat_items_t, 'GGGGGGGGG')
    print(cat_items1, "PPPPPPPPPppp")
    # print(request.user.shop)
    # print(cat_items['cloth'])
    # slide1 = Slider.objects.all().order_by('-updated_at').first()
    items = Item.objects.all()

    items = random.sample(list(items), len(items))

    try:
        cats_all_1 = random.sample(list(cats_all), len(cats_all))
    except:
        cats_all_1 = random.sample(list(cats_all), len(cats_all))
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(items, 24)
    except:
        paginator = Paginator(items, 2)
    try:
        item_p = paginator.page(page)
    except PageNotAnInteger:
        item_p = paginator.page(1)
    except EmptyPage:
        item_p = paginator.page(paginator.num_pages)
    # Get the index of the current page
    index = item_p.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {'shops': shops, 'items': item_p,
               'markets': markets, 'cats': cats, 'cats_nav': cats_nav,
               'slider': slider,
               'cat_items': cat_items,
               'top': top,
               'new': new,
               'latest': latest,
               'cats_all': cats_all,
               'cats_all_phn': cats_all[:6],
               'root_cat': root_cat,
               'page_range': page_range,

               }
    # for key, value in con.items():
    #     print('---------------------->>>>>>>>>>>>>......', key, value)
    #     context[key] = value
    # return render(request, 'visitor/home/a.html', context)
    return render(request, 'visitor/home.html', context)


def side_bar(request):
    shops = Shop.objects.all().order_by('-updated_at')[:10]
    root_cat = RootCat.objects.all()
    context = {'shoping': shops,
               'root_cat': root_cat}
    return render(request, 'layouts/sidebar.html', context)


def add_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ShopForm()
    return render(request, 'add_shop.html', {
        'form': form
    })


def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {
        'form': form
    })


class ShopCreate(LoginRequiredMixin, CreateView):
    model = Shop
    fields = ['title', 'photo']
    template_name = 'add_item.html'

    def form_valid(self, form):
        form.instance.title = self.request.title
        form.instance.photo = self.request.photo
        return super().form_valid(form)


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


'''
def products(request):
    context = {
        'items': Item.objects.all().order_by('-updated_at')
    }
    return render(request, "products.html", context)
'''


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            cats_all = Category.objects.all().order_by('-updated_at')
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True,
                'cats_all': cats_all
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,

                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            # return render(self.request, "a/checkout.html", context)
            return render(self.request, "visitor/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):

        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            mobile_number = form.data.get(
                'mobile_number')
            mobile_number = str(mobile_number)

            mb = mobile_number
            a = mb[:]
            b = "1234567890"
            for char in b:
                a = a.replace(char, "")
            print(a)
            for char in a:
                mb = mb.replace(char, "")
            mobile_number = mb
            print(mb)
            print(mobile_number)

            if form.is_valid():

                payment_option = form.cleaned_data.get(
                    'payment_option')
                order.payment_option = payment_option
                print('payment_option = ', payment_option)

                comment = form.cleaned_data.get(
                    'comment')
                customer_name = form.cleaned_data.get(
                    'customer_name')
                order.customer_name = customer_name
                order.comment = comment
                order.mobile_number = mobile_number
                print('mobile', mobile_number, comment, customer_name)
                try:
                    print("User is entering a new shipping address")
                    shipping_address = form.cleaned_data.get(
                        'shipping_address')
                    print(shipping_address)
                    order.shipping_address = shipping_address
                    order.ordered = True
                    order.save()
                    messages.success(
                        self.request, "Your order was successful! Please Clear Cart ")

                    return redirect("/")
                except:
                    messages.info(
                        self.request, "Please fill in the required shipping address fields")

                # payment_option = form.cleaned_data.get('payment_option')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


'''
class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all().order_by('-updated_at')
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")

'''


class MarketsView1(ListView):
    model = Area
    paginate_by = 10
    # template_name = "a/markets.html"
    template_name = "visitor/markets.html"


class MarketsView(ListView):
    model = Area
    paginate_by = 10

    # template_name = "a/markets.html"
    template_name = "visitor/index.html"
    '''
    template_name = "visitor/blog-details.html"
    template_name = "visitor/blog.html"
    template_name = "visitor/checkout.html"
    template_name = "visitor/contact.html"
    template_name = "visitor/shop-details.html"
    template_name = "visitor/shop-grid.html"
    template_name = "visitor/shoping-cart.html"
    '''


class ShopsView(ListView):
    model = Shop
    paginate_by = 10
    # template_name = "a/shops.html"
    template_name = "visitor/shops.html"


class ProductsView(ListView):
    model = Item
    paginate_by = 10
    # template_name = "a/products.html"
    template_name = "visitor/products.html"


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            cats_all = Category.objects.all().order_by('-updated_at')
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'cats_all': cats_all, }
            # return render(self.request, 'a/cart.html', context)
            return render(self.request, 'visitor/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class CustomerOrderStatusView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            cats_all = Category.objects.all()
            user_orders = Order.objects.filter(
                user=self.request.user, ordered=True)
            print('...............................', user_orders)

            context = {'object': user_orders,
                       'cats_all': cats_all}
            print(user_orders)
            # return render(self.request, 'a/my_order.html', context)
            return render(self.request, 'visitor/my_order.html', context)
        except ObjectDoesNotExist:
            messages.info(
                self.request, "Sorry! You have no order! ")
            return redirect("core:home")


def all_offer_cat(request):
    try:
        category = Category.objects.all().order_by('-updated_at')
        offer = Offer.objects.all().order_by('-updated_at')
        context = {'category': category, 'offer': offer}
    # print(items)
        return render(request, 'home.html', context)
    except ObjectDoesNotExist:
        messages.info(
            self.request, "Sorry! Hopefully they will update their products soon!")
        return redirect("core:checkout")

# can ciew market, shops, and products,


def get_shops(request, id):
    try:
        print('............................... get shop ##########')
        shops = Shop.objects.filter(area=id)
        # category = Category.objects.filter(for_shop=id)
        # offer = Offer.objects.filter(for_shop=id)
        print('-------77777777777777777777777777777777777-----------------', shops)
        # context = {'items': items, 'category': category, 'offer': offer}
        context = {'shops': shops}
        # print(items)
        # return render(request, 'a/main/shops.html', context)
        return render(request, 'visitor/getshops.html', context)
    except ObjectDoesNotExist:
        messages.info(
            self.request, "Sorry! Hopefully they will update their products soon!")
        return redirect("core:checkout")


def get_shop_cat_items(request, id):
    try:

        print('0000000000000000000000000', id)
        # print('...............................', type(slug))
        category = Category.objects.filter(for_shop=id)
        items = Item.objects.filter(category=id)
        offer = Offer.objects.filter(for_shop=id)
        # print('-------77777777777777777777777777777777777-----------------', category)
        context = {'items': items, 'category': category, 'offer': offer,
                   'root_cat': RootCat.objects.all()}

        print(items)
        return render(request, 'shop-items.html', context)
    except ObjectDoesNotExist:
        messages.info(
            self.request, "Sorry! Hopefully they will update their products soon!")
        return redirect("core:checkout")


def get_shopoffe(request, id):
    try:

        # print('0000000000000000000000000', id)
        # print('...............................', type(slug))
        category = Category.objects.filter(for_shop=id)
        items = Item.objects.filter(Offer=id)
        offer = Offer.objects.filter(for_shop=id)
        # print('-------77777777777777777777777777777777777-----------------', category)
        context = {'items': items, 'category': category, 'offer': offer, 'root_cat': RootCat.objects.all()
                   }

        # print(items)
        return render(request, 'shop-items.html', context)
    except ObjectDoesNotExist:
        messages.info(
            self.request, "Sorry! Hopefully they will update their products soon!")
        return redirect("core:checkout")


def ItemDetailView(request, slug):
    item = Item.objects.get(slug=slug)
    market_id = item.shop.area.id
    shop_id = item.shop.id
    cats_all = Category.objects.all()
    context = {
        'item': item,
        'market_id': market_id,
        'shop_id': shop_id,
        'cats_all': cats_all,
        'shops': Shop.objects.all(),
        'root_cat': RootCat.objects.all(),
    }
    return render(request, "visitor/product-details.html", context)


# class ItemDetailView(DetailView):
#     model = Item
#     # template_name = "a/product-details.html"
#     template_name = "visitor/product-details.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.quantity_available += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.quantity_available -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


@login_required
def shop_manager_view(request):
    forms = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            item = Item(
                shop=form.cleaned_data["shop"],
                title=form.cleaned_data["title"],
                price=form.cleaned_data["price"],
                discount_price=form.cleaned_data["discount_price"],
                category=form.cleaned_data["category"],
                offer=form.cleaned_data["offer"],
                description=form.cleaned_data["description"],
                image=form.cleaned_data["image"],
                in_stock=form.cleaned_data["in_stock"],
            )
            item.save()
    items = Item.objects.all().order_by('-updated_at')
    context = {'items': items, 'forms': forms}
    return render(request, 'visitor/shop_manager.html', context)


'''
class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")
'''

# for all category


def category_view(request, slug):
    try:
        cat = get_object_or_404(Category, name=slug)
    except:

        cat = get_object_or_404(Category, slug=slug)
    id = cat.id
    items = Item.objects.filter(category=id)
    items = random.sample(list(items), len(items))
    cat = Category.objects.get(id=id)
    cats = Category.objects.all().order_by('-updated_at')
    cat_items = {}
    cats_all = Category.objects.all().order_by('-updated_at')
    for ca in cats:

        content = Item.objects.filter(category=ca)
        if cat.name not in cat_items.keys():
            print("CAT NAME", ca.name)
            if len(content) > 0:
                cat_items[str(ca.name)] = content
            print(content)

    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(items, 12)
    except:
        paginator = Paginator(items, len(items))
    try:
        item_p = paginator.page(page)
    except PageNotAnInteger:
        item_p = paginator.page(1)
    except EmptyPage:
        item_p = paginator.page(paginator.num_pages)
    # Get the index of the current page
    index = item_p.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    context = {
        'items': item_p,
        'cat': cat,
        'cat_items': cat_items,
        'cats_all': cats_all,
        'root_cat': RootCat.objects.all(),
        'shops': Shop.objects.all(),
        'markets': Area.objects.all(),
        'page_range': page_range,

    }

    return render(request, "visitor/category_view.html", context)

# for shop category


def category_viewS(request, slug, shop):
    try:
        cat = get_object_or_404(Category, name=slug)
    except:

        cat = get_object_or_404(Category, slug=slug)
    id = cat.id
    # print('Shop',shop)

    items = Item.objects.filter(category=id).filter(shop__slug__icontains=shop)
    items = random.sample(list(items), len(items))
    cat = Category.objects.get(id=id)
    cats = Category.objects.all().order_by('-updated_at')
    cat_items = {}
    try:
        shop = Shop.objects.get(slug__icontains=shop)
    except:
        shop = Shop.objects.get(title__icontains=shop)

    # category = Category.objects.filter(for_shop=shop.id)
     # get all shop category
    sc = []
    for ic in Item.objects.filter(shop=shop):
        sc.append(ic.category)

    unique_cat_list = [i for n, i in enumerate(sc) if i not in sc[:n]]
    print("___________> ", unique_cat_list)
    category = Category.objects.filter(name__in=unique_cat_list)
    # end of get all cat

    for ca in cats:

        content = Item.objects.filter(category=ca)
        if cat.name not in cat_items.keys():
            print("CAT NAME", ca.name)
            if len(content) > 0:
                cat_items[str(ca.name)] = content
            print(content)
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(items, 12)
    except:
        paginator = Paginator(items, len(items))
    try:
        item_p = paginator.page(page)
    except PageNotAnInteger:
        item_p = paginator.page(1)
    except EmptyPage:
        item_p = paginator.page(paginator.num_pages)
    # Get the index of the current page
    index = item_p.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    context = {
        'shop': shop,
        'items': item_p,
        'cat': cat,
        'cat_items': cat_items,
        'category': category,
        'this_cat': cat,
        'root_cat': RootCat.objects.all(),
        'shops': Shop.objects.all(),
        'markets': Area.objects.all(),
        'page_range': page_range,
    }
    return render(request, "visitor/shop/cat.html", context)
    # return render(request, "visitor/shop/get_cat_items.html", context)


def conditions_of_use_view(request):
    return render(request, "visitor/footer/conditions_of_use.html", {})


class ShopDetailView(DetailView):
    model = Shop
    template_name = 'visitor/shop/shop_detail.html'


def get_items(request, id):
    try:
        # print('...............................', type(slug))
        items = Item.objects.filter(shop=id)
        items = random.sample(list(items), len(items))
        category = Category.objects.filter(for_shop=id)
        offer = Offer.objects.filter(for_shop=id)
        shop = Shop.objects.get(pk=id)
        cats_all = Category.objects.all()
        print('-------77777777777777777777777777777777777-----------------', category)
        context = {'items': items, 'category': category,
                   'offer': offer, 'shop': shop,
                   'cats_all': cats_all,
                   'root_cat': RootCat.objects.all(),
                   'shops': Shop.objects.all(),
                   'markets': Area.objects.all(),
                   }
        print(items)
        # return render(request, 'a/main/items.html', context)
        return render(request, 'visitor/getItems.html', context)
    except ObjectDoesNotExist:
        messages.info(
            self.request, "Sorry! Hopefully they will update their products soon!")
        return redirect("core:checkout")

# to get shop items


def get_items_slug(request, slug):
    global context
    try:
        my_shop = get_object_or_404(Shop, slug=slug)
        id = my_shop.id
        print('...............................', type(slug))
        items = Item.objects.filter(shop=id)

        items = random.sample(list(items), len(items))

        # category = Category.objects.filter(for_shop=id)
        # get all shop category
        sc = []
        for ic in items:
            sc.append(ic.category)

        unique_cat_list = [i for n, i in enumerate(sc) if i not in sc[:n]]
        print("___________> ", unique_cat_list)
        category = Category.objects.filter(name__in=unique_cat_list)
        # end of get all shop category

        offer = Offer.objects.filter(for_shop=id)
        shop = Shop.objects.get(pk=id)
        cats_all = Category.objects.filter(
            for_shop=shop).order_by('-updated_at')

        page = request.GET.get('page', 1)
        try:
            paginator = Paginator(items, 16)
        except:
            paginator = Paginator(items, len(items))
        try:
            item_p = paginator.page(page)
        except PageNotAnInteger:
            item_p = paginator.page(1)
        except EmptyPage:
            item_p = paginator.page(paginator.num_pages)

        # Get the index of the current page
        index = item_p.number - 1  # edited to something easier without index
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so lets calculate where to slice the list
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        # Get our new page range. In the latest versions of Django page_range returns
        # an iterator. Thus pass it to list, to make our slice possible again.
        page_range = list(paginator.page_range)[start_index:end_index]

        context.update({'items': item_p, 'category': category,
                        'offer': offer, 'shop': shop, 'root_cat': RootCat.objects.all(),
                        'shops': Shop.objects.all(),
                        'markets': Area.objects.all(),
                        'cats_all': cats_all, 'page_range': page_range})
        print(items)
        # return render(request, 'a/main/items.html', context)
        return render(request, 'visitor/shop/getItems.html', context)
    except ObjectDoesNotExist:
        messages.info(
            self.request, "Sorry! Hopefully they will update their products soon!")
        return redirect("core:checkout")


class SearchResultsView(ListView):
    model = Item
    template_name = 'visitor/search/search_new.html'

    def get_queryset(self):  # new

        query = self.request.GET.get('q')

        object_list = Item.objects.filter(title__icontains=query)
        '''
        object_list_shops = Shop.objects.filter(title__icontains=query)
        # object_list_cat = Category.objects.filter(title__icontains=query)
        object_list_markets = Area.objects.filter(name__icontains=query)
        no_result = False
        if len(object_list) == 0 and len(object_list_markets) ==0 and len(object_list_shops) ==0:
            no_result = True
        
        return object_list, object_list_shops,  object_list_markets, no_result
        '''
        return object_list


def search_all(request):

    # template_name = 'visitor/search/search_new.html'
    # def get_queryset(self): # new
    query = request.GET.get('q')
    object_list, object_list_shops, object_list_markets, cats, cat_p, page_range = [
        [], [], [], [], [], []]
    if query != "":

        object_list = Item.objects.filter(
            title__icontains=query).order_by('-updated_at')
        object_list = random.sample(list(object_list), len(object_list))

        object_list_shops = Shop.objects.filter(title__icontains=query)
        # object_list_cat = Category.objects.filter(title__icontains=query)
        object_list_markets = Area.objects.filter(name__icontains=query)

        cats = Item.objects.filter(category__name__icontains=query)
        cats = random.sample(list(cats), len(cats))
        # print(cats, ".................................dufhsdurih")

        if len(cats) > 0:
            object_list = []
        # page f     for categories products
        page = request.GET.get('page', 1)
        try:
            paginator = Paginator(cats, 20)
        except:
            paginator = Paginator(cats, len(cats))
        try:
            cat_p = paginator.page(page)
        except PageNotAnInteger:
            cat_p = paginator.page(1)
        except EmptyPage:
            cat_p = paginator.page(paginator.num_pages)
        # Get the index of the current page

        index = cat_p.number - 1  # edited to something easier without index
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so lets calculate where to slice the list
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        # Get our new page range. In the latest versions of Django page_range returns
        # an iterator. Thus pass it to list, to make our slice possible again.
        page_range = list(paginator.page_range)[start_index:end_index]

    no_result = False
    if len(object_list) == 0 and len(object_list_markets) == 0 and len(object_list_shops) == 0 and len(cats) == 0:
        no_result = True

    suggestion = None
    if no_result:

        items = Item.objects.all().order_by('-updated_at')
        try:
            suggestion = random.sample(list(items), 16)
        except:
            suggestion = random.sample(list(items), len(items))
    context = {'object_list': object_list,
               'object_list_shops': object_list_shops,
               'object_list_markets': object_list_markets,
               'no_result': no_result,
               'suggestion': suggestion,
               'cats': cat_p or None,
               'root_cat': RootCat.objects.all(),
               'search': query, 'page_range': page_range,

               'shops': Shop.objects.all(),
               'markets': Area.objects.all(),

               }

    # return render(request, 'a/main/items.html', context)
    return render(request, 'visitor/search/search_all.html', context)
