
# -*- encoding:utf-8 -*-

from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.helpers import ActionForm
from django.db import models
from django.forms import TextInput, Textarea
from django import forms
import datetime,time
import random
import copy
import math
import itertools
from decimal import Decimal
from django.utils import timezone
from django.db.models import Max,Min,Avg


from Market.models import Designer,NewIdeaBox,Interaction,History,ShopFigure,ShopColor,Area,Market,Level,Security,LMSR,Player,Participation,PlayerTransaction,PriceHistory,Product,SecurityPrice,Attribute,PlayerResult,SecurityResult,PlayerSecurity,NewChromosome,Breakdown,RetailStore,Owner


def GeneticNumberSetting(modeladmin,request,queryset):
	for p in queryset:
		i = 0
		for att in p.attribute_set.all():
			j = 0
			for lev in att.level_set.all():
				lev.number = j
				lev.save()
				j += 1
			att.number = i
			att.level_number = j
			att.save()
			i += 1

		p.genetic_setting = True
		p.save()

'''
a = [0,1,2,3] order[0,2,3,1] = security[0,3,1,2]
'''
def OrderDecision(modeladmin,request,queryset):
	for p in queryset:
		interactions = Interaction.objects.filter(product = p)
		if interactions.count()>0:
			attNumber = p.attribute_set.count()
			l = range(1,attNumber)
			maxValue = 0
			maxOrder = []
			orderModels = list(itertools.permutations(l,(attNumber - 1)))
			nC2 = float(len(list(itertools.combinations(range(0,attNumber),2))))
			for order in orderModels:
				seq = list(order)
				seq.insert(0,0)
				value = 0
				for interaction in p.interaction_set.all():
					i = seq[interaction.level1.attribute.number]
					j = seq[interaction.level2.attribute.number]
					if j > i:
						distance = min((j-i),(attNumber-j+i))
					else:
						distance = min((i-j),(attNumber-i+j))

					value = value + ((nC2 - distance * (attNumber - distance)) / nC2) * float(interaction.effect)

				if value > maxValue:
					maxOrder = seq
					maxValue = value

			p.order = maxOrder
			p.save()

		else:
			attNumber = p.attribute_set.count()
			maxOrder = range(0,attNumber)
			p.order = maxOrder
			p.save()


def MarketMake(modeladmin,request,queryset):
	for p in queryset:
		market = Market(product = p, open_time = p.open_time, close_time = p.close_time,name = p.name, market_number = 1)
		market.save()
		pricehistory = PriceHistory(product = p, number = 1)
		pricehistory.save()
		securityprice = SecurityPrice(market = market)
		securityprice.save()
		for i in range(0,p.security_number):
			attributes = [""] * p.attribute_set.count()
			loop = True
			while loop:
				for att in p.attribute_set.all():
					rand = random.randint(0,(att.level_set.count()-1))
					level = att.level_set.get(number = rand)
					attributes[p.order[att.number]] = level.name
				try:
					test = Security.objects.get(market=market,attributes=attributes)
					attributes = [""] * p.attribute_set.count()
				except Security.DoesNotExist:
					name = ""
					for att_name in attributes:
						name = name + " " + att_name

					security = Security(market=market,number=i)
					security.attributes = attributes
					security.attribute_name = name
					security.save()
					loop = False


def gcd(x, y):
	r = 0
	while not y == 0:
		r = x % y
		x = y
		y = r

	return x


def lcm(x, y):
	r = gcd(x, y)
	return x * y / r


