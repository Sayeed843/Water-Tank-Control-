# Generated by Django 2.0.2 on 2018-04-07 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutMe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('dept', models.CharField(max_length=250)),
                ('university', models.CharField(max_length=250)),
                ('batch', models.CharField(max_length=250)),
                ('img', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='BdWaterBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=250)),
                ('mac', models.CharField(max_length=250)),
                ('gallon', models.CharField(max_length=250)),
                ('use', models.CharField(default=0, max_length=250)),
                ('remaining', models.CharField(default=0, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='DailyStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motorStatus', models.CharField(max_length=250)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('mac_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wpc.BdWaterBoard')),
            ],
        ),
        migrations.CreateModel(
            name='Motor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waterSupply', models.BooleanField()),
                ('mac_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wpc.BdWaterBoard')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upperSensor', models.CharField(max_length=260)),
                ('lowerSensor', models.CharField(max_length=260)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('mac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wpc.BdWaterBoard')),
            ],
        ),
    ]
