from django import forms
from django.contrib.auth.forms import UserCreationForm
from auctionApp.models import *
from datetime import timedelta
from django.utils import timezone

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            return user


class createAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('title', 'description', 'end_date', 'min_price')

    def clean(self):

        data = super(createAuctionForm, self).clean()

        if 'end_date' in data and not (timezone.now() + timedelta(days=3)) <= data.get('end_date'):

            self._errors["end_date"] = self.error_class(["invalid end date"])

        return data


class EditUserForm(forms.Form):
    class Meta:
        model = User
        fields = ('email', 'password1')


class ConfAuctionForm(forms.Form):
    CHOICES = [(x, x) for x in ("Yes", "No")]
    option = forms.ChoiceField(choices=CHOICES)
    b_title = forms.CharField(widget=forms.HiddenInput())
    b_description = forms.CharField(widget=forms.HiddenInput())
    b_end_date = forms.CharField(widget=forms.HiddenInput())
    b_min_price = forms.CharField(widget=forms.HiddenInput())
    b_seller = forms.CharField(widget=forms.HiddenInput())


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('id', 'bid')
