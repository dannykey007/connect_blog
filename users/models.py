from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):  # Must be exactly 'Profile'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try: 
            img = Image.open(self.image.path)

            if img.mode == 'RGBA':
                img = img.convert('RGB')

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except (OSError, Exception):
        # Line of code: Optional safety net if file is missing/broken pass
            pass