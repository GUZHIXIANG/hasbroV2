from rest_framework import serializers
from wechatapp.models.TestModel import *
from wechatapp import models

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


# class TeacherUNSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     def create(self, data):
#         return Teacher.objects.create(**data)

# class TeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = '__all__'


# class StudentUNSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     # teacher = TeacherUNSerializer()
#     teacher_id = serializers.IntegerField()

#     def create(self, data):
#         return Student.objects.create(**data)

#     def update(self, instance, data):
#         return instance.update(**data)


# class StudentSerializer(serializers.Modelserializer):
#     teacher = serializers.CharField(source='teacher.name')
#     # teacher = TeacherSerializer()

#     class Meta:
#         model = Student
#         fields = ['name', 'id', 'teacher']


# class Course_Student_UNSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     # 因为传递过来的数据是字符 所以这里也用 字符类型
#     student_ids = serializers.CharField(max_length=255, write_only=True)

#     def create(self, data):
#         student_ids = eval(data['student_ids'])
#         # 先确定 有 id 的学生
#         student = Student.objects.filter(id__in=student_ids)
#         del data['student_ids']    # 删除多余的字段
#         # 删除了 学生 剩下的就都是课程的了
#         c = Course.objects.create(**data)
#         # 从 课程的 ManyToMany字段 添加
#         c.student.add(*student)
#         # 最后返回的是 c 什么意思？ 就是说 上面 两个结果 都会被 返回 入 第三张连接表
#         return c


# class CourseSerializer(serializers.Modelserializer):
#     student = serializers.CharField(source='student.name')
#     # student = StudentSerializer()

#     class Meta:
#         model = Student
#         fields = ['name', 'id', 'student']


# class Course_Student_Serializer(serializers.Modelserializer):
#     course_id = CourseSerializer()
#     student_id = serializers.CharField(source='student.name')
#     # student_id = StudentSerializer()

#     class Meta:
#         model = models.Course_Student
#         fields = ['id', 'student_id', 'course_id']

