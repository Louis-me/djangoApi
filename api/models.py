from django.db import models


class Login(models.Model):
    url = models.CharField(max_length=300)
    params = models.CharField(max_length=10000)

    def __str__(self):
        return self.url


class Report(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    sum_time = models.CharField(max_length=10)
    passed = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    no_check = models.IntegerField(default=0)
    log = models.CharField(max_length=100, null=True)
    report_path = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ReportItem(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10)
    method = models.CharField(max_length=10)
    params = models.CharField(max_length=1000)
    hope = models.CharField(max_length=100)
    sum_time = models.CharField(max_length=50)
    fact = models.CharField(max_length=10000)
    result = models.IntegerField(default=0)  # 0通过，-1失败，-2不检查
    code = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Case(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10)
    method = models.CharField(max_length=10)
    params = models.CharField(max_length=1000)
    hope = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class FuzzCase(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    url = models.CharField(max_length=100, default='')
    protocol = models.CharField(max_length=10, default='')
    method = models.CharField(max_length=10, default='')
    params = models.CharField(max_length=1000, default='')
    hope = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
