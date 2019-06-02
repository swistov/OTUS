from django.db import models


class ComputerManufacture(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class ComputerModel(models.Model):
    manufacturer = models.ForeignKey(ComputerManufacture,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     default='')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class ComputerType(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Computer(models.Model):

    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(ComputerManufacture, on_delete=models.CASCADE)
    model = models.ForeignKey(ComputerModel, on_delete=models.CASCADE)
    body = models.TextField()
    type = models.ForeignKey(ComputerType, on_delete=models.CASCADE, blank=False)
    price = models.IntegerField(default=0)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} {self.name}'

    class Meta:
        ordering = ['id']
