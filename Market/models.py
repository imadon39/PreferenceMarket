import random
from datetime import datetime
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
import ast
import math


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Player(models.Model):
    user = models.OneToOneField(User, null=True)
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=80,null=True)
    point = models.FloatField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=(('f','Female'), ('m','Male'), ('n','none')))
    is_answered = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class Area(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=(('f','Female'), ('m','Male'), ('a','all')))
    gender_img_url = models.CharField(max_length=100,default="/static/images/gender")
    age_lower = models.PositiveIntegerField()
    age_upper = models.PositiveIntegerField()
    attribute = models.CharField(max_length=200)
    description = models.TextField()
    owners = models.ManyToManyField(Player, through='Owner', through_fields=('area','player'))

    def __unicode__(self):
        return u'%s' % (self.name)


class Owner(models.Model):
    player = models.ForeignKey(Player)
    area = models.ForeignKey(Area)

    def __unicode__(self):
        return "Player " + u'%s' % (self.player.name) + ", Area " + u'%s' % (self.area.name)

class ShopColor(models.Model):
    name = models.CharField(max_length=30)
    img_url = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.name)

class ShopFigure(models.Model):
    name = models.CharField(max_length=30)
    color = models.ManyToManyField(ShopColor)
    img_url = models.CharField(max_length=100,default="/static/images/Shops")

    def __unicode__(self):
        return u'%s' % (self.name)

class Product(models.Model):
    area = models.ForeignKey(Area)
    name = models.CharField(max_length=200)
    order = ListField(default=[],blank=True)
    open_time = models.DateTimeField('open time')
    close_time = models.DateTimeField('close time')
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    genetic_setting = models.BooleanField(default=False)
    cost_setting = models.BooleanField(default=False)
    maltiple_market = models.BooleanField(default=False)
    market_number = models.PositiveIntegerField()
    player_number = models.PositiveIntegerField()
    security_number = models.PositiveIntegerField()
    create_idea = models.BooleanField()

    def __unicode__(self):
        return u'%s' % (self.name)

class RetailStore(models.Model):
    player = models.ForeignKey(Player)
    area = models.ForeignKey(Area)
    figure = models.ForeignKey(ShopFigure)
    color = models.ForeignKey(ShopColor)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % (self.name)

class Market(models.Model):
    product = models.ForeignKey(Product)
    close_time = models.DateTimeField('close time')
    open_time = models.DateTimeField('open time')
    name = models.CharField(max_length=200)
    name_setting = models.BooleanField(default=False)
    market_number = models.PositiveIntegerField(default=1)
    trade_amount = models.PositiveIntegerField(default=0)
    reward_setting = models.BooleanField(default=False)
    participations = models.ManyToManyField(Player, through='Participation', through_fields=('market', 'player'))
    GA_setting = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.name)

    def is_closed(self):
        """check if the market is closed"""
        return self.close_time < timezone.now()

class PlayerResult(models.Model):
    player = models.ForeignKey(Player)
    market = models.ForeignKey(Market)
    investment = models.FloatField(default=0)
    returned = models.FloatField(default=0)
    total_sales = models.FloatField(default=0)
    profit_rate = models.FloatField(default=0)
    checked = models.BooleanField(default=False)
    estimate = models.BooleanField(default=False)
    estimate_time = models.DateTimeField('estimate time')

    def __unicode__(self):
        return u'%s' % (self.player.name)

class Breakdown(models.Model):
    result = models.ForeignKey(PlayerResult)
    product_name = models.CharField(max_length=200)
    attributes = ListField(default=[])
    attribute_name = models.CharField(max_length=300,default="")
    selling_price = models.PositiveIntegerField()
    purchase_number = models.PositiveIntegerField()
    sale_rate = models.FloatField()
    sales = models.FloatField()

    def __unicode__(self):
        return u'%s' % (self.result.player)

class Attribute(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=200)
    number = models.PositiveIntegerField(default=0)
    level_number = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % (self.name)

class Level(models.Model):
    attribute = models.ForeignKey(Attribute)
    name = models.CharField(max_length=200)
    number = models.PositiveIntegerField(default=0)
    interaction = models.ManyToManyField('self', through='Interaction', symmetrical = False)

    def __unicode__(self):
        return u'%s' % (self.name)

class Interaction(models.Model):
    product = models.ForeignKey(Product)
    level1 = models.ForeignKey(Level, related_name = 'level1')
    level2 = models.ForeignKey(Level, related_name = 'level2')
    effect = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.level1) + u'%s' % (self.level2)

class Security(models.Model):
    market = models.ForeignKey(Market)
    product_name = models.CharField(max_length=200,blank=True)
    selling_price = models.IntegerField(null = True)
    gross_margin  = models.IntegerField(default=0)
    attributes = ListField(default=[],blank=True)
    attribute_name = models.CharField(max_length=300,default="")
    VWAP_price = models.FloatField(default=0)
    number = models.PositiveIntegerField()
    VWAP_amount = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s' % (self.product_name)


