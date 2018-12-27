from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import update_session_auth_hash

from auctionApp.forms import UserCreationForm
from auctionApp.models import *
from auctionApp.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import *
from django.core.mail import *
import os


def home(request):
    if request.user.is_superuser:
        auctions = Auction.objects.all()
        return render(request, 'archive.html', {'auctions': auctions})
    else:
        auctions = Auction.objects.filter(lifecycle='A')
        return render(request, "archive.html", {'auctions': auctions})

def show_banned(request):
    if request.user.is_superuser:
        auctions = Auction.objects.filter(lifecycle='B')
        return render(request, "archive.html", {'auctions': auctions})


def show_auction(request, id):
    show_auc = Auction.objects.get(id=id)
    bids = Bid.get_latest_bid(show_auc)
    if bids is not None:
        return render(request, 'show_auction.html', {'auction': show_auc, 'bid': bids})
    else:
        bids = 0.00
        return render(request, 'show_auction.html', {'auction': show_auc, 'bid': bids})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST)
        if form.is_valid():
            user.save()
            messages.add_message(request, messages.INFO, "User updated")
            return HttpResponseRedirect(reverse('home'))
        else:
            form = EditUserForm()
        return render(request, 'editUser.html', {'form': form})


def search(request):

    query = request.GET.get('q')

    results1 = Auction.objects.filter(Q(title__icontains=query))

    results = results1.filter(lifecycle='A')

    return render(request, 'search_results.html', {'results': results})


def ban_auction(request, id):

    if request.user.is_superuser:

        auction = Auction.objects.get(id=id)

        auction.lifecycle = 'B'
        auction.save()

        messages.add_message(request, messages.INFO, "Auction banned")
        #For seller:
        send_mail('Auction banned',
                  'Your auction is banned by admin',
                  'admin@yaas.fi',
                  ['request.user.email'],
                  fail_silently=False)

        #For bidder:
        mails=[]
        bid = Bid.objects.all().filter(auction=auction)
        for bidd in bid:
            if bidd.user.email in mails:
                pass
            else:
                mails.append(bidd.user.email)

        send_mail('Auction banned',
                  'Auction where u had a bid was banned',
                  'admin@yaas.fi',
                  mails,
                  fail_silently=False)


        return HttpResponseRedirect(reverse('home'))

    else:
        messages.add_message(request, messages.INFO, "Have to be admin to ban auction")
        return HttpResponseRedirect(reverse('home'))


def active_auction(request, id):

    if request.user.is_superuser:

        auction = Auction.objects.get(id=id)

        auction.lifecycle = 'A'
        auction.save()

        messages.add_message(request, messages.INFO, "Auction activeted")
        return HttpResponseRedirect(reverse('home'))

    else:
        messages.add_message(request, messages.INFO, "Have to be admin to make auction active")
        return HttpResponseRedirect(reverse('home'))


def emailhistory(request):

    path ="/Users/Aleksi/PycharmProjects/Project/email_backend"
    file_list = os.listdir(path)

    new_dict = {}
    i = 1

    for filenames in file_list:
        with open(os.path.join(path, filenames)) as myfile:

            content = myfile.readline(10)

            new_dict.update({'email'  + ":": file_list })
            i = i+1


    return render(request, 'emailhistory.html', {'files': new_dict})




class AddAuction(View):
    def get(self, request):
        form = createAuctionForm()
        return render(request, 'addAuction.html', {'form': form})

    def post(self, request):
        form = createAuctionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            b_title = cd['title']
            b_description = cd['description']
            b_end_date = cd['end_date']
            b_min_price = cd['min_price']
            b_seller = request.user
            print("Add auction:", b_title, b_description, b_end_date, b_min_price)
            form = ConfAuctionForm({"b_title": b_title, "b_description": b_description, "b_end_date": b_end_date,
                                    "b_min_price": b_min_price, "b_seller": b_seller})
            return render(request, 'wizardtest.html', {'form': form})
        else:
            messages.add_message(request, messages.ERROR, "Not valid data")
            return render(request, 'addAuction.html', {'form': form, })


def save_auction(request):
    option = request.POST.get('option', '')
    if option == 'Yes':
        b_title = request.POST.get('b_title', '')
        b_description = request.POST.get('b_description', '')
        b_end_date = request.POST.get('b_end_date', '')
        b_min_price = request.POST.get('b_min_price', '')
        user = request.user
        auction = Auction(title=b_title, description=b_description, end_date=b_end_date, seller=user,
                          min_price=b_min_price)
        auction.save()

        send_mail('Auction crated',
                  'New auction crated',
                  'admin@yaas.fi',
                  ['request.user.email'],
                  fail_silently=False)
        messages.add_message(request, messages.INFO, "New auction added and confirmation email sent")
        return HttpResponseRedirect(reverse("home"))
    else:
        messages.add_message(request, messages.INFO, "Blog cancelled")
        return HttpResponseRedirect(reverse('home'))


