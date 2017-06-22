from django.shortcuts import render
from .filters import PersonFilter
from .models import Person

def person_list(request):
    f = PersonFilter(request.GET, queryset=Person.objects.all())
    return render(request, 'RSR/index.html', {'filter': f})
