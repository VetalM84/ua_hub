# Generated by Django 4.1.2 on 2022-10-14 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hub", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="name_de",
            field=models.CharField(max_length=50, null=True, verbose_name="Name"),
        ),
        migrations.AddField(
            model_name="category",
            name="name_es",
            field=models.CharField(max_length=50, null=True, verbose_name="Name"),
        ),
        migrations.AddField(
            model_name="category",
            name="name_fr",
            field=models.CharField(max_length=50, null=True, verbose_name="Name"),
        ),
        migrations.AddField(
            model_name="category",
            name="name_it",
            field=models.CharField(max_length=50, null=True, verbose_name="Name"),
        ),
        migrations.AddField(
            model_name="category",
            name="name_pl",
            field=models.CharField(max_length=50, null=True, verbose_name="Name"),
        ),
    ]
