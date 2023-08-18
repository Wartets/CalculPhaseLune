import time
import datetime

k = 719529 #719529 days from 1/1/1 to 1/1/1971 (excluded) #719164 days from 1/1/1 to 1/1/1970 (exluded)
SbyD = 24 * 60 * 60
C = SbyD * (0) # Correction generale

def millisec():
    return (time.time() + k * 24 * 60 * 60) *1000
    
def centisec():
    return (time.time() + k * 24 * 60 * 60) *100

def sec():
    return round(time.time() + k * 24 * 60 * 60) + C

def min():
    return sec() / 60

def hour():
    return sec() / 60 / 60

def day():
    return sec() / 60 / 60 / 24

def year():
    return sec() / 60 / 60 / 24 / 365.256363009 #Periode Revolution Terre

def temps(a = 0):
    if a == -2:
        return millisec()
    elif a == -1:
        return centisec()
    elif a == 0:
        return sec()
    elif a == 1:
        return min()
    elif a == 2:
        return hour()
    elif a == 3:
        return day()
    elif a == 4:
        return year()
    else:
        print("Erreur: Il faut donner un nombre de -2 a 4 (-2:millisec / -1:centisec / 0:sec / 1:min / 2:hour / 3:day / 4:year)")