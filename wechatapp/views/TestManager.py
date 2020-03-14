# 每层view文件必须import
from wechatapp.views import *

# 本view层所需要模型和序列化对象
from wechatapp.models.TestModel import *
from wechatapp.serializers.TestSerializer import *


# # views.py
# class Course_Student_list(APIView):
#     def get(self, request, format=None):
#         course = Course_Student.objects.all()
#         cs = Course_Student_Serializer(instance=course, many=True)
#         return Response({'code': 200,'student_list': cs.data})
