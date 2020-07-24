from django.contrib.syndication.views import Feed

from urbazar_app import views
from .models import Product
from django.urls import reverse


class Archive(Feed):
    title = "UrBazar"
    link = "/feed/"
    description = "Latest Uploaded Products by Students."

    def items(self):
        return Product.objects.all().order_by("-upload_date")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse(views.search_view, kwargs={'feed_query': item.title})

    #kwargs = {'': item.pk}