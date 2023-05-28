from django.shortcuts import render
from .forms import AlerteInvestigationForm

def alerte_investigation(request):
    form = AlerteInvestigationForm()

    if request.method == 'POST':
        form = AlerteInvestigationForm(request.POST)
        if form.is_valid():
            form.save()
            # Rediriger ou afficher un message de succès, selon vos besoins

    return render(request, 'alerte_investigation/alerte_investigation.html', {'form': form})
