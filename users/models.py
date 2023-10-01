from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.core.files.storage import default_storage 

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    phone_number = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #first saving our form than resize image

        image_file = self.image  # Your ImageField
        with default_storage.open(image_file.name) as file:
            # Do something with the file
            img = Image.open(file)
            if img.width > 300 or img.height > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                
            with default_storage.open(image_file.name, 'wb') as output_file:
                img.save(output_file, format='JPEG')
        # img = storage.open(self.image.name, 'w')
        # print(img)
        # format = 'png'
        # self.image.save(img, format)
        # img.close()

    def get_absolute_url(self):
        return self.image
    
    def get_image(self):
        return self.image
