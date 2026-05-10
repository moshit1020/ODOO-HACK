from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    cost_index = models.CharField(max_length=50) # e.g. "$$"
    popularity = models.IntegerField(default=5) # 1-10
    famous_for = models.CharField(max_length=255, blank=True, null=True)
    famous_rides = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Jet Skiing, Banana Boat")
    famous_events = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Sunburn Festival")
    image_url = models.URLField(blank=True, null=True)
    activities_json = models.JSONField(default=dict, blank=True, help_text="JSON structure of activities and attractions")

    def __str__(self):
        return self.name

class Trip(models.Model):
    TRIP_TYPES = [
        ('Single', 'Single'),
        ('Couple', 'Couple'),
        ('Family', 'Family'),
        ('Friends', 'Friends'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    name = models.CharField(max_length=200)
    trip_type = models.CharField(max_length=50, choices=TRIP_TYPES, default='Single')
    num_travelers = models.PositiveIntegerField(default=1)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    cover_photo = models.URLField(blank=True, null=True)
    duration_days = models.IntegerField(default=0, help_text="Number of days for this trip")

    def __str__(self):
        return self.name

class Stop(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Estimated cost for this stop")

    class Meta:
        ordering = ['arrival_date']

    def __str__(self):
        return f"{self.city.name} ({self.trip.name})"

class Activity(models.Model):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration = models.CharField(max_length=100, blank=True, null=True) # e.g., "2 hours"

    def __str__(self):
        return self.name

class ChecklistItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='checklist_items')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True)
    is_packed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Note(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.trip.name} on {self.created_at.date()}"
