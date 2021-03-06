# Generated by Django 3.1.1 on 2020-09-04 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brought_from', models.CharField(max_length=50)),
                ('sold_to', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('c_rate', models.FloatField()),
                ('s_rate', models.FloatField()),
                ('cp', models.FloatField()),
                ('sp', models.FloatField()),
                ('profit', models.FloatField()),
            ],
        ),
    ]
