# Generated by Django 3.2.15 on 2022-10-07 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('blockid', models.AutoField(primary_key=True, serialize=False)),
                ('txcount', models.IntegerField(default=0)),
                ('time_stamp', models.DateTimeField()),
                ('previous', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next', to='home.block')),
            ],
        ),
        migrations.CreateModel(
            name='Memepool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('txcount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Miner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('txid', models.AutoField(primary_key=True, serialize=False)),
                ('sendAddr', models.CharField(max_length=200)),
                ('receiveAddr', models.CharField(max_length=200)),
                ('amount', models.IntegerField(default=0)),
                ('time_stamp', models.DateTimeField()),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.block')),
                ('memepool', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.memepool')),
            ],
        ),
        migrations.CreateModel(
            name='Blockchain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('genesis', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='init_chain', to='home.block')),
                ('latest', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_chain', to='home.block')),
            ],
        ),
    ]
