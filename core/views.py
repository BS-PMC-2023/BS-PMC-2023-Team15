from django.shortcuts import render

# Create your views here.
def core_view(request):
    return render(request, 'base.html', {})
