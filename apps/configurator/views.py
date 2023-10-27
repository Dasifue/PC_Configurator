from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib.auth import mixins
from django.contrib import messages
from django.urls import reverse


from .models import Motherboard, Configuration, CPU
from .forms import ConfigurationForm


class MainView(generic.TemplateView):
    template_name = "index.html"



class MotherboardsListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Motherboard
    queryset = Motherboard.objects.all().order_by("-socket__name")
    context_object_name = "motherboards"
    template_name = "motherboards.html"



class CreateConfigurationView(mixins.LoginRequiredMixin, View):

    def post(self, request):
        form = ConfigurationForm(data=request.POST)

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
            messages.error(request=request, message=f"Error: You have {len(configurations)} main configurations. Please choose only one.")
            return redirect(reverse("main:my_configurations"))
        elif len(configurations) == 0:
            messages.error(request=request, message="Error: you don't have main configuration. Please choose one.")
            return redirect(reverse("main:my_configurations"))
        
        configuration: Configuration = configurations[0]
        configuration.motherboard = motherboard
        configuration.save()
        messages.info(request=request, message="Motherboard selected.")
        return redirect(reverse("main:"))
    


class CPUListView(generic.ListView):
    model = CPU
    queryset = CPU.objects.all()
    context_object_name = "cpu_list"
    template_name = "cpus.html"


class AddCPUToMotherboardView(mixins.LoginRequiredMixin, View):

    def get(self, request, pk):
        cpu = get_object_or_404(CPU, pk=pk)
        configurations = request.user.configurations.filter(main=True)
        print(configurations)
        if len(configurations) > 1:
            messages.error(request=request, message=f"Error: You have {len(configurations)} main configurations. Please choose only one.")
            return redirect(reverse("main:my_configurations"))
        if configurations.count() == 0:
            messages.error(request=request, message="Error: you don't have main configuration. Please choose one.")
            return redirect(reverse("main:my_configurations"))
        
        configuration = configurations.first()
        configuration.cpu = cpu
        configuration.save()
        return redirect(reverse("main:main"))

                
class MyConfigurationsListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Configuration
    queryset = Configuration.objects.all()
    template_name = "my_configurations.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        configurations = self.model.objects.filter(user=user)
        return {'configurations': configurations}
    

class ConfigurationDetailsView(generic.DetailView, generic.UpdateView):
    model = Configuration
    form_class = ConfigurationForm
    pk_url_kwarg = "pk"
    context_object_name = "configuration"
    template_name = "configuration.html"

    def get_success_url(self):
        return self.request.get_full_path()
    

    def get(self, request, pk):
        configuration = get_object_or_404(Configuration, pk=pk)
        form = self.form_class

        motherboard = configuration.motherboard
        cpu = configuration.cpu 
        
        if None not in (motherboard, cpu):
            if motherboard.socket != cpu.socket:
                messages.error(request, "Your motherboard and cpu are incompatible")

        return render(request=request, template_name=self.template_name, context={"form": form, "configuration":configuration})
    

        

    