from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.views.generic.base import TemplateView
from publico.entities import Producto
from django.conf import settings
from django.utils import html

def home(request):
    return render_to_response('publico/home.html',context_instance=RequestContext(request))

def about(request):
    return render_to_response('publico/about.html',context_instance=RequestContext(request))

def layout(request):
    return render_to_response('publico/layout.html',context_instance=RequestContext(request))

def news(request):
    return render_to_response('publico/news.html',context_instance=RequestContext(request))

def news_list(request):
    return render_to_response('publico/news_list.html',context_instance=RequestContext(request))

def news_detail(request):
    return render_to_response('publico/news_detail.html',context_instance=RequestContext(request))

def offers_promotions(request):
    return render_to_response('publico/offers_promotions.html',context_instance=RequestContext(request))

def price(request):
    from django.conf import settings
    import json
    import urllib.request

    datos = request.session['dict']

    if datos['PRODS'] == '':                            
        car = []
    else:
        car = datos['PRODS']   
    
    resp = urllib.request.urlopen(settings.WSPAIS + 'listarPais').read().decode('utf-8')
        
    data = json.loads(resp)

    context = {'productos': car,
                'paises': data['paises']}

    return render_to_response('publico/price.html',context,context_instance=RequestContext(request))


class product_detail(TemplateView):
    template_name = 'publico/product_detail.html'

    def get_context_data(self, **kwargs):
        producto = Productos(self,kwargs)     
        return {'producto': producto['productos'][0]}

def products_catalog(request):
    return render_to_response('publico/products_catalog.html',context_instance=RequestContext(request))

def products_family(request):
    return render_to_response('publico/products_family.html',context_instance=RequestContext(request))

class products_list(TemplateView):  
    template_name = 'publico/products_list.html'    
    def get_context_data(self, **kwargs):
        productos = Productos(self,kwargs)     
        return {'productos': productos}

class search_result(TemplateView):  
    template_name = 'publico/search_result.html'    
    def get_context_data(self, **kwargs):
        if 'busqueda' in kwargs:
            self.request.session['dict']['BUS'] = kwargs['busqueda']
        
        productos = Productos(self,kwargs)     
        return {'productos': productos}

def contact(request):
    return render_to_response('publico/contact.html',context_instance=RequestContext(request))

def Productos(self,kwargs):
    import urllib
    import json  
    
    codArticulo = ''
    familiaID = ''
    familiaPadreID = ''
    busqueda = ''
    seleF = ''
    seleFP = ''
    iseleF = '0'
    iseleFP = '0'

    if 'busqueda' in kwargs:
        busqueda = kwargs['busqueda']
    else:        
        if (kwargs['codArticulo'] != '0'):
            codArticulo = kwargs['codArticulo']

        if (kwargs['familiaID'] != '0'):
            familiaID = kwargs['familiaID']
            iseleF = kwargs['familiaID']
            prod = self.request.session['dict']['SECCIONES']

            for sel in prod:
                if sel['FamiliaID'] == familiaID:
                    seleF = ' / ' + sel['Descripcion']
                    break

        if (kwargs['familiaPadreID'] != '0'):
            familiaPadreID = kwargs['familiaPadreID']
            iseleFP = kwargs['familiaPadreID']
            prod = self.request.session['dict']['SECCIONES']

            for sel in prod:
                if sel['FamiliaID'] == familiaPadreID:
                    seleFP = sel['Descripcion']
                    break
    
    datos = self.request.session['dict']
    datos['DSELFP'] = seleFP
    datos['DSELF'] = seleF
    datos['ISELFP'] = iseleFP
    datos['ISELF'] = iseleF

    data = {}
    data['codArticulo'] = codArticulo
    data['familiaID'] = familiaID
    data['familiaPadreID'] = familiaPadreID
    data['busqueda'] = busqueda

    valores = urllib.parse.urlencode(data)    
    ruta = settings.WSPRODUCTO + 'listarProductos?' + valores

    resp = urllib.request.urlopen(ruta).read().decode('utf-8')
    data = json.loads(resp)
    datos['PRODLIST'] = data['productos']

    if datos['PRODS'] != '':                            
        car = datos['PRODS'] 

        for prod in data['productos']:
            for pcar in car:
                if prod['CodArticulo'] == pcar.CodArticulo:
                    prod['Seleccionado'] = '1'
                    prod['Cantidad'] = pcar.Cantidad
                    break

    self.request.session['dict'] = datos
    return data

class AgregarCarro(TemplateView):
    def get(self, request, *args, **kwargs):        
        id = request.GET['id']
        des = request.GET['des']
        dlinea = request.GET['dlinea']
        famPadre = request.GET['famPadre']
        famHijo = request.GET['famHijo']
        cantidad = request.GET['cantidad']
        
        datos = request.session['dict']

        if datos['PRODS'] == '':                            
            car = []
        else:
            car = datos['PRODS']            
        
        if cantidad == '':
            cantidad = '1'

        car.append(Producto(str(len(car)),id, des, famPadre, famHijo, dlinea,'', cantidad))
        
        datos['CANT'] = str(len(car))
        datos['PRODS'] = car

        request.session['dict'] = datos

        data = '{"cant":"' + str(len(car)) +  '"}'

        return HttpResponse(data,content_type='application/json')

