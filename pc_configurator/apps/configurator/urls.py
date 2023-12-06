from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", view=views.MainView.as_view(), name="main"),
    path("motherboards/list/", view=views.MotherboardsListView.as_view(), name="motherboards"),
    path("cpu/list/", view=views.CPUListView.as_view(), name="cpus"),
    path("configurations/create/", view=views.CreateConfigurationView.as_view(), name="configuration_create"),
    path("configurations/self/", view=views.MyConfigurationsListView.as_view(), name="my_configurations"),
    path("configurations/motherboard/<int:pk>", view=views.AddMotherboardToConfigurationView.as_view(), name="configuration_motherboard"),
    path("configurations/cpu/<int:pk>", view=views.AddCPUToMotherboardView.as_view(), name="configuration_cpu"),
    path("configurations/details/<int:pk>", view=views.ConfigurationDetailsView.as_view(), name="configuration_details"),
]