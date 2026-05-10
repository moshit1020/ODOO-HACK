# Enhance Traveloop with Budgets, Trip Types, and City Highlights

This plan outlines the integration of new travel planning features: categorizing trips by traveler type (Single, Couple, Family), tracking trip budgets, highlighting what Indian cities are famous for (e.g., Goa for scuba diving), and upgrading the website aesthetics with professional assets and animations.

## User Review Required

> [!IMPORTANT]
> **Database Changes**: We will be modifying the `Trip` and `City` database models. This will require generating and running Django migrations (`python manage.py makemigrations` and `python manage.py migrate`). Are you okay with this?
> **Asset Generation**: I will generate custom, professional images using AI for the city cards to give the site a premium, custom feel instead of using standard stock photos.

## Open Questions

> [!TIP]
> 1. Do you want the **Budget** field to just be a text selection (e.g., "Luxury", "Budget") or an actual number where you type in a specific amount (e.g., ₹50,000)? I plan to add an actual number input for budget tracking, along with a text choice. Let me know if you prefer something else!
> 2. The cities currently seeded are Delhi, Mumbai, Jaipur, Agra, Goa, Kochi, Varanasi, Udaipur, Bengaluru, and Chennai. I will update these with specific "Famous For" descriptions. Does this list look good to you?

## Proposed Changes

---

### Database Models

#### [MODIFY] [models.py](file:///c:/Users/banda/OneDrive/Desktop/VS%20problem/traveloop_project/travelapp/models.py)
- **`Trip` Model**: 
  - Add `trip_type` (Choices: Solo, Couple, Family, Friends).
  - Add `budget` (DecimalField to track the numerical budget amount).
- **`City` Model**:
  - Add `famous_for` (TextField to describe activities like scuba diving, jet skiing, etc.).

### Seed Data & Assets

#### [MODIFY] [seed_cities.py](file:///c:/Users/banda/OneDrive/Desktop/VS%20problem/traveloop_project/seed_cities.py)
- Add "famous for" tags to all 10 cities (e.g., Goa: "Scuba diving, Jet Ski, Nightlife", Agra: "Taj Mahal, Heritage").
- Update the seed script to save the `famous_for` field to the database.

#### [NEW] Generated AI Image Assets
- I will use the `generate_image` tool to create visually stunning, professional backgrounds for cities and the hero sections, emphasizing the dynamic aesthetics requested.

### Forms

#### [MODIFY] [forms.py](file:///c:/Users/banda/OneDrive/Desktop/VS%20problem/traveloop_project/travelapp/forms.py)
- Update `TripForm` to include the new `trip_type` and `budget` fields, applying modern CSS classes for styling.

### UI & Animations

#### [MODIFY] [create_trip.html](file:///c:/Users/banda/OneDrive/Desktop/VS%20problem/traveloop_project/templates/travelapp/create_trip.html)
- Add the new `trip_type` dropdown and `budget` input fields.
- Apply dynamic CSS hover animations and transitions to make the form feel interactive and "cool".

#### [MODIFY] [index.html](file:///c:/Users/banda/OneDrive/Desktop/VS%20problem/traveloop_project/templates/travelapp/index.html)
- Display the `famous_for` field on the travel cards so users can see exactly what activities the city offers (e.g., Goa -> Scuba diving).
- Enhance the 3D hover animations on the travel cards.
- Add dynamic micro-animations to buttons and text.

## Verification Plan

### Automated Tests
- Run `python manage.py makemigrations` and `python manage.py migrate` to apply database changes.
- Run `python seed_cities.py` to refresh the city database with the new "famous for" details.
- Restart the Django server.

### Manual Verification
- Navigate to the homepage to confirm the travel cards show the new "Famous For" information with the new AI-generated images and cool animations.
- Attempt to create a new trip and verify the "Trip Type" and "Budget" fields are present, functioning, and styled elegantly.
