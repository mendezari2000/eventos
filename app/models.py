from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def validate(cls, title, description, date):
        errors = {}

        if title == "":
            errors["title"] = "Por favor ingrese un titulo"

        if description == "":
            errors["description"] = "Por favor ingrese una descripcion"

        return errors

    @classmethod
    def new(cls, title, description, date):
        errors = Event.validate(title, description, date)

        if len(errors.keys()) > 0:
            return False, errors

        Event.objects.create(
            title=title,
            description=description,
            date=date,
        )

        return True, None

    def update(self, title, description, date):
        self.title = title or self.title
        self.description = description or self.description
        self.date = date or self.date

        self.save()

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

#clase para la prioridad de las notificaciones
class Priority(models.TextChoices):
    HIGH = 'HIGH', 'High'
    MEDIUM = 'MEDIUM', 'Medium'
    LOW = 'LOW', 'Low'


class Notification(models.Model):

    title = models.CharField(max_length=200)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(
        max_length=6,
        choices=Priority.choices,
        default= Priority.LOW)
    is_read = models.BooleanField(default=False)
    users = models.ManyToManyField('User', related_name='notifications')