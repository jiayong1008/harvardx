# Generated by Django 3.1.7 on 2021-07-07 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0007_auto_20210707_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripdetail',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tripDetail', to='planner.trip'),
        ),
        migrations.AlterUniqueTogether(
            name='tripdetail',
            unique_together={('trip', 'day')},
        ),
    ]