def DeterminLotNumber(modeladmin,request,queryset):
	for p in queryset:
		markets = Market.objects.filter(product = p)
		for m in markets:
			all_securities = Security.objects.filter(market__product = p)
			r = 1
			for s in all_securities:
				r = lcm(r,s.selling_price)

			try:
				lmsr = LMSR.objects.get(product = p)
			except LMSR.DoesNotExist:
				lmsr = LMSR(product = p)

			lmsr.P0 = r
			lmsr.save()
			start_price = [round(lmsr.P0/p.security_number,2)] * p.security_number
			amount = [0] * p.security_number
			securityprice = SecurityPrice.objects.get(market = m)
			securityprice.price = start_price
			securityprice.amount = amount
			securityprice.save()
			data = start_price
			data.insert(0,int(time.mktime(m.open_time.timetuple())) * 1000)
			pricehistory = PriceHistory.objects.get(product = p,is_open = True)
			pricehistory.data = [data]
			pricehistory.save()
			securities = Security.objects.filter(market = m)
			for s in securities:
				s.lot = r / s.selling_price
				s.save()

		p.lot_setting = True
		p.save()


def DeterminCostPrice(modeladmin,request,queryset):
	for p in queryset:
		stock = 100000.0 / (500 * (p.security_number + 1))
		first_market = Market.objects.filter(product = p).get(market_number = 1)	
		try:
			lmsr = LMSR.objects.get(product = p)
			player_number = Participation.objects.filter(market__product = p).count()
			if Market.objects.filter(product = p).count() == 1:
				if player_number >= 20:
					'''market make'''
					new_market = Market(product = p, open_time = p.open_time, close_time = p.close_time,name = p.name, market_number = 2,name_setting = True)
					new_market.save()
					new_securityprice = SecurityPrice(market = new_market,price = [], amount = [])
					new_securityprice.save()
					new_pricehistory = PriceHistory(product = p,data = [], number = 2)
					new_pricehistory.save()
					p.market_number = 2
					for security in first_market.security_set.all():
						new_security = Security(market=new_market,product_name=security.product_name,attributes = security.attributes,attribute_name = security.attribute_name,selling_price = security.selling_price,number=security.number,gross_margin = 500)
						new_security.save()

				elif player_number > 10:
					p.player_number = player_number
					lmsr.b = stock * p.player_number / math.log((1.0 - 1.0 / p.security_number)/(1.0 - 0.99))
					lmsr.save()
				else:
					pass

			elif Market.objects.filter(product = p).count() == 2:
			 	if player_number >= 40:
			 		'''market make'''
			 		new_market = Market(product = p, open_time = p.open_time, close_time = p.close_time,name = p.name, market_number = 3,name_setting = True)
					new_market.save()
					new_securityprice = SecurityPrice(market = new_market,price = [], amount = [])
					new_securityprice.save()
					new_pricehistory = PriceHistory(product = p,data = [], number = 3)
					new_pricehistory.save()
					p.market_number = 3
					for security in first_market.security_set.all():
						new_security = Security(market=new_market,product_name=security.product_name,attributes = security.attributes,attribute_name = security.attribute_name,selling_price = security.selling_price,number=security.number,gross_margin = 500)
						new_security.save()
			 	elif player_number > 21:
			 		p.player_number = player_number
					lmsr.b = stock * p.player_number / math.log((1.0 - 1.0 / p.security_number)/(1.0 - 0.99))
					lmsr.save()
				else:
					pass

			else:
				pass

		except LMSR.DoesNotExist:
			lmsr = LMSR(product = p)
			lmsr.P0 = 500
			lmsr.b = stock * p.player_number / math.log((1.0 - 1.0 / p.security_number)/(1.0 - 0.99))
			lmsr.save()
			securities = Security.objects.filter(market = first_market)
			for s in securities:
				s.gross_margin = 500
				s.save()

		markets = Market.objects.filter(product = p)
		markets.update(open_time = p.open_time)
		markets.update(close_time = p.close_time)
		start_price = [round(lmsr.P0/p.security_number,2)] * p.security_number
		amount = [0] * p.security_number
		start_rate = [round(1.0/p.security_number*0.5+0.5,2)] * p.security_number
		data = copy.copy(start_rate)
		data.insert(0,int(time.mktime(p.open_time.timetuple())) * 1000)
		ph = PriceHistory.objects.filter(product =p,is_open = True)
		ph.update(is_open = False)
		for m in markets:
			securityprice = SecurityPrice.objects.get(market = m)
			securityprice.price = start_price
			securityprice.amount = amount
			securityprice.sale_rate = start_rate
			securityprice.save()
			pricehistory = PriceHistory(product = p,data = [data], number = m.market_number,is_open = True)
			pricehistory.save()

		p.cost_setting = True
		p.save()


