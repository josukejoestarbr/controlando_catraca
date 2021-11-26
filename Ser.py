import serial
#python Ser.py
import time
from datetime import datetime
ser = serial.Serial('/COM3', 9600)
import pymysql
import credenciais
import threading
Host=''
User=''
Password=''
Db=''
Charset=''
Port=0
Host,User,Password,Db,Charset,Port=credenciais.credencialbanco()
db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
global valida
valida=False
valida1=False
cursor = db1.cursor()
aant1=''
aant=''
resposta=''
leitura=''
def worker(message):
    time.sleep(1)
    #print (message)
    with open ('booleana.txt','w+') as t:
        t.write('True')
       
while True:
    a=ser.readline()
    c=a.decode('utf-8')
    
    
    if(len(a)>=2):
        print (c)
        #print(valida)
        with open ('rfid.txt','w+') as t:
            b=str(a)
            t.write(c)
        
        with open ('rfid.txt','r') as t:
           resposta=t.read()       
        
        Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
        db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
        cursor = db1.cursor()
        #b='24 5F F0 2B'
        #sql1 = "SELECT * FROM cadastro "
        #cursor.execute(sql1)
        #retorno = cursor.fetchall()
        #print ('total:',retorno)
        resposta=resposta.replace('\n','')
        sql1 = "SELECT cpf,nome FROM cadastro  WHERE codigo=%s"
        cursor.execute(sql1,resposta)
        retorno = cursor.fetchall()
        print (retorno)
        db1.close()
        if not retorno:
            #retorno='nada'
            print ('recusado')
            aant1=''
            with open ('booleana.txt','w+') as t:
                    t.write('False')
            #t = threading.Thread(target=worker,args=("apagado",))
            #t.start()
        else:
            if aant1!=resposta:
                aant1=resposta
                with open ('booleana.txt','w+') as t:
                    t.write('True')
                print (aant1)
            with open ('booleana.txt','r') as t:
                leitura= t.read()
            leitura=leitura.replace('\n','')
            if leitura=='True':
                ser.write(b"b")
                print('cadastrado:',retorno)
                data = datetime.now()
                data1= data.strftime('%d/%m/%Y/%H:%M')
                data1=str(data1)
                data2= data.strftime('%d/%m/%Y')
                data2=str(data2)
                Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
                db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
                cursor = db1.cursor()
                cpf=''
                nome=''
                for i in retorno:
                    cpf=i[0]
                    nome=i[1]
                sql1= """INSERT INTO cadastro(cpf,nome,codigo,data,data1) VALUES (%s,%s,%s,%s,%s)"""
                cursor.execute(sql1, (cpf,nome,aant,data1,data2))
                db1.commit()
                db1.close()
                data11=str(data)
                data11= data11.split(' ')
                data22=data11[1]
                data22=data22.split('.')
                data22=data22[0]
                
                data11=data11[0]
                data11=data11.split('-')
                data11=data11[2]+'/'+data11[1]+'/'+data11[0]+' '+data22
                salvar='cpf:'+cpf+' nome:'+nome+' data:'+data11
                with open ('credenciais.txt','w+') as t:
                    t.write(salvar)
                print ('dados inseridos em:',data1,"  código:",aant1)
                with open ('booleana.txt','w+') as t:
                    t.write('False')
                t = threading.Thread(target=worker,args=("apagado",))
                t.start()
                
    