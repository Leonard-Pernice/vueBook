from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Max
from .serializers import *

@receiver(post_save, sender=Character)
@receiver(post_save, sender=Player)
@receiver(post_save, sender=Relationship)
@receiver(post_save, sender=Stat)
@receiver(post_save, sender=Skill)
@receiver(post_save, sender=Quest)
@receiver(post_save, sender=Achievement)
@receiver(post_save, sender=Item)
# @receiver(post_save, sender=Equipment)
# @receiver(post_save, sender=Inventory)
# @receiver(post_save, sender=Slot)
@receiver(post_save, sender=Currency)
def set_my_field(sender, instance, **kwargs):
    if instance.referenceToLastRelevantEvent == 0:
        instance.referenceToLastRelevantEvent = instance.id
        instance.save()

@receiver(post_save, sender=Chapter)
def create_related_characters(sender, instance, created, **kwargs):
    # current_paragraph = ParagraphSerializer(instance).data
    # current_chapter_model = Chapter.objects.get(id=current_paragraph['chapter'])
    current_chapter = ChapterSerializer(instance).data
    if created:
        prev_chapter_name = "Chapter " + str(int(current_chapter['name'].split(' ')[1]) - 1)
        prev_chapter = None
        try: 
            prev_chapter = Chapter.objects.get(name = prev_chapter_name)
        except:
            prev_chapter = None
            print("Chapter does not exist!")
        if prev_chapter:
            # Creating copies of all the latest CHARACTER instances
            querysetCharacter = Character.objects.filter(chapter=prev_chapter).values('name', 'lastname').annotate(highest_id=Max('id'))
            for group in querysetCharacter:
                referenceCharacter = Character.objects.get(id=group['highest_id'])
                copyOfCharacter = Character(
                    name=referenceCharacter.name,
                    lastname=referenceCharacter.lastname,
                    chapter=instance,
                    referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                    information=referenceCharacter.information,
                    statusOfNpc=referenceCharacter.statusOfNpc,
                    age=referenceCharacter.age,
                    gender=referenceCharacter.gender,
                    height=referenceCharacter.height,
                    weight=referenceCharacter.weight,
                    species=referenceCharacter.species,
                    race=referenceCharacter.race,
                    image=referenceCharacter.image,
                    thumbnail=referenceCharacter.thumbnail
                )
                copyOfCharacter.save()

@receiver(post_save, sender=Character)
def create_related_players(sender, instance, created, **kwargs):
    current_character = CharacterSerializer(instance).data
    # current_paragraph = ParagraphSerializer(Paragraph.objects.get(id=current_character['paragraph'])).data
    current_chapter_model = Chapter.objects.get(id=current_character['chapter'])
    current_chapter = ChapterSerializer(current_chapter_model).data
    if created and len(Paragraph.objects.filter(chapter = current_chapter['id'])) == 0:
        prev_chapter_name = "Chapter " + str(int(current_chapter['name'].split(' ')[1]) - 1)
        prev_chapter = None
        try: 
            prev_chapter = Chapter.objects.get(name = prev_chapter_name)
        except:
            prev_chapter = None
            print("Chapter does not exist!")
        if prev_chapter:
            queryset = Player.objects.filter(character__chapter=prev_chapter).values('name').annotate(highest_id=Max('id'))
            for group in queryset:
                referencePlayer = Player.objects.get(id=group['highest_id'])
                copyOfPlayer = Player(
                    chapter=current_chapter_model,
                    name=referencePlayer.name,
                    character=instance,
                    referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                    characterName=referencePlayer.characterName,
                    job=referencePlayer.job,
                    title=referencePlayer.title,
                    level=referencePlayer.level,
                    exp=referencePlayer.exp,
                    typ=referencePlayer.typ,
                    image=referencePlayer.image,
                    thumbnail=referencePlayer.thumbnail
                )
                copyOfPlayer.save()
            # Creating copies of all the latest ITEM instances
            querysetItem = Item.objects.filter(belongsTo__chapter=prev_chapter).values('name').annotate(highest_id=Max('id'))
            for group in querysetItem:
                referenceItem = Item.objects.get(id=group['highest_id'])
                copyOfItem = Item(
                    name=referenceItem.name,
                    chapter=current_chapter_model,
                    referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                    typ=referenceItem.typ,
                    slot=referenceItem.slot,
                    quantity=referenceItem.quantity,
                    creator=referenceItem.creator,
                    rarity=referenceItem.rarity,
                    appearance=referenceItem.appearance,
                    details=referenceItem.details,
                    attributes=referenceItem.attributes,
                    charge=referenceItem.charge,
                    durability=referenceItem.durability,
                    belongsTo=instance,
                    isEquipped=referenceItem.isEquipped,
                    inInventory=referenceItem.inInventory,
                    sellValue=referenceItem.sellValue
                )
                copyOfItem.save()


