# Generated by Django 4.2.16 on 2024-10-07 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Ticket", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TicketType",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="ticket",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Ticket.tickettype"
            ),
        ),
    ]