from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions, viewsets
from django.http import JsonResponse
from django.utils.html import escape
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
import math

from .serializers import *

class GetBookView(APIView):
    def get(self, request, book_id):
        book = Book.objects.get(id = book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

class ChapterTest(APIView):
    def get(self, request, pk):
        assert isinstance(pk, int)
        chapter = ChapterSerializer(Chapter.objects.get(name = str('Chapter ' + str(pk)))).data
        chapter_all = Chapter.objects.filter(id = chapter['id']).prefetch_related('paragraphs', 'characters', 'items', 'chapter_players', 'chapter_relationships', 'chapter_stats', 'chapter_skills', 'chapter_quests', 'chapter_achievements', 'chapter_currencies').all()
        chapter_out = ChapterSerializer(chapter_all, many = True).data
        return Response(chapter_out)

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        book = get_object_or_404(Book, id = book_id)
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.validated_data['book'] = book
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
        # serializer = self.get_serializer(data = request.data)
        # if serializer.is_valid():
        #     self.perform_create(serializer)
        #     return Response(serializer.data, status = status.HTTP_201_CREATED)
        # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status = status.HTTP_204_NO_CONTENT)

class GetChapterByNameView(APIView):
    def get(self, request, format = None):
        name = request.query_params.get('name')
        try:
            chapter = Chapter.objects.get(name = name)
        except Chapter.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)