@receiver(post_save, sender=Player)
def create_related_StatsQuestsAchievementsETC(sender, instance, created, **kwargs):
    current_player = PlayerSerializer(instance).data
    current_character = CharacterSerializer(Character.objects.get(id=current_player['character']['id'])).data
    # current_paragraph = ParagraphSerializer(Paragraph.objects.get(id=current_character['paragraph'])).data
    current_chapter_model = Chapter.objects.get(id=current_character['chapter'])
    current_chapter = ChapterSerializer(current_chapter_model).data
    if created and len(Paragraph.objects.filter(chapter = current_chapter['id'])) == 0:
        prev_chapter_name = "Chapter " + str(int(current_chapter['name'].split(' ')[1]) - 1)
        prev_chapter = None
        try: 
            prev_chapter = Chapter.objects.get(name = prev_chapter_name)
        except:
            prev_chapter = None
            print("Chapter does not exist!")
        if prev_chapter:
            # Creating copies of all the latest STAT instances
            querysetStats = Stat.objects.filter(player__character__chapter=prev_chapter).values('name').annotate(highest_id=Max('id'))
            for group in querysetStats:
                referenceStat = Stat.objects.get(id=group['highest_id'])
                copyOfStat = Stat(
                    chapter=current_chapter_model,
                    name=referenceStat.name,
                    player=instance,
                    referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                    base=referenceStat.base,
                    increased=referenceStat.increased,
                    trained=referenceStat.trained,
                    bar=referenceStat.bar
                )
                copyOfStat.save()
            # Creating copies of all the latest QUEST instances
            querysetQuests = Quest.objects.filter(player__character__chapter=prev_chapter).values('name').annotate(highest_id=Max('id'))
            for group in querysetQuests:
                referenceQuest = Quest.objects.get(id=group['highest_id'])
                copyOfQuest = Quest(
                    chapter=current_chapter_model,
                    name=referenceQuest.name,
                    player=instance,
                    referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                    statusOfQuest=referenceQuest.statusOfQuest,
                    description=referenceQuest.description,
                    optional_description=referenceQuest.optional_description,
                    tier=referenceQuest.tier,
                    difficulty=referenceQuest.difficulty,
                    reward_title=referenceQuest.reward_title,
                    reward=referenceQuest.reward,
                    optional_reward=referenceQuest.optional_reward,
                    exp_received=referenceQuest.exp_received
                )
                copyOfQuest.save()
            # Creating copies of all the latest ACHIEVEMENT instances
            querysetAchievement = Achievement.objects.filter(player__character__chapter=prev_chapter).values('name').annotate(highest_id=Max('id'))
            for group in querysetAchievement:
                referenceAchievement = Achievement.objects.get(id=group['highest_id'])
                copyOfAchievement = Achievement(
                    chapter=current_chapter_model,
                    name=referenceAchievement.name,
                    player=instance,
                    referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                    description=referenceAchievement.description,
                    tier=referenceAchievement.tier,
                    difficulty=referenceAchievement.difficulty,
                    reward=referenceAchievement.reward
                )
                copyOfAchievement.save()
            # Creating copies of all the latest RELATIONSHIP instances
            querysetRelationships = Relationship.objects.filter(player__character__chapter=prev_chapter).values('player', 'npc').annotate(highest_id=Max('id'))
            for group in querysetRelationships:
                referenceRelationship = Relationship.objects.get(id=group['highest_id'])
                if len(Relationship.objects.filter(player=referenceRelationship.player, npc=referenceRelationship.npc, player__character__chapter=current_chapter['id'])) > 0:
                    continue
                try:
                    npcName = CharacterSerializer(Character.objects.get(id=int(str(referenceRelationship.npc).split(":")[0]))).data
                    relevantCharacter = Character.objects.get(name=npcName['name'], lastName=npcName['lastName'], chapter=current_chapter['id'])
                    copyOfRelationship = Relationship(
                        chapter=current_chapter_model,
                        player=instance,
                        npc=relevantCharacter,
                        referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                        score=referenceRelationship.score,
                        description=referenceRelationship.description
                    )
                    copyOfRelationship.save()
                except Exception as e:
                    print(e)
                    continue
            # # Creating copies of all the latest INVENTORY instances
            # querysetInventories = Inventory.objects.filter(player__character__chapter=prev_chapter).values('player').annotate(highest_id=Max('id'))
            # for group in querysetInventories:
            #     referenceInventory = Inventory.objects.get(id=group['highest_id'])
            #     copyOfInventory = Inventory(
            #         player=instance,
            #         referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
            #         slots=referenceInventory.slots
            #     )
            #     copyOfInventory.save()
            # # Creating copies of all the latest EQUIPMENT instances
            # querysetItems = Item.objects.filter(chapter=current_chapter).values('name').annotate(highest_id=Max('id'))
            # # This doesn't work because I need to also loop by group and then filter by highest ID. 
            # querysetEquipment = Equipment.objects.filter(player__character__chapter=prev_chapter).values('player').annotate(highest_id=Max('id'))
            # for group in querysetEquipment:
            #     # referenceEquipment = Equipment.objects.get(id=group['highest_id'])
            #     copyOfEquipment = Equipment(
            #         player=instance,
            #         referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1
            #     )
            #     result, querysetItems = itemAllocation(querysetItems, 'Head')
            #     copyOfEquipment.head = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Neck')
            #     copyOfEquipment.neck = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Shoulders')
            #     copyOfEquipment.shoulders = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Back')
            #     copyOfEquipment.back = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Chest')
            #     copyOfEquipment.chest = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Wrist')
            #     copyOfEquipment.wrist = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Waist')
            #     copyOfEquipment.waist = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Underpants')
            #     copyOfEquipment.underpants = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Legs')
            #     copyOfEquipment.legs = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Feet')
            #     copyOfEquipment.feet = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Hand')
            #     copyOfEquipment.main_hand = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Hand')
            #     copyOfEquipment.off_hand = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ranged')
            #     copyOfEquipment.ranged = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Trinket')
            #     copyOfEquipment.trinket = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring1 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring2 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring3 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring4 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring5 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring6 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring7 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring8 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring9 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Ring')
            #     copyOfEquipment.ring10 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Earring')
            #     copyOfEquipment.earring1 = result
            #     result, querysetItems = itemAllocation(querysetItems, 'Earring')
            #     copyOfEquipment.earring1 = result
            #     copyOfEquipment.save()
            # Creating copies of all the latest CURRENCY instances
            querysetCurrencies = Currency.objects.filter(player__character__chapter=prev_chapter).values('player').annotate(highest_id=Max('id'))
            for group in querysetCurrencies:
                referenceCurrency = Currency.objects.get(id=group['highest_id'])
                copyOfCurrency = Currency(
                    chapter=current_chapter_model,
                    name=referenceCurrency.name,
                    player=instance,
                    referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                    amount=referenceCurrency.amount
                )
                copyOfCurrency.save()


