from django.contrib import admin
from django.urls import path, include
import auctionApp.views
from auctionApp.models import *
from auctionApp.views import *
from django.contrib.auth import views as auth_views
from auctionApp.restframework_rest_api import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/statuscheck/', include('celerybeat_status.urls')),
    path('register/', auctionApp.views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls'), name="accounts"),
    path('addAuction/', AddAuction.as_view(), name="addAuction"),
    path('home/', home, name="home"),
    path('edit/<int:id>/', EditAuction.as_view(), name="editAuction"),
    path('editUser/<int:id>', EditUser.as_view(), name="editUser"),
    path('saveAuction/', auctionApp.views.save_auction, name="save_auction"),
    path('showAuction/<int:id>', auctionApp.views.show_auction, name="show_auction"),
    path('makeBid/<int:id>', auctionApp.views.make_bid, name="makeBid"),
    path('search/', auctionApp.views.search, name="search"),
    path('banAuction/<int:id>', auctionApp.views.ban_auction, name="banAuction"),
    path('activeAuction/<int:id>', auctionApp.views.active_auction, name="activeAuction"),
    path('showAllBanned/', auctionApp.views.show_banned, name="showAllBanned"),
    path('emailhistory/', auctionApp.views.emailhistory, name="emailhistory"),
    path('api/auctions/', auction_list),
    path('api/auctions/<int:pk>', AuctionDetail.as_view()),
    path('api/auctions/<str:title>', search_list),
    path('api/auctions/bid/<str:pk>', BidAuction.as_view()),
]

