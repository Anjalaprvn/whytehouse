# Generated migration to remove unused fields from TravelPackage model

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0064_merge_20260401_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelpackage',
            name='child_price',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='child_pricing',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='base_price',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='tax_percentage',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='final_price',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='resort',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='meal_plans',
        ),
    ]
