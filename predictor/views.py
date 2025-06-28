from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import HousePriceForm
import joblib
import pandas as pd
from django.contrib.humanize.templatetags.humanize import intcomma
import os
from django.conf import settings

# ✅ Robust way to load model from project base directory
model_path = os.path.join(settings.BASE_DIR, 'house_price_model.pkl')
model = joblib.load(model_path)

def predict_price(request):
    form = HousePriceForm()
    price_inr = None

    if request.method == 'POST':
        form = HousePriceForm(request.POST)
        if form.is_valid():
            # Prepare amenities as a string (comma-separated)
            amenities_list = form.cleaned_data.get('amenities', [])
            amenities_str = ', '.join(amenities_list) if amenities_list else 'None'
            
            input_data = pd.DataFrame([{
                'Carpet Area': form.cleaned_data['carpet_area'],
                'bedroom': form.cleaned_data['bedroom'],
                'Bathroom': form.cleaned_data['bathroom'],
                'Parking': form.cleaned_data['parking'],
                'City': form.cleaned_data['city'],
                'furnished Type': form.cleaned_data['furnished_type'],
                'Ownership Type': form.cleaned_data['ownership_type'],
                'Type of Property': form.cleaned_data['property_type'],
                'Possession Status': form.cleaned_data['possession_status'],
                'Floor Number': form.cleaned_data.get('floor_number', ''),
                'Amenities': amenities_str
            }])

            try:
                prediction = model.predict(input_data)[0]
                prediction = max(0, round(prediction))
                
                # Handle case when prediction is 0
                if prediction == 0:
                    price_inr = "We're sorry, but we couldn't generate a reliable estimate for this property based on the provided details. Please review your inputs or try with different values."
                else:
                    formatted_price = intcomma(prediction)
                    price_inr = formatted_price

                # Store in session to survive redirect but clear on refresh
                request.session['price'] = price_inr
                request.session.save()  # Ensure session is saved
                return redirect('predict_price')

            except Exception as e:
                price_inr = f"Prediction Error: {e}"

    # GET request after POST redirect
    if 'price' in request.session:
        price_inr = request.session['price']
        del request.session['price']  # clear after first view

    return render(request, 'form.html', {'form': form, 'price_inr': price_inr})
