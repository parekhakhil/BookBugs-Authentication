from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor
import uuid
import os

def rename_path_and_avatar(path):
        def wrapper(instance,filename):
            #avatar = filename.split('.')[0]
            ext = filename.split('.')[-1]
            if instance.pk:
                avatar_id = 'uid_%s'%(instance.pk)
                avatar_name = '%s_%s'%(instance.user.first_name, instance.user.last_name)
                filename = '{}_{}_{}.{}'.format(avatar_id,avatar_name,uuid.uuid4().hex,ext)
            else:
                random_id = 'r_id%s'%(uuid.uuid4().hex)
                filename = '{}_{}'.format(random_id,filename)
            return os.path.join(path,filename)
        return wrapper

avatar_image_upload_path = rename_path_and_avatar('user_avatar/')
# assign it `__qualname__`
avatar_image_upload_path.__qualname__ = 'avatar_image_upload_path'

class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile',on_delete=models.CASCADE)
    avatar = fields.ImageField(upload_to=avatar_image_upload_path,blank=True,default = 'static/user-bg.jpg', dependencies=[
        FileDependency( processor=ImageProcessor(
            format='JPEG', scale={'max_width': 150, 'max_height': 150})),
    ])
    
    about = models.TextField(blank=True)
   # user_type = models.CharField(max_length=1, choices=USER_TYPES, default='b')

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.id and self.avatar:
            current_avatar = UserProfile.objects.get(pk=self.id).avatar
            if current_avatar != self.avatar:
                current_avatar.delete()
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        target = reverse('authapp:profile', args=[self.user.username])
        return target

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()