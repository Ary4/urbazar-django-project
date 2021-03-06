# Generated by Django 2.0.2 on 2018-03-23 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urbazar_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('college_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('star_count', models.DecimalField(decimal_places=0, max_digits=1)),
                ('image', models.FileField(blank=True, null=True, upload_to='user_profile_picture/')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=39.99, max_digits=7),
        ),
    ]
