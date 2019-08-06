import matplotlib.pyplot as plt
import matplotlib
import math
import pandas as pd
import pylab as pl
import numpy as np
import turtle as tl
import random as rand


# functiile astea 3 deseneaza niste forme simple geometrice, in functie de aria data
# toate returneaza o lista cu diferite specificatii ale formei(de ex, un dreptunghi returneaza latimea si lungimea)
def drawSquare(area = 3601): # e destul de obvious ce face functia asta   
    latura = math.sqrt(area)

    tl.forward(latura)
    tl.right(90)
    tl.forward(latura)
    tl.right(90)
    tl.forward(latura)
    tl.right(90)
    tl.forward(latura)
    tl.right(90)

    return [latura] 

def drawRect(area = 3601):  
    latura = math.sqrt(area)
    latime = rand.randrange(60, int(latura) if int(latura) > 60 else 61) # randrange are nevoie de un int pt stop, dar latura era float
    lungime = area / latime                                              # daca area e sub 61^2, cand o rotunjeste la int, devine 60 si atunci nu
                                                                         # selecteaza niciun numar, pt ca randrange se opreste la stop
    tl.forward(lungime)
    tl.right(90)
    tl.forward(latime)
    tl.right(90)
    tl.forward(lungime)
    tl.right(90)
    tl.forward(latime)
    tl.right(90)

    return [int(lungime), latime]

def drawRhombus(area = 3601):
    angle = rand.randrange(30, 161) # alege un unghi random pentru latura
    latura = math.sqrt(area / np.sin(np.deg2rad(angle))) # latura rombului e calculata dupa formula ariei

    tl.right(90 - angle / 2) # stiu ca arata ciudat calculele pt unghi, dar daca ai rabdare sa ti le reprezinti pe o hartie, nu s cn stie ce
    tl.forward(latura)
    tl.right(angle / 2)
    tl.right(90 - (180 - angle) / 2)
    tl.forward(latura)
    tl.right((180 - angle) / 2)
    tl.right(90 - angle / 2)
    tl.forward(latura)
    tl.right(angle / 2)
    tl.right(90 - (180 - angle) / 2)
    tl.forward(latura)
    tl.right((180 - angle) / 2)

    return [latura, angle]

# functia care deseneaza efectiv un cerc e scrisa separat
def drawSemiCircle(point = [0, 0], radius = 0, angle = 0, side = 1):
    tl.up()
    tl.right(angle)
    tl.goto(point[0], point[1])
    tl.down()
    tl.circle(radius, 180)

# urmatoarele functii deseneaza semicercuri peste formele deja desenate, ca sa dea aparenta ca (formele) sunt facute aleatoriu
# functia asta o fac ca sa fie codul mai lizibil, returneaza o latura pe care nu e desenat niciun semicerc sau -1 daca nu gaseste nicio latura
def checkSide(specs = [], stop = 0, whichShape = 1): # whichShape functioneaza in felu urmator: valoarea 1 - e patrat, valoarea 2 - e dreptunghi, val 3 - e romb
    checkIt = []
    whichLatura = 0
    foundGoodCoord = False
    while foundGoodCoord == False and len(checkIt) < 4: # a doua conditie verifica daca au fost incercate toate laturile, caz in care nu se mai pot
        foundGoodCoord = True                           # adauga cercuri
        whichLatura = rand.randrange(1, 5)
        thisSideIsChecked = True
        
        while thisSideIsChecked: # aici tot alege o latura pana cand da de una pe care n a ales o inca
            thisSideIsChecked = False
            for side in checkIt:
                if side == whichLatura:
                    thisSideIsChecked = True
   
            if thisSideIsChecked:
                whichLatura = rand.randrange(1, 5)

        ind = 1 if whichShape == 1 else (2 if whichShape == 2 else 3)
        while ind <= stop: 
            if specs[ind + 1][1] == whichLatura: # e destul de complicat de desenat mai mult de un semicerc pe latura, nu crek pot rezolva problema
                foundGoodCoord = False
            ind += 2
        checkIt.append(whichLatura)

    if len(checkIt) == 4: # daca sunt 4 elemente in checkIt, inseamna ca nu exista nicio latura fara vreun semicerc pe ea
        return -1
    return whichLatura

