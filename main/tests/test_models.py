from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from main.models import Post, Brand, CarModel, City, PostImage

# https://stackoverflow.com/a/26307916/21061376
from django.core.files.uploadedfile import SimpleUploadedFile
image = SimpleUploadedFile(name='test_image.jpg', content=open('main/tests/test_image.jpg', 'rb').read(), content_type='image/jpeg')
#

class PostModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create a user
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        # Create brand
        cls.brand = Brand.objects.create(make='Test Brand')

        # Create car model
        cls.car_model = CarModel.objects.create(name='Test Model', make=cls.brand)

        # Create city
        cls.city = City.objects.create(city='Test City')

        # Create post
        cls.post = Post.objects.create(
            make=cls.brand,
            model=cls.car_model,
            author=cls.user,
            date_posted=timezone.now(),
            city=cls.city,
            year=2020,
            description='Test Description',
            fuel_type='Gas',
            price=10000,
            mileage=15000,
        )

        # Create an image for the post
        cls.post_image = PostImage.objects.create(post=cls.post, images=image)

    def test_post_creation(self):
        post = self.post
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), f'{post.make} {post.model}')
    
    def test_get_image(self):
        post = self.post
        image = post.get_image()
        self.assertIsNotNone(image)
        self.assertEqual(image, self.post_image)
    
    def test_post_fields(self):
        post = self.post
        self.assertEqual(post.make, self.brand)
        self.assertEqual(post.model, self.car_model)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.city, self.city)
        self.assertEqual(post.year, 2020)
        self.assertEqual(post.description, 'Test Description')
        self.assertEqual(post.fuel_type, 'Petrol')
        self.assertEqual(post.price, 10000)
        self.assertEqual(post.mileage, 15000)

