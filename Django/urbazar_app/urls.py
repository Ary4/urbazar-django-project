from django.conf.urls import url
from django.urls import path

from urbazar_app.syndication import Archive
from . import views
from urbazar_app.views import user_view
from urbazar_app.views import search_view
from urbazar_app.views import flagged_view
from urbazar_app.views import landing_view
from urbazar_app.views import upload_view
from urbazar_app.views import edit_profile_view
from urbazar_app.views import add_to_flagged
from urbazar_app.views import remove_from_flagged
from urbazar_app.views import view_alt_user
from urbazar_app.views import signup
from urbazar_app.views import remove_from_user

urlpatterns = [
    path('user/', user_view, name='user'),  # maps to user profile page
    path('search/<str:feed_query>', search_view, name='search'),   #Opens product description when feed is clicked
    path('search', search_view, name='search'),#opens search page when product is searched
    path('flagged/', flagged_view, name='flag'),# opens flagged items of a user
    path('flagged/remove/', remove_from_flagged, name='flag_remove'), # Removes the flagged item from the inventory
    path('user/remove_product/', remove_from_user, name='user_prod_remove'),#removes the product uploaded by the user
    path('add/', add_to_flagged, name='search_add'),#so adds the product to his inventory when he clicks flag
    path('upload/', upload_view, name='upload'),#open upload page to upload a product
    path('edit_profile/', edit_profile_view, name="user_edit"),#edit the profile
    path('alt_user/', view_alt_user, name='alt_user'),#opens another user's profile
    path('', landing_view, name='home'),#home page
    path('signup/', signup, name='signup'),#open signup page if not registered/logged in
    path('feed/', Archive()),#opens feed page

]
