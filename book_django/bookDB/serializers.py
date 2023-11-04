from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'
        depth = 1


class StatSerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    class Meta:
        model = Stat
        fields = '__all__'
        depth = 1

        
class SkillSerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    stat = StatSerializer(many=True, read_only=True)
    class Meta:
        model = Skill
        fields = '__all__'
        depth = 1


class QuestSerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    class Meta:
        model = Quest
        fields = '__all__'
        depth = 1


class AchievementSerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    class Meta:
        model = Achievement
        fields = '__all__'
        depth = 1


class RelationshipSerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    class Meta:
        model = Relationship
        fields = '__all__'
        depth = 1


class PlayerSerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    stats = StatSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    quests = QuestSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    relationships = RelationshipSerializer(many=True, read_only=True)
    class Meta:
        model = Player
        fields = '__all__'
        depth = 1

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     for related_name in ['stats', 'skills', 'quests', 'achievements']:
    #         related_objs = ret.pop(related_name)
    #         ret[related_name] = {obj['name']: obj for obj in related_objs}
    #     return ret

# class InventorySerializer(serializers.ModelSerializer):
#     typeReference = serializers.CharField(read_only=True)
#     players_inventory = PlayerSerializer(many=True, read_only=True)
#     class Meta:
#         model = Inventory
#         fields = '__all__'
    
#     def get_typeReference(self, obj):
#         return obj.typeReference

# class SlotSerializer(serializers.ModelSerializer):
#     typeReference = serializers.CharField(read_only=True)
#     name = serializers.SerializerMethodField()
#     inventories = InventorySerializer(many=True, read_only=True)
#     items_inventory = ItemSerializer(many=True, read_only=True)
#     class Meta:
#         model = Slot
#         fields = '__all__'
    
#     def get_typeReference(self, obj):
#         return obj.typeReference
    
#     def get_name(self, obj):
#         return obj.name

# class EquipmentSerializer(serializers.ModelSerializer):
#     typeReference = serializers.CharField(read_only=True)
#     players_equipment = PlayerSerializer(many=True, read_only=True)
#     items_head = ItemSerializer(many=True, read_only=True)
#     items_neck = ItemSerializer(many=True, read_only=True)
#     items_neck = ItemSerializer(many=True, read_only=True)
#     items_shoulders = ItemSerializer(many=True, read_only=True)
#     items_back = ItemSerializer(many=True, read_only=True)
#     items_chest = ItemSerializer(many=True, read_only=True)
#     items_wrist = ItemSerializer(many=True, read_only=True)
#     items_waist = ItemSerializer(many=True, read_only=True)
#     items_underpants = ItemSerializer(many=True, read_only=True)
#     items_legs = ItemSerializer(many=True, read_only=True)
#     items_feet = ItemSerializer(many=True, read_only=True)
#     items_main_hand = ItemSerializer(many=True, read_only=True)
#     items_off_hand = ItemSerializer(many=True, read_only=True)
#     items_ranged = ItemSerializer(many=True, read_only=True)
#     items_trinket = ItemSerializer(many=True, read_only=True)
#     items_ring1 = ItemSerializer(many=True, read_only=True)
#     items_ring2 = ItemSerializer(many=True, read_only=True)
#     items_ring3 = ItemSerializer(many=True, read_only=True)
#     items_ring4 = ItemSerializer(many=True, read_only=True)
#     items_ring5 = ItemSerializer(many=True, read_only=True)
#     items_ring6 = ItemSerializer(many=True, read_only=True)
#     items_ring7 = ItemSerializer(many=True, read_only=True)
#     items_ring8 = ItemSerializer(many=True, read_only=True)
#     items_ring9 = ItemSerializer(many=True, read_only=True)
#     items_ring10 = ItemSerializer(many=True, read_only=True)
#     items_earring1 = ItemSerializer(many=True, read_only=True)
#     items_earring2 = ItemSerializer(many=True, read_only=True)
#     class Meta:
#         model = Equipment
#         fields = '__all__'
    
#     def get_typeReference(self, obj):
#         return obj.typeReference

class CurrencySerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    players = PlayerSerializer(many=True, read_only=True)
    class Meta:
        model = Currency
        fields = '__all__'
        depth = 1


class CharacterSerializer(serializers.ModelSerializer):
    typeReference = serializers.CharField(read_only=True)
    players = PlayerSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Character
        fields = '__all__'

class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True, read_only=True)
    characters = CharacterSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True)
    chapter_players = PlayerSerializer(many=True, read_only=True)
    chapter_relationships = RelationshipSerializer(many=True, read_only=True)
    chapter_stats = StatSerializer(many=True, read_only=True)
    chapter_skills = SkillSerializer(many=True, read_only=True)
    chapter_quests = QuestSerializer(many=True, read_only=True)
    chapter_achievements = AchievementSerializer(many=True, read_only=True)
    chapter_currencies = CurrencySerializer(many=True, read_only=True)
    book = BookSerializer(read_only=True)
    class Meta:
        model = Chapter
        fields = '__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        paragraphs = ret.pop('paragraphs')
        ret.update({f"{paragraph['id']}": paragraph for paragraph in paragraphs})
        # characters = ret.pop('characters')
        # ret.update({f"{character['name']} {character['lastname']}": character for character in characters})
        return ret

class ReferenceBookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = ['title']

class CreateChapterSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Chapter
        fields = ['book', 'name']

class CreateTextParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ['chapter', 'text', 'textorder']

class CreateEventParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ['chapter', 'attributes', 'exp', 'text', 'textorder']

class CreateCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['chapter', 'referenceParagraph', 'name', 'lastname', 'referenceToLastRelevantEvent', 'information', 'statusOfNpc', 'age', 'gender', 'height', 'weight', 'species', 'race']

class CreatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['chapter', 'character', 'name', 'referenceParagraph', 'referenceToLastRelevantEvent', 'characterName', 'job', 'title', 'level', 'exp', 'typ']

class CreateStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['chapter', 'player', 'name', 'referenceParagraph', 'referenceToLastRelevantEvent', 'base', 'increased', 'trained', 'bar', 'idealValue']

class CreateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['chapter', 'player', 'modifier', 'name', 'referenceParagraph', 'referenceToLastRelevantEvent', 'level', 'exp', 'description', 'typ', 'ap', 'mp', 'st']

class CreateQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ['chapter', 'player', 'name', 'referenceParagraph', 'referenceToLastRelevantEvent', 'statusOfQuest', 'description', 'optional_description', 'tier', 'difficulty', 'reward_title', 'reward', 'optional_reward', 'exp_received']

class CreateAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['chapter', 'player', 'name', 'referenceParagraph', 'referenceToLastRelevantEvent', 'description', 'tier', 'difficulty', 'reward']

class CreateRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['chapter', 'player', 'npc', 'referenceParagraph', 'referenceToLastRelevantEvent', 'score', 'description']

class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['chapter', 'name', 'chapter', 'referenceParagraph', 'referenceToLastRelevantEvent', 'typ', 'slot', 'quantity', 'creator', 'rarity', 'appearance', 'details', 'attributes', 'charge', 'durability', 'belongsTo', 'isEquipped', 'inInventory', 'sellValue']

# class CreateEquipmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Equipment
#         fields = ['player', 'referenceParagraph', 'referenceToLastRelevantEvent', 'head', 'neck', 'shoulders', 'back', 'chest', 'wrist', 'waist', 'underpants', 'legs', 'feet', 'main_hand', 'off_hand', 'ranged', 'trinket', 'ring1', 'ring2', 'ring3', 'ring4', 'ring5', 'ring6', 'ring7', 'ring8', 'ring9', 'ring10', 'earring1', 'earring2']

# class CreateInventorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Inventory
#         fields = ['player', 'referenceParagraph', 'referenceToLastRelevantEvent', 'slots']

# class CreateSlotSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Slot
#         fields = ['inventory', 'item', 'referenceParagraph', 'referenceToLastRelevantEvent']

class CreateCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['chapter', 'name', 'player', 'referenceParagraph', 'referenceToLastRelevantEvent', 'amount']
