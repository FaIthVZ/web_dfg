from django.conf.urls import patterns, include, url
from publico.views import products_list, product_detail, search_result, AgregarCarro, EliminarRegistro, enviocorreo, RegistrarPedido, ObtenerProductos

urlpatterns = patterns('',

    #url(r'^(aps)/$','apps.publico.views.ComercioView'),
    #url(r'^(lisicon)/$','apps.publico.views.ComercioView'),

    url(r'^$','publico.views.home', name='home'),
    url(r'^about$','publico.views.about', name='about'),
    url(r'^layout$','publico.views.layout', name='layout'),
    url(r'^news$','publico.views.news', name='news'),
    url(r'^news_list$','publico.views.news_list', name='news_list'),
    url(r'^news_detail$','publico.views.news_detail', name='news_detail'),
    url(r'^offers_promotions$','publico.views.offers_promotions', name='offers_promotions'),
    url(r'^price$','publico.views.price', name='price'),
    url(r'^product_detail/(?P<codArticulo>[\w|\W]+)/(?P<familiaID>[\w|\W]+)/(?P<familiaPadreID>[\w|\W]+)/$',product_detail.as_view(), name='product_detail'),
    url(r'^products_catalog$','publico.views.products_catalog', name='products_catalog'),
    url(r'^products_family$','publico.views.products_family', name='products_family'),
    url(r'^products_list/(?P<codArticulo>\w+)/(?P<familiaID>[\w|\W]+)/(?P<familiaPadreID>[\w|\W]+)/$',products_list.as_view(), name='products_list'),
    url(r'^search_result/(?P<busqueda>[\w|\W]+)/$',search_result.as_view(), name='search_result'),
    url(r'^contact$','publico.views.contact', name='contact'),
    url(r'^addcar/$',AgregarCarro.as_view()),
    url(r'^delcar/$',EliminarRegistro.as_view()),
	url(r'^sendmail/$',enviocorreo.as_view()), 
    url(r'^sendprice/$',RegistrarPedido.as_view()),
    url(r'^getProducts/$',ObtenerProductos.as_view()),
)