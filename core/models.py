from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import User

# discount/new/ Eid Offer
from django.utils.safestring import mark_safe
import uuid
from PIL import Image


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class area for jolil tower, shopping complex, nixon market etc
class RootCat(TimeStampMixin):
    title = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='rootcat', default='ps/5.png', blank=True, null=True)

    @property
    def category(self):
        x = Category.objects.filter(tags__icontains=self.title)
        return x

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def get_absolute_url(self):

        return reverse("core:area-shops", kwargs={
            # ei khane sudu oi shop er jinish jeno dekhay sei babostha korte hobe
            'id': self.id
        })
    # shop category

# class area for jolil tower, shopping complex, nixon market etc


class Area(TimeStampMixin):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='area', default='ps/5.png')

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'

    @property
    def shops_count(self):
        x = Shop.objects.filter(area=self.id).count()
        print('*********************8888', x)
        return x

    @property
    def items_count(self):
        shops = Shop.objects.filter(area=self.id)
        n = 0
        for item in shops:
            n = Item.objects.filter(shop=item).count()
            n += n
        print('*********************8888= n ', n)
        return n

    '''
    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.url)  # Open image using self

        if img.height != 300 or img.width != 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            # saving image at the same path
            image.save(self.image.url)
    '''

    def get_absolute_url(self):

        return reverse("core:area-shops", kwargs={
            # ei khane sudu oi shop er jinish jeno dekhay sei babostha korte hobe
            'id': self.id
        })
    # shop category


class UserProfile(TimeStampMixin):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ShopType(TimeStampMixin):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Shop(TimeStampMixin):
    title = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='shops/')
    slug = models.SlugField(verbose_name="Shop URL", null=False, unique=True)
    shop_type = models.ForeignKey(
        ShopType, on_delete=models.SET_NULL, null=True, blank=True)
    area = models.ForeignKey(
        Area, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def items_count(self):
        x = Item.objects.filter(shop=self.id).count()
        print('*********************8888', x)
        return x

    '''
    def get_absolute_url_1(self):

        return reverse("core:shop-items", kwargs={
            # ei khane sudu oi shop er jinish jeno dekhay sei babostha korte hobe
            'slug': self.slug
        })

    '''
    # shop category

    def get_category(self):

        cats = Category.objects.filter(for_shop=self.id)

        return ", ".join([p.name for p in cats])

    def get_shop_type(self):

        return ", ".join([p.title for p in self.shop_type.all()])

    def get_shop_offer(self):
        offers = Offer.objects.filter(for_shop=self.id)

        return ", ".join([p.name for p in offers.all()])
        # return offers

    def image_tag(self):
        if self.photo:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.photo.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'
    get_category.short_description = 'Category'

    def get_absolute_url(self):
        return reverse("core:shop-items", kwargs={
            # ei khane sudu oi shop er jinish jeno dekhay sei babostha korte hobe
            'slug': self.slug
        })
    '''
    def save(self):
        super().save()  # saving image first

        img = Image.open(self.photo.path)  # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.photo.path)

    '''


class Category(TimeStampMixin):
    name = models.CharField(max_length=100)
    for_shop = models.ManyToManyField(Shop)
    slug = models.SlugField(verbose_name="Cat URL", null=False, unique=True)
    tags = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse("core:category-view", kwargs={
            # ei khane sudu oi shop er jinish jeno dekhay sei babostha korte hobe
            'slug': self.slug
        })


class Offer(TimeStampMixin):
    name = models.CharField(max_length=100)
    for_shop = models.ManyToManyField(Shop)

    def __str__(self):
        return self.name


class Color(TimeStampMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(TimeStampMixin):

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default="")
    Offer = models.ForeignKey(
        Offer, on_delete=models.SET_NULL, null=True, default="")
    slug = models.SlugField(unique=True, default=uuid.uuid1)
    description = models.TextField(
        null=True, default="No description available")
    image = models.ImageField(upload_to='products/')
    thumb = models.ImageField(
        upload_to='products/thumb/', null=True, blank=True)
    in_stock = models.BooleanField(default=True)

    @property
    def discount(self):
        dp = -((self.price - self.discount_price) / self.price) * 100
        return float("{:.2f}".format(dp))

    @property
    def offer(self):

        return self.Offer

    def thumb_tag(self):
        if self.thumb:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.thumb.url)
        else:
            return 'No Image Found'
    thumb_tag.short_description = 'Image'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Thumb'

    @property
    def image_test(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return 'No Image Found'

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def get_thumb(self):
        host = urlparse(self.url).hostname
        if host.startswith('www.'):
            host = host[4:]
        thumb = 'https://api.thumbalizr.com/?url=http://' + host + '&width=125'
        return thumb

    def __str__(self):
        return self.title

    @property
    def shop_name(self):
        print('------------Ship', self.shop__title)
        return self.shop__title

    @property
    def market_name(self):
        market = self.shop.area
        return market.name

    @property
    def get_size(self):
        x = Size.objects.filter(for_item=self.id)

        return ", ".join([p.name for p in x])

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    '''
    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path)  # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)
    '''


class Size(TimeStampMixin):
    name = models.CharField(max_length=100)
    for_item = models.ManyToManyField(Item)

    def __str__(self):
        return self.name


class OrderItem(TimeStampMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False, verbose_name="Confirm Order")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, verbose_name='ordered quantity')
    quantity_available = models.IntegerField(
        default=1, verbose_name='Available Quantity')

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def image_tag(self):
        if self.item.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.item.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


PAYMENT_CHOICES = (
    ('B', 'BKash'),
    ('C', 'Cash On'),
    ('O', 'Others')
)


class Order(TimeStampMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=200)
    comment = models.CharField(max_length=200, default="NA")
    customer_name = models.CharField(max_length=200, default="NA")
    # 'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)

    # billing_address = models.ForeignKey('Address', related_name = 'billing_address', on_delete = models.SET_NULL, blank = True, null = True)
    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_packed = models.BooleanField(
        default=False, verbose_name="Packing Status")
    being_delivered = models.BooleanField(
        default=False, verbose_name="Shiping Status")

    received = models.BooleanField(default=False, verbose_name="Received ")

    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=200)
    payment_option = models.CharField(
        choices=PAYMENT_CHOICES, max_length=2, null=True)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(TimeStampMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    # country = CountryField(multiple=False)
    # zip = models.CharField(max_length=100)
    # address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


'''
class Payment(TimeStampMixin):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

'''


class Coupon(TimeStampMixin):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(TimeStampMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Slider(TimeStampMixin):
    caption = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='slider', default='ps/5.png')
    subtitle = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.caption

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'
