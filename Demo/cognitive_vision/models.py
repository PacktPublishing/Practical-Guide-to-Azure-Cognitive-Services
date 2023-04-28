from django.db import models


class Results(models.Model):
    file_name = models.CharField(max_length=255, verbose_name='File Name')
    good = models.FloatField()
    bad = models.FloatField()
    passed = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True, auto_created=True)

    class Meta:
        ordering = ['date_created']
        verbose_name_plural = 'results'

    def __str__(self):
        return f"{self.id}-{self.file_name}"

    def get_image(self):
        return f"https://ch10oceansmartst.blob.core.windows.net/{self.file_name}?sp=r&st=2022-07-07T12:07:22Z&se=2035-07-07T20:07:22Z&spr=https&sv=2021-06-08&sr=c&sig=1XxiuHviD%2F3xquRFJTVh1Gb4Cq88bEx6DnzcD2mHQeg%3D"
