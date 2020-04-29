from django.shortcuts import render
from .models import Flights, Passenger
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def index(request):
    context = {
        "flights": Flights.objects.all()
    }
    return render(request,"flights/index.html", context)

def flight(request, flight_id):
    try:
        flight = Flights.objects.get(pk=flight_id)
    except Flights.DoesNotExist:
        raise Http404("Flight does not exist")
    context = {
        "flight": flight,
        "passengers": flight.passenger.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request,"flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flights.objects.get(pk=flight_id)
    except KeyError:
        return render(request,"flights/error.html", {"message": "No Selection."})
    except Passenger.DoesNotExist:
        return render(request,"flights/error.html", {"message": "No passenger."})
    except Flights.DoesNotExist:
        return render(request,"flights/error.html", {"message": "No flight."})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