class CreateChapterView(APIView):
    serializer_class = CreateChapterSerializer

    def get(self, request, book_id, format = None):
        chapters = Chapter.objects.filter(book = book_id)
        serializer = ChapterSerializer(chapters, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            # image = serializer.data.get('image')
            book = Book.objects.filter(id = serializer.data.get('book')).first()
            queryset = Chapter.objects.filter(name = name)
            if queryset.exists():
                chapter = queryset[0]
                chapter.book = book
                chapter.slug = "ch"
                # chapter.image = s
                chapter.save(update_fields = ['book', 'slug'])
                return Response(ChapterSerializer(chapter).data, status = status.HTTP_200_OK)
            else:
                chapter = Chapter(name = name, slug = 'ch', book = book)
                return Response(ChapterSerializer(chapter).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

# check this for info: https://github.com/techwithtim/Music-Controller-Web-App-Tutorial/blob/main/Tutorial%205/api/views.py

class CreateParagraphView(APIView):
    serializer_class = CreateTextParagraphSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            text = serializer.data.get('text')
            textorder = serializer.data.get('textorder')
            queryset = Paragraph.objects.filter(textorder = textorder, chapter = chapter)
            if queryset.exists():
                paragraph = queryset[0]
                paragraph.text = text
                paragraph.attributes = ''
                paragraph.save(update_fields = ['text'])
                return Response(ParagraphSerializer(paragraph).data, status = status.HTTP_200_OK)
            else:
                paragraph = Paragraph(chapter = chapter, text = text, textorder = textorder)
                paragraph.save()
                return Response(ParagraphSerializer(paragraph).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreateEventParagraphView(APIView):
    serializer_class = CreateEventParagraphSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            text = serializer.data.get('text')
            textorder = serializer.data.get('textorder')
            attributes = serializer.data.get('attributes')
            exp = serializer.data.get('exp')
            queryset = Paragraph.objects.filter(textorder = textorder, chapter = chapter)
            if queryset.exists():
                paragraph = queryset[0]
                paragraph.text = text
                paragraph.attributes = attributes
                paragraph.exp = exp
                paragraph.save(update_fields = ['text', 'attributes', 'exp'])
                return Response(ParagraphSerializer(paragraph).data, status = status.HTTP_200_OK)
            else:
                paragraph = Paragraph(chapter = chapter, text = text, textorder = textorder, attributes = attributes, exp = exp)
                paragraph.save()
                return Response(ParagraphSerializer(paragraph).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreateCharacterView(APIView):
    serializer_class = CreateCharacterSerializer

    def get(self, request, format = None):
        chapterid = request.query_params.get('chapter')
        paragraphOfRelevantEvent = request.query_params.get('paragraph')
        name = request.query_params.get('name')
        lastname = request.query_params.get('lastname')
        if chapterid and paragraphOfRelevantEvent and name and lastname:
            characters = Character.objects.filter(name = name, lastname = lastname, referenceParagraph__lt = paragraphOfRelevantEvent, chapter = chapterid)
            serializer = CharacterSerializer(characters, many = True)
            return Response(serializer.data)
        elif chapterid and paragraphOfRelevantEvent:
            characters = Character.objects.filter(referenceParagraph__lt = paragraphOfRelevantEvent, chapter = chapterid)
            serializer = CharacterSerializer(characters, many = True)
            return Response(serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            referenceParagraph = serializer.data.get('referenceParagraph')
            name = serializer.data.get('name')
            lastname = serializer.data.get('lastname')
            referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
            information = serializer.data.get('information')
            statusOfNpc = serializer.data.get('statusOfNpc')
            age = serializer.data.get('age')
            gender = serializer.data.get('gender')
            height = serializer.data.get('height')
            weight = serializer.data.get('weight')
            species = serializer.data.get('species')
            race = serializer.data.get('race')
            queryset = Character.objects.filter(Q(name = name) & Q(lastname = lastname))
            if queryset.exists():
                character = queryset[0]
                character.information = information
                character.statusOfNpc = statusOfNpc
                character.age = age
                character.gender = gender
                character.height = height
                character.weight = weight
                character.species = species
                character.race = race
                character.save(update_fields = ['information', 'statusOfNpc', 'age', 'gender', 'height', 'weight', 'species', 'race'])
                return Response(CharacterSerializer(character).data, status = status.HTTP_200_OK)
            else:
                if referenceToLastRelevantEvent:
                    character = Character(chapter = chapter, referenceParagraph = referenceParagraph, name = name, lastname = lastname, referenceToLastRelevantEvent = referenceToLastRelevantEvent, information = information, statusOfNpc = statusOfNpc, age = age, gender = gender, height = height, weight = weight, species = species, race = race)
                    character.save()
                    return Response(CharacterSerializer(character).data, status = status.HTTP_201_CREATED)
                else:
                    character = Character(chapter = chapter, referenceParagraph = referenceParagraph, name = name, lastname = lastname, information = information, statusOfNpc = statusOfNpc, age = age, gender = gender, height = height, weight = weight, species = species, race = race)
                    character.save()
                    return Response(CharacterSerializer(character).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreatePlayerView(APIView):
    serializer_class = CreatePlayerSerializer

    def get(self, request, format = None):
      chapterid = request.query_params.get('chapter')
      name = request.query_params.get('name')
      index = request.query_params.get('index')
      paragraphOfRelevantEvent = request.query_params.get('paragraph')
      # print(chapterid)
      # print(name)
      # print(index)
      # print(paragraphOfRelevantEvent)
      if chapterid and name and paragraphOfRelevantEvent:
        player = Player.objects.filter(Q(name = name) & Q(referenceParagraph__lt = paragraphOfRelevantEvent) & Q(character__chapter = chapterid)).order_by('-id').first()
        serializer = PlayerSerializer(player)
        return Response(serializer.data)
      if chapterid and name and index:
        boundOfParagraphs = ParagraphSerializer(Paragraph.objects.filter(chapter = chapterid, textorder__lt = index).order_by('-textorder').first()).data
        players = Player.objects.filter(name = name, referenceParagraph__lt = float(boundOfParagraphs['id']), character__chapter = chapterid)
        serializer = PlayerSerializer(players, many = True)
        return Response(serializer.data)
      return Response(status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            print(serializer.data.get('chapter'))
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            character = Character.objects.get(id = serializer.data.get('character'))
            name = serializer.data.get('name')
            referenceParagraph = serializer.data.get('referenceParagraph')
            referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
            characterName = serializer.data.get('characterName')
            job = serializer.data.get('job')
            title = serializer.data.get('title')
            level = serializer.data.get('level')
            exp = serializer.data.get('exp')
            typ = serializer.data.get('typ')
            queryset = Player.objects.filter(Q(characterName = characterName) & Q(referenceParagraph = referenceParagraph))
            if queryset.exists():
                player = queryset[0]
                player.job = job
                player.title = title
                player.level = level
                player.exp = exp
                player.typ = typ
                player.save(update_fields = ['job', 'title', 'level', 'exp', 'typ'])
                return Response(PlayerSerializer(player).data, status = status.HTTP_200_OK)
            else:
                if referenceToLastRelevantEvent:
                    player = Player(chapter = chapter, character = character, name = name, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, characterName = characterName, job = job, title = title, level = level, exp = exp, typ = typ)
                    player.save()
                    return Response(PlayerSerializer(player).data, status = status.HTTP_201_CREATED)
                else:
                    player = Player(chapter = chapter, character = character, name = name, referenceParagraph = referenceParagraph, characterName = characterName, job = job, title = title, level = level, exp = exp, typ = typ)
                    player.save()
                    return Response(PlayerSerializer(player).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreateStatView(APIView):
    serializer_class = CreateStatSerializer

    def get(self, request, format = None):
      route = request.query_params.get('route')
      chapterid = request.query_params.get('chapter')
      statid = request.query_params.get('statid')
      statName = request.query_params.get('statName')
      playerName = request.query_params.get('playerName')
      paragraphOfRelevantEvent = request.query_params.get('paragraph')
      if chapterid and paragraphOfRelevantEvent and route and Stat.objects.filter(player__character__chapter = chapterid):
        if route  ==  'statByID' and statid and playerName: # All instances of a specific stat via ID
          stat = Stat.objects.filter(id = statid).first()
          if stat:
            relevantStatObjects = Stat.objects.filter(player__name = playerName, referenceParagraph__lt = paragraphOfRelevantEvent, player__character__chapter = chapterid, name = stat.name)
            serializer = StatSerializer(relevantStatObjects, many = True)
            return Response(serializer.data)
        elif route  ==  'statByName' and statName and playerName: # All instances of a specific stat via Name
          stat = Stat.objects.filter(name = statName, referenceParagraph__lt = paragraphOfRelevantEvent, player__character__chapter = chapterid).order_by('-id').first()
          serializer = StatSerializer(stat)
          return Response(serializer.data)
        elif route  ==  'allStatsOfPlayer' and playerName: # All stats of player in chapter previous to event
          chapter = get_object_or_404(Chapter, id = chapterid)
          stats = Stat.objects.filter(player__name = playerName, player__referenceParagraph__lt = paragraphOfRelevantEvent, player__character__chapter = chapter)
          serializer = StatSerializer(stats, many = True)
          return Response(serializer.data)
      else:
        return Response("No stats available.")
      return Response(status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            player = Player.objects.get(id = serializer.data.get('player'))
            name = serializer.data.get('name')
            referenceParagraph = serializer.data.get('referenceParagraph')
            referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
            base = serializer.data.get('base')
            increased = serializer.data.get('increased')
            trained = serializer.data.get('trained')
            bar = serializer.data.get('bar')
            idealValue = serializer.data.get('idealValue')
            # Sanity Checking the Bar:
            theoretic_total = math.floor(float(base) + float(increased) + float(trained))
            if float(bar) > theoretic_total:
                return Response({f'Bad value: value of bar is too high by {float(bar) - theoretic_total}!'}, status = status.HTTP_400_BAD_REQUEST)
            queryset = Stat.objects.filter(Q(name = name) & Q(player = player) & Q(referenceParagraph = referenceParagraph))
            if queryset.exists():
                stat = queryset[0]
                stat.base = base
                stat.increased = increased
                stat.trained = trained
                stat.bar = bar
                stat.save(update_fields = ['base', 'increased', 'trained', 'bar'])
                return Response(StatSerializer(stat).data, status = status.HTTP_200_OK)
            else:
                if referenceToLastRelevantEvent:
                    stat = Stat(chapter = chapter, player = player, name = name, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, base = base, increased = increased, trained = trained, bar = bar, idealValue = idealValue)
                    stat.save()
                    return Response(StatSerializer(stat).data, status = status.HTTP_201_CREATED)
                else:
                    stat = Stat(chapter = chapter, player = player, name = name, referenceParagraph = referenceParagraph, base = base, increased = increased, trained = trained, bar = bar, idealValue = idealValue)
                    stat.save()
                    return Response(StatSerializer(stat).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreateSkillView(APIView):
    serializer_class = CreateSkillSerializer

    def get(self, request, format = None):
      chapterid = request.query_params.get('chapter')
      playerName = request.query_params.get('playerName')
      skillName = request.query_params.get('skillName')
      skill = Skill.objects.filter(Q(name = skillName) & Q(player__name = playerName) & Q(player__character__chapter = chapterid))
      serializer = SkillSerializer(skill, many = True)
      return Response(serializer.data)

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            player = Player.objects.get(id = serializer.data.get('player'))
            modifier = Stat.objects.get(id = serializer.data.get('modifier'))
            name = serializer.data.get('name')
            referenceParagraph = serializer.data.get('referenceParagraph')
            referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
            level = serializer.data.get('level')
            exp = serializer.data.get('exp')
            description = serializer.data.get('description')
            typ = serializer.data.get('typ')
            ap = serializer.data.get('ap')
            mp = serializer.data.get('mp')
            st = serializer.data.get('st')
            queryset = Skill.objects.filter(Q(name = name) & Q(player = player) & Q(referenceParagraph = referenceParagraph))
            if queryset.exists():
                skill = queryset[0]
                skill.level = level
                skill.exp = exp
                skill.description = description
                skill.typ = typ
                skill.ap = ap
                skill.mp = mp
                skill.st = st
                skill.save(update_fields = ['level', 'exp', 'description', 'typ', 'ap', 'mp', 'st'])
                return Response(SkillSerializer(skill).data, status = status.HTTP_200_OK)
            else:
                if referenceToLastRelevantEvent:
                    skill = Skill(chapter = chapter, player = player, modifier = modifier, name = name, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, level = level, exp = exp, description = description, typ = typ, ap = ap, mp = mp, st = st)
                    skill.save()
                    return Response(SkillSerializer(skill).data, status = status.HTTP_201_CREATED)
                else:
                    skill = Skill(chapter = chapter, player = player, modifier = modifier, name = name, referenceParagraph = referenceParagraph, level = level, exp = exp, description = description, typ = typ, ap = ap, mp = mp, st = st)
                    skill.save()
                    return Response(SkillSerializer(skill).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreateQuestView(APIView):
    serializer_class = CreateQuestSerializer

    def get(self, request, format = None):
      chapterid = request.query_params.get('chapter')
      playerName = request.query_params.get('playerName')
      questName = request.query_params.get('questName')
      referenceParagraph = request.query_params.get('paragraph')
      quest = Quest.objects.filter(name = questName, referenceParagraph__lt = referenceParagraph, player__character__chapter = chapterid, player__name = playerName).order_by('-id').first()
      serializer = QuestSerializer(quest)
      return Response(serializer.data)

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            player = Player.objects.get(id = serializer.data.get('player'))
            name = serializer.data.get('name')
            referenceParagraph = serializer.data.get('referenceParagraph')
            referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
            statusOfQuest = serializer.data.get('statusOfQuest')
            description = serializer.data.get('description')
            optional_description = serializer.data.get('optional_description')
            tier = serializer.data.get('tier')
            difficulty = serializer.data.get('difficulty')
            reward_title = serializer.data.get('reward_title')
            reward = serializer.data.get('reward')
            optional_reward = serializer.data.get('optional_reward')
            exp_received = serializer.data.get('exp_received')
            queryset = Quest.objects.filter(Q(name = name) & Q(player = player) & Q(referenceParagraph = referenceParagraph))
            if queryset.exists():
                quest = queryset[0]
                quest.statusOfQuest = statusOfQuest
                quest.description = description
                quest.tier = tier
                quest.difficulty = difficulty
                quest.save(update_fields = ['statusOfQuest', 'description', 'tier', 'difficulty'])
                return Response(QuestSerializer(quest).data, status = status.HTTP_200_OK)
            else:
                if referenceToLastRelevantEvent:
                    quest = Quest(chapter = chapter, player = player, name = name, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, statusOfQuest = statusOfQuest, description = description, optional_description = optional_description, tier = tier, difficulty = difficulty, reward_title = reward_title, reward = reward, optional_reward = optional_reward, exp_received = exp_received)
                    quest.save()
                    return Response(QuestSerializer(quest).data, status = status.HTTP_201_CREATED)
                else:
                    quest = Quest(chapter = chapter, player = player, name = name, referenceParagraph = referenceParagraph, statusOfQuest = statusOfQuest, description = description, optional_description = optional_description, tier = tier, difficulty = difficulty, reward_title = reward_title, reward = reward, optional_reward = optional_reward, exp_received = exp_received)
                    quest.save()
                    return Response(QuestSerializer(quest).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreateAchievementView(APIView):
    serializer_class = CreateAchievementSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            player = Player.objects.get(id = serializer.data.get('player'))
            name = serializer.data.get('name')
            referenceParagraph = serializer.data.get('referenceParagraph')
            referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
            description = serializer.data.get('description')
            tier = serializer.data.get('tier')
            difficulty = serializer.data.get('difficulty')
            reward = serializer.data.get('reward')
            queryset = Achievement.objects.filter(Q(name = name) & Q(player = player) & Q(referenceParagraph = referenceParagraph))
            if queryset.exists():
                achievement = queryset[0]
                achievement.description = description
                achievement.tier = tier
                achievement.difficulty = difficulty
                achievement.reward = reward
                achievement.save(update_fields = ['description', 'tier', 'difficulty', 'reward'])
                return Response(AchievementSerializer(achievement).data, status = status.HTTP_200_OK)
            else:
                achievement = Achievement(chapter = chapter, player = player, name = name, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, description = description, tier = tier, difficulty = difficulty, reward = reward)
                achievement.save()
                return Response(AchievementSerializer(achievement).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreateItemView(APIView):
    serializer_class = CreateItemSerializer

    def get(self, request, format = None): 
      chapterid = request.query_params.get('chapter')
      itemName = request.query_params.get('itemName')
      referenceParagraph = request.query_params.get('paragraph')
      item = Item.objects.filter(name = itemName, referenceParagraph__lt = referenceParagraph, chapter = chapterid).order_by('-id').first()
      serializer = ItemSerializer(item)
      return Response(serializer.data)

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            referenceParagraph = serializer.data.get('referenceParagraph')
            referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
            typ = serializer.data.get('typ')
            slot = serializer.data.get('slot')
            quantity = serializer.data.get('quantity')
            creator = serializer.data.get('creator')
            rarity = serializer.data.get('rarity')
            appearance = serializer.data.get('appearance')
            details = serializer.data.get('details')
            attributes = serializer.data.get('attributes')
            charge = serializer.data.get('charge')
            durability = serializer.data.get('durability')
            print("character id is:", serializer.data.get('belongsTo'))
            print(serializer.data)
            belongsTo = Character.objects.get(id = serializer.data.get('belongsTo'))
            isEquipped = serializer.data.get('isEquipped')
            inInventory = serializer.data.get('inInventory')
            sellValue = serializer.data.get('sellValue')
            queryset = Item.objects.filter(Q(chapter = chapter) & Q(name = name) & Q(referenceParagraph = referenceParagraph))
            if queryset.exists():
                item = queryset[0]
                item.typ = typ
                item.slot = slot
                item.quantity = quantity
                item.rarity = rarity
                item.appearance = appearance
                item.save(update_fields = ['typ', 'slot', 'quantity', 'rarity', 'appearance'])
                return Response(ItemSerializer(item).data, status = status.HTTP_200_OK)
            else:
                if referenceToLastRelevantEvent:
                    item = Item(name = name, chapter = chapter, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, typ = typ, slot = slot, quantity = quantity, creator = creator, rarity = rarity, appearance = appearance, details = details, attributes = attributes, charge = charge, durability = durability, belongsTo = belongsTo, isEquipped = isEquipped, inInventory = inInventory, sellValue = sellValue)
                    item.save()
                    return Response(ItemSerializer(item).data, status = status.HTTP_201_CREATED)
                else:
                    item = Item(name = name, chapter = chapter, referenceParagraph = referenceParagraph, typ = typ, slot = slot, quantity = quantity, creator = creator, rarity = rarity, appearance = appearance, details = details, attributes = attributes, charge = charge, durability = durability, belongsTo = belongsTo, isEquipped = isEquipped, inInventory = inInventory, sellValue = sellValue)
                    item.save()
                    return Response(ItemSerializer(item).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

# class CreateEquipmentView(APIView):
#     serializer_class = CreateEquipmentSerializer

#     def post(self, request, format = None):
#         serializer = self.serializer_class(data = request.data)
#         if serializer.is_valid():
#             player = Player.objects.get(id = serializer.data.get('player'))
#             referenceParagraph = serializer.data.get('referenceParagraph')
#             referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
#             head = serializer.data.get('head')
#             neck = serializer.data.get('neck')
#             shoulders = serializer.data.get('shoulders')
#             back = serializer.data.get('back')
#             chest = serializer.data.get('chest')
#             wrist = serializer.data.get('wrist')
#             waist = serializer.data.get('waist')
#             underpants = serializer.data.get('underpants')
#             legs = serializer.data.get('legs')
#             feet = serializer.data.get('feet')
#             main_hand = serializer.data.get('main_hand')
#             off_hand = serializer.data.get('off_hand')
#             ranged = serializer.data.get('ranged')
#             trinket = serializer.data.get('trinket')
#             ring1 = serializer.data.get('ring1')
#             ring2 = serializer.data.get('ring2')
#             ring3 = serializer.data.get('ring3')
#             ring4 = serializer.data.get('ring4')
#             ring5 = serializer.data.get('ring5')
#             ring6 = serializer.data.get('ring6')
#             ring7 = serializer.data.get('ring7')
#             ring8 = serializer.data.get('ring8')
#             ring9 = serializer.data.get('ring9')
#             ring10 = serializer.data.get('ring10')
#             earring1 = serializer.data.get('earring1')
#             earring2 = serializer.data.get('earring2')
#             queryset = Equipment.objects.filter(Q(player = player) & Q(referenceParagraph = referenceParagraph))
#             if queryset.exists():
#                 equipment = queryset[0]
#                 equipment.head = head
#                 equipment.neck = neck
#                 equipment.shoulders = shoulders
#                 equipment.back = back
#                 equipment.chest = chest
#                 equipment.wrist = wrist
#                 equipment.waist = waist
#                 equipment.underpants = underpants
#                 equipment.legs = legs
#                 equipment.feet = feet
#                 equipment.main_hand = main_hand
#                 equipment.off_hand = off_hand
#                 equipment.ranged = ranged
#                 equipment.trinket = trinket
#                 equipment.ring1 = ring1
#                 equipment.ring2 = ring2
#                 equipment.ring3 = ring3
#                 equipment.ring4 = ring4
#                 equipment.ring5 = ring5
#                 equipment.ring6 = ring6
#                 equipment.ring7 = ring7
#                 equipment.ring8 = ring8
#                 equipment.ring9 = ring9
#                 equipment.ring10 = ring10
#                 equipment.earring1 = earring1
#                 equipment.earring2 = earring2
#                 equipment.save(update_fields = ['head', 'neck', 'shoulders', 'back', 'chest', 'wrist', 'waist', 'underpants', 'legs', 'feet', 'main_hand', 'off_hand', 'ranged', 'trinket', 'ring1', 'ring2', 'ring3', 'ring4', 'ring5', 'ring6', 'ring7', 'ring8', 'ring9', 'ring10', 'earring1', 'earring2'])
#                 return Response(EquipmentSerializer(equipment).data, status = status.HTTP_200_OK)
#             else:
#                 equipment = Item(player = player, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, head = head, neck = neck, shoulders = shoulders, back = back, chest = chest, wrist = wrist, waist = waist, underpants = underpants, legs = legs, feet = feet, main_hand = main_hand, off_hand = off_hand, ranged = ranged, trinket = trinket, ring1 = ring1, ring2 = ring2, ring3 = ring3, ring4 = ring4, ring5 = ring5, ring6 = ring6, ring7 = ring7, ring8 = ring8, ring9 = ring9, ring10 = ring10, earring1 = earring1, earring2 = earring2)
#                 equipment.save()
#                 return Response(EquipmentSerializer(equipment).data, status = status.HTTP_201_CREATED)
#         return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

# class CreateInventoryView(APIView):
#     serializer_class = CreateInventorySerializer

#     def get(self, request, format = None):
#         player = request.query_params.get('player')
#         chapterid = request.query_params.get('chapter')
#         paragraph = request.query_params.get('paragraph')
#         if player and chapterid and paragraph:
#             inventory = Inventory.objects.filter(player__name = player, player__character__chapter = chapterid, referenceParagraph__lt = paragraph).order_by('-id').first()
#             return Response(InventorySerializer(inventory).data, status = status.HTTP_200_OK)
#         return Response(status = status.HTTP_400_BAD_REQUEST)

#     def post(self, request, format = None):
#         serializer = self.serializer_class(data = request.data)
#         if serializer.is_valid():
#             player = Player.objects.get(id = serializer.data.get('player'))
#             referenceParagraph = serializer.data.get('referenceParagraph')
#             referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
#             slots = serializer.data.get('slots')
#             queryset = Inventory.objects.filter(Q(player = player) & Q(referenceParagraph = referenceParagraph))
#             if queryset.exists():
#                 inventory = queryset[0]
#                 inventory.slots = slots
#                 inventory.save(update_fields = ['slots'])
#                 return Response(InventorySerializer(inventory).data, status = status.HTTP_200_OK)
#             else:
#                 inventory = Inventory(player = player, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, slots = slots)
#                 inventory.save()
#                 return Response(InventorySerializer(inventory).data, status = status.HTTP_201_CREATED)
#         return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

# class CreateSlotView(APIView):
#     serializer_class = CreateSlotSerializer

#     def post(self, request, format = None):
#         serializer = self.serializer_class(data = request.data)
#         if serializer.is_valid():
#             inventory = Inventory.objects.get(id = serializer.data.get('inventory'))
#             item = Item.objects.get(id = serializer.data.get('item'))
#             referenceParagraph = serializer.data.get('referenceParagraph')
#             referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
#             queryset = Slot.objects.filter(Q(inventory = inventory) & Q(referenceParagraph = referenceParagraph))
#             if queryset.exists():
#                 slot = queryset[0]
#                 slot.item = item
#                 slot.save(update_fields = ['item'])
#                 return Response(SlotSerializer(slot).data, status = status.HTTP_200_OK)
#             else:
#                 slot = Slot(inventory = inventory, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, item = item)
#                 slot.save()
#                 return Response(SlotSerializer(slot).data, status = status.HTTP_201_CREATED)
#         return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class CreateCurrencyView(APIView):
    serializer_class = CreateCurrencySerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            chapter = Chapter.objects.get(id = serializer.data.get('chapter'))
            name = serializer.data.get('name')
            player = Player.objects.get(id = serializer.data.get('player'))
            referenceParagraph = serializer.data.get('referenceParagraph')
            referenceToLastRelevantEvent = serializer.data.get('referenceToLastRelevantEvent')
            amount = serializer.data.get('amount')
            queryset = Currency.objects.filter(Q(player = player) & Q(name = name) & Q(referenceParagraph = referenceParagraph))
            if queryset.exists():
                currency = queryset[0]
                currency.amount = amount
                currency.save(update_fields = ['amount'])
                return Response(CurrencySerializer(currency).data, status = status.HTTP_200_OK)
            else:
                currency = Currency(chapter = chapter, name = name, player = player, referenceParagraph = referenceParagraph, referenceToLastRelevantEvent = referenceToLastRelevantEvent, amount = amount)
                currency.save()
                return Response(CurrencySerializer(currency).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

