import os
import json
import requests
from django.http.response import HttpResponse, JsonResponse
from django import forms
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .models import *



"""FORMS AND HELPER FUNCTIONS"""
# Choice of 'day' field in TripDetailForm (info will be appended by 'recommendation' view)
DAY_CHOICE = [] # e.g. [('1', 'Day 1'), ('2', 'Day 2'), ('3', 'Day 3')]

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['country', 'days']


def activateForm(): # Form will only be activated when called (due to the need of customizing 'day' field)
    class TripDetailForm(forms.ModelForm):
        # day = forms.CharField(widget=forms.Select(choices=DAY_CHOICE))
        day = forms.ChoiceField(choices=DAY_CHOICE)
        duration = forms.DecimalField(label="Duration (Hours)", min_value=0.1, max_value=24.0)

        class Meta:
            model = TripDetail
            fields = ['day', 'duration']

    return TripDetailForm


def lookup(country, pageNum): # Look up popular places for specific country (pagination taken into account)
    index = pageNum * 10 - 10 # Starting number
    
    try: # Contact API
        api_key = os.environ.get('WEBCAM_API_KEY') # link to webcam api - https://api.windy.com/webcams
        # Limit to 11 responses at once, starting from index'th response (we only need 10, 11th is to trigger the existence of next page)
        response = requests.get(f"https://api.windy.com/api/webcams/v2/list/country={country}/orderby=popularity/limit=11,{index}?show=webcams:location,image&key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try: # Parse response
        webcams = response.json()["result"]["webcams"]
        # print("\n\nreturned webcams - ", webcams)
        destinations = []
        for webcam in webcams:
            destination = {
                'name': webcam["title"],
                'image': webcam["image"]["daylight"]["preview"], # Can be 'daylight' or 'current'
                'city': webcam["location"]["city"],
                'region': webcam["location"]["region"]
            }
            destinations.append(destination)
        return destinations
    except (KeyError, TypeError, ValueError):
        return None


"""VIEWS"""
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning(request, "Invalid username and/or password.")
            return render(request, "planner/login.html")
    else:
        return render(request, "planner/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request, "Passwords must match.")
            return render(request, "planner/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(request, "Username already taken.")
            return render(request, "planner/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
        
    else:
        return render(request, "planner/register.html")


def index(request):
    if request.method == "POST": # Planning new trip
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to save your trips.")
            return HttpResponseRedirect(reverse('index'))

        form = TripForm(request.POST)
        if not form.is_valid():
            messages.warning(request, "Invalid form submitted.")
            return HttpResponseRedirect(reverse('index'))

        country = form.cleaned_data["country"]
        days = form.cleaned_data["days"]
        trip = Trip(owner=request.user, country=country, days=days)
        trip.save()
        for day in range(1, int(days) + 1):
            tripDetail = TripDetail(trip=trip, day=day)
            tripDetail.save()
        return HttpResponseRedirect(reverse('detail-trip', args=(trip.id,)))

    # GET Request
    # Limit 8 user trips to show up on index page
    userTrips = Trip.objects.filter(owner=request.user)[:8] if request.user.is_authenticated else None
    pageNum = int(request.GET.get("page") or 1)
    publicTrips = Trip.objects.filter(private=False).order_by('-created')
    p = Paginator(publicTrips, 12)

    try:
        currentPage = p.page(pageNum)
    except EmptyPage:
        messages.warning(request, f"Page {pageNum} does not exist.")
        return HttpResponseRedirect(reverse('index'))

    context = {
        'template': 'index',
        'tripForm': TripForm(),
        'trips': userTrips,
        'currentPage': currentPage
    }
    return render(request, "planner/index.html", context)


def trip(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to save your trips.")
        return HttpResponseRedirect(reverse('index'))

    userTrips = Trip.objects.filter(owner=request.user)
    pageNum = int(request.GET.get("page") or 1)
    p = Paginator(userTrips, 16)

    try:
        currentPage = p.page(pageNum)
    except EmptyPage:
        messages.warning(request, f"Page {pageNum} does not exist.")
        return HttpResponseRedirect(reverse('trip'))

    context = {
        'template': 'trip',
        'tripForm': TripForm(),
        'currentPage': currentPage
    }
    return render(request, "planner/index.html", context)


@csrf_exempt
def detailTrip(request, trip_id): # Shows timeline of users' trip (editable by owners)
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == "POST": # Owner deletes trip / owner wish to clone trip made by another person
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to clone trips.")
            return HttpResponseRedirect(reverse('index'))
        
        purpose = request.POST["purpose"]
        if (purpose == "delete"):
            if (trip.owner != request.user):
                messages.warning(request, "You can't delete trips made by others.")
            trip.delete()
            messages.success(request, "Your trip has been deleted successfully.")

        else: # purpose = clone (User wish to clone trip made by another person)
            newTrip = Trip(owner=request.user, country=trip.country, days=trip.days, clonedFrom=trip.owner)
            newTrip.save()
            for day in range(1, trip.days):
                newTripDetail = TripDetail(trip=newTrip, day=day)
                newTripDetail.save()
                tripDetail = TripDetail.objects.get(trip=trip, day=day)
                for tripDestination in tripDetail.destinations.all():
                    newTripDetailDestination = TripDetailDestination(tripDetail=newTripDetail, destination=tripDestination.destination, duration=tripDestination.duration)
                    newTripDetailDestination.save()
            messages.success(request, "Trip has been cloned.")

        return HttpResponseRedirect(reverse('index'))


    if request.method == "PUT":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "You must be logged in to delete destination."}, status=400)
        elif (trip.owner != request.user):
            return JsonResponse({"error": "You can't delete someone else's destination."}, status=400)
            
        data = json.loads(request.body)
        purpose = data.get("purpose", "") # 'deleteActivity' / 'privacy'

        if (purpose == 'deleteActivity'): # Delete specific activity from TripDetailDestination
            tripDetailID = int(data.get("tripDetailID", ""))
            destinationID = int(data.get("destinationID", ""))
            tripDetailDestination = TripDetailDestination.objects.get(tripDetail__id=tripDetailID, destination__id=destinationID)
            tripDetailDestination.delete()

        elif (purpose == 'privacy'): # Change trip privacy
            private = data.get("private", "")
            trip.private = private
            trip.save()

        return JsonResponse({"message": "Destination deleted."}, status=201)

    # GET Request
    tripDetails = TripDetail.objects.filter(trip=trip).order_by('day')
    pageNum = int(request.GET.get("page") or 1) # Pagination
    p = Paginator(tripDetails, 10)

    try:
        currentPage = p.page(pageNum)
    except EmptyPage:
        messages.warning(request, f"Page {pageNum} does not exist.")
        return HttpResponseRedirect(reverse('detail-trip', args=(trip_id,)))

    context = {
        'template': 'timeline',
        'trip': trip,
        'currentPage': currentPage
    }
    return render(request, "planner/trip.html", context)


def recommendation(request, trip_id): # Recommend destinations to users (through API)
    trip = get_object_or_404(Trip, pk=trip_id)
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to save your trips.")
            return HttpResponseRedirect(reverse('index'))

        form = activateForm() # returns TripDetailForm
        form = form(request.POST)
        if not form.is_valid():
            messages.warning(request, "Invalid form submitted.")
            return HttpResponseRedirect(reverse('recommendation', args=(trip_id,)))
    
        name = request.POST["name"]
        city = request.POST["city"]
        region = request.POST["region"]
        day = form.cleaned_data["day"]
        hours = form.cleaned_data["duration"]

        # Check if activities have exceeded 24 hour (which is non-logical)
        tripDetail = TripDetail.objects.get(trip=trip, day=int(day))
        sum_hours = 0.0
        for destination in tripDetail.destinations.all():
            sum_hours += float(destination.duration)
        if (float(hours) + sum_hours > 24.0):
            messages.warning(request, f"Oops, it seems you have exceeded 24 hours worth of activities in day {day}.")
            return HttpResponseRedirect(reverse('detail-trip', args=(trip_id,)))

        try: # Check if destination already exist
            destination = Destination.objects.get(name=name, city=city, region=region)
        except Destination.DoesNotExist:
            destination = Destination(name=name, city=city, region=region)
            destination.save()

        try:
            tripDetailDestination = TripDetailDestination(tripDetail=tripDetail, destination=destination, duration=hours)
            tripDetailDestination.save()
        except IntegrityError:
            messages.warning(request, f"Oops, it seems this destination already exist on day {day}.")
            return HttpResponseRedirect(reverse('detail-trip', args=(trip_id,)))

        if (trip.clonedFrom): # If trip was previously owned by someone, remove the original owner (as user has now modified the trip)
            trip.clonedFrom = None
            trip.save()

        messages.success(request, "Successfully added destination to your trip.")
        return HttpResponseRedirect(reverse('detail-trip', args=(trip_id,)))

    # GET Request
    pageNum = int(request.GET.get("page") or 1) # Pagination
    tripDetails = lookup(trip.country.code, pageNum) # Always return list of 11 objects
    if not tripDetails: # API failed
        messages.warning(request, f"Something went wrong. Please try again.")
        return HttpResponseRedirect(reverse('recommendation', args=(trip_id,)))

    p = Paginator(tripDetails, 10) # will always be 2 pages with the 1st being what the user wants

    try:
        if (pageNum < 1 or len(tripDetails) == 0):
            raise EmptyPage
        currentPage = p.page(1)
    except EmptyPage:
        messages.warning(request, f"Page {pageNum} does not exist.")
        return HttpResponseRedirect(reverse('recommendation', args=(trip_id,)))

    days = trip.days
    global DAY_CHOICE 
    DAY_CHOICE = [] # Reset it to empty list (in case there are old values residing in it)
    for day in range(1, days+1):
        choice = (f'{day}', f'Day {day}')
        DAY_CHOICE.append(choice)
    form = activateForm() # Activate TripDetailForm after appending information to DAY_CHOICE

    context = {
        'template': 'recommendations',
        'trip': trip,
        'tripDetailForm': form,
        'currentPage': currentPage,
        'pageNum': pageNum
    }
    return render(request, "planner/trip.html", context)