from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^mypage/$', views.mypage, name='mypage'),
    url(r'^mypage_tutorial/$', views.mypage_tutorial, name='mypage_tutorial'),
    url(r'^questionnaire_answ/$', views.questionnaire_answ, name='questionnaire_answ'),
    url(r'^open/$', views.open, name='open'),
    url(r'^login_success/$', views.login_success, name='login_success'),
    url(r'^logout_view/$', views.logout_view, name='logout_view'),
    url(r'^RetailStore_detail/$', views.RetailStore_detail, name='RetailStore_detail'),
    url(r'^history/$', views.history, name='history'),
    url(r'^(?P<rs_id>[0-9]+)/shop_lines/$', views.shop_lines, name='shop_lines'),
    url(r'^(?P<rs_id>[0-9]+)/stock/$', views.stock, name='stock'),
    url(r'^(?P<rs_id>[0-9]+)/create/$', views.create, name='create'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<market_id>[0-9]+)/create_products/$', views.create_products, name='create_products'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<market_id>[0-9]+)/ideaBox_tutorial/$', views.ideaBox_tutorial, name='ideaBox_tutorial'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<market_id>[0-9]+)/created/$', views.created, name='created'),
    url(r'^(?P<rs_id>[0-9]+)/new_market/$', views.new_market, name='new_market'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<market_id>[0-9]+)/participate_market/$', views.participate_market, name='participate_market'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<market_id>[0-9]+)/check_reward/$', views.check_reward, name='check_reward'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<market_id>[0-9]+)/check_reward_end/$', views.check_reward_end, name='check_reward_end'),
    url(r'^(?P<market_id>[0-9]+)/dropout/$', views.dropout, name='dropout'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<market_id>[0-9]+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<market_id>[0-9]+)/market_tutorial/$', views.market_tutorial, name='market_tutorial'),
    url(r'^(?P<market_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<market_id>[0-9]+)/buy/$', views.buy, name='buy'),
    url(r'^(?P<market_id>[0-9]+)/sell/$', views.sell, name='sell'),
    url(r'^(?P<market_id>[0-9]+)/buy_transaction/$', views.buy_transaction, name='buy_transaction'),
    url(r'^(?P<market_id>[0-9]+)/sell_transaction/$', views.sell_transaction, name='sell_transaction'),
    url(r'^(?P<area_id>[0-9]+)/choice_shop/$', views.choice_shop, name='choice_shop'),
    url(r'^(?P<area_id>[0-9]+)/(?P<shop_id>[0-9]+)/choice_color/$', views.choice_color, name='choice_color'),
    url(r'^(?P<area_id>[0-9]+)/(?P<shop_id>[0-9]+)/(?P<color_id>[0-9]+)/give_name/$', views.give_name, name='give_name'),
    url(r'^(?P<area_id>[0-9]+)/(?P<shop_id>[0-9]+)/(?P<color_id>[0-9]+)/open_success/$', views.open_success, name='open_success'),
    url(r'^(?P<rs_id>[0-9]+)/RetailStore_page/$', views.RetailStore_page, name='RetailStore_page'),
    url(r'^(?P<rs_id>[0-9]+)/shoppage_tutorial/$', views.shoppage_tutorial, name='shoppage_tutorial'),
    url(r'^(?P<rs_id>[0-9]+)/accountant/$', views.accountant, name='accountant'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<product_id>[0-9]+)/accountant_table/$', views.accountant_table, name='accountant_table'),
    url(r'^(?P<rs_id>[0-9]+)/(?P<product_id>[0-9]+)/(?P<pr_id>[0-9]+)/breakdown/$', views.breakdown, name='breakdown'),
    ]
