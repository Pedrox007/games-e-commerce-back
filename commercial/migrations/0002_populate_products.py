# Generated by Django 4.1.6 on 2023-02-10 00:00
import json

from django.conf import settings
from django.core.files import File
from django.db import migrations


def create_products(apps, _):
    Product = apps.get_model("commercial", "Product")

    statics_path = "{}/commercial/statics".format(settings.BASE_DIR)
    products_file = open("{}/data/products.json".format(statics_path))
    products_list = json.load(products_file)

    for product in products_list:
        image = File(open("{}/assets/{}".format(statics_path, product["image"]), "rb"))
        product_obj = Product(
            name=product["name"],
            price=product["price"],
            score=product["score"],
        )
        product_obj.image.save(product["image"], image, save=False)
        product_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_products)
    ]
