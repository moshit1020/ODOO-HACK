from django import forms
from django.contrib.auth.models import User
from .models import Trip, City

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name', 'trip_type', 'num_travelers', 'budget', 'start_date', 'end_date', 'description', 'cover_photo']
        widgets = {
            'trip_type': forms.Select(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'state', 'country', 'cost_index', 'popularity', 'famous_for', 'famous_rides', 'famous_events', 'image_url', 'activities_json']
        widgets = {
            'activities_json': forms.Textarea(attrs={'rows': 5, 'placeholder': '{"activity":"description"}'}),
            'famous_for': forms.TextInput(attrs={'placeholder': 'Beaches, Culture, Cuisine'}),
            'famous_rides': forms.TextInput(attrs={'placeholder': 'Jet Skiing, Hot Air Balloon'}),
            'famous_events': forms.TextInput(attrs={'placeholder': 'Carnivals, Festivals'}),
        }
