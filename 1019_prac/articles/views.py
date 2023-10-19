from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer, TopicSerializer
from .models import Article, Comment, Topic
from django.shortcuts import get_object_or_404, get_list_or_404
import json


# Create your views here.
@api_view(["GET", "POST"])
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        topics_string = request.data.get('topics')
        topics_data = json.loads(topics_string)
        # topics_data를 반복하면서
        # topic 테이블에 새로운 토픽이라면 추가하고, 아니면 저장 X
        # 기존에 있던 없던 생성하려던 게시글과는 관계를 설정
        topics = []
        for topic in topics_data:
            topic_data = { "content": topic }
            topic_serializer = TopicSerializer(data=topic_data)
            exist_topic = Topic.objects.filter(content=topic).first()
            if exist_topic:
                topics.append(exist_topic)
            else:
                if topic_serializer.is_valid(raise_exception=True):
                    topic_serializer.save()
                    topics.append(topic_serializer.instance)

        serializer = ArticleListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = serializer.save()
            # article - topics 관계 설정
            article.topics.set(topics)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE", "PUT"])
def article_detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == "GET":
        serializer = ArticleSerializer(article)
        article.views += 1
        article.save()
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        article.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        # or (삭제 메세지를 주고 싶을 때)
        return Response({'message': '삭제 완료'}, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        # partial=True: 특정 필드만 수정하고 싶을 때
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)