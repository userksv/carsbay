from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey
from PIL import Image 
from django.core.files.uploadedfile import InMemoryUploadedFile
import io, os
import boto3

boto3.setup_default_session(region_name=os.getenv('AWS_S3_REGION_NAME'))

# Create your models here.
class Brand(models.Model):
    make = models.CharField(max_length=128)
    def __str__(self) -> str:
        return self.make 


class CarModel(models.Model):
    make = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name 


class City(models.Model):
    city = models.CharField(max_length=128)
    
    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self) -> str:
        return self.city


class Post(models.Model):
    make = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    model = ChainedForeignKey(
                        CarModel,
                        chained_field="make",
                        chained_model_field="make",
                        auto_choose=True,
                        sort=True,
                        )
    # model = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING) 
    year = models.IntegerField()
    description = models.TextField(max_length=1024, default='')
    fuel_type = models.CharField(max_length=16)
    price = models.DecimalField(max_digits=8, decimal_places=0, default=0)
    mileage = models.DecimalField(max_digits=6, decimal_places=0, default=0)

    def __str__(self) -> str:
        return f'{self.make} {self.model}'
    
    def get_image(self):
        return PostImage.objects.filter(post=self).first()


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='post_image', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='post_images', blank=True)

    def __str__(self) -> str:
        return str(f'{self.post.make} {self.post.model} {self.images}')

    def get_s3_image_link(self):
        """
        Getting signed link to image for frontend
        """
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        s3 = boto3.client('s3')
        key = str(self.images)
        # Learn this
        url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': key
            },
            HttpMethod='GET'
        )
        return url
 
    def save(self, *args, **kwargs):
        if self.images:
            self.convert_to_jpeg()
        super(PostImage, self).save(*args, **kwargs)

    def convert_to_jpeg(self):
        img = Image.open(io.BytesIO(self.images.read()))
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.thumbnail((self.images.width / 1.5, self.images.height / 1.5), Image.ANTIALIAS)
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=70)
        output.seek(0)
        self.images = InMemoryUploadedFile(
                output,
                'ImageField',
                "%s.jpg" % self.images.name.split('.')[0],
                'images/jpeg',
                len(output.getvalue()),
                None
            )

    def check_image_size(self):
        ...
        
    def convert_heic_to_jpg(self):
        ...
        

def get_models(pk):
    return CarModel.objects.filter(make=pk)
