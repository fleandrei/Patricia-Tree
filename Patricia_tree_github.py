#-*- coding:Utf-8 -* 
'''D={1:[[1,0,0,1,1],2,0,0], 2:[[1,0,0,0,1],0,0,1]}

print(D[1][0])
print(D[D[1][1]])'''

import random

def gene_elem(nb_bit):# Génére aléatoirement une liste de "nb_bit" bits
    L=[]
    for i in range(nb_bit):
        L.append(random.randint(0,1))
    return L
def gene_alea_list(nb_list,nb_bit): #Génére aléatoirement une liste de "nb_list" liste de "nb_bit" éléments
    L=[]
    i=0
    while(i < nb_list):
        l=[]
        for j in range(nb_bit):
            l.append(random.randint(0,1))
        if(l not in L):
            L.append(l)
            i=i+1
    return L

def arbr_from_list(L):  # Renvoie un arbre Patricia à partir de la liste L
    AP=init_arbre(L[0])
    for i in range(1,len(L)):
        add(AP,L[i])
        #affiche(AP)

    return AP

def affiche(AP):
    for cle,val in AP.items():
        print(str(cle)+" : "+str(val))
    print("\n")

def init_arbre(L):  #Initialise un arbre Patricia (sous forme de dictionnaire) à partir de la liste L
    D={}
    D[0]=[0,0,L,0,0,0,"N","N",0,[0]] # Le 8ème élèment du la liste est une liste d'indice qui n'est présente que sur le premier élément de l'arbre.
    return D

def set_indice(AP): # Renvoie un indice qui n'a pas encore été utilisé dans l'arbre "AP" et qui peut donc servir pour un nouvel élément à insérer.
    L=AP[0][9]  
    if len(AP[0][9])>1:
        return AP[0][9].pop(-1)
    else:
        #print(AP[0][9][0])
        AP[0][9][0]=AP[0][9][0] + 1
        #print(AP[0][9][0])
        return AP[0][9][0]

def compar_list(L1,L2,ini): #Compare les deux listes à partir de l'indice "ini" et renvoie l'indice à partir duquel elles ne sont plus égales. Renvoie -1 si elles sont égales
    N=len(L1)
    i=ini
    #print(L1)
    #print(L2)
    while(i < N and L1[i]==L2[i]  ):
        #print("i="+str(i))
        #print(L1[i])
        #print(L2[i])
        i=i+1
    #print(i)
    
    if i==N:
        return -2
    elif i==ini:
        return ini+1
    else:
        return i
    


def remonte_lien(AP, indice): # Remonte l'arbre afin de trouver un éventuel noeud sur lequel la feuille d'indice "indice" pourrait pointer
    bitnum=AP[indice][1]
    current=indice
    List=AP[current][2]
    l=List[:]
    continu=True
    if List[bitnum]==1: # Si le bit d'indice bitnum est un 1, alors on cherche un élément dans le graph qui est identique à "List" jusqu'au bit d'indice bitnum(mais ce dernier doit être égal à 0) 
        l[bitnum]=0  
        while current != 0 and continu:
            current = AP[current][5] #current prend la valeure de son parent
            if l[0:bitnum]==AP[current][2][0:bitnum]:
                AP[indice][3]=current
                if AP[current][8] != current:
                    print("Problème: Plusieurs feuilles relatives pointent vers current")
                    print(AP[current][8])
                    print("\n")
                AP[current][8]=indice
                continu=False

    elif List[bitnum]==0:#Si le bit d'indice bitnum est un 0, alors on cherche un élément dans le graph qui est identique à "List" jusqu'au bit d'indice bitnum(mais ce dernier doit être égal à 1)
            l[bitnum]=1
            while current != 0 and continu:
                current=AP[current][5]
                if l[0:bitnum]==AP[current][2][0:bitnum]:
                    AP[indice][4]=current
                    if AP[current][8] != current:
                        print("Problème: Plusieurs feuilles relatives pointent vers current")
                        print(AP[current][8])
                        print("\n")
                    AP[current][8]=indice
                    continu=False

