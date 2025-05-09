# Generated by Django 4.2.20 on 2025-04-19 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('first_names', models.TextField()),
                ('apellido_paterno', models.TextField(blank=True, null=True)),
                ('appelido_materno', models.TextField(blank=True, null=True)),
                ('privlages', models.TextField(blank=True, null=True)),
                ('job_description', models.TextField(blank=True, null=True)),
                ('fecha_de_nacimiento', models.DateField()),
                ('date_added', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication', models.TextField()),
                ('description', models.TextField()),
                ('high_low_mid_use', models.IntegerField()),
                ('num_units_per_month', models.IntegerField()),
                ('num_units_in_stock', models.IntegerField()),
                ('date_of_last_restock', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('med_name', models.TextField()),
                ('med_description', models.TextField()),
                ('emp_name', models.TextField()),
                ('to_whom', models.TextField()),
                ('ammount', models.IntegerField()),
                ('restock', models.TextField()),
                ('date_change', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_names', models.TextField()),
                ('apellido_paterno', models.TextField(blank=True, null=True)),
                ('appellido_materno', models.TextField(blank=True, null=True)),
                ('fecha_de_nacimiento', models.DateField()),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meds.employee')),
            ],
        ),
    ]
