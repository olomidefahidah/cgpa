from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CGPARecord ():
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    cgpa = models.FloatField()
    total_units = models.FloatField()
    total_credit_point = models.FloatField()
    created_at = models.DateField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} - {self.semester} - CGPA: {self.cgpa}"