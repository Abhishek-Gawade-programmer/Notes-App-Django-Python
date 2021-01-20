import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


COLOURS_CHOICES = [
    ('red', 'RED'),
    ('green', 'GREEN'),
    ('yellow', 'YELLOW'),
    ('orange', 'ORANGE'),
    ('blue', 'BLUE'),
    ('white', 'WHITE'),

]

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")

    def __str__(self):
        return self.title

class Note(models.Model):
    """
    Description: Model Description 
    """
    id=models.UUIDField(primary_key=True,
                    default=uuid.uuid4,
                    editable=False,
                    db_index=True,)
    category = models.ForeignKey(Category, verbose_name="Category",on_delete=models.CASCADE,blank=True)

    heading=models.CharField(max_length=70,blank=False)
    description =models.TextField(blank=True)
    password_required = models.BooleanField(default=False)
    add_to_fav = models.BooleanField(default=False)
    colour_of_notes = models.CharField(
        max_length=9,
        choices=COLOURS_CHOICES,
        default='white',
    )
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    

    def get_absolute_url(self):
        return reverse('note_detail',args=[str(self.id)])

    def __str__(self):
    	return self.heading 
    class Meta:
        get_latest_by='created'
        ordering=('updated',)

class Note_Password(models.Model):
    """
    Description: Model Description
    """
    author=models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    password= models.CharField(max_length=40,null=True,default=False)

    def __str__(self):
        return str(self.author.username) +f'  ( {self.password} )'
    class Meta:
        pass
