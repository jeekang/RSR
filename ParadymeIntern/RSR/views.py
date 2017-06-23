from django.shortcuts import render
from .filters import PersonFilter
from .models import Person
from django.views import generic

def search(request):
    f = PersonFilter(request.GET, queryset=Person.objects.all())
    return render(request, 'RSR/index.html', {'filter': f})

class detail(generic.DetailView):
    model = Person
    template_name = 'RSR/detail.html'