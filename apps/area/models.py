from django.db import models

# Create your models here.


class Areas(models.Model):
    id = models.CharField(verbose_name='行政编号', max_length=20, primary_key=True)
    name = models.CharField(verbose_name='行政区划名', max_length=20)
    parent_id = models.CharField(
        verbose_name='上级行政编号', max_length=20)
    type = models.IntegerField(verbose_name='行政等级', default=0)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = '行政区划'
        verbose_name_plural = verbose_name