def CopyMarket(modeladmin,request,queryset):
	for m in queryset:
		p = m.product
		securities = m.security_set.all()
		sp = SecurityPrice.objects.get(market = m)
		security_list = Security.objects.filter(market__product = p).exclude(market = m)
		for num in range(0,p.security_number):
			security = securities.get(number = num)
			new_securities = security_list.filter(number = num)
			new_securities.update(product_name = security.product_name)
			new_securities.update(selling_price = security.selling_price)
			new_securities.update(attributes = security.attributes)
			new_securities.update(attribute_name = security.attribute_name)
			new_securities.update(VWAP_price = 0)
			new_securities.update(VWAP_amount = 0)

def MaltipleMarketMake(modeladmin,request,queryset):
	for m in queryset:
		product = m.product
		MSP = SecurityPrice.objects.get(market = m)
		MPH = PriceHistory.objects.get(product = m.product, is_open = True)
		for i in range(2,(product.market_number+1)):
			market = Market(product = product, open_time = product.open_time, close_time = product.close_time,name = product.name, market_number = i,name_setting = True)
			market.save()
			securityprice = SecurityPrice(market = market,price = MSP.price, amount = MSP.amount)
			securityprice.save()
			pricehistory = PriceHistory(product = market.product,data = MPH.data, number = i)
			pricehistory.save()
			for security in m.security_set.all():
				new_security = Security(market=market,product_name=security.product_name,attributes = security.attributes,attribute_name = security.attribute_name,selling_price = security.selling_price,number=security.number)
				new_security.save()

		product.maltiple_market = True
		product.save()
		m.name_setting = True
		m.save()


def MarketRestart(modeladmin,request,queryset):
	for p in queryset:
		market_set = Market.objects.filter(product = p)
		market_set.update(open_time = p.open_time)
		market_set.update(close_time = p.close_time)
		market = market_set.get(market_number = 1)
		ph = PriceHistory.objects.filter(product = market.product,is_open = True)
		ph.update(is_open = False)
		sp = SecurityPrice.objects.get(market = market)
		data = copy.copy(sp.sale_rate)
		data.insert(0,int(time.mktime(p.open_time.timetuple())) * 1000)
		data = [data]
		for m in market_set:
			pricehistory = PriceHistory(product = m.product,data = data, number = m.market_number)
			pricehistory.save()



