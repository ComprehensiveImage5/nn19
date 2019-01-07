from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.
class CheckIn(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.owner.username + ": " + self.status

class Soldier(models.Model):
    RANK_CHOICES = (
        ('unset', '--Unset--'),
        ('private', 'Private'),
        ('private_fc', 'Private First Class'),
        ('lance_c', 'Lance Corporal'),
        ('nut_c', 'Nut Corporal'),
        ('sergeant', 'Sergeant'),
        ('s_sergeant', 'Staff Sergeant'),
        ('n_sergeant', 'Nut Sergeant'),
        ('m_sergeant', 'Master Sergeant'),
        ('lieutenant', 'Lieutenant'),
        ('captain', 'Captain'),
        ('major', 'Major'),
        ('colonel', 'Colonel'),
        ('general', 'General'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=10, choices=RANK_CHOICES, default="unset")

    def __str__(self):
        return self.user.username

    def __text_color__(self, c):
        h = c.lstrip('#')
        t = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
        l = (0.299*t[0] + 0.587*t[1] + 0.114*t[2])/255
        if l < 0.5:
            return "#FFFFFF"
        else:
            return "#000000"

    def get_color(self):
        color = "#000000"
        if self.rank == 'unset':
            color = "#000000"
        elif self.rank == 'private':
            color = "#FF0000"
        elif self.rank == "private_fc":
            color = "#FFA500"
        elif self.rank == "lance_c":
            color = "#FFFF00"
        elif self.rank == "nut_c":
            color = "#8B4513"
        elif self.rank == "sergeant":
            color = "#00BFFF"
        elif self.rank == "s_sergeant":
            color = "#0000FF"
        elif self.rank == "n_sergeant":
            color = "#191970"
        elif self.rank == "m_sergeant":
            color = "#8FBC8F"
        elif self.rank == "lieutenant":
            color = "#32CD32"
        elif self.rank == "captain":
            color = "#008000"
        elif self.rank == "major":
            color = "#6B8E23"
        elif self.rank == "colonel":
            color = "#556B2F"
        elif self.rank == "general":
            color = "#BDB76B"
        return (color, self.__text_color__(color))