@receiver(post_save, sender=Stat)
def create_related_Skills(sender, instance, created, **kwargs):
    current_stat = StatSerializer(instance).data
    current_player_model = Player.objects.get(id=current_stat['player']['id'])
    current_player = PlayerSerializer(current_player_model).data
    current_character = CharacterSerializer(Character.objects.get(id=current_player['character']['id'])).data
    # current_paragraph = ParagraphSerializer(Paragraph.objects.get(id=current_character['paragraph'])).data
    current_chapter_model = Chapter.objects.get(id=current_character['chapter'])
    current_chapter = ChapterSerializer(current_chapter_model).data
    if created and len(Paragraph.objects.filter(chapter = current_chapter['id'])) == 0:
        prev_chapter_name = "Chapter " + str(int(current_chapter['name'].split(' ')[1]) - 1)
        prev_chapter = None
        try: 
            prev_chapter = Chapter.objects.get(name = prev_chapter_name)
        except:
            prev_chapter = None
            print("Chapter does not exist!")
        if prev_chapter:
            # Creating copies of all the latest SKILL instances
            querysetSkills = Skill.objects.filter(player__character__chapter=prev_chapter).values('name').annotate(highest_id=Max('id'))
            for group in querysetSkills:
                referenceSkill = Skill.objects.get(id=group['highest_id'])
                if len(Skill.objects.filter(name=referenceSkill.name, player__character__chapter=current_chapter['id'])) > 0:
                    continue
                try:
                    statName = StatSerializer(Stat.objects.get(id=int(str(referenceSkill.modifier).split(":")[0]))).data
                    relevantStat = Stat.objects.get(name=statName['name'], player__character__chapter=current_chapter['id'])
                    copyOfSkill = Skill(
                        chapter=current_chapter_model,
                        name=referenceSkill.name,
                        player=current_player_model,
                        modifier=relevantStat,
                        referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
                        level=referenceSkill.level,
                        exp=referenceSkill.exp,
                        description=referenceSkill.description,
                        typ=referenceSkill.typ,
                        ap=referenceSkill.ap,
                        mp=referenceSkill.mp,
                        st=referenceSkill.st
                    )
                    copyOfSkill.save()
                except Exception as e:
                    print(e)
                    continue