def EstimateResult(modeladmin,request,queryset):
	nowtime = timezone.now()
	for p in queryset:
		lmsr = LMSR.objects.get(product = p)
		first = True
		market_list = p.market_set.all()
		for m in market_list:
			var = 0
			nvalue = 0
			vwap = 0
			accommodate = 1
			sp = SecurityPrice.objects.get(market = m)
			for s in m.security_set.all():
				try:
					s.VWAP_price/s.VWAP_amount
					vwap += s.VWAP_price/s.VWAP_amount
				except ZeroDivisionError:
					nvalue += 1

			if nvalue > 0:
				total = lmsr.P0 - vwap
				if total > 0:
					if vwap ==0:
						nvalue = lmsr.P0/float(nvalue)
					else:
						nvalue = total/float(nvalue)

				elif total < 0:
					accommodate = lmsr.P0 / vwap
					nvalue = 0

				else:
					nvalue = 0

			else:
				total = lmsr.P0 - vwap
				if total < 0:
					accommodate = lmsr.P0 / vwap

			for s in m.security_set.all():
				if first:
						sr = SecurityResult(product = p,estimate_time = nowtime,attributes = s.attributes,attribute_name = s.attribute_name,number = var,product_name = s.product_name)
				else:
					sr = SecurityResult.objects.get(product = p,estimate_time = nowtime,attributes = s.attributes)
				try:
					sr.VWAP_result += (s.VWAP_price/s.VWAP_amount) * accommodate
					vwap += (s.VWAP_price/s.VWAP_amount) * accommodate
				except ZeroDivisionError:
					sr.VWAP_result += nvalue

				sr.last_price_result += sp.price[var]
				sr.save()
				var += 1

			first = False
					
		for sr in SecurityResult.objects.filter(product = p,estimate_time = nowtime):
			sr.VWAP_result = sr.VWAP_result/p.market_number
			sr.last_price_result = sr.last_price_result/p.market_number
			sr.GA_setting = True
			try:
				sr.sale_rate = round(sr.VWAP_result / lmsr.P0 * 0.5 + 0.5,2)
			except ZeroDivisionError:
				sr.sale_rate = 0.5

			sr.save()
			for ph in PriceHistory.objects.filter(product = p,is_open = True):
				history = History(pricehistory = ph,result = sr,estimate_time = nowtime)
				history.save()

		market_list.update(GA_setting = False)


def PayoffDecision(modeladmin,request,queryset):
	for p in queryset:
		lmsr = LMSR.objects.get(product = p)
		security_result = SecurityResult.objects.filter(product = p)
		participations = Participation.objects.filter(market__product = p).exclude(reward_checked = False)
		for participation in participations:
			player = participation.player
			player_security = PlayerSecurity.objects.filter(player = player,security__market__product =p)
			total_sale = 0
			try:
				pr = PlayerResult.objects.get(player =player,market = participation.market,estimate = False)
				for ps in player_security:
					sr = security_result.filter(number = ps.security.number).latest('estimate_time')
					pr.estimate_time = sr.estimate_time
					sales = round((ps.security.gross_margin + lmsr.P0) * ps.amount * sr.sale_rate, 2)
					player.point +=  sales 
					pr.total_sales +=  sales
					breakdown = Breakdown(result = pr, product_name = sr.product_name,attributes = sr.attributes,
						attribute_name=ps.security.attribute_name,selling_price= ps.security.selling_price,
						purchase_number = ps.amount, sale_rate = sr.sale_rate,sales = sales)
					breakdown.save()
					pr.estimate_time = sr.estimate_time

				pr.estimate = True
				total_sale = pr.total_sales + pr.returned
				try:
					pr.profit_rate = round(total_sale / pr.investment,2)
				except ZeroDivisionError:
					pr.profit_rate = 0

				player.point += 3000
				player.save()
				pr.save()
				player_security.delete()

			except PlayerResult.DoesNotExist:
				pass

		participations.update(reward_checked = False)
			

def RouletteWheelSelection(candidates, probabilities):
    rand = random.random()
    for candidate, probability in zip(candidates, probabilities):
        if rand < probability:
            return candidate

