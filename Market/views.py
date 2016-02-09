from django.shortcuts import render,get_object_or_404, render_to_response ,render, redirect
from Market.models import Designer,NewIdeaBox,ShopFigure,ShopColor,Owner,RetailStore,Area,Market,Security,LMSR,Player,Participation,PlayerTransaction,PriceHistory,Product,SecurityPrice,Attribute,Level,PlayerSecurity,PlayerResult,SecurityResult,PlayerSecurity,Breakdown
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext, Context,loader
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from .forms import NewLevelForm,CreateNewUserForm,LoginForm,CreateRetailStoreNameForm,TransactionForm,CreateNewIdeaForm
from django.contrib.auth.models import User
from decimal import Decimal
from json import dumps
import sys
import datetime,time
import copy
from django.views import generic
from django.utils import timezone
from scipy.stats import norm
import math
import os
import binascii
import random

def createNewUser(request):
    form = CreateNewUserForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password1 = form.cleaned_data["password1"]
        email = form.cleaned_data["email"]
        age = form.cleaned_data['age']
        gender = form.cleaned_data['gender']
        user = User.objects.create_user(username=username)
        user.set_password(password1)
        player = Player(user=user, name=username,age=age,gender=gender,point=100000,email = email)
        player.save()
        user.save()
        p = PlayerTransaction(player=player)
        p.save()
        return render(request, "Market/create_new_user_successful.html")
    return render(request, "Market/create_new_user.html", {"form": form})

