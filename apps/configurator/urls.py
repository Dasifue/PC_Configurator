from django.urls import path

from .views import (
    MainView,
    MotherboardsListView,
    CreateConfigurationView,
    AddMotherboardToConfigurationView,
    MyConfigurationsListView
)

app_name = "main"

urlpatterns = [
    path("", view=MainView.as_view(), name="main"),
    path("motherboards/list/", view=MotherboardsListView.as_view(), name="motherboards"),
    path("configurations/create/", view=CreateConfigurationView.as_view(), name="configuration_create"),
    path("configurations/self/", view=MyConfigurationsListView.as_view(), name="my_configurations"),
    path("configurations/motherboard/<int:pk>", view=AddMotherboardToConfigurationView.as_view(), name="configuration_motherboard"),
]