'''add permet d'ajouter un élèment de liste 'Liste' dans l'arbre Patricia 'AP' '''
def add(AP,List):
    current=0#indice dans l'arbre (dictionaire) du noeud sur lequel on se trouve
    bitnum=0#numéros du bit à tester
    #preced=0indice dans l'arbre du précédent noeud
    #inser=[current,bitnum,List,current,current,current]
    #preced=-1
    new_indice=set_indice(AP) #indice que va avoir l'élément que l'on va ajouter
    continu=True
    while(continu):
        L=AP[current][2] #Liste du noeud courrant
       # print(List)
        #print(L)
        if List[AP[current][1]]==0: #Si le bit courant du noeud courrant est égale à 0, on regarde le fils gauche
            left=AP[current][3] #indice du fils gauche
            if ((AP[current][1]>=bitnum) and (bitnum < len(List)-1)): #Si indice du bit de comparaison du noeud actuel est plus petit que celui du noeud qu'on veut insérer, alors on ne met plus à jour "bitnum" car il a atteint sa valeure définitive
                bitnum=compar_list(AP[current][2], List, bitnum) # bitnum est égal au nombre de bits que la liste à insérer et la liste du noeud courrant ont en commun en partant du début.
         #   print("\n bitnum="+str(bitnum))
            if bitnum <0:
                    print("L'élément à insérer est déjà dans l'arbre")
                    return -1
            
            if AP[current][6]=="N": #Si le noeud courrant ne pointe pas (vers la gauche) vers des élèments d'indice de comparaison supérieur au sien 
                AP[current][6]="L"
                if AP[AP[current][3]][8]==current:
                    AP[AP[current][3]][8]=AP[current][3] #Si current avait pour fils gauche un noeud plus haut dans l'arbre, alors ce dernier ne considère plus le noeud courrant comme pointant sur lui 
                AP[current][3]=new_indice
                if bitnum >= len(List):
                    print("len(List) pour left="+str(len(List)))
                    AP[new_indice]=[new_indice, bitnum-1, List, new_indice, new_indice, current, "N", "N",new_indice]
                    continu=False
                #print("bitnum="+str(bitnum))
                elif bitnum <len(List):
                    AP[new_indice]=[new_indice, bitnum, List, new_indice, new_indice, current, "N", "N",new_indice]
                    remonte_lien(AP, new_indice) #Vérifie si l'élément que l'on a inséré peut pointer vers un précédent noeud de l'arbre.
                    continu=False
                else:
                    print("Problème left ajout feuile\n")
                    continu=False
            elif bitnum < AP[left][1]: # Cas où on doit insérer notre élèment entre deux noeuds.
                l=AP[left][2]  #liste du noeud de gauche
                AP[current][3]=new_indice
                #print("\n bitnum="+str(bitnum))
                if l[bitnum]==0:
                    AP[new_indice]=[new_indice, bitnum, List, left, new_indice, current,"L","N",new_indice]
                else:
                    AP[new_indice]=[new_indice, bitnum, List, new_indice, left, current,"N","R",new_indice]
                AP[left][5]=new_indice
                continu=False
            elif (bitnum>=AP[left][1] and AP[current][6]!="N"): # On ne peut pas encore insérer notre élèment. On parcour le graph jusqu'à l'élément suivant. 
                current=left
                #print("current ="+str(current))
            else:
                print("\n probl left\n")
        elif List[AP[current][1]]==1:  #Si le bit d'indice bitnum est égale à 1, on regarde le fils droite. Le code à l'intérieur du "elif" est très similaire(même symétrique) à celui présent dans le premier "if"
            right=AP[current][4] #indice du fils droit
            if AP[current][1]>=bitnum:
                bitnum=compar_list(AP[current][2], List, bitnum)
            #print("\n bitnum="+str(bitnum))
            if bitnum <0:
                    print("L'élément à insérer est déjà dans l'arbre\n")
                    return -1
            if AP[current][7]=="N":
                AP[current][7]="R"
                #print("bitnum="+str(bitnum))
                if AP[AP[current][4]][8]==current:
                    AP[AP[current][4]][8]=AP[current][4] #Si current avait pour fils droit un noeud plus haut dans l'arbre, alors ce dernier ne considère plus le noeud courrant comme pointant sur lui 
                AP[current][4]=new_indice
                if bitnum >= len(List): #Si le noeud courrant ne pointe pas vers des élèments d'indice de comparaison supérieur au sien(c'est comme si on atteint une feuille d'un arbre, mais qui peut néanmoins pointer vers un élèment plus haut de l'arbre)
                     #print("len(List) pour right ="+str(len(List)))
                     AP[new_indice]=[new_indice, bitnum-1, List, new_indice, new_indice, current, "N", "N",new_indice]
                     continu=False
                elif bitnum <len(List):
                    AP[new_indice]=[new_indice, bitnum, List, new_indice, new_indice, current, "N", "N",new_indice]
                    remonte_lien(AP, new_indice)#Vérifie si l'élément que l'on a inséré peut pointer vers un précédent noeud de l'arbre.
                    continu=False
                else:
                    print("Problème right ajout feuille\n")
                    continu=False
            elif bitnum < AP[right][1]:
                l=AP[right][2]  #liste du noeud de droite
                AP[current][4]=new_indice
                #print("\n bitnum="+str(bitnum))
                if l[bitnum]==0:
                    AP[new_indice]=[new_indice, bitnum, List, right, new_indice, current,"L","N",new_indice]
                else:
                    AP[new_indice]=[new_indice, bitnum, List, new_indice, right, current,"N","R",new_indice]
                AP[right][5]=new_indice
                continu=False
            elif (bitnum>=AP[right][1] and AP[current][7]!="N"):
                current=right
                #print("current ="+str(current))
            else:
                print("\n probl right \n")

    
    return new_indice
        

