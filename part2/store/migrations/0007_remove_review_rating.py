# Generated by Django 5.0.7 on 2024-07-18 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_collection_featured_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
    ]