def login_success(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse("Inactive Account")
        elif user.is_active:
            login(request, user)
            return render(request,'Market/login_success.html/')
        else:
            return HttpResponse("Inactive Account")

    return render(request, "Market/login.html", {"form": form})


@login_required(login_url='/Top/')
def questionnaire_answ(request):
    player = Player.objects.get(id=request.user.player.id)
    player.point += 1000
    player.save()            
    return render_to_response('Market/questionnaire_answer.html',{'back_url':"/market/mypage/"})

@login_required(login_url='/Top/')
def mypage(request):
    my_player = Player.objects.get(id=request.user.player.id)
    if my_player.is_answered==False:
        my_player.is_answered = True
        my_player.save()
        return render(request, "Market/questionnaire.html",{'back_url':"/market/mypage/","link":"/market/questionnaire_answ"})
    else:
        players = Player.objects.order_by('-point')
        current_rank = 0
        counter = 0
        rank = 0
        for player in players:
            if counter < 1:
                current_rank += 1
                counter += 1
            elif player.point is players[counter - 1].point:
                counter += 1
            else:
                current_rank = counter + 1
                counter += 1
            if player.point == my_player.point:
                rank = current_rank
                break
                
        return render_to_response('Market/mypage.html',{'player':my_player,'rank':rank,'total':players.count()},context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def mypage_tutorial(request):
    return render_to_response('Market/mypage_tutorial.html',context_instance=RequestContext(request))


@login_required(login_url='/Top/')
def history(request):
    player = Player.objects.get(id=request.user.player.id)
    rs_list = RetailStore.objects.filter(player = player)
    if rs_list:
        return render(request,'Market/history.html',{'player': player,'rs_list':rs_list})
    else:
        return render_to_response('Market/error.html', {'error_message': "No shops are available",'back_url':"/market/mypage/"},
            context_instance=RequestContext(request))


@login_required(login_url='/Top/')
def open(request):
    player = Player.objects.get(id=request.user.player.id)
    new_areas = Area.objects.exclude(owners = player)
    if new_areas:
        return render(request,'Market/open.html',{'player': player,'new_areas':new_areas})
    else:
        return render_to_response('Market/error.html', {'error_message': "No areas are available",'back_url':"/market/mypage/"},
            context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def choice_shop(request,area_id):
    shop_list = ShopFigure.objects.all()
    area = Area.objects.get(id = area_id)
    return render(request,'Market/choice_shop.html',{'shop_list': shop_list,'area':area})

@login_required(login_url='/Top/')
def choice_color(request,area_id,shop_id):
    area = Area.objects.get(id = area_id)
    shop = ShopFigure.objects.get(id = shop_id)
    colors = ShopColor.objects.all()
    return render(request,'Market/choice_color.html',{'shop': shop,'area':area,'colors':colors})

@login_required(login_url='/Top/')
def give_name(request,area_id,shop_id,color_id):
    area = Area.objects.get(id = area_id)
    shop = ShopFigure.objects.get(id = shop_id)
    color = ShopColor.objects.get(id = color_id)
    return render(request,'Market/give_name.html',{'shop': shop,'area':area,'color':color})

@login_required(login_url='/Top/')
def open_success(request,area_id,shop_id,color_id):
    player = Player.objects.get(id=request.user.player.id)
    form = CreateRetailStoreNameForm(request.POST)
    area = Area.objects.get(id = area_id)
    shop = ShopFigure.objects.get(id = shop_id)
    color = ShopColor.objects.get(id = color_id)
    if form.is_valid():
        name = form.cleaned_data["name"]
        owner = Owner(player = player,area = area)
        owner.save()
        try:
            new_store = RetailStore.objects.get(player = player, area = area)
            return render_to_response('Market/open_success.html', 
                {'shop': new_store.figure,'area':area,'color':new_store.color,'new_store':new_store,
                'error_message': "You already open this shop !",}, 
                context_instance=RequestContext(request))
        except (KeyError, RetailStore.DoesNotExist):
            new_store = RetailStore(player = player, area = area, name = name,figure = shop, color = color)
            new_store.save()
            return render(request,'Market/open_success.html',{'shop': shop,'area':area,'color':color,'new_store':new_store})

    return render(request, "Market/give_name.html", {"form": form,'shop': shop,'area':area,'color':color})

@login_required(login_url='/Top/')
def RetailStore_detail(request):
    player = Player.objects.get(id=request.user.player.id)
    rs_detail = RetailStore.objects.filter(player = player)
    if rs_detail:
        return render(request,'Market/RetailStore_detail.html',{'player': player,'rs_detail':rs_detail})
    else:
        return render_to_response('Market/error.html', {'error_message': "No Shops are available",'back_url':"/market/mypage/"},
            context_instance=RequestContext(request))


@login_required(login_url='/Top/')
def RetailStore_page(request,rs_id):
    player = Player.objects.get(id=request.user.player.id)
    if player.is_answered==False:
        player.is_answered = True
        player.save()
        return render(request, "Market/questionnaire.html",{'back_url':"/market/"+rs_id+"/RetailStore_page/","link":"/market/"+rs_id+"/questionnaire_answer"})

    rs = RetailStore.objects.get(id = rs_id)
    return render(request,'Market/RetailStore_page.html',{'player': player,'rs':rs})    

@login_required(login_url='/Top/')
def shoppage_tutorial(request,rs_id):
    rs = RetailStore.objects.get(id = rs_id)
    return render(request,'Market/shoppage_tutorial.html',{'rs':rs})

@login_required(login_url='/Top/')
def accountant(request,rs_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    product_list = Product.objects.filter(area = rs.area)
    pr_list = PlayerResult.objects.filter(player = player,market__product__area = rs.area,estimate = True,checked = True)
    if pr_list:
        return render(request,'Market/accountant.html',{'product_list':product_list,'player': player,'rs':rs,'pr_list':pr_list})
    else:
        return render_to_response('Market/error.html', {'error_message': "No accountants are available",'back_url':"/market/" + rs_id + "/RetailStore_page/"},
            context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def accountant_table(request,rs_id,product_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    product = Product.objects.get(id = product_id)
    pr_list = PlayerResult.objects.filter(player = player,market__product = product,estimate = True,checked = True)
    if pr_list:
        return render(request,'Market/accountant_table.html',{'rs': rs,'product':product,'pr_list':pr_list})
    else:
        return render(request,'Market/accountant_table.html',{'error_message':"error"})

@login_required(login_url='/Top/')
def breakdown(request,rs_id,product_id,pr_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    product = Product.objects.get(id = product_id)
    pr = PlayerResult.objects.get(id = pr_id)
    breakdowns = Breakdown.objects.filter(result = pr)
    return render(request,'Market/breakdown.html',{'rs': rs,'product':product,'breakdowns':breakdowns})

@login_required(login_url='/Top/')
def new_market(request,rs_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    participation_list = Participation.objects.filter(player = player)
    market_list = Market.objects.filter(product__area = rs.area).filter(market_number = 1)
    for participate in participation_list:
        market_list = market_list.exclude(product = participate.market.product)

    if market_list:
        return render_to_response('Market/new_market.html', {'market_list': market_list,'rs':rs},context_instance=RequestContext(request))
    else:
        return render_to_response('Market/error.html', {'error_message': "No categories are available",'back_url':"/market/" + rs_id + "/RetailStore_page/"},
            context_instance=RequestContext(request))

   

@login_required(login_url='/Top/')
def participate_market(request, rs_id,market_id):
    player = Player.objects.get(id=request.user.player.id)
    market = get_object_or_404(Market, pk=market_id)
    new_market_number = random.randint(1,market.product.market_number)
    new_market = Market.objects.get(product = market.product,market_number = new_market_number)
    securities = Security.objects.filter(market = new_market)
    rs = RetailStore.objects.get(id = rs_id)
    try:
        pr = PlayerResult.objects.get(player =player,market = market,estimate = True,checked=False)
        pr.checked = True
        pr.save()
        try:
            PlayerResult.objects.get(player =player,market__product = market.product,estimate = False,checked=False)
        except PlayerResult.DoesNotExist:
            new_pr = PlayerResult(player =player,market = new_market,estimate_time = timezone.now())
            new_pr.save()
    except PlayerResult.DoesNotExist:
        try:
            PlayerResult.objects.get(player =player,market__product = market.product,estimate = False,checked=False)
        except PlayerResult.DoesNotExist:
            new_pr = PlayerResult(player =player,market = new_market,estimate_time = timezone.now())
            new_pr.save()

    try:
        participation = Participation.objects.get(market = market, player = player)
        participation.reward_checked = True
        participation.market = new_market
        participation.save()
    except Participation.DoesNotExist:
        participation = Participation(market = new_market, player = player)
        participation.save()

    for security in securities:
        try:
            PlayerSecurity.objects.get(player = player,security = security)
        except PlayerSecurity.DoesNotExist:
            ps = PlayerSecurity(player = player,security = security,amount = 0)
            ps.save()

    designers = Designer.objects.filter(player = player,newIdea__accept = True,newIdea__product = market.product,checked = False)
    if designers.count()>0:        
        point = 10000 * designers.count()
        designers.update(checked=True)
        return render_to_response('Market/accept_idea.html', {'market': new_market,'rs':rs,'designers':designers,'point':point},
            context_instance=RequestContext(request))
    else:
        return render_to_response('Market/participate_market.html', {'market': new_market,'rs':rs},context_instance=RequestContext(request))


@login_required(login_url='/Top/')
def shop_lines(request,rs_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    player_market = Market.objects.filter(participations = player).filter(product__area = rs.area)
    if player_market:
        ps_list = PlayerSecurity.objects.filter(player=player,security__market=player_market)
        participation = Participation.objects.filter(player = player)

        return render_to_response('Market/shop_lines.html', {
            'rs':rs,'market_list': player_market,'ps_list':ps_list,'participation':participation},
            context_instance=RequestContext(request))

    else:
        return render_to_response('Market/error.html', {'error_message': "No products are available",'back_url':"/market/" + rs_id + "/RetailStore_page/"},
            context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def index(request,rs_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    player_market = Market.objects.filter(participations = player)
    if player_market:
        open_market_list = player_market.filter(close_time__gt = timezone.now())
        close_market_list = player_market.filter(close_time__lte = timezone.now())
        end_market_list = player_market.filter(product__end_time__lte = timezone.now())
        participation = Participation.objects.filter(player = player)

        return render_to_response('Market/index.html', {
            'rs':rs,'participation':participation,'open_market_list': open_market_list,'close_market_list': close_market_list,
            'end_market_list': end_market_list},
            context_instance=RequestContext(request))

    else:
        return render_to_response('Market/error.html', {'error_message': "No products are available",'back_url':"/market/" + rs_id + "/RetailStore_page/"},
            context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def stock(request,rs_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    player_market = Market.objects.filter(participations = player).filter(product__area = rs.area)
    if player_market:
        open_market_list = player_market.filter(close_time__gt = timezone.now())
        close_market_list = player_market.filter(close_time__lte = timezone.now())
        end_market_list = player_market.filter(product__end_time__lte = timezone.now())
        participation = Participation.objects.filter(player = player)

        return render_to_response('Market/stock.html', {
            'rs':rs,'participation':participation,'open_market_list': open_market_list,'close_market_list': close_market_list,
            'end_market_list': end_market_list},
            context_instance=RequestContext(request))

    else:
        return render_to_response('Market/error.html', {'error_message': "No Markets are available",'back_url':"/market/" + rs_id + "/RetailStore_page/"},
            context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def create(request,rs_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    participation = Participation.objects.filter(player = player)
    create_market_list = Market.objects.filter(participations = player).filter(close_time__gt = timezone.now()).filter(product__create_idea = True).filter(product__area = rs.area)
    if create_market_list:
        return render_to_response('Market/create.html', {
            'rs':rs,'participation':participation,'create_market_list': create_market_list},
            context_instance=RequestContext(request))

    else:
        return render_to_response('Market/error.html', {'error_message': "No Markets are available",'back_url':"/market/" + rs_id + "/RetailStore_page/"},
            context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def create_products(request,rs_id,market_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    market = Market.objects.get(id=market_id)
    area = market.product.area
    security = Security.objects.filter(market=market)
    attribute_list = Attribute.objects.filter(product = market.product)

    return render_to_response('Market/create_products.html', {
        'area':area,'rs':rs,'market':market,'attribute_list': attribute_list,'security':security,'player':player},
        context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def ideaBox_tutorial(request,rs_id,market_id):
    rs = RetailStore.objects.get(id = rs_id)
    market = Market.objects.get(id=market_id)
    return render_to_response('Market/ideaBox_tutorial.html', {'rs':rs,'market':market},context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def created(request,rs_id,market_id):
    player = Player.objects.get(id=request.user.player.id)
    rs = RetailStore.objects.get(id = rs_id)
    market = Market.objects.get(id=market_id)
    area = market.product.area
    security = Security.objects.filter(market=market)
    order_levels = request.POST.getlist('levels')
    attributes = [""] * len(order_levels)
    levels = [""] * len(order_levels)
    attribute_list = Attribute.objects.filter(product = market.product)

    if player.point < 500:
        return render_to_response('Market/create_products.html', {'error_message':"money_error",
            'area':area,'rs':rs,'market':market,'attribute_list': attribute_list,'security':security,'player':player},
            context_instance=RequestContext(request))

    for att in attribute_list:
        attributes[market.product.order[att.number]] = att.name
        levels[market.product.order[att.number]] = order_levels[att.number]
    
    newAttributes = request.POST.getlist('NewAtt')
    newLevels = request.POST.getlist('NewLevel')

    if(len(newAttributes) > 0 and len(newLevels) > 0):
        for i in range(0,len(newAttributes)):
            if(newAttributes[i] == "" and  not newLevels[i] == ""):
                return render_to_response('Market/create_products.html', {'error_message':"error1",
                'area':area,'rs':rs,'market':market,'attribute_list': attribute_list,'security':security,'player':player},
                context_instance=RequestContext(request))

            elif(not newAttributes[i] == "" and newLevels[i] == ""):
                return render_to_response('Market/create_products.html', {'error_message':"error1",
                    'area':area,'rs':rs,'market':market,'attribute_list': attribute_list,'security':security,'player':player},
                    context_instance=RequestContext(request))

            else:
                try:
                    Attribute.objects.get(product = market.product,name = newAttributes[i])
                    return render_to_response('Market/create_products.html', {'error_message':"error4",
                        'area':area,'rs':rs,'market':market,'attribute_list': attribute_list,'security':security,'player':player},
                        context_instance=RequestContext(request))
                except (KeyError, Attribute.DoesNotExist):
                    pass
      
        try:
            newIdea = NewIdeaBox.objects.get(product = market.product,contain_newAtt = True,attributes = levels,
                newAttribute = newAttributes,newLevel = newLevels)
            try:
                designer = Designer.objects.get(player = player,newIdea = newIdea)
                return render_to_response('Market/create_products.html', {'error_message':"error3",
                    'area':area,'rs':rs,'market':market,'attribute_list': attribute_list,'security':security,'player':player},
                    context_instance=RequestContext(request))
            except (KeyError, Designer.DoesNotExist):
                designer = Designer(player = player,newIdea = newIdea)
                designer.save()
                newIdea.number = newIdea.number + 1
                newIdea.save()
                name = ""
                for i in range(0,len(newAttributes)):
                    attributes.append(newAttributes[i])
                    levels.append(newLevels[i])
                player.point = player.point - 500
                player.save()
                return render_to_response('Market/created.html', {'rs':rs,'market':market,'attributes':attributes,'levels':levels},
                    context_instance=RequestContext(request))
        except (KeyError, NewIdeaBox.DoesNotExist):
            name = ""
            for level in levels:
                name = name + " " + level
            attName = ""
            levelName = ""
            for i in range(0,len(newAttributes)):
                attName = attName + " " + newAttributes[i]
                levelName = levelName + " " + newLevels[i]
            name = name + " " + levelName
            newIdea = NewIdeaBox(product = market.product,contain_newAtt = True,attributes = levels,attribute_name = name,
                newAttribute=newAttributes,newLevel = newLevels,newAttribute_name=attName,newLevel_name=levelName)
            newIdea.save()
            designer = Designer(player = player,newIdea = newIdea)
            designer.save()
            for i in range(0,len(newAttributes)):
                attributes.append(newAttributes[i])
                levels.append(newLevels[i])
            player.point = player.point - 500
            player.save()
            return render_to_response('Market/created.html', {'rs':rs,'market':market,'attributes':attributes,'levels':levels},
            context_instance=RequestContext(request))

    else:
        try:
            Security.objects.get(market = market, attributes = levels)
            return render_to_response('Market/create_products.html', {'error_message':"error2",
                        'area':area,'rs':rs,'market':market,'attribute_list': attribute_list,'security':security,'player':player},
                        context_instance=RequestContext(request))
        except (KeyError, Security.DoesNotExist):
            try:
                newIdea = NewIdeaBox.objects.get(product = market.product, attributes = levels)
                try:
                    designer = Designer.objects.get(player = player,newIdea = newIdea)
                    return render_to_response('Market/create_products.html', {'error_message':"error3",
                        'area':area,'rs':rs,'market':market,'attribute_list': attribute_list,'security':security,'player':player},
                        context_instance=RequestContext(request))
                except (KeyError, Designer.DoesNotExist):
                    designer = Designer(player = player,newIdea = newIdea)
                    designer.save()
                    newIdea.number = newIdea.number + 1
                    newIdea.save()
                    player.point = player.point - 500
                    player.save()
                    return render_to_response('Market/created.html', {'rs':rs,'market':market,'attributes':attributes,'levels':levels},
                        context_instance=RequestContext(request))
            except (KeyError, NewIdeaBox.DoesNotExist):
                name = ""
                for level in levels:
                    name = name + " " + level
                newIdea = NewIdeaBox(product = market.product, attributes = levels, attribute_name = name)
                newIdea.save()
                designer = Designer(player = player,newIdea = newIdea)
                designer.save()
                player.point = player.point - 500
                player.save()
                return render_to_response('Market/created.html', {'rs':rs,'market':market,'attributes':attributes,'levels':levels},
                context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def check_reward(request,rs_id,market_id):
    player = Player.objects.get(id=request.user.player.id)
    market = get_object_or_404(Market, pk=market_id)
    rs = RetailStore.objects.get(id = rs_id)
    pr = PlayerResult.objects.get(player = player,checked = False,market = market)
    breakdown = Breakdown.objects.filter(result = pr)

    return render_to_response('Market/check_reward.html', {'market':market,'rs':rs,'pr':pr,'breakdown': breakdown},
        context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def check_reward_end(request,rs_id,market_id):
    player = Player.objects.get(id=request.user.player.id)
    market = get_object_or_404(Market, pk=market_id)
    rs = RetailStore.objects.get(id = rs_id)
    pr = PlayerResult.objects.get(player = player,checked = False,market = market)
    breakdown = Breakdown.objects.filter(result = pr)
    pr = PlayerResult.objects.get(player =player,market = market,estimate = True,checked=False)
    pr.checked = True
    pr.save()
    participation = Participation.objects.get(market = market, player = player)
    participation.reward_checked = True
    participation.save()

    return render_to_response('Market/check_reward_end.html', {'market':market,'rs':rs,'pr':pr,'breakdown': breakdown},
        context_instance=RequestContext(request))


@login_required(login_url='/Top/')
def dropout(request,market_id):
    player = Player.objects.get(id=request.user.player.id)
    market = get_object_or_404(Market, pk=market_id)
    pr = PlayerResult.objects.get(player = player,checked = False,market = market)
    pr.checked = True
    pr.save()
    participation = Participation.objects.get(player = player,market = market)
    participation.delete()

    return render_to_response('Market/dropout.html', {'market':market},context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def market_tutorial(request, rs_id, market_id):
    market = get_object_or_404(Market, pk=market_id)
    rs = RetailStore.objects.get(id = rs_id)
    return render_to_response('Market/market_tutorial.html',{'market':market,'rs':rs},context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def detail(request, rs_id, market_id):
    player = Player.objects.get(id=request.user.player.id)
    market = get_object_or_404(Market, pk=market_id)
    rs = RetailStore.objects.get(id = rs_id)
    product = market.product
    if market.is_closed() == True:
        return render_to_response('Market/market_end.html', {'rs':rs},
            context_instance=RequestContext(request))
        return HttpResponse("This market is closed")
    else:
        lmsr = get_object_or_404(LMSR, product = product)
        security = market.security_set.all()
        attribute_list = Attribute.objects.filter(product = market.product)
        history = []

        data = SecurityPrice.objects.get(market = market).sale_rate
        price = SecurityPrice.objects.get(market = market).price

        name_list = [s.product_name.encode('utf-8') for s in security]
        namedata = [binascii.b2a_hex(name) for name in name_list]

        nowdata = (copy.copy(data))
        nowtime = int(time.mktime(timezone.now().timetuple())) * 1000
        nowdata.insert(0,nowtime)

        ph = PriceHistory.objects.get(product = product,number = market.market_number, is_open = True)
        ph.data.append(nowdata)
        ph.save()
   
        history = copy.copy(ph.data)
    
        data = dumps(data)
        history = dumps(history)
        ctime = int(time.mktime(market.close_time.timetuple())) * 1000
        stime = int(time.mktime(market.open_time.timetuple())) * 1000

        fmt = '%Y-%m-%d %H:%M:%S'
        close_time = market.close_time.strftime(fmt)
        end_time = product.end_time.strftime(fmt)


    return render_to_response('Market/detail.html', {
                    'security_number':security.count(),'rs':rs,'P0':lmsr.P0,'player':player,'close_time':close_time,'security':security,'market': market,
                    'attribute_list':attribute_list,'data':history,'share':data,'name':namedata,'ctime':ctime,'stime':stime,'end_time':end_time,
                    'now':nowtime,'nowprice':data,'player':player,'price':price,'count':range(0,attribute_list.count())
                },context_instance=RequestContext(request))


@login_required(login_url='/Top/')
def buy_transaction(request, market_id):
    market = get_object_or_404(Market, pk=market_id)
    security = SecurityPrice.objects.get(market = market)
    lmsr = LMSR.objects.get(product = market.product)

    return render_to_response('Market/buy_transaction.html', {'market': market,'price':security.price,'share':security.sale_rate,'P0':lmsr.P0},
                               context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def sell_transaction(request, market_id):
    market = get_object_or_404(Market, pk=market_id)
    security = SecurityPrice.objects.get(market = market)
    lmsr = LMSR.objects.get(product = market.product)

    return render_to_response('Market/sell_transaction.html', {'market': market,'price':security.price,'share':security.sale_rate,'P0':lmsr.P0},
                               context_instance=RequestContext(request))

@login_required(login_url='/Top/')
def buy(request, market_id):
    form = TransactionForm(request.POST)
    m = get_object_or_404(Market, pk=market_id)
    price = SecurityPrice.objects.get(market = m).price
    sale_rate = SecurityPrice.objects.get(market = m).sale_rate
    lmsr = get_object_or_404(LMSR, product = m.product)
    player = Player.objects.get(id=request.user.player.id)

    try:
        selected_security = m.security_set.get(pk=request.POST['security'])
        selected_security_price = SecurityPrice.objects.get(market = m)
    except (KeyError, Security.DoesNotExist):
        return render_to_response('Market/buy_transaction.html', {
            'market': m,'price': price,'share':sale_rate,'P0':lmsr.P0,'error_message': "Choice Secuiry",
        }, context_instance=RequestContext(request))

    else:
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            action = "buy"
            p_cost = lmsr.p_cost_function(selected_security_price.amount)
            try:
                n_cost = lmsr.n_cost_function(selected_security_price.amount,amount,selected_security.number)
            except OverflowError:
                return render_to_response('Market/buy_transaction.html', {
                    'market': m,'price': price,'share':sale_rate,'P0':lmsr.P0,'Overflow_message': "Overflow",
                    }, context_instance=RequestContext(request))
            cost = n_cost - p_cost + selected_security.gross_margin * amount

            p = PlayerTransaction.objects.get(player = player)
            p.market = m
            p.security_number = selected_security.number
            p.amount = amount
            p.action =action
            p.cost = round(cost,2)
            p.save()

            return render_to_response('Market/transaction.html', {
                        'market': m,'selected_security':selected_security,'amount':amount,'action':action,'cost':round(cost,2)
                    },context_instance=RequestContext(request))

        return render(request, "Market/buy_transaction.html", {"form": form,'market': m,'price': price,'share':sale_rate,'P0':lmsr.P0})


@login_required(login_url='/Top/')
def sell(request, market_id):
    form = TransactionForm(request.POST)
    m = get_object_or_404(Market, pk=market_id)
    price = SecurityPrice.objects.get(market = m).price
    sale_rate = SecurityPrice.objects.get(market = m).sale_rate
    lmsr = get_object_or_404(LMSR, product = m.product)
    player = Player.objects.get(id=request.user.player.id)
    try:
        selected_security = m.security_set.get(pk=request.POST['security'])
        selected_security_price = SecurityPrice.objects.get(market = m)
    except (KeyError, Security.DoesNotExist):
        return render_to_response('Market/sell_transaction.html', {
            'market': m,'price': price,'share':sale_rate,'P0':lmsr.P0,'error_message': "Choice Secuiry",
        }, context_instance=RequestContext(request))

    else:
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            action = "sell"
            p_cost = lmsr.p_cost_function(selected_security_price.amount)
            try:
                n_cost = lmsr.n_cost_function(selected_security_price.amount,amount*(-1),selected_security.number)
            except OverflowError:
                return render_to_response('Market/sell_transaction.html', {
                    'market': m,'price': price,'share':sale_rate,'P0':lmsr.P0,'Overflow_message': "Overflow",
                    }, context_instance=RequestContext(request))
            cost = n_cost - p_cost - selected_security.gross_margin * amount

            try:
                p = PlayerTransaction.objects.get(player = player)
            except PlayerTransaction.DoesNotExist:
                p = PlayerTransaction.objects.get(player=player)
                p.save()

            p.market = m
            p.security_number = selected_security.number
            p.amount = amount
            p.action =action
            p.cost = round(cost,2)
            p.save()

            return render_to_response('Market/transaction.html', {
                        'market': m,'selected_security':selected_security,'amount':amount,'action':action,'cost':round(cost * (-1),2)
                    },context_instance=RequestContext(request))

        return render(request, "Market/sell_transaction.html", {"form": form,'market': m,'share':sale_rate,'price': price,'P0':lmsr.P0})



@login_required(login_url='/Top/')
def results(request, market_id):
    m = get_object_or_404(Market, pk=market_id)
    lmsr = get_object_or_404(LMSR, product = m.product)
    player = Player.objects.get(id=request.user.player.id)
    security = SecurityPrice.objects.get(market = m)
    try:
        pr = PlayerResult.objects.get(player = player, market = m,estimate = False)
    except MultipleObjectsReturned:
        pr_list = PlayerResult.objects.filter(player = player, market = m,estimate = False)
        pr_list.delete()
        pr = PlayerResult(player = player, market = m,estimate = False,estimate_time = timezone.now())
        pr.save()
    except PlayerResult.DoesNotExist:
        pr = PlayerResult.objects.get(player = player, market = m,estimate = False)
        pr.save()

    pt = PlayerTransaction.objects.get(player=player)
    trade_security = Security.objects.filter(market = m).get(number = pt.security_number)
    trade_security_price = SecurityPrice.objects.get(market = m)
   
    try:
        ps = PlayerSecurity.objects.get(player = player,security = trade_security)
    except PlayerSecurity.DoesNotExist:
        ps = PlayerSecurity(player = player,security = trade_security,amount = 0)

    if pt.action == "buy":
        if player.point - pt.cost >= 0 :
            ps.amount += pt.amount
            player.point -= pt.cost
            pr.investment += pt.cost
            trade_security_price.amount[pt.security_number] += pt.amount
        else:
            return render_to_response('Market/buy_transaction.html', {
                'market': m,'price':security.price,'share':security.sale_rate,'P0':lmsr.P0,'error_message': "You don't have enough price",
            }, context_instance=RequestContext(request))
    elif pt.action == "sell":
        if ps.amount >= pt.amount:
            ps.amount -= pt.amount
            player.point -=  pt.cost
            pr.returned -= pt.cost
            trade_security_price.amount[pt.security_number] -= pt.amount
        else :
            return render_to_response('Market/sell_transaction.html', {
                'market': m,'price':security.price,'share':security.sale_rate,'P0':lmsr.P0,'error_message': "You don't have enough products",
            }, context_instance=RequestContext(request))

    security = m.security_set.all()
    cost_sum = sum([math.exp(s/lmsr.b) for s in trade_security_price.amount])
    trade_security_price.price = [round(lmsr.P0*math.exp(s/lmsr.b)/cost_sum,2) for s in trade_security_price.amount]
    trade_security_price.sale_rate = [round(s/lmsr.P0*0.5+0.5,2) for s in trade_security_price.price]

    trade_security_price.save()

    if m.trade_amount > 10:
        trade_security.VWAP_amount += int(pt.amount)
        trade_security.VWAP_price += abs(pt.cost) - trade_security.gross_margin * pt.amount
        trade_security.save()

    m.trade_amount += 1
    pt.transaction = False
    m.save()
    ps.save()
    pt.save()
    pr.save()
    player.save()
    
    return render_to_response('Market/results.html', {'market': m,'player':player,'sale_rate':trade_security_price.sale_rate},
                               context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return render(request,'Market/logout_view.html')
