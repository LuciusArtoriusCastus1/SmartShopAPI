# Generated by Django 4.2.5 on 2023-12-29 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orders_decline_description_orders_declined'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='decline_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
