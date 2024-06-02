from django import forms

Intensity_Choices = [
    ('Mild', 'Mild'),
    ('Moderate', 'Moderate'),
    ('Severe', 'Severe'),
]

BLOOD_TYPE_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
]


class UserProfileForm(forms.Form):
    phone_number = forms.CharField(max_length=15, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    last_menstrual_period = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    due_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    current_weight = forms.DecimalField(max_digits=5, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    height = forms.DecimalField(max_digits=4, decimal_places=1, required=False,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    blood_type = forms.ChoiceField(choices=BLOOD_TYPE_CHOICES, required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    emergency_contact = forms.CharField(max_length=100, required=False,
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))


class ContractionForm(forms.Form):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    duration = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    intensity = forms.ChoiceField(choices=Intensity_Choices, widget=forms.Select(attrs={'class': 'form-control'}))


class WeightTrackerForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    weight = forms.DecimalField(max_digits=5, decimal_places=2,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))


class DeliveryDatePredictionForm(forms.Form):
    last_menstrual_period = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    cycle_length = forms.IntegerField(
        initial=28,
        min_value=20,
        max_value=45,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '28'})
    )

    def calculate_due_date(self):
        from datetime import timedelta

        lmp = self.cleaned_data['last_menstrual_period']
        cycle_length = self.cleaned_data['cycle_length']

        # Typically, pregnancy lasts about 280 days (40 weeks) from the first day of the LMP.
        average_pregnancy_duration = timedelta(days=280)

        # Adjust due date based on cycle length if it's different from the typical 28 days.
        adjusted_due_date = lmp + average_pregnancy_duration + timedelta(days=(cycle_length - 28))

        return adjusted_due_date


class SymptomAssessmentForm(forms.Form):
    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describe your symptoms...'}),
        label="Describe your symptoms"
    )
