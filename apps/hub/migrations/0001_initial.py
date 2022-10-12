# Generated by Django 4.1.2 on 2022-10-10 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
                (
                    "name_en",
                    models.CharField(max_length=50, null=True, verbose_name="Name"),
                ),
                (
                    "name_uk",
                    models.CharField(max_length=50, null=True, verbose_name="Name"),
                ),
                (
                    "name_ru",
                    models.CharField(max_length=50, null=True, verbose_name="Name"),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("cadetblue", "cadetblue"),
                            ("lightred", "lightred"),
                            ("beige", "beige"),
                            ("green", "green"),
                            ("blue", "blue"),
                            ("red", "red"),
                            ("purple", "purple"),
                            ("lightgreen", "lightgreen"),
                            ("darkblue", "darkblue"),
                            ("orange", "orange"),
                            ("gray", "gray"),
                            ("pink", "pink"),
                            ("lightblue", "lightblue"),
                            ("lightgray", "lightgray"),
                            ("darkpurple", "darkpurple"),
                            ("darkgreen", "darkgreen"),
                            ("darkred", "darkred"),
                            ("black", "black"),
                            ("white", "white"),
                        ],
                        max_length=50,
                        verbose_name="Color",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Icon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
            ],
            options={
                "verbose_name": "Icon",
                "verbose_name_plural": "Icons",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Marker",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("latitude", models.FloatField(verbose_name="Latitude")),
                ("longitude", models.FloatField(verbose_name="Longitude")),
                (
                    "comment",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Comment"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Date"
                    ),
                ),
                (
                    "likes_count",
                    models.BigIntegerField(default="0", verbose_name="Likes count"),
                ),
                (
                    "ip",
                    models.GenericIPAddressField(null=True, verbose_name="IP address"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="hub.category",
                        verbose_name="Category",
                    ),
                ),
                (
                    "like",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        related_name="likes",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Like",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="markers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "Mark",
                "verbose_name_plural": "Marks",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comment_text",
                    models.TextField(max_length=300, verbose_name="Comment"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Date"
                    ),
                ),
                (
                    "marker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="hub.marker",
                        verbose_name="Mark",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="hub.icon",
                verbose_name="Icon",
            ),
        ),
    ]
