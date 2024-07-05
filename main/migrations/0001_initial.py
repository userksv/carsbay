# Generated by Django 4.2 on 2023-10-09 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.brand')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('year', models.IntegerField()),
                ('description', models.TextField(default='', max_length=1024)),
                ('fuel_type', models.CharField(max_length=16)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=8)),
                ('mileage', models.DecimalField(decimal_places=0, default=0, max_digits=6)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.city')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.brand')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.carmodel'))
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', sorl.thumbnail.fields.ImageField(default='post_images/default.jpg', upload_to='post_images')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_image', to='main.post')),
            ],
        ),
    ]
