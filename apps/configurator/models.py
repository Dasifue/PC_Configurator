from django.db import models

MANUFACTURER_CHOICES = (
    ("intel", "Intel"),
    ("amd", "AMD"),
)

class CPUsocket(models.Model):
    name = models.CharField("Name", max_length=100)

    class Meta:
        verbose_name = "CPU socket"
        verbose_name_plural = "CPU sockets"

    def __str__(self):
        return self.name


class RAMtype(models.Model):
    name = models.CharField("Name", max_length=100)

    class Meta:
        verbose_name = "RAM type"
        verbose_name_plural = "RAM types"

    def __str__(self):
        return self.name


class Chipset(models.Model):
    name = models.CharField("Name", max_length=100)

    class Meta:
        verbose_name = "Chipset"
        verbose_name_plural = "Chipsets"
    
    def __str__(self):
        return self.name
    


class CPU(models.Model):
    manufacturer = models.CharField("Manufacturer", max_length=10, choices=MANUFACTURER_CHOICES, null=False, blank=False)
    socket = models.ForeignKey(CPUsocket, on_delete=models.SET_NULL, null=True, related_name="cpu", verbose_name="Socket")
    mark = models.CharField("Mark", max_length=100)
    generation = models.CharField("Generation", max_length=100)
    cores = models.PositiveSmallIntegerField("Cores")
    threads = models.PositiveSmallIntegerField("Threads")
    frequency = models.DecimalField("Frequency", max_digits=5, decimal_places=2)
    turbo_frequency = models.DecimalField("Turbo frequency", max_digits=5, decimal_places=2)
    max_ram = models.PositiveSmallIntegerField("Max RAM")
    memory_type = models.ForeignKey(RAMtype, on_delete=models.SET_NULL, null=True, related_name="cpu", verbose_name="Memory type")
    tdp = models.PositiveIntegerField("TDP")

    class Meta:
        verbose_name = "CPU"
        verbose_name_plural = "CPU's"

    def __str__(self):
        return f"{self.manufacturer} {self.mark} - {self.generation}"
    
    @property
    def name(self):
        return f"{self.manufacturer} {self.mark} - {self.generation}"
    
    def is_visible(self):
        return self.socket is not None
  


class CPUimages(models.Model):
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, related_name="images", verbose_name="CPU")
    image = models.ImageField("Image", upload_to="cpu/", null=False, blank=False)

    class Meta:
        verbose_name = "CPU image"
        verbose_name_plural = "CPU images"
    
    def __str__(self):
        return self.cpu.__str__()


class RAM(models.Model):
    memory_type = models.ForeignKey(RAMtype, on_delete=models.CASCADE, related_name="ram", verbose_name="RAM")
    size = models.PositiveSmallIntegerField("Size")
    tdp = models.PositiveIntegerField("TDP")

    class Meta:
        verbose_name = "RAM"
        verbose_name_plural = "RAM's"

    def __str__(self):
        return f"{self.memory_type.name} - {self.size} Gb"
    

class RAMimage(models.Model):
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE, related_name="images", verbose_name="RAM")
    image = models.ImageField("Image", upload_to="ram/", null=False, blank=False)

    class Meta:
        verbose_name = "RAM image"
        verbose_name_plural = "RAM images"

    def __str__(self):
        return self.ram.__str__()


class Motherboard(models.Model):
    socket = models.ForeignKey(CPUsocket, on_delete=models.SET_NULL, null=True, related_name="motherboards", verbose_name="Socket")
    chipset = models.ForeignKey(Chipset, on_delete=models.SET_NULL, null=True, related_name="motherboards", verbose_name="Chipset")
    name = models.CharField("Name", max_length=255)
    memory_type = models.ForeignKey(RAMtype, on_delete=models.SET_NULL, null=True, related_name="motherboards", verbose_name="Memory type")
    memory_slots = models.PositiveSmallIntegerField("RAM slots count")

    class Meta:
        verbose_name = "Motherboard"
        verbose_name_plural = "Motherboards"

    def __str__(self):
        return f"{self.chipset.name} {self.name} {self.socket.name}"

    def is_visible(self):
        return self.socket is not None
  

class MotherboardImages(models.Model):
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE, related_name="images", verbose_name="Motherboard")
    image = models.ImageField("Image", upload_to="motherboard/", null=False, blank=False)
    
    class Meta:
        verbose_name = "Motherboard image"
        verbose_name_plural = "Motherboard images"

    def __str__(self):
        return self.motherboard.name