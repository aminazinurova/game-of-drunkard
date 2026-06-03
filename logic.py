class Node:    
    def __init__(self, znach):
        self.znach = znach  
        self.next = None    

class Ochered:    
    def __init__(self):
        self.nachalo = None  
        self.konec = None    
        self.razmer = 0      

    def dobavit(self, znach):
        novy = Node(znach)
        if self.konec is None:
            self.nachalo = novy
            self.konec = novy
        else:
            self.konec.next = novy
            self.konec = novy
        self.razmer += 1

    def ubrat(self):
        if self.nachalo is None:
            return None
        znach = self.nachalo.znach
        self.nachalo = self.nachalo.next
        if self.nachalo is None:
            self.konec = None
        self.razmer -= 1
        return znach

    def pusta(self):
        return self.nachalo is None

    def v_spisok(self):
        res = []
        tek = self.nachalo
        while tek is not None:
            res.append(tek.znach)
            tek = tek.next
        return res

def sravnit(karta1, karta2):
    if karta1 == 0 and karta2 == 9:
        return 1
    if karta1 == 9 and karta2 == 0:
        return 2
    
    if karta1 > karta2:
        return 1
    return 2

def hod(que1, que2):
    k1 = que1.ubrat()
    k2 = que2.ubrat()
    winner = sravnit(k1, k2)

    if winner == 1:
        que1.dobavit(k1)
        que1.dobavit(k2)
    else:
        que2.dobavit(k1)
        que2.dobavit(k2)
        
    if que1.pusta():
        return "second"
    if que2.pusta():
        return "first"
    return None

def zapustit_igru(spisok1, spisok2, max_hodov=1000000):
    koloda1 = Ochered()
    koloda2 = Ochered()
    
    for k in spisok1:
        koloda1.dobavit(k)
    for k in spisok2:
        koloda2.dobavit(k)
        
    for nomer_hoda in range(1, max_hodov + 1):
        rez = hod(koloda1, koloda2)
        if rez:
            return rez, nomer_hoda
            
    return "botva", max_hodov
