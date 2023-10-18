from django.shortcuts import render
from gpu.models import GPUList, GPU
from .utils import get_specs, get_headers, compare_gpus
import requests
from django.db.models import Q

# Create your views here.


def home(request):
    gpu_names = []
    gpulist = GPUList.objects.only('id', 'ProductName').all()
    for i in gpulist:
        gpu_names.append({"value": i.id, "text": i.ProductName})
    context = {"gpulist": gpu_names}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def compare(request):
    if request.method == "POST":
        gpu_num = 'gpu'
        num = 1
        context = {}
        user_gpu1 = request.POST.get('gpu1', False)
        compare_mode = request.POST.get('comparemode', False)
        user_gpu2 = request.POST.get('gpu2', False)
        if user_gpu1 and user_gpu2:
            gpu_data = []
            gpu1, gpu2 = GPUList.objects.select_related('gpu_specs').filter(
                Q(id=user_gpu1) | Q(id=user_gpu2))
            selected_gpus = [gpu1, gpu2]
            for g in selected_gpus:
                if g.gpu_specs:
                    context[gpu_num+str(num)] = g
                    num += 1
                    continue
                response = requests.get(g.URL, headers=get_headers()).content
                data = get_specs(response)
                gpu_data.append(data)
                for gpu in gpu_data:
                    created_gpu = GPU.objects.create(
                        name=gpu.get("Graphics Processor", {}
                                     ).get("GPU Name", None),
                        variant=gpu.get("Graphics Processor", {}).get(
                            "GPU Variant", None),
                        architecture=gpu.get("Graphics Processor", {}).get(
                            "Architecture", None),
                        foundry=gpu.get("Graphics Processor",
                                        {}).get("Foundry", None),
                        process_size=gpu.get("Graphics Processor", {}).get(
                            "Process Size", None),
                        transistors=gpu.get("Graphics Processor", {}).get(
                            "Transistors", None),
                        density=gpu.get("Graphics Processor",
                                        {}).get("Density", None),
                        die_size=gpu.get("Graphics Processor",
                                         {}).get("Die Size", None),
                        chip_package=gpu.get("Graphics Processor", {}).get(
                            "Die Size", None),
                        release_date=gpu.get("Graphics Card", {}).get(
                            "Release Date", None),
                        generation=gpu.get("Graphics Card", {}).get(
                            "Generation", None),
                        production=gpu.get("Graphics Card", {}).get(
                            "Production", None),
                        launch_price=gpu.get("Graphics Card", {}).get(
                            "Launch Price", None),
                        bus_interface=gpu.get("Graphics Card", {}).get(
                            "Bus Interface", None),
                        boost_clock=gpu.get("Clock Speeds", {}).get(
                            "Boost Clock", None),
                        gpu_clock=gpu.get("Clock Speeds", {}).get("Base Clock") or gpu.get(
                            "Clock Speeds", {}).get("GPU Clock") or None,
                        memory_clock=gpu.get("Clock Speeds", {}).get(
                            "Memory Clock", None),
                        memory_size=gpu.get("Memory", {}).get(
                            "Memory Size", None),
                        memory_type=gpu.get("Memory", {}).get(
                            "Memory Type", None),
                        memory_bus=gpu.get("Memory", {}).get(
                            "Memory Bus", None),
                        bandwidth=gpu.get("Memory", {}).get("Bandwidth", None),
                        shading_units=gpu.get("Render Config", {}).get(
                            "Shading Units", None),
                        tmus=gpu.get("Render Config", {}).get("TMUs", None),
                        rops=gpu.get("Render Config", {}).get("ROPs", None),
                        l1_cache=gpu.get("Render Config", {}).get(
                            "L1 Cache", None),
                        l2_cache=gpu.get("Render Config", {}).get(
                            "L2 Cache", None),
                        pixel_rate=gpu.get("Theoretical Performance", {}).get(
                            "Pixel Rate", None),
                        texture_rate=gpu.get("Theoretical Performance", {}).get(
                            "Texture Rate", None),
                        fp32_performance=gpu.get(
                            "Theoretical Performance", {}).get("FP16 (half)", None),
                        fp64_performance=gpu.get("Theoretical Performance", {}).get(
                            "FP32 (float)", None),
                        slot_width=gpu.get("Board Design", {}).get(
                            "Slot Width", None),
                        length=gpu.get("Board Design", {}).get("Length", None),
                        tdp=gpu.get("Board Design", {}).get("TDP", None),
                        suggested_psu=gpu.get("Board Design", {}).get(
                            "Suggested PSU", None),
                        outputs=gpu.get("Board Design", {}).get(
                            "Outputs", None),
                        power_connectors=gpu.get("Board Design", {}).get(
                            "Power Connectors", None),
                        board_number=gpu.get("Board Design", {}).get(
                            "Board Number", None),
                        directx=gpu.get("Graphics Features", {}
                                        ).get("DirectX", None),
                        opengl=gpu.get("Graphics Features", {}
                                       ).get("OpenGL", None),
                        opencl=gpu.get("Graphics Features", {}
                                       ).get("OpenCL", None),
                        vulkan=gpu.get("Graphics Features", {}
                                       ).get("Vulkan", None),
                        shader_model=gpu.get("Graphics Features", {}).get(
                            "Shader Model", None)
                    )
                    g.gpu_specs = created_gpu
                    g.save()
                    context[gpu_num+str(num)] = g
                    num += 1

            compared_gpu = compare_gpus(gpu1, gpu2, compare_mode)
            context['compare'] = compared_gpu
            return render(request, 'partials/comparsion.html', context)
