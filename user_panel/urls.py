from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('domestic/', views.domestic, name='domestic'), 
    path('about/', views.about, name='about'),
   
    path('contact/', views.contact, name='contact'),
    path('packages/',views.packages,name='packages'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('hospitality/', views.hospitality, name='hospitality'), 
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/", views.blog_list, name="blog"),  # ✅ alias for old templates
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),


]