def GA(modeladmin,request,queryset):
	for p in queryset:
		lmsr = LMSR.objects.get(product = p)
		sr_list = SecurityResult.objects.filter(GA_setting = True).filter(product = p).order_by('-last_price_result')
		candidates = []
		probabilities = []
		for sr in sr_list:
			candidates.append(sr.number)
			probabilities.append(sr.last_price_result)

		probabilities = [sum(probabilities[:x+1]) for x in range(len(probabilities))]
		probabilities = [x/probabilities[-1] for x in probabilities]
		market = Market.objects.get(product = p,market_number = 1)
		securities = market.security_set.all()
		elite_number = sr_list[0].number
		elite = securities.get(number = elite_number)
		elite_chromosome = NewChromosome(product = p, attributes = elite.attributes)
		elite_chromosome.save()
		amax = len(elite.attributes) - 1
		try:
			newIdea = NewIdeaBox.objects.get(product = p,add_market = True,accept = False)
			change_number = sr_list[securities.count()-1].number
			chromosomes = market.security_set.all().exclude(number = change_number).exclude(number = elite_number)
			designers = Designer.objects.filter(newIdea = newIdea)
			for designer in designers:
				player = designer.player
				player.point = player.point + 10000
				player.save()

			idea_attributes = copy.copy(newIdea.attributes)
			for att in p.attribute_set.all():
				try:
					level = idea_attributes[p.order[att.number]]
					try:
						Level.objects.get(attribute = att,name = level)
					except Level.DoesNotExist:
						new_level = Level(attribute = att,name = level,number = att.level_set.count())
						new_level.save()
						att.level_number += 1
						att.save()
				except IndexError:
					level = Level.objects.get(attribute = att,name = u"なし")
					idea_attributes.append(level.name)

			if newIdea.contain_newAtt:
				count = 0
				for new_att in newIdea.newAttribute:
					idea_attributes.append(newIdea.newLevel[count])
					new_attribute = Attribute(product = p,name = new_att,number = p.attribute_set.count(),level_number = 2)
					new_attribute.save()
					new_level = Level(attribute = new_attribute,name = newIdea.newLevel[count], number = 0)
					new_level.save()
					non_level = Level(attribute = new_attribute,name = u"なし",number = 1)
					non_level.save()
					p.order.append(amax + count + 1)
					p.save()
					elite_chromosome.attributes.append(u"なし")
					elite_chromosome.save()
					for chromosome in chromosomes:
						chromosome.attributes.append(u"なし")
						chromosome.save()

					for security in securities:
						security.attributes.append(u"なし")
						security.save()
						
					count = count + 1

			else:
				pass

			new_chromosome = NewChromosome(product = p, attributes = idea_attributes)
			new_chromosome.save()
			newIdea.accept = True
			newIdea.add_market = False
			newIdea.save()

		except NewIdeaBox.DoesNotExist:
			chromosomes = market.security_set.all().exclude(number = elite_number)

		for c in chromosomes:
			check = True
			att = copy.copy(c.attributes)
			mutation = random.random()

			while check:
				if mutation <= 0.1:
					target = random.randint(0,amax)
					target_att = Attribute.objects.get(product = p,number = target)
					point = random.randint(0,(target_att.level_number-1))
					att[p.order[target]] = Level.objects.get(attribute = target_att,number = point).name	
				else:
					target = RouletteWheelSelection(candidates, probabilities)
					point1 = random.randint(0,amax)
					point2 = random.randint(0,amax)
					if point1 > point2:
						point = point1
						point1 = point2
						point2 = point
					att[point1:point2] =  securities.get(number = target).attributes[point1:point2]
				try:
					NewChromosome.objects.get(attributes = att)
				except NewChromosome.DoesNotExist:
					new_chromosome = NewChromosome(product = p, attributes = att)
					new_chromosome.save()
					check = False

		new_securities = NewChromosome.objects.filter(product = p)
		var = 0
		for ns in new_securities:
			security = securities.get(number = var)
			security.attributes = ns.attributes
			name = ""
			for att_name in ns.attributes:
				name = name + " " + att_name
			security.attribute_name = name
			security.VWAP_price = 0
			security.VWAP_amount = 0
			security.selling_price = 0
			security.save()
			var += 1

		new_securities.delete()
		start_price = [round(lmsr.P0/p.security_number,2)] * p.security_number
		amount = [0] * p.security_number
		sp = SecurityPrice.objects.get(market = market)
		sp.price = start_price
		sp.amount = amount
		sp.save()
		market.GA_setting = False
		market.save()
		sr_list.update(GA_setting = False)

def QuestionnaireSetting(modeladmin,request,queryset):
	queryset.update(is_answered = False)

