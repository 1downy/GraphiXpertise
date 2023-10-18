from bs4 import BeautifulSoup
import random
from dateutil import parser


def get_specs(content):
    soup = BeautifulSoup(content, "html.parser")
    # print(soup.prettify())
    element = soup.find('div', class_='sectioncontainer')
    details = element.find_all('section', class_="details")
    graphics_card = {}
    for section in details:
        if section.find("h2").text == "Relative Performance" or "GPU Notes" in section.find("h2").text:
            continue
        if section.get("id") == "boards":
            continue
        title = section.find('h2').text.replace('\t', '').replace('\n', '')
        for data in section.find_all('div'):
            section_dict = {}
            for dl in section.find_all('dl'):
                # Extract the title (dt) and text (dd)
                key = dl.find('dt').text.replace('\n', '').replace('\t', '')
                if key == "Reviews":
                    continue
                value = dl.find('dd').text.replace('\n', '').replace('\t', '')
                if key == "Release Date":
                    if value == "Never Released":
                        formatted_date = None
                    else:
                        parsed_date = parser.parse(value)
                        formatted_date = parsed_date.strftime('%Y-%m-%d')
                    section_dict[key] = formatted_date
            # Create or update the inner dictionary
                else:
                    section_dict[key] = value

        # Add the inner dictionary to the outer dictionary
        graphics_card[title] = section_dict
    # print(graphics_card)
    return graphics_card


def get_headers():

    user_agents_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.257",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    ]
    user_agent = random.choice(user_agents_list)

    headers = {
        "authority": "www.techpowerup.com",
        "method": "GET",
        'User-Agent': user_agent,
        "scheme": "https",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.techpowerup.com/gpu-specs/",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"'
    }

    return headers


def normalize_date(date_string):
    try:
        # Try to parse the date using dateutil
        parsed_date = parser.parse(date_string)

        # Format the parsed date in ISO format
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        return formatted_date
    except ValueError:
        # Handle parsing errors or invalid date formats
        return None


def compare_gpus(gpu1, gpu2, mode):
    compare_gpu1 = gpu1.gpu_specs.numeric_specifications
    compare_gpu2 = gpu2.gpu_specs.numeric_specifications
    # Define weights for each specification
    gaming_weights = {
        'shading_units': 0.15,       # Importance of the number of shading units
        'tmus': 0.1,                # Importance of texture mapping units
        'rops': 0.1,                # Importance of raster operations units
        'gpu_clock': 0.25,           # Importance of GPU clock speed
        'boost_clock': 0.15,        # Importance of boost clock speed
        'memory_size': 0.05,        # Importance of memory size
        'memory_type': 0.05,        # Importance of memory type
        'memory_bus': 0.1,          # Importance of memory bus width
        'bandwidth': 0.15,          # Importance of memory bandwidth
        'tdp': -0.02,                # Importance of thermal design power
        'directx': 0.05,            # Importance of DirectX support
        'opengl': 0.05,             # Importance of OpenGL support
        'opencl': 0.05,             # Importance of OpenCL support
        'vulkan': 0.05,             # Importance of Vulkan support
        'shader_model': 0.05,      # Importance of shader model support
        'fp32_performance': 0.1,    # Importance of floating-point 32-bit performance
        'fp64_performance': 0.05,   # Importance of floating-point 64-bit performance
        'pixel_rate': 0.1,         # Importance of pixel fill rate
        'texture_rate': 0.1,       # Importance of texture fill rate
        'release_date': 0.1,       # Importance of release date
    }
    raw_weights = {
        'shading_units': 0.15,       # Importance of the number of shading units
        'tmus': 0.1,                # Importance of texture mapping units
        'rops': 0.1,                # Importance of raster operations units
        'gpu_clock': 0.15,          # Importance of GPU clock speed
        'boost_clock': 0.1,         # Importance of boost clock speed
        'memory_size': 0.05,        # Importance of memory size
        'memory_type': 0.05,        # Importance of memory type
        'memory_bus': 0.1,          # Importance of memory bus width
        'bandwidth': 0.1,           # Importance of memory bandwidth
        'tdp': 0.01,                # Importance of thermal design power
        'directx': 0.05,            # Importance of DirectX support
        'opengl': 0.05,             # Importance of OpenGL support
        'opencl': 0.05,             # Importance of OpenCL support
        'vulkan': 0.05,             # Importance of Vulkan support
        'shader_model': 0.05,      # Importance of shader model support
        'fp32_performance': 0.2,    # Importance of floating-point 32-bit performance
        'fp64_performance': 0.1,    # Importance of floating-point 64-bit performance
        'pixel_rate': 0.1,         # Importance of pixel fill rate
        'texture_rate': 0.1,       # Importance of texture fill rate
        'release_date': 0.05,      # Importance of release date
    }

    if mode == 'raw':
        weights = raw_weights
    else:
        weights = gaming_weights

    def calculate_score(specs):
        try:
            score = sum(weights[key] * (specs[key] if specs[key] is not None else 0)
                        for key in specs)
            return score
        except Exception as e:
            # print(e, "Exception")
            return e

    score1 = calculate_score(compare_gpu1)
    score2 = calculate_score(compare_gpu2)
    # Compare the scores to determine which GPU is better

    context = {}

    total = score1 + score2
    gpu1_percent = int((score1 / total) * 100)
    gpu2_percent = int((score2 / total) * 100)
    context['gpu1_percent'] = gpu1_percent
    context['gpu2_percent'] = gpu2_percent

    if score1 > score2:
        context['rating'] = f"{gpu1.ProductName} is {abs(gpu1_percent - gpu2_percent)}% better."
    elif score1 < score2:
        context['rating'] = f"{gpu2.ProductName} is {abs(gpu1_percent - gpu2_percent)}% better."
    else:
        context['rating'] = "Both GPUs have the same overall score."
    return context
