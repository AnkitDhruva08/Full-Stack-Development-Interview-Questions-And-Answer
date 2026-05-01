from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import User, Publisher, Book
from .serializers import UserSerializer, PublisherSerializer, BookSerializer
from django.db.models import Count, F
# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer





class PublisherAPIView(APIView):

    @extend_schema(responses=PublisherSerializer(many=True))
    def get(self, request):
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)

    @extend_schema(request=PublisherSerializer, responses=PublisherSerializer)
    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class BookAPIView(APIView):

    @extend_schema(responses=BookSerializer(many=True))
    def get(self, request):
        books = Book.objects.all()
        authors = Book.objects.select_related('publisher')  
        for i in authors:
            print('publishers name ::::', i.publisher.name)  

        # orm query a writer how many book he has written
        publishers = Publisher.objects.annotate(
                total_books=Count('book')
            )
        
        for p in publishers:
            titles = Book.objects.filter(publisher=p).values_list('title', flat=True)

            print(
                "Publisher:", p.name,
                "Count:", p.total_books,
                "Titles:", list(titles)
            )
        book_couunts = Book.objects.aggregate(count=Count('id'))
        print('total book count ::::', book_couunts['count'])

        books_with_publishers = Book.objects.select_related('publisher').annotate(
            publisher_name=F('publisher__name')
        ).values('title', 'publisher_name')
        for book in books_with_publishers:
            print(f"Book: {book['title']}, Publisher: {book['publisher_name']}")



        # prefetch related example
        publishers = Publisher.objects.prefetch_related('book_set')
        for publisher in publishers:
            print(f"Publisher: {publisher.name}")
            for book in publisher.book_set.all():
                print(f"  Book: {book.title}")


        pub = Publisher.objects.distinct().values('name')
        print('distinct publishers ::::', pub)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @extend_schema(request=BookSerializer, responses=BookSerializer)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)