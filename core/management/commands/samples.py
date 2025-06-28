import os
from faker import Faker

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from core.models import Currency, Category, Brand, Profile, Color, Size
from main.models import Product, ProductImage, ProductVariant, Review

class Command(BaseCommand):
    help = 'Create sample data'

    def handle(self, *args, **options):
        call_command('migrate')
        if not Currency.objects.count():
            Currency.objects.bulk_create([
                Currency(name='United States Dollar', code='USD', code3='USD', symbol='$', order=1),
                Currency(name='Iraqi Dinar', code='IQD', code3='IQD', symbol='د.ع', order=2),
                Currency(name='Saudi Riyal', code='SAR', code3='SAR', symbol='ر.س', order=3),
            ])

            self.stdout.write(self.style.SUCCESS('Successfully created sample currencies'))

        if not User.objects.count():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))

        if not Category.objects.count():
            categories = [
                Category(name=name) for name in [
                    'Mobiles', 'Laptops', 'Tablets', 'Computers', 'Accessories',
                    'Headphones', 'Speakers', 'Printers', 'Monitors', 'Cameras',
                ]
            ]
            Category.objects.bulk_create(categories)

            self.stdout.write(self.style.SUCCESS('Successfully created sample categories'))

        if not Brand.objects.count():
            brands = [
                Brand(name=name) for name in [
                    'Apple', 'Samsung', 'Google', 'Microsoft', 'Lenovo',
                    'Asus', 'Dell', 'Huawei', 'Sony', 'Xiaomi', 'Oppo',
                    'Vivo', 'Motorola', 'Nokia', 'HTC', 'LG', 'Philips',
                    'Toshiba', 'Panasonic', 'Casio', 'Fujifilm', 'Nikon',
                    'Canon', 'Olympus', 'Realme', 'Pentax', 'HP',
                ]
            ]
            Brand.objects.bulk_create(brands)

            self.stdout.write(self.style.SUCCESS('Successfully created sample brands'))

        if not Profile.objects.count():
            # create fake 1000 customers and profiles
            users = [
                User(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    is_active=False,
                    is_staff=False,
                    is_superuser=False,
                ) for i in range(1000)
            ]
            User.objects.bulk_create(users)
            user_ids = User.objects.values_list('id', flat=True)

            fake = Faker(locale='ar_SA')

            profiles = [
                Profile(
                    user_id=user_id, 
                    name=fake.name(),
                    slug=fake.slug(),
                    email=fake.email(), 
                    phone_number=fake.phone_number(), 
                    address=fake.address(), 
                    city=fake.city(), 
                    country_code=fake.country_code(), 
                    postal_code=fake.postalcode(),
                    birth_date=fake.date_of_birth(),
                    country_of_birth=fake.country_code(),
                ) 
                for _, user_id in enumerate(user_ids)
            ]
            Profile.objects.bulk_create(profiles)

            self.stdout.write(self.style.SUCCESS('Successfully created sample profiles'))

        if not Color.objects.count():
            colors = [
                Color(name=name, hex_value=hex_value) for name, hex_value in [
                    ('Red', '#F44336'),
                    ('Pink', '#E91E63'),
                    ('Purple', '#9C27B0'),
                    ('Deep Purple', '#673AB7'),
                    ('Indigo', '#3F51B5'),
                    ('Blue', '#2196F3'),
                    ('Cyan', '#00BCD4'),
                    ('Teal', '#009688'),
                    ('Green', '#4CAF50'),
                    ('Light Green', '#8BC34A'),
                    ('Lime', '#CDDC39'),
                    ('Yellow', '#FFEB3B'),
                    ('Amber', '#FFC107'),
                    ('Orange', '#FF9800'),
                    ('Deep Orange', '#FF5722'),
                    ('Brown', '#795548'),
                    ('Grey', '#9E9E9E'),
                    ('Blue Grey', '#607D8B'),
                    ('Black', '#000000'),
                    ('White', '#FFFFFF'),
                ]
            ]
            Color.objects.bulk_create(colors)

            self.stdout.write(self.style.SUCCESS('Successfully created sample colors'))

        if not Size.objects.count():
            sizes = [
                Size(unit=unit, size=size) for unit, size in [
                    ('in', 1),
                    ('in', 2),
                    ('in', 3),
                    ('in', 4),
                    ('in', 5),
                    ('in', 6),
                    ('in', 7),
                    ('in', 8),
                    ('in', 9),
                    ('in', 10),
                    ('in', 11),
                    ('in', 12),
                    ('in', 13),
                    ('in', 14),
                    ('in', 15),
                ]
            ]
            Size.objects.bulk_create(sizes)

            self.stdout.write(self.style.SUCCESS('Successfully created sample sizes'))
        
        if not Product.objects.count():
            from random import choices
            fake = Faker()
            colors = Color.objects.all()
            sizes = Size.objects.all()
            categories = Category.objects.all()
            brands = Brand.objects.all()

            product_names = [
                'Apple iPhone 13 Pro', 'Apple iPhone 13', 'Samsung Galaxy S22 Ultra', 'Samsung Galaxy S22', 'Google Pixel 6 Pro', 'Google Pixel 6', 'Apple MacBook Air', 'Apple MacBook Pro', 'Samsung Galaxy Tab S8', 'Samsung Galaxy Tab S7 FE', 'Apple iPad', 'Apple iPad Pro', 'Apple Watch Series 8', 'Apple Watch Series 7', 'Samsung Galaxy Watch4', 'Samsung Galaxy Watch4 Classic', 'Apple AirPods Pro', 'Apple AirPods', 'Samsung Galaxy Buds2', 'Samsung Galaxy Buds Pro', 'Apple iMac', 'Apple iMac Pro', 'Apple Mac Pro', 'Apple Mac Mini', 'Apple TV 4K', 'Apple TV HD', 'Samsung The Frame', 'Samsung The Serif', 'Samsung The Sero', 'Samsung The Premiere', 'Samsung QN900A', 'Samsung QN800A', 'Samsung QN700A', 'Samsung QN650A', 'Samsung QN600A', 'Samsung QN550A', 'Samsung QN500A', 'Samsung QN450A', 'Samsung QN400A', 'Samsung QN350A', 'Samsung QN300A', 'Samsung QN250A', 'Samsung QN200A', 'Samsung QN150A', 'Samsung QN100A'
            ]

            products = [
                Product(
                    name=choices(product_names)[0],
                    slug=fake.slug(),
                    description=fake.text(),
                    price=fake.random_int(min=1000, max=10000),
                    category=choices(categories)[0],
                    brand=choices(brands)[0],
                    is_featured=choices([True, False])[0],
                    has_size=choices([True, False])[0],
                    has_color=choices([True, False])[0],
                )
                for _ in range(100)
            ]
            Product.objects.bulk_create(products)

            product_variants = [
                ProductVariant(
                    product_id=product_id,
                    color=choices(colors)[0],
                    size=choices(sizes)[0],
                )
                for product_id in Product.objects.filter(Q(has_size=True)| Q(has_color=True)).values_list('id', flat=True)
            ]
            ProductVariant.objects.bulk_create(product_variants)

            product_images = [
                ProductImage(
                    product_id=product_id,
                    image='media/product/{}.jpg'.format(product_id),
                )
                for product_id in Product.objects.all().values_list('id', flat=True)
            ]
            ProductImage.objects.bulk_create(product_images)
            self.stdout.write(self.style.SUCCESS('Successfully created sample products'))