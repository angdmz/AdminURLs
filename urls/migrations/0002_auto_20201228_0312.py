# Generated by Django 3.1.4 on 2020-12-28 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0002_auto_20201228_0312'),
        ('urls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='logic.project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='public_id',
            field=models.UUIDField(),
        ),
    ]