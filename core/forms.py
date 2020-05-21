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