def drawCircleOnSquare(area = 3601, specs = [60], stop = 0): # functia asta verifica toate cercurile desenate in patrat pana acum, ca sa determine
    latura = specs[0]                                        # cum sa deseneze cercul curent; parametrii reprezinta : 
                                                             # area = aria patratului, are default valoarea minima 3601
    foundGoodCoord = False                                   # specs = o lista care are diferite date despre forma actuala si semicercurile din ea; o descriere mai detaliata a parametrului specs e mai jos in functie
    radius = 0                                               # stop = ultimu index din lista specs, default e 0 pt ca specs are minim un element(dimensiunea laturei patratului) 
    startPoint = 0
    center = [0, 0]
    whichLatura = checkSide(specs, stop, 1)
    if whichLatura == -1:
        return stop

    # in while ul de mai jos, whichSide e garantat o latura pe care se poate desena
    foundGoodCoord = False
    while foundGoodCoord == False:
        foundGoodCoord = True
        radius = rand.randrange(30, int(latura / 2))
        startPoint = rand.randrange(60, int(latura))
        if whichLatura == 2 or whichLatura == 4: # daca e pe o latura laterala, coordonatele pt y sunt negative, testoasa incepe la (0, 0)
            startPoint *= -1 
        
        incompatible = True # urmeaza sa verific daca startPoint si radius sunt compatibile cu latura, adica daca cercul "intra" pe latura
                            # indicata de whichLatura
        while incompatible:
            incompatible = False
            if whichLatura == 1:
                if startPoint - 2 * radius < 0:
                    incompatible = True
            elif whichLatura == 2:
                if startPoint + 2 * radius > 0:
                    incompatible = True
            elif whichLatura == 3:
                if startPoint + 2 * radius > latura:
                    incompatible = True
            else:
                if startPoint - 2 * radius < -latura:
                    incompatible = True
            
            if incompatible: # daca valori actuale nu s ok, caut altele    
                radius = rand.randrange(30, int(latura / 2))
                if whichLatura == 1 or whichLatura == 2: # valorile minime si maxime pe care le poate lua sunt legate de felul in care turtle
                    startPoint = rand.randrange(60, int(latura))# deseneaza cercuri, se observa experimental cand rulezi programul
                else:
                    startPoint = rand.randrange(1, int(latura) - 60)

                if whichLatura == 2 or whichLatura == 4: # daca e pe o latura laterala, coordonatele pt y sunt negative                       # coordonatelor pt startPoint
                    startPoint *= -1

        if whichLatura == 1 : # determina centrul cercului pe care vrea sa l deseneze in functie de latura pe care se afla(testoasa merge mereu 
           center = [startPoint - radius, 0] #                                                                                 inainte)
        elif whichLatura == 2:
           center = [latura, startPoint - radius]
        elif whichLatura == 3:
            center = [startPoint - radius, -latura]
        else:
            center = [0, startPoint - radius]

        ind = 1
        while ind <= stop and foundGoodCoord == True: # lista specs o sa aiba pe fiecare pozitie impara o alta lista care are coordonatele x1, x2(sau y1, y2) ale unui cerc de
                                                      # pe patrat si pe fiecare pozitie para are o lista de forma [r, s], unde r e raza cercului si s e latura pe care se afla
            coords = specs[ind]
            extras = specs[ind + 1]
            if abs(radius - extras[0]) <= math.sqrt((coords[0] - center[0]) * (coords[0] - center[0]) + (coords[1] - center[1]) * (coords[1] - center[1])) \
               and math.sqrt((coords[0] - center[0]) * (coords[0] - center[0]) + (coords[1] - center[1]) * (coords[1] - center[1])) <= radius + extras[0]: # formula asta verifica daca doua cercuri se intersecteaza, scuze ca arata asa nasol
                foundGoodCoord = False;
            secondCenter = center # verific daca, de asemenea, si al doilea cerc se intersecteaza cu vreun cerc
            if whichLatura == 1:  # aici setez efectiv coordonatele
                secondCenter[1] = -latura
            elif whichLatura == 2:
                secondCenter[0] = 0
            elif whichLatura == 3:
                secondCenter[1] = 0
            else:
                secondCenter[0] = latura
                                                                                                                                                                                   # caracterul "\" e folosit ca sa lipeasca doua linii de cod
            if abs(radius - extras[0]) <= math.sqrt((coords[0] - secondCenter[0]) * (coords[0] - secondCenter[0]) + (coords[1] - secondCenter[1]) * (coords[1] - secondCenter[1])) \
               and math.sqrt((coords[0] - secondCenter[0]) * (coords[0] - secondCenter[0]) + (coords[1] - secondCenter[1]) * (coords[1] - secondCenter[1])) <= radius + extras[0]: # formula asta verifica daca doua cercuri se intersecteaza, scuze ca arata asa nasol
                foundGoodCoord = False;
            ind += 2
            
    # aici se incheie while u asta titanic cu conditia cu foundGoodCoord

    # aici desenez semicercurile
    specs.append(center) # folosesc append pt ca metoa append modifica si obiectul original din "specs"(e totuna cu variabile trimise prin referinta
    specs.append([radius, whichLatura]) # in C\C++; gen void foo(int& x)
    if whichLatura == 1:
        drawSemiCircle([startPoint, 0], radius, 270, 1) # argumentele sunt in ordinea asta: coordonatele unde sa deseneze, raza, unghiul testoasei
        center[1] = -latura                             # latura
        drawSemiCircle([startPoint, -latura], radius, 180, 1)  
        tl.right(270) # rotesc "testoasa" inapoi la rotatia normala
        specs.append(center)
        specs.append([radius, 3])
    elif whichLatura == 2:
        drawSemiCircle([latura, startPoint], radius, 0, 2)
        center[0] = 0
        drawSemiCircle([0, startPoint], radius, 180, 2)
        tl.right(180)
        specs.append(center)
        specs.append([radius, 4]) 
    elif whichLatura == 3:
        drawSemiCircle([startPoint, -latura], radius, 90, 3)
        center[1] = 0
        drawSemiCircle([startPoint, 0], radius, 180, 3)
        tl.right(90) # rotesc "testoasa" inapoi la rotatia normala
        specs.append(center)
        specs.append([radius, 1])
    else:
        drawSemiCircle([0, startPoint], radius, 180, 4)
        center[0] = latura
        drawSemiCircle([latura, startPoint], radius, 180, 4)
        specs.append(center)
        specs.append([radius, 2])
    return stop + 4

