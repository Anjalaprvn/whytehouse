from django.shortcuts import render

# Create your views here.
def index(request):
     return render(request, 'user/international.html')
def domestic(request):
    return render(request, 'user/domestic.html') 
def about(request):
    return render(request, 'user/about.html')
def blog(request):
    return render(request, 'user/blog.html')
def blog_detail(request,slug):
    return render(request, 'user/blog_detail.html')
def contact(request):
    return render(request, 'user/contact.html')
def packages(request):
    return render(request,'user/packages.html')
def package_detail(request,slug):
    return render(request, 'user/package_detail.html')
def hospitality(request):
    return render(request, 'user/hospitality.html')