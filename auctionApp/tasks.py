from __future__ import absolute_import, unicode_literals
from .views import *
from datetime import *
from celery import *
from celery.task import periodic_task
from celery.schedules import crontab

app = Celery('tasks', broker='amqp://localhost//', backend='amqp')


@periodic_task(
    run_every=(crontab(minute='*/60')),
    name='Resolve action',
    ignore_result=True
)
def resolve_auction():

        auctions = Auction.objects.all().filter(lifecycle='A')

        now = datetime.now(timezone.utc)

        for auc in auctions:

            difference = auc.end_date - now

            difference_in_min = difference / timedelta(minutes=1)

            if difference_in_min < 1:
                bid = get_object_or_404(Bid, auction=auc)
                auc.lifecycle = 'D'
                auc.winner = bid.bidder
                auc.save()

        auctions = Auction.objects.all().filter(lifecycle='D')

        for auc in auctions:

            auc.lifecycle = 'E'
            auc.save()
            send_mail('Resolved',
                      'Youre auction has finished',
                      'admin@yaas.fi',
                      auc.seller.email,
                      fail_silently=False)
            """
            # for bidders
            mails = []
            bid = Bid.objects.all().filter(auction=auc)
            for bidd in bid:
                if bidd.user.email in mails:
                    pass
                else:
                    mails.append(bidd.user.email)

            send_mail('resolved',
                      'Auction in which you bid has resolved',
                      'admin@yaas.fi',
                      mails,
                      fail_silently=False)"""