def drawCircleOnRect(area = 3601, specs = [60, 60], stop = 1): # variabilele au aceasi insemnatate ca la functia precedenta, doar ca specs are acum
    lungime = specs[0]                                         # 2 elemente minim, latimea si lungime(latimea e pe index 0 si lungimea pe index 1)
    latime = specs[1]

    minim = int(min(latime, lungime)) # raza unui semicerc nu poate fi, evident, mai mare ca minimul dintre lungime si latime
    foundGoodCoord = False
    radius = 0
    startPoint = 0
    center =[0, 0]
    whichLatura = checkSide(specs, stop, 2) # folosesc aceasi codificare pt laturi ca la patrat
    if whichLatura == -1:
        return stop

    while foundGoodCoord == False: # while ul asta o sa fie more or less identic cu cel de la patrat
        foundGoodCoord = True
        radius = rand.randrange(60, minim)
        startPoint = rand.randrange(60, minim)
        if whichLatura == 2 or whichLatura == 4: # daca e pe o latura laterala, coordonatele pt y sunt negative, testoasa incepe la (0, 0)
            startPoint *= -1 
        
        incompatible = True # urmeaza sa verific daca startPoint si radius sunt compatibile cu latura, adica daca cercul "intra" pe latura
                            # indicata de whichLatura
        while incompatible:
            incompatible = False
            if whichLatura == 1:
                if startPoint - 2 * radius < 0:
                    incompatible = True
            elif whichLatura == 2:
                if startPoint + 2 * radius > 0:
                    incompatible = True
            elif whichLatura == 3:
                if startPoint + 2 * radius > lungime:
                    incompatible = True
            else:
                if startPoint - 2 * radius < -latime:
                    incompatible = True
            
            if incompatible: # daca valori actuale nu s ok, caut altele    
                radius = rand.randrange(30, int(minim / 2))
                if whichLatura == 1 or whichLatura == 2: # valorile minime si maxime pe care le poate lua sunt legate de felul in care turtle
                    startPoint = rand.randrange(60, int(lungime) if whichLatura == 1 else int(latime))# deseneaza cercuri, se observa experimental cand rulezi programul
                else:
                    startPoint = rand.randrange(1, int(lungime) if whichLatura == 3 else int(latime) - 60)

                if whichLatura == 2 or whichLatura == 4: # daca e pe o latura laterala, coordonatele pt y sunt negative                       # coordonatelor pt startPoint
                    startPoint *= -1

        if whichLatura == 1 : # determina centrul cercului pe care vrea sa l deseneze in functie de latura pe care se afla(testoasa merge mereu 
           center = [startPoint - radius, 0] #                                                                                 inainte)
        elif whichLatura == 2:
           center = [lungime, startPoint - radius]
        elif whichLatura == 3:
            center = [startPoint - radius, -latime]
        else:
            center = [0, startPoint - radius]
        
        ind = 2
        while ind <= stop and foundGoodCoord == True: # lista specs o sa aiba pe fiecare pozitie para o alta lista care are coordonatele x1, x2(sau y1, y2) ale unui cerc de
                                                      # pe patrat si pe fiecare pozitie impara are o lista de forma [r, s], unde r e raza cercului si s e latura pe care se afla
            coords = specs[ind]
            extras = specs[ind + 1]
            if abs(radius - extras[0]) <= math.sqrt((coords[0] - center[0]) * (coords[0] - center[0]) + (coords[1] - center[1]) * (coords[1] - center[1])) \
               and math.sqrt((coords[0] - center[0]) * (coords[0] - center[0]) + (coords[1] - center[1]) * (coords[1] - center[1])) <= radius + extras[0]: # formula asta verifica daca doua cercuri se intersecteaza, scuze ca arata asa nasol
                foundGoodCoord = False;
            secondCenter = center # verific daca, de asemenea, si al doilea cerc se intersecteaza cu vreun cerc
            if whichLatura == 1:  # aici setez efectiv coordonatele
                secondCenter[1] = -latime
            elif whichLatura == 2:
                secondCenter[0] = 0
            elif whichLatura == 3:
                secondCenter[1] = 0
            else:
                secondCenter[0] = lungime
                                                                                                                                                                                   # caracterul "\" e folosit ca sa lipeasca doua linii de cod
            if abs(radius - extras[0]) <= math.sqrt((coords[0] - secondCenter[0]) * (coords[0] - secondCenter[0]) + (coords[1] - secondCenter[1]) * (coords[1] - secondCenter[1])) \
               and math.sqrt((coords[0] - secondCenter[0]) * (coords[0] - secondCenter[0]) + (coords[1] - secondCenter[1]) * (coords[1] - secondCenter[1])) <= radius + extras[0]: # formula asta verifica daca doua cercuri se intersecteaza, scuze ca arata asa nasol
                foundGoodCoord = False;
            ind += 2
            
    # aici se incheie while u asta titanic cu conditia cu foundGoodCoord

    # aici desenez semicercurile
    specs.append(center) # folosesc append pt ca metoa append modifica si obiectul original din "specs"(e totuna cu variabile trimise prin referinta
    specs.append([radius, whichLatura]) # in C\C++; gen void foo(int& x)
    if whichLatura == 1:
        drawSemiCircle([startPoint, 0], radius, 270, 1) # argumentele sunt in ordinea asta: coordonatele unde sa deseneze, raza, unghiul testoasei
        center[1] = -latime                             # latura
        drawSemiCircle([startPoint, -latime], radius, 180, 1)  
        tl.right(270) # rotesc "testoasa" inapoi la rotatia normala
        specs.append(center)
        specs.append([radius, 3])
    elif whichLatura == 2:
        drawSemiCircle([lungime, startPoint], radius, 0, 2)
        center[0] = 0
        drawSemiCircle([0, startPoint], radius, 180, 2)
        tl.right(180)
        specs.append(center)
        specs.append([radius, 4]) 
    elif whichLatura == 3:
        drawSemiCircle([startPoint, -latime], radius, 90, 3)
        center[1] = 0
        drawSemiCircle([startPoint, 0], radius, 180, 3)
        tl.right(90) # rotesc "testoasa" inapoi la rotatia normala
        specs.append(center)
        specs.append([radius, 1])
    else:
        drawSemiCircle([0, startPoint], radius, 180, 4)
        center[0] = lungime
        drawSemiCircle([lungime, startPoint], radius, 180, 4)
        specs.append(center)
        specs.append([radius, 2])
    return stop + 4

