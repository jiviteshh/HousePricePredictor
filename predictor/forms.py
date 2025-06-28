from django import forms
import pandas as pd

# Load your dataset to extract unique values for dropdowns
df = pd.read_csv('properties.csv', low_memory=False)

# Clean and fill dropdowns
df['Parking'] = df['Parking'].astype(str).str.extract(r'(\d+)')
df['Parking'] = pd.to_numeric(df['Parking'], errors='coerce')
df.dropna(subset=['City', 'furnished Type', 'Ownership Type', 'Type of Property'], inplace=True)

# Extract choices
CITY_CHOICES = sorted(df['City'].dropna().unique())
FURNISHING_CHOICES = sorted(df['furnished Type'].dropna().unique())
OWNERSHIP_CHOICES = sorted(df['Ownership Type'].dropna().unique())
PROPERTY_TYPE_CHOICES = sorted(df['Type of Property'].dropna().unique())

# Define possession status choices
POSSESSION_STATUS_CHOICES = [
    ('', 'Select an option'),
    ('Ready to Move', 'Ready to Move'),
    ('Under Construction', 'Under Construction'),
]

# Define amenities choices
AMENITIES_CHOICES = [
    ('swimming_pool', 'Swimming Pool'),
    ('gymnasium', 'Gymnasium'),
    ('club_house', 'Club House'),
    ('garden', 'Garden'),
    ('security', 'Security'),
]

# Define floor number choices (1-50 floors)
FLOOR_CHOICES = [('', 'Select an option')] + [(str(i), str(i)) for i in range(1, 51)]

class HousePriceForm(forms.Form):
    carpet_area = forms.FloatField(label="Carpet Area (sqft)")
    bedroom = forms.IntegerField(label="Number of Bedrooms")
    bathroom = forms.IntegerField(label="Number of Bathrooms")
    parking = forms.IntegerField(label="Parking Spaces")

    city = forms.ChoiceField(
        choices=[('', 'Select an option')] + [(c, c) for c in CITY_CHOICES],
        required=True
    )
    furnished_type = forms.ChoiceField(
        label="Furnished Type", 
        choices=[('', 'Select an option')] + [(f, f) for f in FURNISHING_CHOICES],
        required=True
    )
    ownership_type = forms.ChoiceField(
        label="Ownership Type", 
        choices=[('', 'Select an option')] + [(o, o) for o in OWNERSHIP_CHOICES],
        required=True
    )
    property_type = forms.ChoiceField(
        label="Property Type", 
        choices=[('', 'Select an option')] + [(p, p) for p in PROPERTY_TYPE_CHOICES],
        required=True
    )
    
    possession_status = forms.ChoiceField(
        label="Possession Status",
        choices=POSSESSION_STATUS_CHOICES,
        required=True
    )
    
    floor_number = forms.ChoiceField(
        label="Floor Number",
        choices=FLOOR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'conditional-field'})
    )
    
    amenities = forms.MultipleChoiceField(
        label="Amenities",
        choices=AMENITIES_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'amenities-checkboxes'})
    )

    def clean(self):
        cleaned_data = super().clean()
        property_type = cleaned_data.get('property_type')
        floor_number = cleaned_data.get('floor_number')
        
        # Validate floor number is required for apartments
        if property_type == 'Apartment' and not floor_number:
            self.add_error('floor_number', 'Floor number is required for apartments.')
        
        return cleaned_data
