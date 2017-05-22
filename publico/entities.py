class Familia():
    def __init__(self, FamiliaID, PadreFamiliaID, Descripcion, Grafico, Hijos):        
        self.FamiliaID = FamiliaID
        self.PadreFamiliaID = PadreFamiliaID
        self.Descripcion = Descripcion
        self.Grafico = Grafico
        self.Hijos = Hijos

    def __str__(self):
        return self.Descripcion

class Producto():    
    def __init__(self, Id, CodArticulo, Descripcion, FamiliaPadre, FamiliaHijo, Linea, Aplicacion, Cantidad):
        self.Id = Id
        self.CodArticulo = CodArticulo
        self.Descripcion = Descripcion
        self.FamiliaPadre = FamiliaPadre
        self.FamiliaHijo = FamiliaHijo        
        self.Linea = Linea
        self.Aplicacion = Aplicacion
        self.Cantidad = Cantidad
    
    def __str__(self):
        return self.Descripcion

class FamiliaRes:
    def __init__(self, estado, mensaje):
        self.estado = estado
        self.mensaje = mensaje
        self.familia = None
        self.familias = []

    def __str__(self):
        return self.estado

    def ContarFamilia(self):
        return self.familias.count()

    def json_object(self, dato):
                
        if dato['familia'] != None:
            self.familia = Familia(dato['familia']['FamiliaID'], dato['familia']['PadreFamiliaID'], dato['familia']['Descripcion'], dato['familia']['Grafico'], dato['familia']['Hijos'])

        if dato['familias'] != None:            
            for fam in dato['familias']:
                familia = Familia(fam['FamiliaID'], fam['PadreFamiliaID'], fam['Descripcion'], fam['Grafico'], fam['Hijos'])
                self.familias.append(familia)