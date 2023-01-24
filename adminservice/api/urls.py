
from django.urls import path

from . import views

urlpatterns = [
    path('csrf/', views.get_csrf, name='api-csrf'),
    path('login/', views.login_view, name='api-login'),
    path('logout/', views.logout_view, name='api-logout'),
    path('session/', views.session_view, name='api-session'),
    path('whoami/', views.whoami_view, name='api-whoami'),
    path('register/', views.register_view, name='api-whoami'),
    path('mytenant/', views.mytenant_view, name='api-mytenant'),
    path('tenant/', views.specifictenant_view, name="api-theme"),
    path('subscription/', views.subscription_view, name='api-subscription'),
    path('theme/', views.theme_view, name='api-theme'),
    path('freetenants/', views.freetenants_view, name='api-theme'),
]