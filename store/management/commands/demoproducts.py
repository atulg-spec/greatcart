import os
import random
import shutil
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings
from store.models import Product, Variation, ProductGallery
from category.models import Category

class Command(BaseCommand):
    help = 'Add 100 demo products with gallery and variations'

    def handle(self, *args, **kwargs):
        # Define categories for men's wear
        category_names = ['Shirts', 'T-Shirts', 'Jeans', 'Trousers', 'Jackets']

        # Create categories if they don't exist
        categories = {}
        for cat_name in category_names:
            category, created = Category.objects.get_or_create(
                category_name=cat_name, defaults={'slug': slugify(cat_name)}
            )
            categories[cat_name] = category

        # Define sample images directory
        sample_dir = os.path.join(settings.BASE_DIR, 'static/sample/')
        media_dir = os.path.join(settings.MEDIA_ROOT, 'products/')

        os.makedirs(media_dir, exist_ok=True)  # Ensure the media directory exists

        # Get all images from the sample directory
        images = [img for img in os.listdir(sample_dir) if img.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

        if not images:
            self.stdout.write(self.style.ERROR("No images found in static/sample/. Please add some images."))
            return

        # Add 100 demo products
        for i in range(100):
            product_name = f'Demo Product {i+1}'
            slug = slugify(product_name)
            price = random.randint(1000, 5000)
            stock = random.randint(10, 100)
            discount_percent = random.choice([10, 15, 20])
            category = random.choice(list(categories.values()))  # Assign a random category
            
            product = Product.objects.create(
                product_name=product_name,
                slug=slug,
                description='This is a demo product.',
                price=price,
                stock=stock,
                is_available=True,
                category=category,
                discount_percent=discount_percent,
            )

            # Assign and copy images
            img_path = os.path.join(sample_dir, images[i % len(images)])
            new_img_path = os.path.join(media_dir, images[i % len(images)])

            shutil.copyfile(img_path, new_img_path)  # Copy image to media directory
            
            product.images = f'products/{images[i % len(images)]}'  # Save relative path
            product.save()

            # Add secondary image if available
            if len(images) > 1:
                secondary_img_path = os.path.join(sample_dir, images[(i + 1) % len(images)])
                new_secondary_img_path = os.path.join(media_dir, images[(i + 1) % len(images)])

                shutil.copyfile(secondary_img_path, new_secondary_img_path)  # Copy secondary image
                product.secondary_image = f'products/{images[(i + 1) % len(images)]}'
                product.save()

            # Add images to ProductGallery
            for img in images[2:]:
                img_path = os.path.join(sample_dir, img)
                new_img_path = os.path.join(media_dir, img)

                shutil.copyfile(img_path, new_img_path)
                ProductGallery.objects.create(product=product, image=f'products/{img}')

            # Add product variations (Color & Size)
            colors = ['Red', 'Blue', 'Green', 'Black', 'White']
            sizes = ['S', 'M', 'L', 'XL', 'XXL']
            
            for color in colors:
                Variation.objects.create(product=product, variation_category='color', variation_value=color)
            
            for size in sizes:
                Variation.objects.create(product=product, variation_category='size', variation_value=size)

        self.stdout.write(self.style.SUCCESS('Successfully added 100 demo products with images and variations!'))
