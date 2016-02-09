from django import template
from Market.models import Breakdown,Market,Security,LMSR,Player,Participation,PlayerTransaction,PriceHistory,Area,SecurityPrice,Attribute,Level,PlayerSecurity,PlayerResult,SecurityResult
#-*- coding: UTF-8 -*- 

register = template.Library()


@register.filter(name='LevelFilter')
def NumberFilter(queryset,number):
	return levelSet.get(number = number) 


@register.filter(name='AttributeFilter')
def AttributeFilter(queryset,attribute):
	return queryset.filter(attribute = attribute)

@register.filter(name='AttributeOrder')
def AttributeOrder(number,product):
	attribute_list = product.attribute_set.all()
	count = 0
	for order in product.order:
		if order is number:
			return attribute_list.get(number = count).name
		count = count + 1

@register.filter(name='LevelFilter')
def LevelFilter(attribute):
	return Level.objects.filter(attribute = attribute)

@register.filter(name='RewardCheckd')
def RewardCheckd(queryset,obj):
	participant = queryset.get(market = obj)
	return participant.reward_checked


@register.filter(name='MarketName')
def MarketName(obj):
	market = obj.market
	name = market.question.name
	return name

@register.filter(name='BreakdownFilter')
def BreakdownFilter(pr):
	breakdown_list = Breakdown.objects.filter(result = pr)
	return breakdown_list

@register.filter(name='StockFilter')
def StockFilter(product,player):
	ps = PlayerSecurity.objects.get(player = player,security = product)
	return ps.amount


@register.filter(name='SecurityFilter')
def SecurityFilter(ps_list,market):
	security_list = ps_list.filter(security__market = market)
	return security_list

@register.filter(name='MarketFilter')
def MarketFilter(market):
	security_list = Security.objects.filter(market = market)
	return security_list

@register.filter(name='MarketNameGet')
def MarketNameGet(market_name,player_number):
	number = player_number
	market = Market.objects.filter(market_number=number)
	return market


@register.filter(name='SecurityGet')
def SecurityGet(security,ps_list):
	try:
		ps = ps_list.get(security=security)
		return ps.amount
	except (KeyError, PlayerSecurity.DoesNotExist):
		return 0

@register.filter(name='PlayerResultCheck')
def PlayerResultCheck(market,pr_list):
	try:
		pr = pr_list.get(market=market)
		return True
	except (KeyError, pr_list.DoesNotExist):
		return False

@register.filter(name='PlayerResultFilter')
def PlayerResultFilter(market,pr_list):
	pr = pr_list.filter(market=market)
	return pr

@register.filter(name='PlayerResultFil')
def PlayerResultFil(market,pr_list):
	pr = pr_list.filter(market__name = market)
	return pr

