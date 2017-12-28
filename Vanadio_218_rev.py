    

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 11:38:23 2017

@author: cabrera
"""
##############################################################################
                #IMPORTO LOS PAQUETES QUE VOY A USAR
##############################################################################

import numpy as np
import matplotlib.pyplot as plt
from Prom_Ponderado import Prom_Ponderado 
from Prom_Ponderado_detector import Prom_Ponderado_detector 


plt.close('all')
##############################################################################
#              DEFINICION DE VARIABLES GLOBALES
##############################################################################
#defino nume: cantidad de filas y columnas cuadrada, no se si lo vuelvo a usar
nume=128
col=nume
fil=nume

numor_ini=528178#530756
numor_final=528197#-10 #530765
#defino mov: cantidad de movimientos del detector en un numor
mov=25

#defino maxteta: que va a ser la que me da el lugar del maximo theta del espacio
maxteta=(numor_final-numor_ini+1)*mov#revisar pero creo q esta bien
#defino ti: es el delta tita entre pasos teorico
ti=0.05
ti2=ti/2
#defino distdet: la distancia angular entre detectores
delmov=1.25

#defino inic: es el valor en el que se centra el primer detector teoricamente
inic=135.0#125.0
#defino b: me va a defenir el vector espacio de angulos 
b=[]

for n in range(-1-col*25,maxteta+1) : #llega hasta un rango mas grande del que necesito 160.225 aunque solo necesito que llegue a 158.75+0.05
    b.append(inic-ti2+n*ti)

#defino guardo:guardar en "lecturas" los angulos leidos de cada shot
lecturas=[]
monitor=[]
#defino contador: va a servirme de respaldo para controlar que f tiene el tama;o que deberia tener
contador=0
Md_size=[]
for cor in range (0,128):
    Md_size.append(np.zeros((nume,col*25+1+maxteta-25)))
    
A_accounts=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
E_det=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
Idrh1=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
Idrh2=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
E_Idrh1=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
effi_d=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
E_effi_d=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
eff_1=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
E_eff_1=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
posiciones_ocupadas=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))
#Aux2=np.zeros(shape=(fil,fil,col*25+1+maxteta-25))

I_2_d=np.zeros((fil,col*25+1+maxteta-25))
#defino M: es la matriz local que guarda la lectura de f ordenada
M=np.zeros((fil,col))


#defino Ma: es la matriz ampliada en la cual voy a rehubicar los datos ya pesados
Ma=np.zeros((fil,col*25+1+maxteta-25)) #el mas dos es porque sume a izquierda y derecha un lugar mas aunque deberia ser 12 grados +2
Mo=np.zeros((fil,col*25+1+maxteta-25))
Mo1=np.zeros((fil,col*25+1+maxteta-25))

sigma_ai_sum=np.zeros((fil,col*25+1+maxteta-25))
sigma_ai=np.zeros((fil,col*25+1+maxteta-25))
E_I_ideal=np.zeros((fil,col*25+1+maxteta-25))
##############################################################################
#SECCION: OPERTURA DE DOCUMENTOS 
##############################################################################
filename=numor_ini-1
for numors in range(0,numor_final-numor_ini+1) :
    filename = filename + 1
    fichero = open(str(filename),'r')
    print numors
    ver=numors
    
    ###############################################################################
    #DEFINICION DE VARIABLES LOCALES (DEBERIA ORDENAR LUEGO POR ORDEN DE APARICION Y VER SI REALMENTE SON LOCALES JEJE)
    ###############################################################################
    #defino line: es el array que va leyendo del documento
    line="0"
    #defino datos_del_experimento: guarda toda la primera parte del documento
    datos_del_experimento=[]
    #defino auxline: donde voy a juntar los datos hasta poder entrar a un shot
    auxline=[]

    #defino r: se va a mover de 0 a movlocdet, aqui lo defino en cero para que se reinicie cada vez que cambio de numors
    r=0
    #defino f: donde se guardaran las cuentas de la medicion r
    f=[]
    

    ###############################################################################
    # LEE LOS PRIMEROS DATOS DEL DOCUMENTO Y LOS GUARDA EN datos_del_experimento
    ###############################################################################
    # el dato de que el for va de 0 a 42 lo saque mediante prueba/error
    for x in xrange(0,42) :
        line=np.array(fichero.readline().split()).astype(str)
        datos_del_experimento.append(line)
    ###############################################################################
    #        LEE LOS DATOS CENTRALES DEL DOCUMENTO 
    ###############################################################################
    while r < 25 : #25 OJO QUE LO CAMBIE PARA VER
        #print r
        #defino P: bandera para extraer el peso en angulo. Con P=0 reinicio para cada shot
        Q=0 
        #defino ii: va a ser el encargado de guardar la posicion angular correspondiente al espacio en b y a la matriz ampliada Ma
        #lo reinicio para asegurarme que entre siempre a algun angulo
        ii=col*24
        #defino t_moni_TCou_angx1000: guarda el dato que me interesa porque empieza a iterar antes de que aparezca el valor que quiero
        t_moni_TCou_angx1000=auxline 
        #defino auxiline: con la cual me voy a preguntar si estoy en un nuevo shot
        auxline=np.array(fichero.readline().split())
        #defino pepe: leo a auxiline como string
        pepe=str(auxline)
        #Me pregunto si leo una I en el ultimo array leido
        if 'I' in pepe :
            #print "entro"
            #defino gurado: con las siguientes sentencias cosnsigo guardar en "lecturas" los angulos leidos de cada shot
            mo=t_moni_TCou_angx1000[1]
            mon=float(mo)
            moni=mon/1000000.0 
            monitor.append(moni)
            
            an=t_moni_TCou_angx1000[3]
            ann1=float(an)
            ann=ann1/1000
            lecturas.append(ann)
            #la siguiente sentencia es para que salte la fila que me dal el dato de numeros de datos
            iline2=np.array(fichero.readline().split()).astype(float)
            #defino ext: me da los valores a izquierdas del espacio angular del angulo leido con un ancho ti (ojo que quizas le cambie el nombre a ti)
            ext=[lecturas[r+numors*25]-ti2,lecturas[r+numors*25]+ti2]
            #print ext[0]
            ##################################################################
            #junto los datos del shot en f
            ##################################################################
            for i in xrange(0,1639) :
                iline=np.array(fichero.readline().split()).astype(float)
                if i not in [1638]:
                    #print 'entro aqui'
                    for lugar in range(0,10) :
                        f.append(iline[lugar])
                        contador=contador+1
                else :
                    #print "entro aca"
                    for lugar4 in range(0,4) :
                        f.append(iline[lugar4])
                        contador=contador+1
                        #para confirmar que lee bien me podria peguntar si contador y len(f)== a 16384 guardado en el iline2  
             
                  
            
            
            
            while Q != 1 :
                #print "entro aui tambie"
                #print ii
                if ext[0] >= b[ii] and ext[0] < b[ii+1] :
                    #print "entro en el if"
                    #print ii
                    Q=1
                    q=b[ii+1]-ext[0]# voy a ver donde car a izquierda y con eso calculo que deberia alcanzar para definir todo el espacio
                    peso=q/ti #peso para b[i-1]la diferencia para b[i]
                    med=(b[ii]+b[ii+1])/2
                    ##############################################################
                    #Armo la matriz local
                    ##############################################################
                    kj=col
                    for n in range(col,0,-1):
                        aux1a=(n-1)*fil+r*col*fil
                        aux1b=n*fil+r*col*fil
                        kj=kj-1
                        #print aux1a,aux1b,kj
                        if n%2 == 0 :
                            ki=fil
                            for k in range(aux1b-1,aux1a-1,-1) :
                                ki=ki-1
                                M[ki][kj]=f[k]
                        else :
                            #print "n impar"
                            kio=0
                            for kimp in range(aux1b-1,aux1a-1,-1) :
                                M[kio][kj]=f[kimp]
                                kio=kio+1
                    
                    #print M
                    ##############################################################
                    #Armo la matriz ampliada                    
                    ###############################################################
                    kj=ii
                    
                    for n in range(col,0,-1):
                        aux1a=(n-1)*fil+r*col*fil#+numors*25
                        aux1b=n*fil+r*col*fil#+numors*25
                        kj=kj-25
                        
                        
                        #print ii,kj
                        #print aux1a,aux1b,kj
                        if n%2 == 0 :
                            #print "detector impar"
                            kio=0
                            for kimp in range(aux1b-1,aux1a-1,-1) :
                                
                                #Md_size[n-1][kio][kj]=Md_size[n-1][kio][kj]+peso*f[kimp]
                                #Md_size[n-1][kio][kj+1]=Md_size[n-1][kio][kj+1]+(1.0-peso)*f[kimp]
                                
                                Ma[kio][kj]=Ma[kio][kj]+peso*f[kimp]#/monitor[r+numors*25]
                                Ma[kio][kj+1]=Ma[kio][kj+1]+(1-peso)*f[kimp]#/monitor[r+numors*25]
                                
                                                                
                                Mo1[kio][kj]=Mo[kio][kj]+peso*monitor[r+numors*25]
                                Mo1[kio][kj+1]=Mo[kio][kj+1]+(1-peso)*monitor[r+numors*25]
                                
                                                               
                                if monitor[r+numors*25] != 0 and  f[kimp] != 0 :
                                    #Para la parte [2]
                                    Idrh1[128-n][kio][kj]=Idrh1[n-1][kio][kj]+peso*f[kimp]/monitor[r+numors*25]
                                    Idrh1[128-n][kio][kj+1]=Idrh1[n-1][kio][kj+1]+(1-peso)*f[kimp]/monitor[r+numors*25]
                                    
                                    Idrh2[128-n][kio][kj]=Idrh2[n-1][kio][kj]+peso*monitor[r+numors*25]
                                    Idrh2[128-n][kio][kj+1]=Idrh2[n-1][kio][kj+1]+(1-peso)*monitor[r+numors*25]
                                    
                                    E_Idrh1[128-n][kio][kj]=E_Idrh1[n-1][kio][kj]+(peso**2)*(f[kimp])
                                    E_Idrh1[128-n][kio][kj+1]=E_Idrh1[n-1][kio][kj+1]+((1-peso)**2)*(f[kimp])
                                
                                
                                #e_Mo[kio][kj]=e_Mo[kio][kj]+(peso*monitor[r+numors*25])**0.5
                                #e_Mo[kio][kj+1]=e_Mo[kio][kj+1]+((1-peso)*monitor[r+numors*25])**0.5
                                
                             #   sigma_ai[kio][kj]=sigma_ai[kio][kj]+peso*(f[kimp])**1.5
                              #  sigma_ai[kio][kj+1]=sigma_ai[kio][kj+1]+(1.0-peso)*(f[kimp])**1.5
                                
                               # sigma_ai_sum[kio][kj]=sigma_ai_sum[kio][kj]+peso*(f[kimp])**0.5
               #                 sigma_ai_sum[kio][kj+1]=sigma_ai_sum[kio][kj+1]+(1.0-peso)*(f[kimp])**0.5
                                
                #                I_2_d[kio][kj]=I_2_d[kio][kj]+peso*(f[kimp])**2
                 #               I_2_d[kio][kj+1]=I_2_d[kio][kj+1]+(1.0-peso)*(f[kimp])**2
                                
                                
                                
                                
                                    
                                kio=kio+1

                        else :
                            ki=fil
                            for k in range(aux1b-1,aux1a-1,-1) :
                                ki=ki-1
                                
                                #Md_size[n-1][ki][kj]=Md_size[n-1][ki][kj]+peso*f[k]
                                #Md_size[n-1][ki][kj+1]=Md_size[n-1][ki][kj+1]+(1.0-peso)*f[k]
                                
                                
                                Ma[ki][kj]=Ma[ki][kj]+peso*f[k]#/monitor[r+numors*25]
                                Ma[ki][kj+1]=Ma[ki][kj+1]+(1-peso)*f[k]#/monitor[r+numors*25]
                                
                                
                                Mo1[ki][kj]=Mo[ki][kj]+peso*monitor[r+numors*25]
                                Mo1[ki][kj+1]=Mo[ki][kj+1]+(1-peso)*monitor[r+numors*25]
                                
                                if monitor[r+numors*25] != 0 and  f[k] != 0 :
                                    #Para la parte [2]
                                    Idrh1[128-n][ki][kj]=Idrh1[n-1][ki][kj]+peso*f[k]/monitor[r+numors*25]
                                    Idrh1[128-n][ki][kj+1]=Idrh1[n-1][ki][kj+1]+(1-peso)*f[k]/monitor[r+numors*25]
                                    
                                    Idrh2[128-n][ki][kj]=Idrh2[n-1][ki][kj]+peso*monitor[r+numors*25]
                                    Idrh2[128-n][ki][kj+1]=Idrh2[n-1][ki][kj+1]+(1-peso)*monitor[r+numors*25]
                                    
                                    E_Idrh1[128-n][ki][kj]=E_Idrh1[n-1][ki][kj]+(peso**2)*(f[k])
                                    E_Idrh1[128-n][ki][kj+1]=E_Idrh1[n-1][ki][kj+1]+((1-peso)**2)*(f[k])
                                
                                
                                #e_Mo[ki][kj]=e_Mo[ki][kj]+(peso*monitor[r+numors*25])**0.5
                                #e_Mo[ki][kj+1]=e_Mo[ki][kj+1]+((1-peso)*monitor[r+numors*25])**0.5
                                
                 #               sigma_ai[ki][kj]=sigma_ai[ki][kj]+peso*(f[k])**1.5
                  #              sigma_ai[ki][kj+1]=sigma_ai[ki][kj+1]+(1.0-peso)*(f[k])**1.5
                                
                   #             sigma_ai_sum[ki][kj]=sigma_ai_sum[ki][kj]+peso*(f[k])**0.5
                    #            sigma_ai_sum[ki][kj+1]=sigma_ai_sum[ki][kj+1]+(1.0-peso)*(f[k])**0.5
                                
                     #           I_2_d[ki][kj]=I_2_d[ki][kj]+peso*(f[k])**2
                      #          I_2_d[ki][kj+1]=I_2_d[ki][kj+1]+(1.0-peso)*(f[k])**2
                                
                                
                                
                                
                        
                        
                    #print Ma    
                
                ii=ii+1
                #print ii
            #print "sali!!!!!!!!!!!!!!!!!!!"
            #print "r"
            #print r
            r=r+1        #print Q

#%%
Idrh=np.zeros((fil,fil,col*25+1+maxteta-25))
for d in range(0,128): 
    Idrh[d]=np.divide(Idrh1[d], Idrh2[d],out=np.zeros_like(Idrh1[d]), where=Idrh2[d]!=0) #DIVIDIRA LAS 128 MATRICES POR LAS 128?

Ideal, Ideal1 = Prom_Ponderado(Idrh1,E_Idrh1,fil,fil,col*25+1+maxteta-25)
Mo=np.sum(Idrh2,axis=0)
Ideal_Mo=np.divide(Ideal1,Mo,out=np.zeros_like(Ideal), where=Mo!=0)
'''
fig = plt.figure(11)
plt.pcolormesh(Ideal)
#plt.savefig('Ideal.jpg')
fig = plt.figure(12)
plt.pcolormesh(Ideal1)
#plt.savefig('Ideal1.jpg')
'''
Effi_d=np.zeros((fil,fil,col*25+1+maxteta-25))
for d in range(0,128):
    Effi_d[d]=np.divide(Ideal1, Idrh1[d],out=np.zeros_like(Ideal), where=Idrh[d]!=0)




effi,effi1 = Prom_Ponderado_detector(Effi_d,Effi_d,fil,fil,col*25+1+maxteta-25)
'''
fig = plt.figure(13)
plt.pcolormesh(effi1,clim=(0.06,0.1))
plt.hist(effi1.ravel(), bins=266, range=(0.01, 4.0), fc='k', ec='k')
fig = plt.figure(14)
plt.hist(Mo.ravel(), bins=266, range=(0.01, 40), fc='k', ec='k') 
'''
for d in range(0,128,8):
    print d
    
    
    f=plt.figure(d)
    plt.hist(Idrh1[d].ravel(), bins=266, range=(0.01, 100), fc='k', ec='k')
    
    
#plt.savefig('Ideal1.jpg')

#%%
'''



#Eficiencia parte [2a]


for d in range (127,-1,-1) :
#mov detector
    Aux2=np.divide(E_Idrh[d],Idrh[d],out=np.zeros_like(E_Idrh[d]), where=Idrh[d]!=0)
    
    print d
    #ignored_states = np.seterr(**old_err_state)
    
    effi_d[d]=np.divide(I_ideal,Idrh[d],out=np.zeros_like(I_ideal), where=Idrh[d]!=0)


    for k in range (0,col*25+1+maxteta-25):
    #move columns
    
        for mr in range (0,128):
        #move row
        
            #effi_d[d][mr][k]=I_ideal[mr][k]/Idrh[d][ki][kj]
            E_effi_d[d][mr][k]=E_effi_d[d][mr][k]+effi_d[d][mr][k]*((Aux1[mr][k])**2+(Aux2[ki][kj])**2)**0.5
            if E_effi_d[d][mr][k] != 0:    
                
                eff_1[d][mr][k]=eff_1[d][mr][k]+effi_d[d][mr][k]*(effi_d[d][mr][k]/E_effi_d[d][mr][k])
                E_eff_1[d][mr][k]=E_eff_1[d][mr][k]+(effi_d[d][mr][k]/E_effi_d[d][mr][k])
            if effi_d[d][mr][k] !=0:
                posiciones_ocupadas[d][mr][k]=posiciones_ocupadas[d][mr][k]+1
    
    

             
eff_2=np.zeros((128,128))
E_eff_2=np.zeros((128,128))
total_posicioes=np.zeros((128,128))
eff_2p=np.zeros((128,128))
#eff_2b=np.zeros((128,128))
#E_eff_2b=np.zeros((128,128))

for d in range (127,-1,-1) :
#mov detector
    print d
    
    eff_2[:,d]=np.nansum(eff_1[d],axis=1)
    E_eff_2[:,d]=np.nansum(E_eff_1[d],axis=1)
    
    eff_2p[:,d]=np.nansum(effi_d[d],axis=1)
    total_posicioes[:,d]=np.nansum(posiciones_ocupadas[d],axis=1)
    #eff_2b[:,d]=np.nansum(effi_d[d],axis=1)
    #E_eff_2b[:,d]=np.nansum(E_effi_d[d],axis=1)

    
    
eff=np.divide(eff_2,E_eff_2,out=np.zeros_like(eff_2), where=E_eff_2!=0)
eff_b=np.divide(eff_2p,total_posicioes,out=np.zeros_like(eff_2p), where=total_posicioes!=0)







###################################################
#       PRIMER INTENTO DE GRAFICA
###################################################


xi=0
# Representamos
fig = plt.figure(num=200)
plt.imshow(Ma)
fig = plt.figure(num=201)
plt.imshow(Mo)



f,(x1,x2,x3,x4)=plt.subplots(4, sharex=True)
x1.imshow(Idrh[126],clim=(0, 40))
x1.set_title('Cuentas de un shot (pesado por monitor individual)') #necesario en Parte [2]
x2.imshow(Idrh[100],clim=(0, 40))
x3.imshow(Idrh[80],clim=(0, 40))
x4.imshow(Idrh[20],clim=(0, 40))



f,(x11,x21,x31,x41)=plt.subplots(4, sharex=True)
x11.imshow(E_Idrh[126],clim=(0, 40))
x11.set_title('Error Cuentas de un shot (pesado por monitor individual)') #necesario en Parte [2]
x21.imshow(E_Idrh[100],clim=(0, 40))
x31.imshow(E_Idrh[80],clim=(0, 40))
x41.imshow(E_Idrh[20],clim=(0, 40))
f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)


f,(x12,x22,x32,x42)=plt.subplots(4, sharex=True)
x12.imshow(sigma_ai)
x12.set_title('sigma_ai')
x22.imshow(sigma_ai_sum)
x22.set_title('sigma_ai_sum')
x32.imshow(I_d)
x32.set_title('I_d')
x42.imshow(Aux2)
x42.set_title('Aux2')

vamos=np.divide(eff,eff_b)

f,(x13,x23,x33,x43)=plt.subplots(4, sharex=True)
x13.imshow(vamos,clim=(0.8, 1))
x13.set_title('comparacion entre pesada y no pesada por error')
x23.imshow(eff,clim=(0.02, 0.09))
x23.set_title('eff')
x33.imshow(eff_b,clim=(0,0.1))
x33.set_title('eficiencia no pedada por error')
x43.imshow(eff_b,clim=(0, 2))
x43.set_title('eficiencia no pedada por error')





#imgplot = plt.imshow(Idrh[126],clim=(0.0, 2.3))#, cmap="hot"
#imgplot.set_cmap('nipy_spectral')
#plt.colorbar()


####################################
#imprime detector por detector
#####################################
#for muestra in range(0,128) :
 #   fig = plt.figure(num=muestra)
  #  plt.imshow(Md_size[muestra])



#####################################################
'''

#https://matplotlib.org/examples/pylab_examples/subplots_demo.html
#plt.hist(I_ideal.ravel(), bins=266, range=(0.0, 4.0), fc='k', ec='k')
#https://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero














