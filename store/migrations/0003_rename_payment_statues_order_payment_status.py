# Generated by Django 5.0.6 on 2024-06-27 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_birthdate_customer_birth_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment_statues',
            new_name='payment_status',
        ),
    ]
