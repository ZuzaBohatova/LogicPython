##Logik - Zuzana Bohatová - zimní semestr 2020/21 - NPRG030 Programování 1
import itertools, sys, time
def spravnyvstup(): #kontroluje správně zadaný vstup, jestli má délku 5, a obsahuje jen čísla od 0 do 7
    global kod      #zadaný kód od uživatele
    x = input("Zadejte 5-místný kód skládající se z číslic 0 až 7, např. 23534:")
    def nacticislo(m):
        while True:
            try:
                return int(m)
            except ValueError:
                print('To nebylo číslo.')
                spravnyvstup()
    nacticislo(x)
    x = list(x)
    if len(x)== 5:
        kod = (int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]))
        if(kod[0]//8)==0 and (kod[1]//8)==0 and (kod[2]//8)==0 and (kod[3]//8)==0 and (kod[4]//8)==0: return kod
        else:
            print("Kod má obsahovat pouze číslice 0 až 7, zadejte ho znovu")
            spravnyvstup()
    else:
        print("Kod má obsahovat přesně 5 míst")
        spravnyvstup()
opakovani = 0
def vyhodnoceni(tip, proti): #vyhodnocuje vypsáním X a O na kolik jsou shodné kombinace tip a proti
    global opakovani    #počet kolikrát jsme hádali
    vyhodnoceni, pom, odhad, srovnani =[], list(proti),list(tip), list(proti)
    if (odhad == proti) and (proti == list(kod)):   ##když se odhad rovná proti a proti se rovná kodu,
        opakovani += 1                              ##tak jste vyhráli
        print(tip, 5*["X"])
        print("Vyhrál jsem na", opakovani,". pokus, správná kombinace je:", odhad)
        time.sleep(1)
        sys.exit()
    else:
        for x in range(0,5):                #prirazuje do vyhodnoceni X
            if odhad[x]==proti[x]:
                vyhodnoceni.append("X")
                odhad[x],srovnani[x],pom[x]=-1,-2,-2    #meni hodnoty, abychom cislo ohodnocené X neohodnotili i O
        for z in range(0,5):                #prirazuje do hodnoceni O
            if odhad[z] in pom and z!= srovnani.index(odhad[z]):
                pom.remove(odhad[z])
                vyhodnoceni.append("O")
        if list(kod) == proti and (tuple(tip) in odhady) == False:
            if vyhodnoceni != []: odhady[tuple(tip)]=vyhodnoceni
            opakovani += 1
            print(tip, vyhodnoceni)
        if len(vyhodnoceni) == 5 and proti == list(kod): spravnebarvy.append(tip)   #vyhodnoceni delky 5 = správné barvy na spatnych pozicich
        if len(vyhodnoceni)!= 0 and ("X" in vyhodnoceni) == False and proti == list(kod):
            l = 0                           ##kdyz ve vyhodnoceni neni zadne X, tak zadne z cisel neni na spravne pozici
            for p in (a,b,c,d,e):           ##proto tyto cisla muzeme odstranit z listu a, b, c, d, e
                if tip[l] in p:
                    p.remove(tip[l])
                l+=1
        return vyhodnoceni

a,b,c,d,e = list(range(8)),list(range(8)),list(range(8)),list(range(8)),list(range(8))
##listy reprezentujici jednotlive pozice kombinace, obsahuji cisla ktera na nich mohou byt
pocet, odhady, moznosti, spravnebarvy = 0, {}, [], []   #pocet = součet delek hodnoceni z prvnich "barevnych" odhadu
##odhady - ukladaji se sem jiz vyhodnocene odhady, klic = odhad, hodnota = vyhodnoceni daneho odhadu
##moznosti = ukladaji se sem v listech mozne kombinace jednotlivych cisel podle ohodnocení
##spravnebarvy - uklozi se sem kombinace jejiz ohodnoceni ma delku 5

def kombsop(seznam, mist):      #vytvari kombinace s opakovanim
    if mist == 1: a = [[i] for i in seznam]
    else: a = list(itertools.combinations_with_replacement(seznam, mist))
    return a

def Barvy(v,u,x,y,z):       #uskutecnuje pocatecni 4 "barevne" tahy a vyvozuje z nich dusledky
    global a,b,c,d,e,pocet,spravnebarvy
    odhad, reakce =(v,u,x,y,z),vyhodnoceni([v,u,x,y,z],list(kod))   #odhad = hadany tah, reakce = jeho vyhodnoceni
    pocet+= len(reakce)                                 #pricita delku reakce k promenne pocet 
    if pocet == 5 and odhad != (6,6,6,7,7):             #odstrani zbyla cisla ze seznamu a,b,c,d,e 
        for j in (a,b,c,d,e): del(j[(j.index(z+1)):])   
    if len(reakce) != 0:                                
        moznosti.append(kombsop([v,z],len(reakce)))     #pridava do moznosti kombinace 
        if reakce==["X"]:                               #kdyz je reakce jen X, muzeme odstranit z a,b,c,d,e
            for w in (a,b,c): w.remove(odhad[4])        #prvky ktere jsou v kombinaci ale nelezi na danych pozicich
            for i in (d,e): i.remove(odhad[0])
        elif reakce==["X","X"]:                         #kdyz je reakce XX, muzeme z d,e odstranit prvky ktere
            for w in (d,e): w.remove(odhad[0])          #nelezi na danem miste
    else:                                               
        for i in (a,b,c,d,e):                           #kdyz je reakce prazdna, vime ze zadne z cisel nelezi v hledane kombinaci
            for w in range (0,5):
                if odhad[w] in i: i.remove(odhad[w])
    if pocet == 5: return True                          #kdyz je pocet 5, mame jiz vsechny barvy a muzeme tuto funkci ukoncit
    if odhad == (6,6,6,7,7):                            #prosli jsme jiz vsechny barvy a pocet stale neni 5
        if pocet == 2:                                  
            for klic in odhady: vyhodnoceni(5*[klic[4]], list(kod)) #kdyz pocet = 2, je jen jedna varianta 
        klice = []
        for klic in odhady:klice.append(klic)
        for p in range(0,len(klice)-1):                 #radi odhady podle delky vyhodnoceni, od nejmensiho k nejvyssimu
            if len(odhady[klice[p]])>len(odhady[klice[p+1]]): klice[p], klice[p+1]=klice[p+1], klice[p]
        if pocet == 3:                                  #rozlisuje varianty pro pocet = 3
            if len(odhady[klice[0]]) == 1:
                odhad = [klice[1][4],klice[1][4],klice[1][4],klice[1][4],klice[0][4]]
                if len(vyhodnoceni(odhad, list(kod))) != 5: odhad = [klice[1][4],klice[0][0],klice[1][4],klice[1][4],klice[1][4]]
                else:return True
            elif len(odhady[klice[0]]) == 3:
                odhad = 5*[klice[0][0]]
                if len(vyhodnoceni(odhad, list(kod))) != 5: odhad = [klice[0][4],klice[0][4],klice[0][0],klice[0][4],klice[0][4]]
                else:return True
        if pocet == 4:                                  #rozlisuje varianty pro pocet = 4
            if len(odhady[klice[0]]) == 4:
                odhad = [klice[0][4],klice[0][0],klice[0][4],klice[0][0],klice[0][4]]
                if len(vyhodnoceni(odhad,list(kod)))!=5:odhad = [klice[0][0],klice[0][0],klice[0][0],klice[0][4],klice[0][0]]
                else:return True
            elif len(odhady[klice[0]]) == 2:
                odhad=[klice[0][4],klice[1][4],klice[0][4],klice[0][4],klice[1][4]]
                pom = len(vyhodnoceni(odhad, list(kod)))
                if pom==4:
                    odhad=[klice[1][4],klice[0][4],klice[1][4],klice[0][4],klice[1][4]]
                    if len(vyhodnoceni(odhad,list(kod)))!=5:
                        odhad=[klice[0][4],klice[1][4],klice[0][4],klice[1][0],klice[0][4]]
                    else:return True
                elif pom==3:
                    odhad=[klice[1][0],klice[0][4],klice[0][4],klice[1][0],klice[0][4]]
                    if len(vyhodnoceni(odhad,list(kod)))!=5: odhad=[klice[0][0],klice[1][4],klice[1][4],klice[0][4],klice[1][4]]
                    else: return True
                elif pom==2:odhad=[klice[1][4],klice[0][0],klice[1][4],klice[0][0],klice[1][4]]
                else:return True
            elif len(odhady[klice[1]]) == 1:
                odhad = [klice[0][0],klice[1][0],klice[2][4],klice[2][4],klice[2][4]]
                pom = len(vyhodnoceni(odhad, list(kod)))
                if pom == 3: odhad = [klice[2][4],klice[2][4],klice[1][4],klice[2][4],klice[0][4]]
                elif pom == 4:
                    odhad = [klice[2][4],klice[2][4],klice[0][0],klice[2][4],klice[1][4]]
                    if len(vyhodnoceni(odhad, list(kod))) != 5:odhad = [klice[2][4],klice[2][4],klice[0][4],klice[2][4],klice[1][0]]
                    else:return True
                else:return True
            elif len(odhady[klice[1]]) == 3:
                odhad = [klice[1][0],klice[1][0],klice[0][0],klice[1][0],klice[1][0]]
                pom = len(vyhodnoceni(odhad, list(kod)))
                if pom == 1: odhad = [klice[0][4],klice[1][4],klice[1][4],klice[1][0],klice[1][4]]
                elif pom == 2: odhad = [klice[0][0],klice[1][4],klice[1][4],klice[1][0],klice[1][4]]
                elif pom == 4: odhad = [klice[1][0],klice[1][0],klice[1][0],klice[0][4],klice[1][0]]
                else:return True
        vyhodnoceni(odhad, list(kod))
        return True
    Barvy(v+2,u+2,x+2,y+2,z+2)
    
def KombiBarev():       
    kombinace, kombinacebarev, mista, shoda = [], [], [], []
    for f in range(0,len(moznosti)):
        for t in moznosti[f]: moznosti[f][moznosti[f].index(t)] = list(t)
    for x in moznosti[0]: #vytvari kombinace z listu moznosti
        for i in range(0,len(x)): kombinacebarev.append(x[i])
        for z in moznosti[1]:
            for y in range(0,len(z)): kombinacebarev.append(z[y])
            if len(moznosti) == 2:
                kombinace.append(list(kombinacebarev))
                del(kombinacebarev[(5-len(z)):5])
            else:
                for w in moznosti[2]:
                    for u in range(0,len(w)):
                        kombinacebarev.append(w[u])
                    if len(moznosti) == 3:
                        kombinace.append(list(kombinacebarev))
                        del(kombinacebarev[(5-len(w)):5])
                    else:
                        for r in moznosti[3]:
                            for s in range(0,len(r)):
                                kombinacebarev.append(r[s])
                            kombinace.append(list(kombinacebarev))
                            del(kombinacebarev[(5-len(r)):5])
                        del(kombinacebarev[(5-len(w)-len(r)):5])
                if len(moznosti)==3: del(kombinacebarev[(5-len(z)-len(w)):5])
                else:del(kombinacebarev[(5-len(z)-len(w)-len(r)):5])
        kombinacebarev.clear()
    for j in a:
        for k in b:                         ##vytvari kombinace z listu a, b, c, d, e
            for l in c:
                for m in d:
                    for n in e:
                        g =[j,k,l,m,n]
                        g.sort()
                        mista.append(g)
    for komb in kombinace:                  ##porovnava listy kombinace a mista a shodné kombinace pridava do shody
        if komb in mista: shoda.append(komb)
    NajdiBarvy(shoda)       
    return

permutace = []
def VytvorPermutace(prvky, v):      ##vytvari permutace
    global permutace
    if prvky==[]:           #do listu permutace priklada jen ty permutace, ktere jeste v listu nejsou
        if (v in permutace) == False:   #a pouze ty permutace, které odpovídají umistenim cisel listy a,b,c,d,e
            if v[0] in a and v[1] in b and v[2] in c and v[3] in d and v[4] in e: permutace.append(v)
    else:
        for i in range (0, len(prvky)):
            VytvorPermutace(prvky[:i]+prvky[i+1:], v+[prvky[i]] )        

def NajdiBarvy(shoda):      ##prochází všechny prvky a hledá ty, které odpovídají dosavadním odhadům a jeich hodnoceni
    for shod in shoda:          
        delka, h = 0, True
        for odhad, hodnoceni in odhady.items():
            if len(vyhodnoceni(odhad,shod))!=len(hodnoceni):
                h = False
            delka +=1
        if h == True and delka == len(odhady): Pozice(shod)
##kdyz vsechny odhady odpovidaji tak funkce pozice vytvori permutace daneho odhadu
            
def Pozice(spravne):        #vytvari permutace daneho odhadu a testuje ktery z nich odpovida hodnocenim vsem predchozim odhadum
    VytvorPermutace(spravne, [])
    for p in permutace:
        pom, r = True, 0
        for odhad, hodnoceni in odhady.items():
            if vyhodnoceni(odhad, p) != hodnoceni: pom = False
            r +=1
        if pom == True and r == len(odhady):        #pokud odhad odpovida vyhodnoctiho, pokud jsme nevyhrali, tak se celá funkce opakuje
            if len(vyhodnoceni(p, list(kod))) != 5: Pozice(spravne)    
                           
print("Pravidla hry: Zadáte pěticiferné číslo a program se ho snaží uhodnout, každý tip se ohodnotí kombinací X a O, kde X znamená správné číslo na správném místě a O znamená správné číslo, ale na špatném místě.")
spravnyvstup()
Barvy(0,0,0,1,1)
if spravnebarvy == []:
    KombiBarev()
else: Pozice(spravnebarvy[0])


