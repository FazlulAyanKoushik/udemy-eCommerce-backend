# Generated by Django 4.1.5 on 2023-01-24 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to=product.models.upload_image)),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('numReview', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('countInStock', models.IntegerField(blank=True, default=0, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