def find(AP, List): #Cherche "List" dans le graph "AP": Renvoie son indice si l'élément se trouve dans AP et -1 si il ne s'y trouve pas.
    current=0
    bitnum=0
    sizelist=len(List)
    continu=True
    while(continu):
        bitnum=AP[current][1] 
        if(List[bitnum]==0): # Si le bit de comparaison est 0 alors:
            left=AP[current][3] #On regarde la fils de gauche
            if(AP[current][6]=="L"): # Si le noeud courrant admet un fils gauche d'indice de comparaison plus grand que le sien
                current=left     # On se déplace dans le fils gauche           
            elif(AP[current][6]=="N" and left==current): #Si on atteint un noeud qui n'a pas de fils gauche
                if(AP[current][2][:]==List[:]): #Si c'est le noeud recherché: 
                    return current #on renvoie son indice dans le graph
                else:
                    return -1 #Sinon cela veut dire que l'élément recherché ne se trouve pas dans l'arbre et on renvoie -1
            elif(AP[current][6]=="N" and left!=current): # Si on est dans une feuille relative c-à-d qu'elle pointe vers un noeud de plus petit indice de comparaison. 
                if(AP[current][2][:]==List[:]): #On teste d'abord si le noeud courrant est l'élément recherché
                    return current
                elif(AP[left][2][:]==List[:]): # Si ce n'est pas le cas, on regarde si le fils gauche sur lequel pointe le noeud courrant est l'élément recherché 
                    return left
                else:
                    return -1 #Sinon, cela veut dire que l'élément recherché n'est pas dans l'arbre
        elif(List[bitnum]==1): #Si le bit de comparaison est un 1: Le raisonnement est annalogue au cas précedent 
            right=AP[current][4]
            if(AP[current][7]=="R"):
                current=right                
            elif(AP[current][7]=="N" and right==current):
                if(AP[current][2][:]==List[:]):
                    return current
                else:
                    return -1
            elif(AP[current][7]=="N" and right!=current):
                if(AP[current][2][:]==List[:]):
                    return current
                elif(AP[right][2][:]==List[:]):
                    return right
                else:
                    return -1

