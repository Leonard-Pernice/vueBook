from io import BytesIO
from PIL import Image
import math

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files import File
from django.db import models

# Create your models here. Where we describe to the database what types of information we're going to use and store. 

class Book(models.Model):
    title = models.CharField(max_length=100, default = "Book 1")
    author = models.CharField(max_length=100, default = "Leonard Pernice")
    # other fields for book information

    def __str__(self):
        return self.title

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ('id',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name = image.name)

        return thumbnail

# class ChapterInit(models.Model):
#     chapter = models.ForeignKey(Chapter, related_name='chapterinits', on_delete=models.CASCADE)

class Paragraph(models.Model):
    name = models.CharField(default="", max_length=255, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, related_name='paragraphs', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    attributes = models.TextField(default="", blank=True, null=True)
    c = models.CharField(default="", max_length=255, blank=True, null=True)
    exp = models.DecimalField(default=0, decimal_places=4, max_digits=15 , blank=True, null=True)
    text = models.TextField(default="", blank=True, null=True)
    textorder = models.DecimalField(default=0, decimal_places=30, max_digits=38)
    referenceToLastRelevantEvent = models.IntegerField(default=1)
    class Meta:
        ordering = ('id',)

    def __str__(self):
        if self.text == None:
            return 'none-type paragraph'
        if len(self.text.split()) > 0:
            words = self.text.split()
            firstwords = words[:5]
            displayedname = ' '.join([str(self.id), ': '] + firstwords)
        else:
            displayedname = 'no-text paragraph'
        return displayedname

class Character(models.Model):
    name = models.CharField(max_length=255)
    lastname = models.CharField(default="", max_length=255)
    chapter = models.ForeignKey(Chapter, related_name='characters', on_delete=models.CASCADE)
    referenceParagraph = models.IntegerField(default=1)
    referenceToLastRelevantEvent = models.IntegerField(default=0)

    information = models.TextField(default="", blank=True, null=True)
    statusOfNpc = models.TextField(default="", blank=True, null=True)
    age = models.IntegerField(default=20)
    gender = models.CharField(max_length=255)
    height = models.IntegerField(default=170)
    weight = models.IntegerField(default=65)
    species = models.CharField(max_length=255, default="Human")
    race = models.CharField(max_length=255, default="", blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    @property
    def typeReference(self):
        return 'character'

    def __str__(self):
        return ''.join([str(self.id), ': ', self.name, ' ', self.lastname])

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name = image.name)

        return thumbnail

class Player(models.Model):
    name = models.CharField(default="", max_length=255)
    chapter = models.ForeignKey(Chapter, related_name='chapter_players', on_delete=models.CASCADE)
    character = models.ForeignKey(Character, related_name='players', on_delete=models.CASCADE)
    referenceParagraph = models.IntegerField(default=1)
    referenceToLastRelevantEvent = models.IntegerField(default=0)

    characterName = models.CharField(max_length=255, default="JohnBrass", blank=True, null=True)
    job = models.CharField(max_length=255, default="-", blank=True, null=True)
    title = models.CharField(max_length=255, default="-", blank=True, null=True)
    level = models.IntegerField(default=0)
    # exp = models.IntegerField(default=0)
    exp = models.DecimalField(default=0.00, max_digits=5, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1 - 10**(-4))])
    typ = models.CharField(max_length=255, default="Character")

    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    @property
    def typeReference(self):
        return 'player'

    def __str__(self):
        return ''.join([str(self.id), ': ', self.name])

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name = image.name)

        return thumbnail

class Relationship(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='chapter_relationships', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='relationship', on_delete=models.CASCADE)
    npc = models.ForeignKey(Character, related_name='relationship', on_delete=models.CASCADE)
    referenceParagraph = models.IntegerField(default=1)
    referenceToLastRelevantEvent = models.IntegerField(default=0)

    score = models.IntegerField(default=0)
    description = models.TextField(default="")

    @property
    def typeReference(self):
        return 'relationship'
    
    def __str__(self):
        return ''.join([str(self.id), ': ', self.player, ' <-> ', self.npc])

# class Companion(models.Model):

class Stat(models.Model):
    name = models.CharField(default="", max_length=255)
    chapter = models.ForeignKey(Chapter, related_name='chapter_stats', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='stats', on_delete=models.CASCADE)
    referenceParagraph = models.IntegerField(default=1)
    referenceToLastRelevantEvent = models.IntegerField(default=0)

    base = models.IntegerField(default=50)
    increased = models.IntegerField(default=0)
    trained = models.DecimalField(decimal_places = 2, max_digits = 16, default=0)
    bar = models.IntegerField(default=50)
    idealValue = models.CharField(default='max', max_length=10)

    @property
    def typeReference(self):
        return 'stat'

    def __str__(self):
        return ''.join([str(self.id), ': ', self.name])

class Skill(models.Model):
    name = models.CharField(default="", max_length=255)
    chapter = models.ForeignKey(Chapter, related_name='chapter_skills', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='skills', on_delete=models.CASCADE)
    modifier = models.ForeignKey(Stat, related_name='stats', on_delete=models.CASCADE)
    referenceParagraph = models.IntegerField(default=0)
    referenceToLastRelevantEvent = models.IntegerField(default=0)

    level = models.IntegerField(default=0)
    exp = models.DecimalField(default=0.0000, max_digits=5, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1 - 10**(-4))])
    description = models.TextField(default="")
    typ = models.CharField(default="Active", max_length=256, blank=True, null=True)
    ap = models.IntegerField(default=0, blank=True, null=True)
    mp = models.IntegerField(default=0, blank=True, null=True)
    st = models.IntegerField(default=0, blank=True, null=True)

    @property
    def typeReference(self):
        return 'skill'

    def __str__(self):
        return ''.join([str(self.id), ': ', self.name])

