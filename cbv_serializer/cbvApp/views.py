from django.shortcuts import render
from .models import Student
from .serializer import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

## this perform only non primary key based operation

class CustomPagination(PageNumberPagination):
    page_size = 2
    # page_size_query_param = 'page_size'  # This allows the client to specify the page size via query parameter
    # max_page_size = 10  # Maximum number of items allowed per page



class StudentList(APIView):
    # pagination_class = PageNumberPagination  
    pagination_class = CustomPagination
    # page_size = 1
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name','score']


    # def get (self,request):
    #     paginator = self.pagination_class()
    #     all_student = Student.objects.all()
    #     serializer = StudentSerializer(all_student, many=True)
    #     # return Response (serializer.data)
    #     return paginator.get_paginated_response(serializer.data)

    def get(self, request):
        paginator = self.pagination_class()
        students = Student.objects.all()
        # students = self.filter_queryset(Student.objects.all()) 
        paginated_students = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(paginated_students, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link()
        })

    def post (self,request):
        breakpoint()
        post_data = request.data
        serializer = StudentSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data,status=status.HTTP_201_CREATED)
        return Response (serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
class StudentDetails(APIView):
    

    def get_object(self,pk):
        # print("hai da motta")
        try:
            return Student.objects.get(pk=pk)
            print("hai da motta")
        
        except Student.DoesNotExist:
            raise Http404

    def get (self,request,pk):
        student1 = self.get_object(pk)
        # print("hai da motta")
        serializer = StudentSerializer(student1)
        return Response (serializer.data)

    def put (self,request,pk):
        
        put_data = request.data
        student1 = self.get_object(pk)
        serializer = StudentSerializer(student1,data=put_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        student1 = self.get_object(pk)
        student1.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)

