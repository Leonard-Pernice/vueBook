from django.urls import path, include
from rest_framework import routers

from bookDB import views

router = routers.DefaultRouter()
router.register(r'chapters', views.ChapterViewSet)

urlpatterns = [
    path('get-book/<int:book_id>/', views.GetBookView.as_view()),
    path('', include(router.urls)),
    path('get-chapter/', views.GetChapterByNameView.as_view()),
    path('chapter/<int:pk>/', views.ChapterTest.as_view()),
    path('create-chapter/', views.CreateChapterView.as_view()),
    path('create-chapter/<int:book_id>/', views.CreateChapterView.as_view(), name='chapter-list'),
    path('create-paragraph/', views.CreateParagraphView.as_view()),
    path('create-eventparagraph/', views.CreateEventParagraphView.as_view()),
    path('create-character/', views.CreateCharacterView.as_view()),
    path('create-player/', views.CreatePlayerView.as_view()),
    path('create-stat/', views.CreateStatView.as_view()),
    path('create-skill/<str:name>/', views.CreateSkillView.as_view(), name='specific-skill-list'),
    path('create-skill/', views.CreateSkillView.as_view()),
    path('create-quest/', views.CreateQuestView.as_view()),
    path('create-achievement/', views.CreateAchievementView.as_view()),
    path('create-item/', views.CreateItemView.as_view()),
    # path('create-equipment/', views.CreateEquipmentView.as_view()),
    # path('create-inventory/', views.CreateInventoryView.as_view()),
    # path('create-slot/', views.CreateSlotView.as_view()),
    path('create-currency/', views.CreateCurrencyView.as_view()),
]