class Quest(models.Model):
    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, related_name='chapter_quests', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='quests')
    referenceParagraph = models.IntegerField(default=1)
    referenceToLastRelevantEvent = models.IntegerField(default=0)
    # other fields for quest information
    statusOfQuest = models.CharField(max_length=255, default="Ongoing")
    description = models.TextField(default="")
    optional_description = models.TextField(default="", blank=True, null=True)
    tier = models.IntegerField(default=1)
    difficulty = models.IntegerField(default=1)
    reward_title = models.CharField(max_length=100)
    reward = models.TextField(default="", blank=True, null=True)
    optional_reward = models.TextField(default="", blank=True, null=True)
    exp_received = models.DecimalField(default=0.0, max_digits=12, decimal_places=4, blank=True, null=True)

    @property
    def typeReference(self):
        return 'quest'

    def __str__(self):
        return ''.join([str(self.id), ': ', self.name])

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, related_name='chapter_achievements', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='achievements')
    referenceParagraph = models.IntegerField(default=1)
    referenceToLastRelevantEvent = models.IntegerField(default=0)
    # other fields for achievement information
    description = models.TextField(default="")
    tier = models.IntegerField(default=1)
    difficulty = models.IntegerField(default=1)
    reward = models.TextField()

    @property
    def typeReference(self):
        return 'achievement'

    def __str__(self):
        return ''.join([str(self.id), ': ', self.name])

class Item(models.Model):
    name = models.CharField(max_length=255)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='items')
    referenceParagraph = models.IntegerField(default=1)
    referenceToLastRelevantEvent = models.IntegerField(default=0)

    typ = models.CharField(max_length=255)
    slot = models.CharField(max_length=255, default="", blank=True, null=True)
    quantity = models.IntegerField(default=1)
    creator = models.CharField(max_length=255, default="", blank=True, null=True)
    rarity = models.CharField(max_length=100)
    appearance = models.TextField()
    details = models.TextField()
    attributes = models.TextField(default="", blank=True, null=True)
    charge = models.IntegerField(default=0, blank=True, null=True)
    durability = models.IntegerField(default=100, blank=True, null=True)

    belongsTo = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='items')
    isEquipped = models.BooleanField(default=False)
    inInventory = models.BooleanField(default=True)
    sellValue = models.IntegerField(default=0)

    @property
    def typeReference(self):
        return 'item'

    def __str__(self):
        return ''.join([str(self.id), ': ', self.name])

class Currency(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='chapter_currencies', on_delete=models.CASCADE)
    name = models.CharField(default="Coin", max_length=100)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='currencies')
    referenceParagraph = models.IntegerField(default=1)
    referenceToLastRelevantEvent = models.IntegerField(default=0)
    amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)

    @property
    def typeReference(self):
        return 'currency'

    def __str__(self):
        return ''.join([str(self.id), ': ', str(self.name), ' of ', str(self.player)])

# class Equipment(models.Model):
#     player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='players_equipment')
#     referenceParagraph = models.IntegerField(default=1)
#     referenceToLastRelevantEvent = models.IntegerField(default=0)

#     head = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_head', blank=True, null=True)
#     neck = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_neck', blank=True, null=True)
#     shoulders = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_shoulders', blank=True, null=True)
#     back = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_back', blank=True, null=True)
#     chest = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_chest', blank=True, null=True)
#     wrist = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_wrist', blank=True, null=True)
#     waist = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_waist', blank=True, null=True)
#     underpants = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_underpants', blank=True, null=True)
#     legs = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_legs', blank=True, null=True)
#     feet = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_feet', blank=True, null=True)
#     main_hand = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_main_hand', blank=True, null=True)
#     off_hand = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_off_hand', blank=True, null=True)
#     ranged = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ranged', blank=True, null=True)
#     trinket = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_trinket', blank=True, null=True)
#     ring1 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring1', blank=True, null=True)
#     ring2 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring2', blank=True, null=True)
#     ring3 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring3', blank=True, null=True)
#     ring4 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring4', blank=True, null=True)
#     ring5 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring5', blank=True, null=True)
#     ring6 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring6', blank=True, null=True)
#     ring7 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring7', blank=True, null=True)
#     ring8 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring8', blank=True, null=True)
#     ring9 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring9', blank=True, null=True)
#     ring10 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_ring10', blank=True, null=True)
#     earring1 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_earring1', blank=True, null=True)
#     earring2 = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_earring2', blank=True, null=True)

#     @property
#     def typeReference(self):
#         return 'equipment'

#     def __str__(self):
#         return ''.join([str(self.id), ' - inventory of: ', str(self.player)])

# class Inventory(models.Model):
#     player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='players_inventory')
#     referenceParagraph = models.IntegerField(default=1)
#     referenceToLastRelevantEvent = models.IntegerField(default=0)

#     slots = models.IntegerField(default=16)

#     @property
#     def typeReference(self):
#         return 'inventory'

#     def __str__(self):
#         return ''.join([str(self.id), ': ', str(self.player)])

# class Slot(models.Model):
#     inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='inventories')
#     item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items_inventory', blank=True, null=True)
#     referenceParagraph = models.IntegerField(default=1)
#     referenceToLastRelevantEvent = models.IntegerField(default=0)

#     @property
#     def typeReference(self):
#         return 'slot'

#     @property
#     def name(self):
#         return self.item.name

#     def __str__(self):
#         return ''.join([str(self.id), ': ', str(self.item)])
