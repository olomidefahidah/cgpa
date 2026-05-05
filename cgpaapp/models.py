from django.db import models
from django.contrib.auth.models import User


class CGPARecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cgpa_records'
    )

    semester = models.CharField(max_length=50)
    gpa = models.FloatField(default=0.0)
    total_units = models.FloatField(default=0.0)
    total_credit_point = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first (better UX)

    def __str__(self):
        return f"{self.user.username} - {self.semester} - GPA: {self.gpa}"


# ─────────────────────────────
# COURSES IN EACH SEMESTER
# ─────────────────────────────

class SemesterCourse(models.Model):
    record = models.ForeignKey(
        CGPARecord,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    name = models.CharField(max_length=100)
    unit = models.FloatField()
    score = models.FloatField()
    grade = models.CharField(max_length=2)
    credit_point = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.grade})"