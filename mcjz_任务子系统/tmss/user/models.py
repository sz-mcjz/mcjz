from django.db import models


# 部门
class Department(models.Model):
    name = models.CharField(max_length=125)

    class Meta:
        db_table = 'mcjz_department'


# 员工
class Staff(models.Model):
    username = models.CharField(max_length=125)
    id_card = models.CharField(max_length=18)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    telephone = models.CharField(max_length=11)
    password = models.CharField(max_length=125)
    icon = models.CharField(max_length=255)

    class Meta:
        db_table = 'mcjz_staff'
