from django.shortcuts import render
from django.http import HttpResponse


TEMPLATE_DIR = (
    'os.path.join(BASE_DIR, "templates"),'
)
def login_view (request):
    return render(request, "LogIn_Page.html")
def profile_view (request):
    return render(request, "Profile.html")
def student_view (request):
    return render(request, "student_page.html")
def lecturer_view (request):
    return render(request, "lecturer_page.html")

def manager_view (request):
    return render(request, "manager_page.html")

def malfunction_view (request):
    return render(request, "malfunction_page.html")

def products_view (request):
    return render(request, "products_page.html")

def studio_view (request):
    return render(request, "studio_list.html")

def podcast_view (request):
    return render(request, "podcast_page.html")
def contact_view(request):
    return render(request, "contact.html")
def camera_catalog_view(request):
    return render(request, "Camera_Catalog.html")
def signout(request):
    pass