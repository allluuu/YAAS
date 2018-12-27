from rest_framework import serializers
from auctionApp.models import *

class AuctionListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('title', 'id', 'description', 'seller', 'end_date', 'min_price')


class AuctionDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('title', 'description', 'seller', 'start_date', 'end_date', 'min_price',
                  'lifecycle')


class BidSeriaalizers(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'auction', 'bidder', 'bid', 'timestamp')
