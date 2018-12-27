from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from django.shortcuts import get_object_or_404
from rest_framework import generics

from auctionApp.models import Auction
from auctionApp.serializers import *


@api_view(['GET'])
#@authentication_classes([BasicAuthentication])
#@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer,])
def auction_list(request):
    auctions = Auction.objects.all()
    serializers = AuctionListSerializers(auctions, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def search_list(request, title):
    auctions = Auction.objects.all()
    auc = auctions.filter(title__icontains=title)
    serializers = AuctionListSerializers(auc, many=True)
    return Response(serializers.data)


@api_view(['GET'])
@renderer_classes([JSONRenderer,])
def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    serializers = AuctionDetailSerializers(auction)
    return Response(serializers.data)

@renderer_classes([JSONRenderer,])
class AuctionDetail(APIView):
    #authentication_classes = (BasicAuthentication,)
    #permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        serializers = AuctionDetailSerializers(auction)
        return Response(serializers.data)

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        data = request.data
        print(request.data)
        serializers = AuctionDetailSerializers(auction, data=data)
        if serializers.is_valid():
            serializers.save()
            return serializers.data
        else:
            return Response(serializers.errors, status=400)

@renderer_classes([JSONRenderer,])
class BidAuction(APIView):
    #authentication_classes = (BasicAuthentication,)
    #permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        #bid = Bid.objects.filter()
        bid = get_object_or_404(Bid, id=pk)
        serializers = BidSeriaalizers(bid)
        return Response(serializers.data)

    def post(self, request, pk):
        bid = get_object_or_404(Bid, pk=pk)
        data = request.data
        print(request.data)
        serializers = BidSeriaalizers(bid, data=data)
        if serializers.is_valid():
            serializers.save()
            return serializers.data
        else:
            return Response(serializers.errors, status=400)




