from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib.auth import mixins
from django.contrib import messages
from django.urls import reverse


from .models import Motherboard, Configuration, CPU
from .forms import CreateConfigurationForm


class MainView(generic.TemplateView):
    template_name = "index.html"



class MotherboardsListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Motherboard
    queryset = Motherboard.objects.all().order_by("-socket__name")
    context_object_name = "motherboards"
    template_name = "motherboards.html"



class CreateConfigurationView(mixins.LoginRequiredMixin, View):

    def post(self, request):
        form = CreateConfigurationForm(data=request.POST)

        main = request.POST.get("main")
        print(type(main), "\n\n\n")

        if form.is_valid():
            configuration = form.save(commit=False)
            configuration.user = request.user
            configuration.save()
            messages.info(request=request, message="Configuration created")
            return redirect(reverse("main:configuration_details", kwargs={"pk": configuration.pk}))
        messages.error(request=request, message="Error: check data")
        return redirect(reverse("main:my_configurations"))


class AddMotherboardToConfigurationView(mixins.LoginRequiredMixin, View):

    def get(self, request, pk):
        motherboard = get_object_or_404(Motherboard, pk=pk)
        configurations = request.user.configurations.filter(main=True)

        if len(configurations) > 1:
            messages.error(request=request, message="Error: You have 2 or more main configurations. Please choose only one.")
            return redirect(reverse("main:my_configurations"))
        elif len(configurations) == 0:
            messages.error(request=request, message="Error: you don't have main configuration. Please choose one.")
            return redirect(reverse("main:my_configurations"))
        
        configuration: Configuration = configurations[0]
        configuration.motherboard = motherboard
        configuration.save()
        messages.info(request=request, message="Motherboard selected.")
        return redirect(reverse("main:cpus"))
        
                
class MyConfigurationsListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Configuration
    queryset = Configuration.objects.all()
    template_name = "my_configurations.html"
    context_object_name = "configurations"