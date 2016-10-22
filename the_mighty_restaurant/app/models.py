from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime, timedelta
# Create your models here.

ACCESS_LEVELS = [
    ('s', 'Server'),
    ('o', 'Owner'),
    ('c', 'Chef'),
]


class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    access_level = models.CharField(max_length=1, choices=ACCESS_LEVELS)

    def __str__(self):
        return self.access_level

    @property
    def is_owner(self):
        return self.access_level == 'o'

    @property
    def is_chef(self):
        return self.access_level == 'c'

    @property
    def is_server(self):
        return self.access_level == 's'


@receiver(post_save, sender="auth.User")
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Profile.objects.create(user=instance)


class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    server = models.ForeignKey("auth.User")
    item = models.ForeignKey(MenuItem)
    drink = models.CharField(max_length=20)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    table_number = models.IntegerField()
    completed = models.BooleanField(default=False)

    def is_recent(self):
        hrs24 = datetime.now() - timedelta(days=1)
        if Order.objects.filter(creation_time__gte=hrs24):
            return True
        else:
            return False

    @property
    def order_profits(self):
        return self.item.price

    @property
    def is_completed(self):
        return self.completed


class Table(models.Model):
    paid = models.BooleanField(default=False)

    @property
    def is_paid(self):
        return self.paid
