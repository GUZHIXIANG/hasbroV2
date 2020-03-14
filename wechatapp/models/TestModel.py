from django.db import models

class Test(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=10)
    age = models.IntegerField(verbose_name='年龄')
    CHOICE = ((0,'未知'),(1,'男'),(2,'女'))
    sex = models.IntegerField(verbose_name='性别',choices=CHOICE,default=0)
    type = models.ForeignKey('Type',on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name.__str__()
    
    class Meta:
        app_label = 'wechatapp'
        verbose_name = 'Test'
        verbose_name_plural = '测试用例'


class Test2(models.Model):
    user = models.ForeignKey(Test,on_delete=models.CASCADE,related_name='test2')
    phone = models.CharField(verbose_name='手机号',max_length=13)
    class Meta:
        app_label = 'wechatapp'
        verbose_name = 'Test2'
        verbose_name_plural = '测试用例2'
    def __str__(self):
        return self.phone.__str__()

class Test3(models.Model):
    name = models.CharField(verbose_name='分组', max_length=13)
    user = models.ManyToManyField(Test)


    class Meta:
        app_label = 'wechatapp'
        verbose_name = 'Test3'
        verbose_name_plural = '测试用例4'

    def __str__(self):
        return self.name.__str__()


class Test4(models.Model):
    name = models.CharField(verbose_name='权限', max_length=13)
    user = models.ManyToManyField(Test,through='Test41')

    class Meta:
        app_label = 'wechatapp'
        verbose_name = 'Test4'
        verbose_name_plural = '测试用例5'

    def __str__(self):
        return self.name.__str__()

class Test41(models.Model):
    name = models.ForeignKey(Test4, on_delete=models.CASCADE)
    user = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        app_label = 'wechatapp'
        verbose_name = 'Test41'
        verbose_name_plural = '测试用例5-1'



class Type(models.Model):
    name = models.CharField(verbose_name='类别名', max_length=10)
    desc = models.CharField(verbose_name='类别描述', max_length=100)

    class Meta:
        app_label = 'wechatapp'
        verbose_name = 'Type'
        verbose_name_plural = '测试用例3'

    def __str__(self):
        return self.name.__str__()



'''##################################'''
# # 教师表
# class Teacher(models.Model):
# 	name = models.CharField(max_length=32)

# # 学生表


# class Student(models.Model):
# 	name = models.CharField(max_length=32)
# 	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

# # 课程表


# class Course(models.Model):
#     name = models.CharField(max_length=32)
#     student = models.ManyToManyField(Student)

