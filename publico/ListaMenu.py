from publico.entities import FamiliaRes
from django.conf import settings
import json
import urllib.request

def listaMenu(request):    
    if 'dict' not in request.session:        
        resp = urllib.request.urlopen(settings.WSFAMILIA + 'listarFamilia').read().decode('utf-8')
        
        data = json.loads(resp)       
        
        dict = {            
            'PRODS': '',
            'PRODLIST': '',            
            'CANT': '0',
            'BUS' : '',
            'ISELFP': 0,
            'ISELF': 0,
            'DSELFP': '',
            'DSELF': '',
            'SECCIONES': data['familias'],
        }

        request.session['dict'] = dict        
    else:
        dict = request.session['dict']
    return dict