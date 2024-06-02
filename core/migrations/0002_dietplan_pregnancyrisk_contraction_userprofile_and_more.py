# Generated by Django 5.0.6 on 2024-06-02 16:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PregnancyRisk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('Nutrition', 'Nutrition'), ('Exercise', 'Exercise'), ('Medical', 'Medical'), ('Environmental', 'Environmental'), ('Emotional', 'Emotional'), ('Other', 'Other')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Contraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('duration', models.DurationField(help_text='Duration of the contraction in seconds.')),
                ('intensity', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start_time'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('last_menstrual_period', models.DateField()),
                ('current_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('blood_type', models.CharField(max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WeightTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