class EditAuction(LoginRequiredMixin, View):
    def get(self, request, id):
        auction = get_object_or_404(Auction, id=id)
        if request.user.id == auction.seller.id:
            return render(request, "editAuction.html",
                          {'user': request.user,
                            'title': auction.title,
                            'description': auction.description,
                            'id': auction.id,
                            'min_price': auction.min_price,
                            'end_date': auction.end_date})
        else:
            messages.add_message(request, messages.INFO, "Cant edit")
            return HttpResponseRedirect(reverse("home"))

    def post(self, request, id):
        auctions = Auction.objects.filter(id=id)
        if len(auctions) > 0:
            auction = auctions[0]
        else:
            messages.add_message(request, messages.INFO, "Invalid auction ID")
            return HttpResponseRedirect(reverse("home"))

        title = request.POST["title"].strip()
        description = request.POST["description"].strip()
        auction.title = title
        auction.description = description
        auction.updated = timezone.now()
        auction.save()
        messages.add_message(request, messages.INFO, "Auction posted")
        return HttpResponseRedirect(reverse("home"))

@login_required
def make_bid(request, id):
    latest = Bid.get_latest_bid(id)
    auction = Auction.get_active_by_id(id)
    if auction:

        if auction.seller.id == request.user.id:
            messages.add_message(request, messages.INFO, "cannot bid in own auction")
            return HttpResponseRedirect(reverse('home'))

        elif auction.end_date <= timezone.now():
            messages.add_message(request, messages.INFO, "auction has ended")
            return HttpResponseRedirect(reverse('home'))

        elif latest and request.user.id == latest.bidder.id:
            messages.add_message(request, messages.INFO, "you are already winning")
            return HttpResponseRedirect(reverse('home'))

        elif not auction.lifecycle == 'A':
            messages.add_message(request, messages.INFO, "Auction not active")
            return HttpResponseRedirect(reverse('home'))


        else:

            if request.method == 'POST':
                form = BidForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data

                    cd_bid = cd['bid']

                    if (cd_bid > auction.min_price) and (cd_bid > auction.get_latest(id)):

                        bidder = auction.get_bidder()

                        send_mail('Loosing',
                                  'Someone made better bid than you to auction :' + auction.title,
                                  'admin@yaas.fi',
                                  [bidder],
                                  fail_silently=False)


                        bid = Bid()
                        bid.bid = cd_bid
                        bid.auction = auction
                        bid.bidder = request.user
                        bid.save()
                        messages.add_message(request, messages.INFO, "Bid made")
                        send_mail('Auction made',
                                  'Someone made bid your auction:' + auction.title + 'ammount:'
                                  + str(auction.get_latest(id)),
                                  'admin@yaas.fi',
                                  [auction.seller.email],
                                  fail_silently=False)

                        #soft deadlines:
                        if auction.end_date - timezone.now() < timedelta(minutes=5):
                            auction.end_date = auction.end_date + timedelta(minutes=5)
                            auction.save()
                            messages.add_message(request, messages.INFO, "5 min added to auction deadline")

                        return HttpResponseRedirect(reverse('home'))
                    else:
                        messages.add_message(request, messages.INFO, "Bid needs to be biggeer than previous bid")
                        return HttpResponseRedirect(reverse('home'))
                else:
                    messages.add_message(request, messages.ERROR, "Not valid bit")
                    return HttpResponseRedirect(reverse('home'))

            else:
                messages.add_message(request, messages.INFO, "cant find an auction")
                return HttpResponseRedirect(reverse('home'))


class EditUser(LoginRequiredMixin, View):

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        if request.user.id == user.id:
            return render(request, 'editUser.html', {'user': request.user,
                                                     'id': user.id,
                                                     'email': user.email,
                                                     'password': user.password})
        else:
            messages.add_message(request, messages.INFO, "Cant edit user")
            return HttpResponseRedirect(reverse("home"))


    def post(self, request, id):

        user = get_object_or_404(User, id=id)

        email = request.POST['email'].strip()
        #password = request.POST['password'].strip()
        user.email = email
        #user.password = password
        user.save()
        messages.add_message(request, messages.INFO, "user editet")
        return HttpResponseRedirect(reverse("home"))