def DrawPriceHistory(modeladmin,request,queryset):
	import pyper as pr
	import pandas as pd
	r = pr.R(use_pandas = "True")
	for p in queryset:
		r.assign("Title",p.name)
		r("pdf('data.pdf')")
		r("par(mfrow=c(4,3))")
		for count, pr in enumerate(PriceHistory.objects.filter(product = p)):
			r("A<-c()")
			r("B<-c()")
			r("C<-c()")
			r("D<-c()")
			r("E<-c()")
			r("EF<-c()")
			r("G<-c()")
			r("H<-c()")
			r("I<-c()")
			r("J<-c()")
			for price in pr.data:
				r.assign("price",price[1])
				r("A<-append(A,price)")
				r.assign("price",price[2])
				r("B<-append(B,price)")
				r.assign("price",price[3])
				r("C<-append(C,price)")
				r.assign("price",price[4])
				r("D<-append(D,price)")
				r.assign("price",price[5])
				r("E<-append(E,price)")
				r.assign("price",price[6])
				r("EF<-append(EF,price)")
				r.assign("price",price[7])
				r("G<-append(G,price)")
				r.assign("price",price[8])
				r("H<-append(H,price)")
				r.assign("price",price[9])
				r("I<-append(I,price)")
				r.assign("price",price[10])
				r("J<-append(J,price)")

			r.assign("title","term:"+str(count+1))
			r("plot(A,type='b',main=title,col='red',xlab='',ylab='',ylim=c(0.4,0.8))")
			r("par(new=T)")
			r("plot(B,type='b',col='blue',ann=F,ylim=c(0.4,0.8))")
			r("par(new=T)")
			r("plot(C,type='b',col='green',ann=F,ylim=c(0.4,0.8))")
			r("par(new=T)")
			r("plot(D,type='b',col='pink',ann=F,ylim=c(0.4,0.8))")
			r("par(new=T)")
			r("plot(E,type='b',col='purple,ann=F,ylim=c(0.4,0.8)')")
			r("par(new=T)")
			r("plot(EF,type='b',col='yellow',ann=F,ylim=c(0.4,0.8))")
			r("par(new=T)")
			r("plot(G,type='b',col='orange',ann=F,ylim=c(0.4,0.8))")
			r("par(new=T)")
			r("plot(H,type='b',col='greenyellow',ann=F,ylim=c(0.4,0.8))")
			r("par(new=T)")
			r("plot(I,type='b',col='cyan',ann=F,ylim=c(0.4,0.8))")
			r("par(new=T)")
			r("plot(J,type='b',col='sienna',ann=F,ylim=c(0.4,0.8))")

		r("legend('topright',inset=.05,c('A','B','C','D','E','EF','G','H','I','J'),fill=c('red','blue','green','pink','purple','yellow','orange','greenyellow','cyan','sienna'),horiz=True)")
		r("dev.off()")

GeneticNumberSetting.short_description = "Setting Genetic number"
MarketMake.short_description = "Make Market"
MaltipleMarketMake.short_description = "Make Maltiple Market" 
MarketRestart.short_description = "Restart Markets"
EstimateResult.short_description = "Estimate Result"
PayoffDecision.short_description = "Decide Payoff"
GA.short_description = "GA"
CopyMarket.short_description = "Copy Market"
DeterminCostPrice.short_description = "Determin Cost Price"
OrderDecision.short_description = "Decide Order"
QuestionnaireSetting.short_description = "Setting Questionnaire"
DrawPriceHistory.short_description = "Draw PriceHistory"

class AreaAdmin(admin.ModelAdmin):
	fieldsets = [
		('Name',               {'fields': ['name']}),
		('Gender',               {'fields': ['gender']}),
		('Gender Image',               {'fields': ['gender_img_url']}),
		('Lower Age',               {'fields': ['age_lower']}),
		('Upper Age',               {'fields': ['age_upper']}),
		('Attribute',               {'fields': ['attribute']}),
		('Description',               {'fields': ['description']}),
	]
	list_display=('name','gender','age_lower','age_upper','attribute')