# @receiver(post_save, sender=Inventory)
# def create_related_Slots(sender, instance, created, **kwargs):
#     current_inventory = InventorySerializer(instance).data
#     current_player_model = Player.objects.get(id=current_inventory['player'])
#     current_player = PlayerSerializer(current_player_model).data
#     current_character = CharacterSerializer(Character.objects.get(id=current_player['character'])).data
#     # current_paragraph = ParagraphSerializer(Paragraph.objects.get(id=current_character['paragraph'])).data
#     current_chapter_model = Chapter.objects.get(id=current_character['chapter'])
#     current_chapter = ChapterSerializer(current_chapter_model).data
#     if created and len(Paragraph.objects.filter(chapter = current_chapter['id'])) == 0:
#         prev_chapter_name = "Chapter " + str(int(current_chapter['name'].split(' ')[1]) - 1)
#         prev_chapter = None
#         try: 
#             prev_chapter = Chapter.objects.get(name = prev_chapter_name)
#         except:
#             prev_chapter = None
#             print("Chapter does not exist!")
#         if prev_chapter:
#             # Creating copies of all the latest SLOT instances
#             querysetItems = Item.objects.filter(chapter=current_chapter, inInventory=True)
#             # Gotta put the right items into new slots. Per player. 
#             # Question: how do I know which Item belongED to which player?
#             querysetSlots = Slot.objects.filter(inventory__player__character__chapter=prev_chapter).values('inventory').annotate(highest_id=Max('id'))
#             for group in querysetSlots:
#                 referenceSlot = Slot.objects.get(id=group['highest_id'])
#                 # current_item_name = ItemSerializer(Item.objects.get(id=referenceSlot['item'])).data
#                 # current_item = Item.objects.get(name=current_item_name['name'], chapter=current_chapter['id'])
#                 copyOfSlot = Slot(
#                     inventory=instance,
#                     player=current_player_model,
#                     referenceParagraph=int(ParagraphSerializer(Paragraph.objects.all().order_by('-id').first()).data['id']) + 1,
#                     item=current_item
#                 )
#                 copyOfSlot.save()

# I should not look for the highest ID value, but the highest referenceParagraph value, since new instances might be added later