class EliminarRegistro(TemplateView):
    def get(self, request, *args, **kwargs):
        import json        
        id = request.GET['id']        
        
        datos = request.session['dict']

        car = datos['PRODS']            
        
        for i in range(0,len(car)):
            if id == car[i].CodArticulo:
                del car[i]
                break

        for i in range(0,len(car)):
            car[i].Id = str(i)

        datos['CANT'] = str(len(car))
        datos['PRODS'] = car

        request.session['dict'] = datos
        data = json.dumps(car, default=lambda o: o.__dict__).encode('utf-8')
        return HttpResponse(data,content_type='application/json')

    
class enviocorreo(TemplateView):
    def get(self, request, *args, **kwargs):
        import urllib
        import json
        from django.template import Context
        from django.template.loader import get_template

        nombre = request.GET['nombre']
        correo = request.GET['correo']
        comentario = request.GET['comentario']
        asunto = request.GET['asunto']

        data = {'nombre' : nombre,
                'correo' : correo,
                'comentario' : comentario,
                'asunto' : asunto}

        #valores = urllib.parse.urlencode(data)
        valores = json.dumps(data)
        valores = valores.encode('utf-8')        
        ruta = settings.WSCONTACTO + 'registrarContacto'
        req = urllib.request.Request(ruta, valores)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Content-Length', len(valores))
        resp = urllib.request.urlopen(req)

        ctx = {
            'name': nombre,
            'question': comentario
        }

        message = get_template('publico/email_contact.html').render(Context(ctx))

        email = EmailMessage(
            'Consulta: ' + asunto,
            message,
            'DFG - COSTUMER SERVICE <ldelgado@jywrepuestos.com>',
            [correo]
            #,
            #headers = {'Reply-To': 'contact_email@gmail.com' }
            )
        email.content_subtype = 'html'
        email.send()
        return HttpResponse()

class RegistrarPedido(TemplateView):
    def get(self, request, *args, **kwargs):
        import urllib
        import json
        import time
        from django.template import Context
        from django.template.loader import get_template
        
        empresa = request.GET['empresa']
        nombre = request.GET['nombre']
        RUC = request.GET['RUC']
        email = request.GET['email']
        telefono = request.GET['telefono']
        celular = request.GET['celular']
        mensaje = request.GET['mensaje']
        productos = request.GET['productos']
        pais = request.GET['pais']

        data = {'empresa': empresa,
                'nombre' : nombre,
                'RUC': RUC,
                'email' : email,
                'telefono' : telefono,
                'celular' : celular,
                'pais': pais,
                'mensaje' : mensaje}

        valores = json.dumps(data)
        valores = valores.encode('utf-8')        
        ruta = settings.WSCOTIZACION + 'registrarCotizacion'
        req = urllib.request.Request(ruta, valores)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Content-Length', len(valores))
        resp = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp)

        productos = json.loads(productos)

        for prod in productos['productos']:
            data = {'cotizacionID': resp,
                'cod_articulo' : prod['Codigo'],
                'cantidad': prod['Cantidad']}
            valores = json.dumps(data)
            valores = valores.encode('utf-8')        
            ruta = settings.WSCOTIZACION + 'registrarCotizacionDetalle'
            reqD = urllib.request.Request(ruta, valores)
            reqD.add_header('Content-Type', 'application/json')
            reqD.add_header('Content-Length', len(valores))
            urllib.request.urlopen(reqD)

        datsess = self.request.session['dict']
        productos = datsess['PRODS']
        datsess['PRODS'] = ''
        datsess['CANT'] = '0'
        self.request.session['dict'] = datsess  

        ctx = {'correlativo' : pais + '-' + resp,
                'fecha' : time.strftime("%d/%m/%y"),
                'empresa': empresa,
                'nombre' : nombre,
                'RUC': RUC,
                'email' : email,
                'telefono' : telefono,
                'celular' : celular,
                'mensaje' : mensaje,
                'productos' : productos
        }

        message = get_template('publico/email_price.html').render(Context(ctx))

        email = EmailMessage(
            'Cotización: ' + 'PE-0001',
            message,
            'DFG - COSTUMER SERVICE <ldelgado@jywrepuestos.com>',
            [email]
            #,
            #headers = {'Reply-To': 'contact_email@gmail.com' }
            )
        email.content_subtype = 'html'
        email.send()
                
        return HttpResponse()

class ObtenerProductos(TemplateView):
    def get(self, request, *args, **kwargs):
        import json
        data = request.session['dict']['PRODLIST']      
        data = json.dumps(data, default=lambda o: o.__dict__).encode('utf-8')
        return HttpResponse(data,content_type='application/json')

class ListarPais(TemplateView):
    def get(self, request, *args, **kwargs):
        import json
        ruta = settings.WSPRODUCTO + 'listarPais'

        resp = urllib.request.urlopen(ruta).read().decode('utf-8')
        data = json.loads(resp)
        return HttpResponse(data['paises'],content_type='application/json')