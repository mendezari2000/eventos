from django.db import models
from django.utils.timezone import now

class Venue (models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    capacity = models.IntegerField()
    contact = models.CharField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @classmethod
    def validate(cls, name, description):
        errors = {}

        if name  == "":
            errors["name"] = "La categoría debe tener un nombre"
        
        if description  == "":
            errors["description"] = "La categoría debe tener una descripción"

        return errors
    
    @classmethod
    def new(cls, name, description, is_active):
        errors = Category.validate(name, description)

        if len(errors.keys()) > 0:
            return False, errors
        
        Category.objects.create(
            name=name,
            description=description,
            is_active=is_active,
        )

        return True, None


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
    def validate(cls, title, description, date, venue, category):
        errors = {}

        if title == "":
            errors["title"] = "Por favor ingrese un título"

        if description == "":
            errors["description"] = "Por favor ingrese una descripción"

        if not date:
            errors["date"] = "Por favor ingrese una fecha válida"
        elif date < now():
            errors["date"] = "La fecha no puede ser en el pasado"

        if venue is None:
            errors["venue"] = "Debe asignar un venue válido"

        if category is None:
            errors["category"] = "Debe asignar una categoría válida"

        return errors

    @classmethod
    def new(cls, title, description, date, venue=None, category=None):
        errors = cls.validate(title, description, date, venue, category)

        if errors:
            return False, errors

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            venue=venue,
            category=category
        )

        return True, None

    def update(self, title, description, date, venue=None, category=None):
        self.title = title or self.title
        self.description = description or self.description
        self.date = date or self.date
        if venue is not None:
            self.venue = venue
        if category is not None:
            self.category = category

        self.save()

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
    @classmethod
    def validate(cls, username, email):
        errors = {}

        if not username:
            errors["username"] = "Por favor ingrese un nombre de usuario"

        if not email:
            errors["email"] = "Por favor ingrese un correo electrónico valido"

        return errors

    @classmethod
    def new(cls, username, email):
        errors = cls.validate(username,email)

        if errors:
            return False, errors

        User.objects.create(
            username = username,
            email = email
        )
        return True, None
    
    def update(self, username=None, email=None):
        self.username = username 
        self.email = email

        self.save()


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

    @classmethod
    def validate(cls, title, message, priority):
        errors = {}

        if not title:
            errors["title"] = "Por favor ingrese un título"
        
        if not message:
            errors["message"] = "Por favor ingrese un mensaje"
        
        if priority not in [choice[0] for choice in Priority.choices]:
            errors["priority"] = "Por favor ingrese una prioridad válida"
        
        return errors
        
    @classmethod
    def new(cls, title, message, priority, users):
        errors = cls.validate(title, message, priority)

        if errors:
            return False, errors

        notification = Notification.objects.create(
            title=title,
            message=message,
            priority=priority
        )
        
        notification.users.set(users)

        return True, None
    
    def update(self, title=None, message=None, priority=None):
        if title:
            self.title = title
        if message:
            self.message = message
        if priority:
            self.priority = priority
        
        self.save()
    



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

        if title == "":
            errors["title"] = "El titulo del comentario es obligatorio"

        if text == "":
            errors["text"] = "El texto del comentario es obligatorio"

        return errors
    
    @classmethod
    def new(cls, user, event, title, text):
        errors = Comment.validate(user, event, title, text)

        if len(errors.keys()) > 0:
            return False, errors

        Comment.objects.create(
            user=user,
            event=event,
            title=title,
            text=text,
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

    def _str_(self):
        return f"Rating de {self.title} igual a {self.rating}"
    
    @classmethod
    def validate (cls, title, text, rating, user, event):
        errors = {}

        if title == "":
            errors["title"] = "Debe ingresar un titulo"

        if text == "":
            errors["text"] = "Debe ingresar un texto"

        if title == "":
            errors["title"] = "Debe ingresar un titulo"

        if (rating<0) and (rating>5):
            errors["rating"] = "Debe ingresar un puntuación"
        
        if user is None:
            errors["user"] = "Es obligatorio un usuario"
        
        if event is None:
            errors["event"] = "Es obligatorio ingresar el evento"

        return errors
    
    @classmethod 
    def new (cls, title, text, rating, user=None, event=None):
        errors = Rating.validate(title, text, rating);

        if len(errors.keys()) > 0:
            return False, errors
        
        Rating.objects.create(
            title=title,
            text=text,
            rating=rating,
            user=user,
            event=event,
        )
        return True, None

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

    def __str__(self):
        return f"Codigo de ticket: {self.ticket_code}"
    
    @classmethod
    def validate(cls, ticket_code, quantity, type_ticket, user, event):
        errors={}

        if ticket_code =="":
            errors["ticket_code"] = "El codigo del ticket es obligatorio"
        
        if quantity<0:
            errors["quantity"] = "Debe ingresar una cantidad valida"

        if type_ticket not in [choice[0] for choice in Type_Ticket.choices]:
            errors["type_ticket"] = "Debe ingresar un tipo de ticket valido"
        
        if user is None:
            errors["user"]= "Debe asignarle el ticket a un usuario"
        
        if event is None:
            errors["event"]= "Debe asignarle el ticket a un evento"
        
        return errors
    
    @classmethod
    def new(cls, ticket_code, quantity, type_ticket, user=None, event=None):
        errors = cls.validate(ticket_code, quantity,type_ticket,user,event)

        if len(errors.keys()) > 0:
            return False, errors
        
        Ticket.objects.create(
            ticket_code=ticket_code,
            quantity=quantity,
            type_ticket=type_ticket,
            user=user,
            event=event,
        )
        return True, None