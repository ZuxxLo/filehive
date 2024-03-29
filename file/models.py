from djongo import models
from user.models import User

 # from bson.objectid import ObjectId        file=models.FileField(upload_to =f'files/%y/%m/%d/{_id}')



# Create your models here.
class File(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=254)
    file=models.FileField(upload_to =f'files/%y/%m/%d/')
    owner = models.CharField(max_length=254)
    download_url = models.URLField

    class Meta:
            # Specify the custom collection name
            db_table = 'file'
    def __str__(self):
        return self.title    