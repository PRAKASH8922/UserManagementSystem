from django.db import models


class CtUserDetails(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'ct_user_details'

    def __str__(self):
        return f"{self.id} - {self.name} ({self.email})"

    def get_user_details(self):
        return f"ID: {self.id}, Name: {self.name}, Email: {self.email}"
