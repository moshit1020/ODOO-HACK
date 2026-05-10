from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from .models import Trip, City, Stop, Activity, ChecklistItem
from .forms import RegistrationForm, TripForm, CityForm


def staff_user_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseForbidden('You do not have permission to access this page.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    cities = City.objects.all()[:10]
    return render(request, 'travelapp/index.html', {'cities': cities})

@login_required
def dashboard(request):
    trips = Trip.objects.filter(user=request.user).order_by('start_date').prefetch_related('stops__city')
    return render(request, 'travelapp/dashboard.html', {'trips': trips})

@login_required
def create_trip(request):
    cities = City.objects.all()
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            
            # Create a stop for the selected primary destination
            city_id = request.POST.get('primary_destination')
            if city_id:
                city = get_object_or_404(City, id=city_id)
                Stop.objects.create(
                    trip=trip,
                    city=city,
                    arrival_date=trip.start_date,
                    departure_date=trip.end_date
                )
                
            return redirect('dashboard')
    else:
        form = TripForm()
    return render(request, 'travelapp/create_trip.html', {'form': form, 'cities': cities})

@login_required
def itinerary(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    stops = trip.stops.all()
    cities = City.objects.all()
    return render(request, 'travelapp/itinerary.html', {
        'trip': trip,
        'stops': stops,
        'cities': cities
    })

@login_required
def add_stop(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id, user=request.user)
        city_id = request.POST.get('city_id')
        arrival_date = request.POST.get('arrival_date')
        departure_date = request.POST.get('departure_date')
        
        city = get_object_or_404(City, id=city_id)
        Stop.objects.create(
            trip=trip, city=city, 
            arrival_date=arrival_date, departure_date=departure_date
        )
        return redirect('itinerary', trip_id=trip.id)
    return redirect('dashboard')

@login_required
def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    return render(request, 'travelapp/city_detail.html', {'city': city})

@staff_user_required
def admin_panel(request):
    context = {
        'city_count': City.objects.count(),
        'trip_count': Trip.objects.count(),
        'user_count': User.objects.count(),
    }
    return render(request, 'travelapp/admin_panel.html', context)

@staff_user_required
def admin_city_list(request):
    cities = City.objects.order_by('name')
    return render(request, 'travelapp/admin_city_list.html', {'cities': cities})

@staff_user_required
def admin_city_create(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_city_list')
    else:
        form = CityForm()
    return render(request, 'travelapp/admin_city_form.html', {'form': form, 'page_title': 'Create City'})

@staff_user_required
def admin_city_edit(request, city_id):
    city = get_object_or_404(City, id=city_id)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('admin_city_list')
    else:
        form = CityForm(instance=city)
    return render(request, 'travelapp/admin_city_form.html', {'form': form, 'page_title': f'Edit City: {city.name}'})

@staff_user_required
def admin_city_delete(request, city_id):
    city = get_object_or_404(City, id=city_id)
    if request.method == 'POST':
        city.delete()
        return redirect('admin_city_list')
    return render(request, 'travelapp/admin_confirm_delete.html', {
        'object_name': city.name,
        'cancel_url': 'admin_city_list',
        'delete_url': 'admin_city_delete',
        'object_id': city.id,
        'item_type': 'city',
    })

@staff_user_required
def admin_trip_list(request):
    trips = Trip.objects.select_related('user').prefetch_related('stops__city').order_by('-start_date')
    return render(request, 'travelapp/admin_trip_list.html', {'trips': trips})

@staff_user_required
def admin_trip_delete(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        trip.delete()
        return redirect('admin_trip_list')
    return render(request, 'travelapp/admin_confirm_delete.html', {
        'object_name': trip.name,
        'cancel_url': 'admin_trip_list',
        'delete_url': 'admin_trip_delete',
        'object_id': trip.id,
        'item_type': 'trip',
    })
