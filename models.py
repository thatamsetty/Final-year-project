from django.db import models

# Create your models here.
class Department(models.Model):
    department_name=models.CharField(max_length=100)
    email=models.EmailField(null=True)
    password=models.CharField(max_length=30,null=True)


    def __str__(self):
        return self.department_name
    
    class Meta:
        db_table='Department'







class Faculty(models.Model):
    name=models.CharField(max_length=50)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    email=models.EmailField()
    designation= models.CharField(max_length=50,null=True )


    def __str__(self):
        return self.name
    
    class Meta:
        db_table='Faculty'



class Subject(models.Model):
    name=models.CharField(max_length=50)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    is_lab=models.BooleanField(default=False)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table='Subject'




class Timetable(models.Model):
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9, null=True)  # 'Monday', 'Tuesday', etc.
    period = models.IntegerField(null=True)  # Period number (1, 2, 3, etc.)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    



   

    class Meta:
        db_table='Timetable'

    