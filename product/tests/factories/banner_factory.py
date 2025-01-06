import factory

from product.models.banner import Banner


class BannerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Banner
