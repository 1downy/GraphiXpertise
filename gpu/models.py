import re
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class GPUList(models.Model):
    ProductName = models.CharField(max_length=500)
    GPUChip = models.CharField(max_length=120)
    Released = models.DateField(null=True, default=None)
    Bus = models.CharField(max_length=255)
    Memory = models.CharField(max_length=255)
    GPUclock = models.CharField(max_length=255)
    Memoryclock = models.CharField(max_length=255)
    Shaders_TMUs_ROPs = models.CharField(max_length=255)
    URL = models.URLField()
    gpu_specs = models.ForeignKey(
        'GPU', on_delete=models.SET_NULL, related_name="details", verbose_name="GPU", null=True, default=None)

    class Meta:
        ordering = ['ProductName']

    def __str__(self):
        return self.ProductName

    def save(self, *args, **kwargs):
        if "https://" not in self.URL:
            self.URL = f"https://www.techpowerup.com{self.URL}"
        super().save(*args, **kwargs)


class GPU(models.Model):
    name = models.CharField(max_length=100, verbose_name='GPU Name', null=True)
    variant = models.CharField(
        max_length=100, verbose_name='GPU Variant', null=True)
    architecture = models.CharField(
        max_length=100, verbose_name='Architecture', null=True)
    foundry = models.CharField(
        max_length=100, verbose_name='Foundry', null=True)
    process_size = models.CharField(
        max_length=20, verbose_name='Process Size', null=True)
    transistors = models.CharField(
        max_length=100, verbose_name='Transistors', null=True)
    density = models.CharField(
        max_length=20, verbose_name='Density', null=True)
    die_size = models.CharField(
        max_length=20, verbose_name='Die Size', null=True)
    chip_package = models.CharField(
        max_length=100, verbose_name='Chip Package', null=True)
    release_date = models.DateField(verbose_name='Release Date', null=True)
    generation = models.CharField(
        max_length=100, verbose_name='Generation', null=True)
    production = models.CharField(
        max_length=100, verbose_name='Production', null=True)
    launch_price = models.CharField(
        max_length=100, verbose_name='Launch Price', null=True)
    bus_interface = models.CharField(
        max_length=100, verbose_name='Bus Interface', null=True)
    gpu_clock = models.CharField(
        max_length=100, verbose_name='GPU Clock', null=True)
    boost_clock = models.CharField(
        max_length=100, verbose_name="Boost Clock", null=True)
    memory_clock = models.CharField(
        max_length=100, verbose_name='Memory Clock', null=True)
    memory_size = models.CharField(
        max_length=100, verbose_name='Memory Size', null=True)
    memory_type = models.CharField(
        max_length=100, verbose_name='Memory Type', null=True)
    memory_bus = models.CharField(
        max_length=20, verbose_name='Memory Bus', null=True)
    bandwidth = models.CharField(
        max_length=100, verbose_name='Bandwidth', null=True)
    shading_units = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Shading Units', null=True)
    tmus = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='TMUs', null=True)
    rops = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='ROPs', null=True)
    l1_cache = models.CharField(
        max_length=100, verbose_name='L1 Cache', null=True)
    l2_cache = models.CharField(
        max_length=100, verbose_name='L2 Cache', null=True)
    pixel_rate = models.CharField(
        max_length=100, verbose_name='Pixel Rate, null=True')
    texture_rate = models.CharField(
        max_length=100, verbose_name='Texture Rate', null=True)
    fp32_performance = models.CharField(
        max_length=100, verbose_name='FP32 (float)', null=True)
    fp64_performance = models.CharField(
        max_length=100, verbose_name='FP64 (double)', null=True)
    slot_width = models.CharField(
        max_length=100, verbose_name='Slot Width', null=True)
    length = models.CharField(max_length=20, verbose_name='Length', null=True)
    tdp = models.CharField(max_length=100, verbose_name='TDP', null=True)
    suggested_psu = models.CharField(
        max_length=100, verbose_name='Suggested PSU', null=True)
    outputs = models.CharField(
        max_length=100, verbose_name='Outputs', null=True)
    power_connectors = models.CharField(
        max_length=100, verbose_name='Power Connectors', null=True)
    board_number = models.CharField(
        max_length=100, verbose_name='Board Number', null=True)
    directx = models.CharField(
        max_length=20, verbose_name='DirectX', null=True)
    opengl = models.CharField(max_length=20, verbose_name='OpenGL', null=True)
    opencl = models.CharField(max_length=20, verbose_name='OpenCL', null=True)
    vulkan = models.CharField(max_length=20, verbose_name='Vulkan', null=True)
    shader_model = models.CharField(
        max_length=20, verbose_name='Shader Model', null=True)

    @property
    def numeric_specifications(self):
        fields_to_convert = {
            'shading_units': 'Shading Units',
            'tmus': 'TMUs',
            'rops': 'ROPs',
            'gpu_clock': 'GPU Clock',
            'boost_clock': 'Boost Clock',
            'memory_size': 'Memory Size',
            'memory_type': 'Memory Type',
            'memory_bus': 'Memory Bus',
            'bandwidth': 'Bandwidth',
            'tdp': 'TDP',
            'directx': 'DirectX',
            'opengl': 'OpenGL',
            'opencl': 'OpenCL',
            'vulkan': 'Vulkan',
            'shader_model': 'Shader Model',
            'fp32_performance': 'FP32 (float)',
            'fp64_performance': 'FP64 (double)',
            'pixel_rate': "Pixel Rate",
            'texture_rate': 'Texture Rate',
            'release_date': 'Release Date'
        }

        numeric_specifications = {}

        for field_name, field_verbose_name in fields_to_convert.items():
            field_value = getattr(self, field_name)

            if field_value is not None:
                # Use a regular expression to remove non-numeric characters
                cleaned_string = str(field_value).replace(
                    "_", '.').replace(',', '.')
                if field_name == "memory_type":
                    memory_types = {
                        "System Shared": 4.0,
                        "Legacy": 4.5,
                        "SGRAM": 4.5,
                        "CDRAM": 4.7,
                        "LPDDR3": 5.0,
                        "SDR": 5.0,
                        "DDR": 5.3,
                        "DDR2": 5.5,
                        "GDDR2": 5.5,
                        "eDRAM": 5.7,
                        "DDR3": 6.0,
                        "GDDR3": 6.0,
                        "LPDDR4": 6.0,
                        "DDR3L": 6.2,
                        "LPDDR4X": 6.3,
                        "GDDR4": 6.5,
                        "DDR4": 6.5,
                        "LPDDR5": 7.0,
                        "GDDR5": 7.5,
                        "GDDR5X": 8.0,
                        "GDDR6": 8.5,
                        "GDDR6X": 9.0,
                        "HBM": 9.0,
                        "HBM2": 9.3,
                        "HBM2e": 9.5,
                        "HBM3": 9.7,
                    }
                    numeric_specifications[field_name] = memory_types[cleaned_string]
                    continue
                if field_name == "pixel_rate":
                    pixel_rate = field_value.split(' ')
                    if pixel_rate[1] == "MPixel/s":
                        numeric_specifications[field_name] = float(
                            pixel_rate[0]) / 1000.0
                        continue
                if field_name == "texture_rate":
                    texture_rate = field_value.split(' ')
                    if texture_rate[1] == "MTexel/s":
                        numeric_specifications[field_name] = float(
                            texture_rate[0]) / 1000.0
                        continue
                if field_name == "memory_size":
                    memory_size = field_value.split(' ')
                    if memory_size[1] == "MB":
                        numeric_specifications[field_name] = float(
                            float(memory_size[0]) / 1024)
                        continue
                if field_name == "fp64_performance":
                    fp64_performance = field_value.split(' ')
                    if fp64_performance[1] == "GFLOPS":
                        numeric_specifications[field_name] = float(
                            float(fp64_performance[0]) / 1000)
                        continue
                if field_name == "fp32_performance":
                    fp32_performance = field_value.split(' ')
                    if fp32_performance[1] == "GFLOPS":
                        numeric_specifications[field_name] = float(
                            float(fp32_performance[0]) / 1000)
                        continue

                match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_string)
                if match:
                    cleaned_value = match.group()

                    try:
                        numeric_value = float(cleaned_value)
                    except ValueError as e:
                        numeric_value = None
                        print(
                            f"Error converting {field_verbose_name} to a numeric value.")
                else:
                    numeric_value = None
            else:
                numeric_value = None

            # Update the model with the cleaned numeric value

            numeric_specifications[field_name] = numeric_value

        return numeric_specifications

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'GPUs'