# functia asta doar apeleaza diverse functii ca sa deseneze o forma random de arie specificata
def drawRandomShape(area = 3601):
    whichShape = rand.randrange(1, 4) # ahem, din ce am citit in documentatie, randrange nu include si ultimu element(adica alege doar din 1, 2, 3)
    shapeSpecs = []
    #whichShape = 2
    if whichShape == 1:
        shapeSpecs = drawSquare(area)
    elif whichShape == 2:
        shapeSpecs = drawRect(area)
    else:
        shapeSpecs = drawRhombus(area)

    irregularities = rand.randrange(1, 4) # pt ca momentan lucrez doar cu patrulatere, selecteaza maxim 4 laturi pe care sa deseneze chestii in plus
    if whichShape == 1:
        howManySpecs = 0 
        while irregularities > 0: # deseneaza toate cercurile
            howManySpecs = drawCircleOnSquare(area, shapeSpecs, howManySpecs)
            irregularities -= 1
    elif whichShape == 2:
        howManySpecs = 1
        while irregularities > 0:
            howManySpecs = drawCircleOnRect(area, shapeSpecs, howManySpecs)
            irregularities -= 1

        
#filtrez inputu, in caz ca e scris aiurea si vreun caracter, ca sa nu dea erori de memorie
area = input("ce dimensiuni(minim 3601 plox): ")
while area.isdigit() == False or float(area) <= 3600:
    print("Aria poate fi doar un numar! No introduce caractere non-numerice!")
    area = input("ce dimensiuni(minim 3601 plox): ")

#inputu e default string, ii fac conversia la float ca sa pot aplica radacina patrata 
area = float(area)
tl.hideturtle()
drawRandomShape(area)


#ca sa nu mai dea probleme fereastra
tl.done()
 