from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0044_add_employee_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
