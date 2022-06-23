import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import EditSettings


@login_required
@user_passes_test(lambda u: u.is_superuser)
def managed_settings(request):
    file = open('settings.json')
    settings = json.load(file)

    return render(request, 'management/managed-settings.html', {'settings': settings})


def edit_cost_settings(request):
    post_url = reverse('management:edit-cost-settings', args=())
    back_url = reverse('management:managed-settings', args=())

    file = open("settings.json", "r")
    settings = json.load(file)
    file.close()

    if request.method == 'POST':
        form = EditSettings(request.POST, settings=settings)
        if form.is_valid():
            settings["professeur"]["hour_price"] = form.cleaned_data['teacher_hour_price']
            settings["professeur"]["eq_td"]["cm"] = form.cleaned_data['teacher_price_cm']
            settings["professeur"]["eq_td"]["td"] = form.cleaned_data['teacher_price_td']
            settings["professeur"]["eq_td"]["tp"] = form.cleaned_data['teacher_price_tp']

            settings["vacataire"]["hour_price"] = form.cleaned_data['contractor_hour_price']
            settings["vacataire"]["eq_td"]["cm"] = form.cleaned_data['contractor_price_cm']
            settings["vacataire"]["eq_td"]["td"] = form.cleaned_data['contractor_price_td']
            settings["vacataire"]["eq_td"]["tp"] = form.cleaned_data['contractor_price_tp']

            with open("settings.json", 'w') as file:
                json_object = json.dumps(settings, indent=4)
                file.write(json_object)
                file.close()

            return HttpResponseRedirect(reverse('management:managed-settings', args=()))
    else:
        form = EditSettings(settings=settings)
        return render(request, 'management/edit-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url})
