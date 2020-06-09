from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Shop, Item

PAYMENT_CHOICES = (
    ('B', 'BKash'),
    ('C', 'Cash On Delivery'),
    ('O', 'Others')
)


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('title', 'photo', )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'price', 'discount_price', 'category',
                  'Offer', 'slug', 'description', 'image',)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=True)
    mobile_number = forms.CharField(required=True)
    comment = forms.CharField(required=False)
    customer_name = forms.CharField(required=True)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-Offer': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class CreateProductForm(forms.Form):
    shop = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Shop Name"
        })
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Product Name"
        })
    )
    price = forms.FloatField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Price"
        })
    )
    discount_price = forms.FloatField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Discount Price"
        })
    )
    category = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Category"
        })
    )
    offer = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Offer"
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "description"
        })
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            # "class": "form-control",
            # "placeholder": "Image"
            "id": "myfile"
        })
    )
    in_stock = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            # "class": "form-control",
            # "placeholder": "In Stock"
            "id": "in_stock"
        })
    )
    # body = forms.CharField(widget=forms.Textarea(
    #     attrs={
    #         "class": "form-control",
    #         "placeholder": "Leave a comment!"
    #     })
    # )

    # shop = forms.ForeignKey(Shop, on_delete=models.CASCADE)
    # title = forms.CharField(max_length=100)
    # price = forms.FloatField()
    # discount_price = forms.FloatField(blank=True, null=True)
    # category = forms.ForeignKey(
    #     Category, on_delete=forms.SET_NULL, null=True, default="")
    # Offer = forms.ForeignKey(
    #     Offer, on_delete=forms.SET_NULL, null=True, default="")
    # slug = forms.SlugField(unique=True, default=uuid.uuid1)
    # description = forms.TextField(
    #     null=True, default="No description available")
    # image = forms.ImageField(upload_to='products/')
    # in_stock = forms.BooleanField(default=True)

    # shipping_address = forms.CharField(required=True)
    # mobile_number = forms.CharField(required=True)
    # comment = forms.CharField(required=False)
    # customer_name = forms.CharField(required=True)
