import csv
from django.core.management.base import BaseCommand
from gpu.models import GPUList
from datetime import datetime
import re


class Command(BaseCommand):
    help = 'Import data from CSV file into the model'

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        # csv_file = options['csv_file']
        with open('D:\Programming Projects\Web Development Fullstack\gpu\management\commands\gpu_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Released'] != 'Never Released':
                    pattern = r'(?P<month>\w{3}) (?P<day>\d{1,2})(?P<suffix>st|nd|rd|th), (?P<year>\d{4})'
                    match = re.match(pattern, row['Released'])

                    if match:
                        month = match.group('month')
                        day = match.group('day')
                        year = match.group('year')

                        # Convert month name to its numeric representation
                        month_number = datetime.strptime(month, '%b').month

                        # Construct the date string in YYYY-MM-DD format
                        formatted_date = f'{year}-{month_number:02d}-{day}'
                else:
                    formatted_date = None
                GPUList.objects.create(
                    ProductName=row['Product Name'],
                    GPUChip=row['GPU Chip'],
                    Memory=row['Memory'],
                    Released=formatted_date,
                    Bus=row['Bus'],
                    Memoryclock=row['Memory clock'],
                    GPUclock=row['GPU clock'],
                    Shaders_TMUs_ROPs=row['Shaders / TMUs / ROPs'],
                    URL=row['URL'],
                    # Add more fields as needed
                )
