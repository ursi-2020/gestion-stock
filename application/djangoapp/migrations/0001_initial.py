# Generated by Django 2.2.3 on 2019-07-22 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeProduit', models.CharField(max_length=200)),
                ('quantity', models.PositiveIntegerField()),
            ],
        )
    ]
