from django.db import models

class Venue (models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    capacity = models.IntegerField()
    contact = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField()

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.username

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

    def __str__(self):
        return f"Notification {self.title} - {self.created_at}"

class RefundRequest (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refund_requests')
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    ticket_code = models.CharField(max_length=100)
    reason = models.TextField()
    #el campo created_at se autogenera con la fecha en la que se crea la soli.
    created_at = models.DateField(auto_now_add=True)

    @classmethod
    def validate(cls, user, ticket_code, reason):
        errors = {}

        if ticket_code =="":
            errors["ticket_code"] = "El codigo de la solicitud es obligatorio"
        
        if reason == "":
            errors["reason"] = "El motivo de la solicitud es obligatorio"

        if user == "":
            errors["user"] = "El usuario de la solicitud es obligatorio"   
        
        return errors

    @classmethod
    def new(cls, user, ticket_code, reason):
        errors = RefundRequest.validate(user, ticket_code, reason)

        if len(errors.keys()) > 0:
            return False, errors

        RefundRequest.objects.create(
            user=user,
            ticket_code=ticket_code,
            reason=reason,
        )

        return True, None
    
    def __str__(self):
        return f"Refund {self.ticket_code} by {self.user.username}"
    
class Comment (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def validate(cls, user, event, title, text):
        errors = {}

        if not user:
            errors["user"] = "El usuario del comentario es obligatorio"
        
        if not event:
            errors["event"] = "El evento del comentario es obligatorio"

        if not title:
            errors["title"] = "El titulo del comentario es obligatorio"

        if not text:
            errors["text"] = "El texto del comentario es obligatorio"

        return errors
    
    @classmethod
    def new(cls, user, event, title, text):
        errors = Comment.validate(user, event, title, text)

        if len(errors.keys()) > 0:
            return False, errors

        comment = Comment.objects.create(
            user=user,
            event=event,
            title=title,
            text=text
        )

        return True, None

    def __str__(self):
        return f"Comment by {self.user.username} on {self.event}"

class Rating(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User',on_delete=models.CASCADE, related_name='ratings')
    event = models.ForeignKey('Event',on_delete=models.CASCADE, related_name='ratings') 

class Type_Ticket(models.TextChoices):
    GENERAL = 'general', 'General'
    VIP = 'vip', 'Vip'
    
class Ticket(models.Model):
    buy_date = models.DateField(auto_now_add=True)
    ticket_code = models.CharField(max_length=100, unique=True)
    quantity= models.IntegerField()
    type_ticket = models.CharField(
        max_length=7,
        choices=Type_Ticket.choices,
        default=Type_Ticket.GENERAL)
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='tickets')
    event = models.ForeignKey('Event',on_delete=models.CASCADE, related_name='tickets')