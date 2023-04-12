from django.shortcuts import render
# Create your views here.
TEMPLATE_DIR = (
'os.path.join(BASE_DIR, "templates"),'
)
def camera_catalog_view (request):
    return render(request, "Camera_Catalog.html")