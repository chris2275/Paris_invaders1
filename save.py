from datetime import datetime
# si seulement ,import datetime , ca oblige a faire now = datetime.datetime.now()
# le datetime module inclut un datetime objet qui inclut une now fonction 
# par contre avec from datetime import datetime , on peut faire:now = datetime.now() 
# il fait reference a l'objet datetime et non au module

def save(level,alienkills,spaceshipkills,time,secs):
    f=open('data/save.txt','w')
    f.write(str(level)+'\n')
    f.write(str(alienkills)+'\n')
    f.write(str(spaceshipkills)+'\n')
    f.write(str(time)+'\n')
    f.write(str(secs)+'\n')

    now=datetime.now()# obtenir la date et l'heure actuelles
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write(dt_string)
    f.close()

def read():
    r=open('data/save.txt','r')
    level=int(r.readline())
    alienkills=r.readline()
    spaceshipkills=r.readline()
    time=r.readline()
    secs=int(r.readline())
    date=r.readline()
    time=time.replace("\n","")
    date=date.replace("\n","")
    alienkills=alienkills.replace("\n","")
    spaceshipkills=spaceshipkills.replace("\n","")
    r.close()

    return [date,level,alienkills,spaceshipkills,time,secs]

def readlevel():
    try:
        r=open('data/save.txt','r')
        level=int(r.readline())
        return level
    except:
        return 0

def readseconds():
    try:
        r=open('data/save.txt','r')
        a=r.readline()
        b=r.readline()
        c=r.readline()
        d=r.readline()
        secs=int(r.readline())
        return secs
    except:
        return 0