'''Cette fonction supprime l'élément correspondant à liste envoyée en deuxième paramètre. Si cet élément n'est pas dans l'arbre, alors elle renvoie -1; sinon elle
renvoie la lise qui a été supprimée (la même que celle passée en paramètre)'''
def pop(AP,List):
    numpop=find(AP,List)
    if (numpop<0):
        print("Error: This element is not in our Patricia Tree\n")
        return -1
    else:
        parent=AP[numpop][5]
        indpar=AP[parent][1]
        res=AP[numpop][2]
        if AP[numpop][6]=="N" and AP[numpop][7]=="N": #si il s'agit d'une feuille abssolue
            AP[AP[numpop][3]][8]=AP[numpop][3]
            AP[AP[numpop][4]][8]=AP[numpop][4]
            if AP[parent][3]==numpop: #Si l'élément à enlever correspond au fils gauche de son parent 
                AP[parent][6]="N"
                AP[parent][3]=parent
                if AP[parent][2][indpar] == 1: #si le bit de comparaison du parent est 1, alors le parent ne peut pointer vers le haut de l'arbre que par la gauche
                    remonte_lien(AP, parent)
               
            elif numpop==AP[parent][4]: #Si l'élément à enlever correspond au fils droit de son parent
                AP[parent][7]="N"
                AP[parent][4]=parent
                if AP[parent][2][indpar] == 0: #si le bit de comparaison du parent est 0, alors le parent ne peut pointer vers le haut de l'arbre que par la droite
                    remonte_lien(AP, parent)

            AP[0][9].append(numpop)# On ajoute dans la liste des indice disponibles (9ème élèment de la racine de l'arbre) l'indice de l'élèment que l'on a supprimé afin de le recycler
            del AP[numpop]
        elif AP[numpop][6]=="L" and AP[numpop][7]=="N": #Si l'élément à supprimer a un fils gauche mais pas de fils droit
            AP[AP[numpop][4]][8]=AP[numpop][4]
            if AP[parent][3]==numpop: #Si l'élément à enlever correspond au fils gauche de son parent
                AP[parent][3]=AP[numpop][3]
                AP[AP[numpop][3]][5]=parent
            elif numpop==AP[parent][4]: #Si l'élément à enlever correspond au fils droit de son parent
                AP[parent][4]=AP[numpop][3]
                AP[AP[numpop][3]][5]=parent
            indpoi=AP[numpop][8] #indpoi: indice de l'élément qui pointe vers numpop tout en étant plus bas dans l'arbre
            if indpoi != numpop:
                remonte_lien(AP,indpoi)
            AP[0][9].append(numpop)# On ajoute dans la liste des indice disponibles (9ème élèment de la racine de l'arbre) l'indice de l'élèment que l'on a supprimé afin de le recycler
            del AP[numpop]
        elif AP[numpop][6]=="N" and AP[numpop][7]=="R": #Si l'élément à supprimer a un fils droit mais pas de fils gauche
            AP[AP[numpop][3]][8]=AP[numpop][3]
            if AP[parent][3]==numpop: #Si l'élément à enlever correspond au fils gauche de son parent
                AP[parent][3]=AP[numpop][4]
                AP[AP[numpop][4]][5]=parent
            elif numpop==AP[parent][4]: #Si l'élément à enlever correspond au fils droit de son parent
                AP[parent][4]=AP[numpop][4]
                AP[AP[numpop][4]][5]=parent
            indpoi=AP[numpop][8]
            if indpoi != numpop:
                remonte_lien(AP,indpoi)
            AP[0][9].append(numpop)# On ajoute dans la liste des indice disponibles (9ème élèment de la racine de l'arbre) l'indice de l'élèment que l'on a supprimé afin de le recycler
            del AP[numpop]
        elif AP[numpop][6]=="L" and AP[numpop][7]=="R":#Si l'élèment à supprimer a 2 fils
            indpoi=AP[numpop][8] #indpoi: indice de l'élément qui pointe vers numpop tout en étant plus bas dans l'arbre
            parent_poi=AP[indpoi][5] #parent_poi est le parent de indpoi
            AP[numpop][8]=numpop
            ind_par_poi=AP[parent_poi][1] #numéro du bit de comparaison du parent de indpoi
            '''ASTUCE:On va supprimer la feuille d'indice indpoi et on va remplacer la liste de l'élément à supprimer(d'indice numpop) par la liste de indpoi'''
            if AP[parent_poi][3]==indpoi: #Si l'élément indpoi à enlever correspond au fils gauche de son parent 
                AP[parent_poi][6]="N"
                AP[parent_poi][3]=parent_poi
                if AP[parent_poi][2][ind_par_poi] == 1: #si le bit de comparaison du parent est 1, alors le parent_poi ne peut pointer vers le haut de l'arbre que par la gauche
                    remonte_lien(AP, parent_poi)
               
            elif indpoi==AP[parent_poi][4]: #Si l'élément indpoi à enlever correspond au fils droit de son parent
                AP[parent_poi][7]="N"
                AP[parent_poi][4]=parent_poi
                if AP[parent_poi][2][ind_par_poi] == 0: #si le bit de comparaison du parent_poi est 0, alors le parent ne peut pointer vers le haut de l'arbre que par la droite
                    remonte_lien(AP, parent_poi)
            AP[numpop][2]=AP[indpoi][2][:]
            AP[0][9].append(indpoi)
            del AP[indpoi]
            #res=indpoi

            
    return res
        
                 
             
             
    
