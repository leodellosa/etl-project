from django.shortcuts import render, redirect
from .models import APISettings
from .forms import APISettingsForm
from django.contrib import messages

def admin_settings(request):
    settings, _ = APISettings.objects.get_or_create(pk=1)

    if request.method == "POST":
        form = APISettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings saved successfully.")
            return redirect('admin-settings')
        else:
            messages.error(request, "There were errors in the form. Please correct them and try again.")
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = APISettingsForm(instance=settings)

    return render(request, "admin_settings.html", {"form": form})
