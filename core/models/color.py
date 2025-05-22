import csv

from django.db import models


class Color(models.Model):
    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"
        ordering = ["number"]
    name = models.CharField(max_length=100)  # Color name (e.g., "Red")
    number = models.CharField(max_length=100)  # Color number, can be used for a color code
    hex_value = models.CharField(max_length=10)  # Hex value of the color (e.g., "#FF0000" for red)

    @staticmethod
    def import_colors_from_csv(csv_file_path):
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                __, created = Color.objects.get_or_create(
                    number=row['Colour Number'],
                    name=row['Colour Name'],
                    hex_value=row['Hex']
                )
                if created:
                    print(f"تم إضافة اللون: {row['Colour Name']} ({row['Colour Number']})")
                else:
                    print(f"اللون {row['Colour Name']} موجود بالفعل.")