'''def verif(AP):
    N=len(AP)
    t=-1
    for i in range(N):
        if (AP[i][6] =="L") and (AP[i][7] == "R") and (AP[i][8]==i):
            t=i
    return t'''

def fonction_test(AP):
    N=len(AP) #Taille de l'arbre
    n=len(AP[1][2]) #Nombre de bits dans un élément
    '''Test de la fonction find()'''
    print(" We check if following elements are contained in ou Patricia Tree:")
    print("- find(AP,"+str(AP[N//2][2])+"):")
    ind=find(AP,AP[N//2][2])
    if(ind==-1):
        print("This element isn't contained in the Patricia Tree.\n")
    else:
        print("the following element "+str(AP[N//2][2])+" can be found at the index: "+str(ind)+" of the list coding for the tree\n")

    l=gene_elem(n)
    print("- find(AP,"+str(l)+"):")
    ind=find(AP,l)
    if(ind==-1):
        print("This element is not in the Patricia Tree.\n")
    else:
        print("the following element "+str(l)+" can be found at the index: "+str(ind)+" of the list coding for the tree\n")

    l=gene_elem(n)
    print("- find(AP,"+str(l)+"):")
    ind=find(AP,l)
    if(ind==-1):
        print("This element is not in the Patricia Tree.\n")
    else:
        print("the following element "+str(l)+" can be found at the index: "+str(ind)+" of the list coding for the tree\n")
    print("print(AP):\n")
    affiche(AP)
    '''Let's check the pop() function\n ATTENTION: La fonction pop() est suceptible de changer les indices de certains éléments (mais ce n'est pas grave en théorie)\n'''
    print("Let's now check the pop() function:\n")
    print("- pop(AP,"+str(AP[N//2][2])+") :")
    l=pop(AP,AP[N//2][2])
    if l != -1:
        print("element "+str(l)+" has been erased from the list coding for the Patricia tree.\n")
    print("- pop(AP,"+str(AP[N-2][2])+") :")
    l2=[]
    l2[:]=pop(AP,AP[N-2][2])
    if( l2 != -1):
        print("element "+str(l2)+" has been erased from the list coding for the Patricia tree.\n")
    l=gene_elem(n)
    print("- pop(AP,"+str(l)+") :")
    if(pop(AP,l) != -1):
        print("element "+str(l)+" has been erased from the list coding for the Patricia tree.\n")
    print("print(AP):\n")
    affiche(AP)
    '''Teste de la fonction add()'''
    print("Let's now check the add()function:\n")
    print("- add(AP,"+str(l)+") :")
    ind=add(AP,l)
    if ind != -1:
        print("Element "+str(l)+" has been added in the Patricia tree at index "+str(ind)+".\n")
        
    print("- add(AP,"+str(l2)+") :")
    ind=add(AP,l2)
    if ind != -1:
        print("Element "+str(l2)+" has been added in the Patricia tree at index "+str(ind)+".\n")    
    print("Let's print the Patricia tree :\n")
    affiche(AP)




'''Test de L'implémentation:'''
'''Génére aléatoirement une Liste de listes représenant les éléments de l'arbre      Patricia: En premier argument: le nombre d'éléments de l'arbre(sachant qu'on peut on
(rajout par la suite) et en deuxième argument: Le nombre de bit par élément.
Attention: Tous les éléments doivent avoir le même nombre de bits.'''
Lf=gene_alea_list(10,8)
'''Crée à partir de la liste crée ci-dessus, un Arbre Patricia "AP" implémenté sous la forme d'un dictionnaire.'''
AP=arbr_from_list(Lf)
print("This is a Patricia tree generated randomly: \n ")
affiche(AP) #Affiche l'Arbre Patricia
'''Fonction qui va afficher un petit test des trois fonctions principales: add(), pop(), find() '''
fonction_test(AP)






'''       
Arbre_Pat=init_arbre([0,1,1])
print(Arbre_Pat)
add(Arbre_Pat,[0,1,0])
print(Arbre_Pat)
print(compar_list([1,1,1],[1,0,1],0))
print(set_indice(Arbre_Pat))
print(Arbre_Pat)
add(Arbre_Pat,[0,0,1])
print(Arbre_Pat)
add(Arbre_Pat,[0,0,0])
print(Arbre_Pat)
add(Arbre_Pat,[1,1,0])
affiche(Arbre_Pat)
add(Arbre_Pat,[1,0,1])
affiche(Arbre_Pat)
print("\n \n")
print(find(Arbre_Pat,[1,0,0]))
print(find(Arbre_Pat,[0,1,0]))
print(find(Arbre_Pat,[1,1,0]))
print(pop(Arbre_Pat,[1,1,0]))
affiche(Arbre_Pat)
add(Arbre_Pat,[1,1,1])
affiche(Arbre_Pat)
print(pop(Arbre_Pat,[1,1,0]))
print(pop(Arbre_Pat,[0,0,1]))
affiche(Arbre_Pat)
print("\n \n \n \n \n \n \n ")
L=[1,0,0,1,1]
A_P=init_arbre(L)
for i in range(len(L)):
    l=L[:]
    if l[i]==1:
        l[i]=0
    else:
        l[i]=1  
    new=add(A_P,l)
    print("num du nouveau indice:"+str(new))
    print(A_P)
    print("\n \n \n \n")
L2=[1,0,0,1,1]
AP2=init_arbre(L2)
LL=[[0,1,0,0,0],[0,0,1,0,1],[0,0,0,1,1],[1,0,0,1,0],[0,1,0,0,1],[0,0,0,0,1],[0,1,1,1,0]]
for l in LL:
    add(AP2,l)
    print(AP2)
'''

'''print(find(AP,[1,0,0,1,0,0,1,1]))
print(find(AP,[1,1,0,1,0,0,1,1]))
print(find(AP,[1,0,1,1,0,1,0,1]))
print(find(AP,[1,1,0,1,1,0,1,0]))
print("test="+str(verif(AP)))
print(pop(AP,[1,0,0,1,0,0,1,1]))
print(pop(AP,[1,1,0,1,0,0,1,1]))
print(pop(AP,[1,0,1,1,0,1,0,1]))
print(pop(AP,[1,1,0,1,1,0,1,0]))
print(pop(AP, AP[2][2]))
affiche(AP)
print(add(AP,[1,1,0,1,1,0,1,0]))
print(find(AP,[1,0,0,1,0,0,1,1]))
print(find(AP,[1,1,0,1,0,0,1,1]))
print(find(AP,[1,0,1,1,0,1,0,1]))
print(find(AP,[1,1,0,1,1,0,1,0]))
print(find(AP, AP[7][2]))'''

