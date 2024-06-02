from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.views.generic import CreateView
from .models import User, UserProfile, Contraction, WeightTracker, PregnancyRisk, DietPlan
from .admin import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserProfileForm, ContractionForm, DeliveryDatePredictionForm, WeightTrackerForm, \
    SymptomAssessmentForm, DietPlanForm
from .decorators import user_required
from django.utils.dateparse import parse_duration
from .symptom_assesment import get_assessment

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout_view(request):
    logout(request)
    return redirect('user-login')


class UserRegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register_user.html'
    success_url = reverse_lazy('user-profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = User.objects.get(email=email)
        user.is_staff = False
        user.save()
        login(self.request, user)
        return redirect('user-login')


class RegularUserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'user_login.html'
    redirect_authenticated_user = True
    redirect_field_name = 'next'

    def get_success_url(self):
        user_profile = UserProfile.objects.filter(user=self.request.user)
        if user_profile.exists():
            return reverse_lazy('dashboard')
        else:
            return reverse_lazy('user-profile')


@user_required()
def index_view(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    days_left = user_profile.due_date - datetime.today().date()

    ctx = {
        'weight': WeightTracker.objects.filter(user=request.user).first().weight if WeightTracker.objects.filter(user=request.user).count() != 0  else user_profile.current_weight,
        'delivery_date': user_profile.due_date,
        'days_left': days_left.days,
        'height': user_profile.height,
        'mild_contractions': Contraction.objects.filter(intensity='Mild', user=request.user).count(),
        'severe_contractions': Contraction.objects.filter(intensity='Severe', user=request.user).count(),
        'moderate_contractions': Contraction.objects.filter(intensity='Moderate', user=request.user).count(),
        'contractions': Contraction.objects.filter(user=request.user)[:5]
    }
    return render(request, 'index.html', ctx)


@user_required()
def weight_tracker_view(request):
    if request.method == 'POST':
        form = WeightTrackerForm(request.POST)
        if form.is_valid():
            weight_record = WeightTracker.objects.create(
                user=request.user,
                date=form.data['date'],
                weight=form.data['weight'],
            )
            weight_record.save()
            return redirect('weight-tracker')
    ctx = {
        'form': WeightTrackerForm(),
        'weight_records': WeightTracker.objects.filter(user=request.user)
    }
    return render(request, 'weight_tracker.html', ctx)


@user_required()
def delivery_day_view(request):
    if request.method == 'POST':
        form = DeliveryDatePredictionForm(request.POST)
        if form.is_valid():
            date = form.calculate_due_date()
            return render(request, 'delivery_estimator.html', {
                'form': DeliveryDatePredictionForm(),
                'date':date
            })

    ctx = {
        'form': DeliveryDatePredictionForm()
    }
    return render(request, 'delivery_estimator.html', ctx)


@user_required()
def contractions_view(request):
    if request.method == 'POST':
        form = ContractionForm(request.POST)
        if form.is_valid():
            print(type(form.data['start_time']))
            contraction = Contraction.objects.create(
                user=request.user,
                start_time=form.data['start_time'],
                duration=form.data['duration'],
                intensity=form.data['intensity'],
            )
            contraction.save()
    ctx = {
        'form': ContractionForm(),
        'contractions_list': Contraction.objects.filter(user=request.user)
    }
    return render(request, 'contractions.html', ctx)


@user_required()
def risk_view(request):
    if request.method == 'POST':
        form = DietPlanForm(request.POST)
        if form.is_valid():
            data = get_assessment(form.data['diet_plan'])
            return render(request, 'diet.html', {
                'form': DietPlanForm(),
                'response': data['text']
            })
    ctx = {
        'form': DietPlanForm()
    }
    return render(request, 'diet.html', ctx)


@user_required()
def chat_view(request):
    if request.method == 'POST':
        form = SymptomAssessmentForm(request.POST)
        if form.is_valid():
            data = get_assessment(form.data['symptoms'])
            return render(request, 'chat_doc.html', {
                'form': SymptomAssessmentForm(),
                'response': data['text']
            })
    ctx = {
        'form': SymptomAssessmentForm()
    }
    return render(request, 'chat_doc.html', ctx)


@user_required()
def diet_view(request):
    if request.method == 'POST':
        form = DietPlanForm(request.POST)
        if form.is_valid():
            data = get_assessment(form.data['diet_plan'])
            return render(request, 'diet.html', {
                'form': DietPlanForm(),
                'response': data['text']
            })
    ctx = {
        'form': DietPlanForm()
    }
    return render(request, 'diet.html', ctx)


@user_required()
def create_user_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = UserProfile.objects.create(
                user=request.user,
                phone_number=form.data['phone_number'],
                date_of_birth=form.data['date_of_birth'],
                current_weight=form.data['current_weight'],
                last_menstrual_period=form.data['last_menstrual_period'],
                height=form.data['height'],
                due_date=form.data['due_date'],
                emergency_contact=form.data['emergency_contact'],
                blood_type=form.data['blood_type']
            )
            profile.save()
            return redirect('dashboard')

    ctx = {
        'form': UserProfileForm()
    }
    return render(request, 'create_user_profile.html', ctx)


@user_required()
def logout_view(request):
    logout(request)
    return redirect('dashboard')