class SecurityResultAdmin(admin.ModelAdmin):
	fieldsets = [
		('attributes',               {'fields': ['attribute_name']}),
		('number',               {'fields': ['number']}),
		('last price result',               {'fields': ['last_price_result']}),
		('VWAP result',               {'fields': ['VWAP_result']}),
		('GA setting',               {'fields': ['GA_setting']}),
	]
	list_display=('attribute_name','last_price_result','VWAP_result','estimate_time','number','GA_setting')


class NewChromosomeAdmin(admin.ModelAdmin):
	fieldsets = [
		('attributes',               {'fields': ['attributes']}),
	]

class ShopColorInline(admin.TabularInline):
	model = ShopFigure.color.through
	readonly_fields = ['color_name']
	def color_name(self, instance):
		return instance.color.name
	color_name.short_description = 'color name'


class ShopColorAdmin(admin.ModelAdmin):
	fieldsets = [
		('name',               {'fields': ['name']}),
		('url',               {'fields': ['img_url']}),
	]

class ShopFigureAdmin(admin.ModelAdmin):
	fieldsets = [
		('name',               {'fields': ['name']}),
		('img_url',               {'fields': ['img_url']}),
	]
	inlines = [ShopColorInline]
	exclude = ('color',)

class LevelInline(admin.TabularInline):
	model = Level
	extra = 0

class AttributeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Product',               {'fields': ['product']}),
		(None,               {'fields': ['name']}),
	]
	inlines = [LevelInline]
	list_display=('name','product')


class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 0

class SecurityAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,		{'fields':['product_name']}),
		('attributes',		{'fields':['attribute_name']}),
		('number',		{'fields':['number']}),
		]
	list_display=('product_name','market','attribute_name','VWAP_price')

class MarketInline(admin.StackedInline):
	model = Market
	extra = 0

class LMSRInline(admin.TabularInline):
	model = LMSR
	extra = 0

class InteractionInline(admin.TabularInline):
	model = Interaction
	extra = 0

class ProductAdmin(admin.ModelAdmin):
	fieldsets = [
		('Area',               {'fields': ['area']}),
        ('Name',               {'fields': ['name']}),
        ('Market Number', {'fields': ['market_number']}),
        ('Player Number', {'fields': ['player_number']}),
        ('Order', {'fields': ['order']}),
        ('Security Number', {'fields': ['security_number']}),
        ('Create Idea', {'fields': ['create_idea']}),
        ('Start information', {'fields': ['start_time'], 'classes': ['collapse']}),
        ('end information', {'fields': ['end_time'], 'classes': ['collapse']}),
        ('Open information', {'fields': ['open_time'], 'classes': ['collapse']}),
        ('Close information', {'fields': ['close_time'], 'classes': ['collapse']}),
    ]
	inlines = [AttributeInline,InteractionInline,MarketInline,LMSRInline]
	actions = [DrawPriceHistory,GeneticNumberSetting,OrderDecision,MarketMake,DeterminCostPrice,MarketRestart,EstimateResult,PayoffDecision,GA]
	list_display = ('name', 'area','close_time','genetic_setting','maltiple_market','cost_setting')
	list_filter = ['close_time']


class SecurityInline(admin.TabularInline):
    model = Security
    extra = 0

class SecurityPriceInline(admin.TabularInline):
	model = SecurityPrice
	extra = 0


class MarketAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',               {'fields': ['name']}),
        ('Market number',               {'fields': ['market_number']}),
        ('Reward Setting',               {'fields': ['reward_setting']}),
        ('GA setting',               {'fields': ['GA_setting']}),
        ('Name setting',               {'fields': ['name_setting']})
    ]
    inlines = [SecurityInline,SecurityPriceInline]
    actions = [MaltipleMarketMake,CopyMarket]
    list_display = ('name','market_number','trade_amount','GA_setting','name_setting')

class LMSRAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['b']}),
        (None,               {'fields': ['P0']}),
    ]
    list_display = ('b', 'P0')

class PlayerTransactionInline(admin.TabularInline):
    model = PlayerTransaction
    extra = 3

class PlayerResultInline(admin.TabularInline):
    model = PlayerResult
    extra = 0

class PlayerSecurityInline(admin.TabularInline):
	model = PlayerSecurity
	extra = 0

class RetailStoreInline(admin.TabularInline):
	model = RetailStore
	extra = 0

class OwnerInline(admin.TabularInline):
	model = Owner
	extra = 0

class ParticipationInline(admin.TabularInline):
	model = Participation
	extra = 0

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',               {'fields': ['name']}),
        ('Point',               {'fields': ['point']}),
        ('Age',               {'fields': ['age']}),
        ('Gender',               {'fields': ['gender']}),
        ('email',               {'fields': ['email']}),
        ('is_answered',               {'fields': ['is_answered']}),
    ]
    inlines = [ParticipationInline,PlayerResultInline,PlayerSecurityInline,PlayerTransactionInline,RetailStoreInline,OwnerInline]
    actions = [QuestionnaireSetting]
    list_display = ('name', 'point','is_answered')

class SecurityPriceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Price',               {'fields': ['price']}),
    ]
    display = ('name')

class SecurityPriceInline(admin.StackedInline):
	model = SecurityPrice
	extra = 0

class HistoryInline(admin.TabularInline):
	model = History
	extra = 0

class PriceHistoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('product',               {'fields': ['product']}),
        ('data',               {'fields': ['data']}),
        ('open',               {'fields': ['is_open']}),
    ]

class BreakdownAdmin(admin.ModelAdmin):
    fieldsets = [
	    ('PlayerResult',               {'fields': ['result']}),
        ('product_name',               {'fields': ['product_name']}),
        ('sell price',               {'fields': ['selling_price']}),
        ('attributes',               {'fields': ['attribute_name']}),
        ('purchase number',               {'fields': ['purchase_number']}),
        ('sale rate',               {'fields': ['sale_rate']}),
    	('sales',               {'fields': ['sales']})
    ]

class HistoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('product',               {'fields': ['pricehistory']}),
        ('data',               {'fields': ['data']}),
    ]

class DesignerInline(admin.TabularInline):
	model = Designer
	extra = 0


class NewIdeaBoxAdmin(admin.ModelAdmin):
    fieldsets = [
        ('product',               {'fields': ['product']}),
        ('number',               {'fields': ['number']}),
        ('new attribute',               {'fields': ['attribute_name']}),
        ('new attribute',               {'fields': ['newAttribute']}),
        ('new level',               {'fields': ['newLevel_name']}),
        ('add_market',               {'fields': ['add_market']}),
        ('attributes',               {'fields': ['attributes']}),
        ('accept',               {'fields': ['accept']}),
        ('contain newAtt',               {'fields': ['contain_newAtt']})
    ]
    list_display = ('product','number', 'attribute_name','add_market','accept')
    inlines = [DesignerInline]


admin.site.register(Area, AreaAdmin)
admin.site.register(NewIdeaBox,NewIdeaBoxAdmin)
admin.site.register(Market, MarketAdmin)
admin.site.register(SecurityResult,SecurityResultAdmin)
admin.site.register(Security,SecurityAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(SecurityPrice, SecurityPriceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(LMSR,LMSRAdmin)
admin.site.register(Player,PlayerAdmin)
admin.site.register(PriceHistory,PriceHistoryAdmin)
admin.site.register(NewChromosome,NewChromosomeAdmin)
admin.site.register(Breakdown,BreakdownAdmin)
admin.site.register(ShopFigure,ShopFigureAdmin)
admin.site.register(ShopColor,ShopColorAdmin)