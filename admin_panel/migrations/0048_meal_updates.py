# Generated manually for meal model updates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0047_update_resort_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='meal_type',
            field=models.CharField(choices=[('veg', 'Vegetarian'), ('non-veg', 'Non-Vegetarian'), ('both', 'Both')], default='both', max_length=20),
        ),
        migrations.AddField(
            model_name='meal',
            name='price_per_person',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]