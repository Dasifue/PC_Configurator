from django.contrib import admin

from .models import (
    CPUsocket,
    CPUimages,
    CPU,
    RAM,
    RAMimage,
    RAMtype,
    Chipset,
    Motherboard,
    MotherboardImages,
)

class RAMimagesInstanceInline(admin.TabularInline):
    model = RAMimage


class CPUimagesInstanceInline(admin.TabularInline):
    model = CPUimages


class MotherboardImagesInstanceInline(admin.TabularInline):
    model = MotherboardImages


class RAMtypeInstanceInline(admin.TabularInline):
    model = RAMtype


@admin.register(CPUsocket)
class CPUsocketAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(CPU)
class CPUadmin(admin.ModelAdmin):
    list_display = ("name", "socket")
    search_fields = ("manufacturer", "mark", "generation")
    list_filter = ("socket", "manufacturer", "mark", "generation", "cores", "threads", "memory_type")
    inlines = (CPUimagesInstanceInline, )

    def display_socket(self):
        return self.socket.__str__()


@admin.register(RAM)
class RAMadmin(admin.ModelAdmin):
    list_filter = ("memory_type", "size", "tdp")
    inlines = (RAMimagesInstanceInline,)


@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display = ("name", "chipset", "socket")
    search_fields = ("name",)
    list_filter = ("socket", "chipset", "memory_type", "memory_slots")
    inlines = (MotherboardImagesInstanceInline,)


@admin.register(Chipset)
class ChipsetAdmin(admin.ModelAdmin):
    search_fields = ("name", )


@admin.register(RAMtype)
class RAMtypeAdmin(admin.ModelAdmin):
    search_fields = ("name", )