class SecurityResult(models.Model):
    product = models.ForeignKey(Product)
    product_name = models.CharField(max_length=200)
    attributes = ListField(default=[],blank=True)
    attribute_name = models.CharField(max_length=300,default="")
    last_price_result = models.FloatField(default=0)
    VWAP_result = models.FloatField(default=0)
    sale_rate = models.FloatField(default=0)
    number = models.IntegerField()
    GA_setting = models.BooleanField(default=False)
    estimate_time = models.DateTimeField('estimate_time')

    def __unicode__(self):
        return u'%s' % (self.product.name)

class PriceHistory(models.Model):
    product = models.ForeignKey(Product)
    number = models.IntegerField()
    data = ListField(default=[],blank = True)
    is_open = models.BooleanField(default=True)
    histories = models.ManyToManyField(SecurityResult, through='History', through_fields=('pricehistory','result'))

    def __unicode__(self):
        return u'%s' % (self.product.name)


class History(models.Model):
    pricehistory = models.ForeignKey(PriceHistory)
    result = models.ForeignKey(SecurityResult)
    estimate_time = models.DateTimeField('estimate_time')

    def __unicode__(self):
        return "Product " + u'%s' % (self.pricehistory.product) + ", Time " + u'%s' % (self.estimate_time)

class SecurityPrice(models.Model):
    market = models.OneToOneField(Market)
    price = ListField(default=[],blank = True)
    sale_rate = ListField(default=[],blank = True)
    amount = ListField(default=[],blank = True)

    def __unicode__(self):
        return u'%s' % (self.market.product.name)

class NewChromosome(models.Model):
    product = models.ForeignKey(Product)
    attributes = ListField(default=[])

    def __unicode__(self):
        return u'%s' % (self.attributes)


class LMSR(models.Model):
    product = models.OneToOneField(Product)
    b = models.FloatField(default=0)
    P0 = models.FloatField(default=0)

    def __str__(self):
        return str(self.b)

    def p_cost_function(self,security_price_amount):
        total_sum = sum([math.exp(s/self.b) for s in security_price_amount])

        CQm = self.P0*self.b*math.log(total_sum)

        return round(CQm,2)

    def n_cost_function(self,security_price_amount,amount,selected_security_number):
        selected_security_number = selected_security_number - 1
        security_price_amount[selected_security_number] += amount
        total_sum = sum([math.exp(s/self.b) for s in security_price_amount])
        CQm = self.P0*self.b*math.log(total_sum)

        return round(CQm,2)


class Participation(models.Model):
    player = models.ForeignKey(Player)
    market = models.ForeignKey(Market)
    reward_checked = models.BooleanField(default=True)

    def __unicode__(self):
        return "Player " + u'%s' % (self.player.name) + ", Market " + u'%s' % (self.market.name)

class PlayerSecurity(models.Model):
    player = models.ForeignKey(Player)
    security = models.ForeignKey(Security)
    amount = models.IntegerField()
    
    def __unicode__(self):
        return "Player " + u'%s' % (self.player.name) + ", Security " + u'%s' % (self.security.product_name)

    def can_sell(self):
        """check player can sell the security"""
        return self.amount > 0

class PlayerTransaction(models.Model):
    player = models.OneToOneField(Player)
    market = models.ForeignKey(Market,null = True)
    security_number = models.IntegerField(default = 0)
    amount = models.IntegerField(default = 0)
    action = models.CharField(max_length=10,blank =True)
    cost = models.FloatField(default = 0)

    def __unicode__(self):
        return u'%s' % (self.player.name)

class NewIdeaBox(models.Model):
    product = models.ForeignKey(Product)
    number = models.PositiveIntegerField(default=1)
    attributes = ListField()
    attribute_name = models.CharField(max_length=300,default="")
    contain_newAtt = models.BooleanField(default=False)
    newAttribute = ListField(default=[],blank=True)
    newAttribute_name = models.CharField(max_length=300,null=True,blank=True)
    newLevel = ListField(default=[],blank=True)
    newLevel_name = models.CharField(max_length=300,null=True,blank=True)
    add_market = models.BooleanField(default=False)
    accept = models.BooleanField(default=False)
    designers = models.ManyToManyField(Player, through='Designer', through_fields=('newIdea','player'))

    def __unicode__(self):
        return u'%s' % (self.attribute_name)

class Designer(models.Model):
    newIdea = models.ForeignKey(NewIdeaBox)
    player = models.ForeignKey(Player)
    checked = models.BooleanField(default=False)

    def __unicode__(self):
        return "Idea: " +u'%s' % (self.newIdea) + ", Player: " + u'%s' % (self.player)

