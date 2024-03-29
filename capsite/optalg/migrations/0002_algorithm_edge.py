# Generated by Django 3.2.7 on 2022-12-05 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('optalg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225, null=True)),
                ('desc', models.CharField(max_length=1500, null=True)),
                ('url', models.CharField(max_length=225, unique=True)),
                ('scraped', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=1)),
                ('alg_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alg_one', to='optalg.algorithm')),
                ('alg_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alg_two', to='optalg.algorithm')),
            ],
        ),
    ]
