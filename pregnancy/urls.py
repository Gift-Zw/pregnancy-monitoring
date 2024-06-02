"""
URL configuration for pregnancy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name="dashboard"),
    path('weight-tracker/', views.weight_tracker_view, name="weight-tracker"),
    path('delivery-date-calculator/', views.delivery_day_view, name="delivery-date"),
    path('risks/', views.risk_view, name="risks"),
    path('contractions/', views.contractions_view, name="contractions"),
    path('chat/', views.chat_view, name="chat"),
    path('diet/', views.diet_view, name="diet"),
    path('logout/', views.logout_view, name="logout"),
    path('log-in/', views.RegularUserLoginView.as_view(), name="user-login"),
    path('register/', views.UserRegistrationView.as_view(), name="user-register"),
    path('user-profile/', views.create_user_profile_view, name="user-profile"),


]
