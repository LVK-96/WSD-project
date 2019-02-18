# Generated by Django 2.1.4 on 2019-02-18 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField(default=0)),
                ('link', models.URLField(default='', unique=True)),
                ('description', models.TextField(default='', max_length=1000)),
                ('genre', models.CharField(choices=[('AC', 'Action'), ('AD', 'Adventure'), ('AR', 'Arcade'), ('FA', 'Fantacy'), ('PU', 'Puzzle'), ('RA', 'Racing'), ('SP', 'Sports'), ('ST', 'Strategy'), ('TR', 'Trivia'), ('OT', 'Other')], default='OT', max_length=2)),
                ('dev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Highscore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('state', models.TextField(default='')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('OP', 'Proceeded to pay'), ('AP', 'Accepted payment'), ('CAN', 'Canceled payment'), ('SUC', 'Succesfull payment'), ('FAI', 'Failed payment')], default='OP', max_length=20)),
                ('session_key', models.CharField(max_length=500)),
                ('games_and_prices', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('total', models.FloatField(default=0)),
                ('games', models.ManyToManyField(to='store.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='highscore',
            unique_together={('game', 'player')},
        ),
    ]
