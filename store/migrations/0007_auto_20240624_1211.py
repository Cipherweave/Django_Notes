# Generated by Django 5.0.6 on 2024-06-24 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_customer_test'),
    ]

    operations = [
        migrations.RunSQL("""
            INSERT INTO store_collection (title)
            VALUES ('collection1')
        """, """
            DELETE FROM store_collection
            WHERE title = 'collection1'
        """)
    ]
