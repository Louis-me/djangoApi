# Generated by Django 2.1.4 on 2019-01-28 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('protocol', models.CharField(max_length=10)),
                ('method', models.CharField(max_length=10)),
                ('params', models.CharField(max_length=1000)),
                ('hope', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FuzzCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('url', models.CharField(default='', max_length=100)),
                ('protocol', models.CharField(default='', max_length=10)),
                ('method', models.CharField(default='', max_length=10)),
                ('params', models.CharField(default='', max_length=1000)),
                ('hope', models.CharField(max_length=100, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Case')),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300)),
                ('params', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_time', models.CharField(max_length=100)),
                ('sum_time', models.CharField(max_length=10)),
                ('passed', models.IntegerField(default=0)),
                ('failed', models.IntegerField(default=0)),
                ('no_check', models.IntegerField(default=0)),
                ('log', models.CharField(max_length=100, null=True)),
                ('report_path', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ReportItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('protocol', models.CharField(max_length=10)),
                ('method', models.CharField(max_length=10)),
                ('params', models.CharField(max_length=1000)),
                ('hope', models.CharField(max_length=100)),
                ('sum_time', models.CharField(max_length=50)),
                ('fact', models.CharField(max_length=10000)),
                ('result', models.IntegerField(default=0)),
                ('code', models.IntegerField(default=0)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Report')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TaskModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.IntegerField(default=0)),
                ('name', models.CharField(default='', max_length=100)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Task')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Module'),
        ),
    ]
