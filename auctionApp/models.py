from django.contrib.auth.models import *
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *
from django.db.models import Q


class Auction(models.Model):
    LIFECYCLES = (
        ('A', 'Active'),
        ('B', 'Banned'),
        ('D', 'Due'),
        ('E', 'Adjudicated'),
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller', blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    min_price = models.DecimalField(max_digits=16, decimal_places=2)
    lifecycle = models.CharField(max_length=1, choices=LIFECYCLES, default='A')
    banned = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    @property
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.description

    @classmethod
    def get_active(cls):
        return cls.objects.filter(Q(active=True) & Q(banned=False))

    @classmethod
    def find_active(cls, criteria):
        return cls.objects.filter((Q(title__contains=criteria) | Q(description__contains=criteria))
                                  & (Q(active=True) & Q(banned=False)))

    @classmethod
    def get_active_by_id(cls, idid):
        try:
            auction = cls.objects.get(id=idid)
        except ObjectDoesNotExist:
            auction = None
        if auction and auction.lifecycle == 'A':
            return auction
        else:
            return None

    def get_latest(self, id):
        a = Auction.objects.get(id=id)
        bidd = a.bid_set.filter(id=id)
        if bidd:
            return bidd.bid
        else:
            return 0.00

    def get_history(self):
        return Bid.get_bids(self)

    def get_bidder(self):
        bidders = []
        for b in self.get_history():
            if b.bidder not in bidders:
                bidders.append(b.bidder)

        return bidders


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bid = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bid)

    @classmethod
    def get_latest_bid(cls, auct):
        try:
            bidd = cls.objects.filter(auction=auct).latest('timestamp')
        except ObjectDoesNotExist:
            bidd = None
        return bidd


    @classmethod
    def get_bids(cls, auction):
        bids = cls.objects.filter(auction=auction).order_by("-timestamp")
        return bids


