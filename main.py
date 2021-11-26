#python -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org 
from flask import Flask, request, render_template,send_file,session,redirect,json , jsonify # Importa a biblioteca
import sqlite3
import time
from datetime import datetime
import sqlite3
from waitress import serve
import pymysql
import credenciais
from datetime import date
#porta 3306
#db1 = pymysql.connect(host='localhost', user='root', password='aablcoa12', db='mysql', charset='utf8mb4',port = 3306)
#import pymysql
#porta 3306

Host=''
User=''
Password=''
Db=''
Charset=''
Port=0
Host,User,Password,Db,Charset,Port=credenciais.credencialbanco()
db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)

cursor = db1.cursor()
#sql=''' 
#CREATE TABLE IF NOT EXISTS tabela(nome varchar(90),date varchar(30), endereco varchar(120),cpf varchar(90),cpfprop varchar(90),
#contrato varchar(10),aluguel varchar(20),date1  varchar(20),date2  varchar(20)) 

#'''

sql7=''' 
CREATE TABLE IF NOT EXISTS cadastro(nome varchar(70),telefone varchar (30),cpf varchar (20),setor varchar(30),cargo varchar (20) ,codigo varchar (50),data varchar(30),data1 varchar(30)) 

'''

sql8=''' 
CREATE TABLE IF NOT EXISTS registro(cpf varchar (20),codigo varchar (50),data varchar(30)) 

'''
#cursor.execute(sql)

cursor.execute(sql7)
cursor.execute(sql8)
db1.commit()
db1.close()
from datetime import date
import json


app = Flask(__name__) # Inicializa a aplicação

import os
app.secret_key = "senha_secreta"
import webbrowser
@app.route('/inicio', methods=['GET']) # Nova rota
def inicio():
    if request.args.get('busca'):
        with open('credenciais.txt','r') as t:
            tarjalida=t.readline()
        return jsonify(tarjalida)
    return render_template('inicio.html')
@app.route('/consulta', methods=['GET']) # Nova rota
def consulta():
    rg=request.args.get('rg')
    nome=request.args.get('nome')
    datain=request.args.get('datain')
    
    dataout=request.args.get('dataout')
    rgvalida=request.args.get('rgvalida')
    nomevalida=request.args.get('nomevalida')
    datainvalida=request.args.get('datainvalida')
    dataoutvalida=request.args.get('dataoutvalida')
    #todos juntos, pesquisa
    Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
    db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
    cursor = db1.cursor()
    if rgvalida=='sim' and nomevalida=='sim' and datainvalida=='sim' and dataoutvalida=='sim':
        datain=datain.replace('-','/')
        sql1 = "SELECT * FROM cadastro  WHERE nome=%s and cpf=%s and data1>=%s  and data1<=%s"
        cursor.execute(sql1,(nome,rg,datain,dataout))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if rgvalida=='sim' and nomevalida=='sim' and datainvalida=='sim':
        datain=datain.replace('-','/')
        sql1 = "SELECT * FROM cadastro  WHERE nome=%s and cpf=%s and data1>=%s "
        cursor.execute(sql1,(nome,rg,datain))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if rgvalida=='sim' and nomevalida=='sim'  and dataoutvalida=='sim':
        sql1 = "SELECT * FROM cadastro  WHERE nome=%s and cpf=%s   and data1<=%s"
        cursor.execute(sql1,(nome,rg,dataout))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if rgvalida=='sim' and datainvalida=='sim'  and dataoutvalida=='sim':
        datain=datain.replace('-','/')
        sql1 = "SELECT * FROM cadastro  WHERE cpf=%s and data1>=%s   and data1<=%s"
        cursor.execute(sql1,(rg,datain,dataout))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if nomevalida=='sim' and datainvalida=='sim'  and dataoutvalida=='sim':
        sql1 = "SELECT * FROM cadastro  WHERE cpf=%s and data1>=%s   and data1<=%s"
        cursor.execute(sql1,(nome,datain,dataout))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if rgvalida=='sim' and nomevalida=='sim':
        sql1 = "SELECT * FROM cadastro  WHERE nome=%s and cpf=%s"
        cursor.execute(sql1,(nome,rg))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if  datainvalida=='sim' and dataoutvalida=='sim':
        datain=datain.replace('-','/')
        sql1 = "SELECT * FROM cadastro  WHERE  data1>=%s  and data1<=%s"
        cursor.execute(sql1,(datain,dataout))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if rgvalida=='sim':
        sql1 = "SELECT * FROM cadastro  WHERE   cpf=%s "
        cursor.execute(sql1,(rg,))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if nomevalida=='sim':
        sql1 = "SELECT * FROM cadastro  WHERE   nome=%s "
        cursor.execute(sql1,(nome,))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if datainvalida=='sim':
        datain=datain.replace('-','/')
        print (datain)
        sql1 = "SELECT * FROM cadastro "
        cursor.execute(sql1)
        retorno = cursor.fetchall()
        print (retorno)
        sql1 = "SELECT * FROM cadastro  WHERE   data1>=%s "
        cursor.execute(sql1,(datain,))
        retorno = cursor.fetchall()
        return jsonify (retorno)
    if dataoutvalida=='sim':
        sql1 = "SELECT * FROM cadastro  WHERE   data1<=%s "
        cursor.execute(sql1,(dataout,))
        retorno = cursor.fetchall()
        return jsonify (retorno)
        

    
    return render_template('consulta.html')

@app.route('/busca', methods=['GET']) # Nova rota
def busca():
    if request.args.get('busca'):
        with open('rfid.txt','r') as t:
            tarjalida=t.readline()
        return jsonify(tarjalida)
@app.route('/historico', methods=['GET','POST']) # Nova rota
def historico():
    if request.method=='GET':
        if request.args.get('busca')=='sim':
            rg=request.args.get('rg')
            print (cpf)
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM registro  WHERE cpf=%s"
            cursor.execute(sql1,(rg,))
            retorno = cursor.fetchall()
            if not retorno:
                retorno='nada'
            print (retorno)
            db1.close()
            return jsonify(retorno)
    return render_template('historico.html')
@app.route('/', methods=['GET','POST']) # Nova rota
def index():
    retorno=''
    Host=''
    User=''
    Password=''
    Db=''
    Charser=''
    Port=0
    if request.method=='POST':

        if request.form['deleta']=='atualiza':
            print ('entrou no cadastro ')
            cpf=request.form['codigo']
            codigonovo=request.form['codigonovo']
            cpf1=request.form['cpf1']
            if codigonovo=='' or cpf1=='':
                return jsonify('preencha adequadamente os campos')
            data_atual = date.today()
            data_atual=str(data_atual)
            data_atual=data_atual.split('-')
            data_atual=data_atual[2]+'/'+data_atual[1]+'/'data_atual[0]
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1= """INSERT INTO registro(cpf,codigo,data) VALUES (%s,%s,%s)"""
            cursor.execute(sql1, (cpf1,codigonovo,data_atual))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            cursor.execute('UPDATE cadastro SET codigo=%s WHERE codigo=%s ',(codigonovo,cpf))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM cadastro"
            cursor.execute(sql1)
            retorno = cursor.fetchall()
            print (retorno)
            db1.close()
            return jsonify(retorno)
        if request.form['deleta']=='apaga':
            print ('entrou no cadastro ')
            cpf=request.form['codigo']
            
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            cursor.execute('DELETE FROM cadastro WHERE codigo=%s ',(cpf,))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM cadastro"
            cursor.execute(sql1)
            retorno = cursor.fetchall()
            print (retorno)
            db1.close()
            return jsonify(retorno)
        if request.form['busca']:
            #print ('entrou na blacklist')
            cpf=request.form['cpf']
            nome=request.form['nome']
            telefone=request.form['telefone']
            setor=request.form['setor']
            cargo=request.form['cargo']
            codigo=request.form['codigo']
            data= datetime.now()
            data = data.strftime('%d/%m/%Y')
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1= """INSERT INTO cadastro(cpf,nome,telefone,setor,cargo,codigo,data) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql1, (cpf,nome,telefone,setor,cargo,codigo,data))
            db1.commit()
            db1.close()
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1= """INSERT INTO registro(cpf,codigo,data) VALUES (%s,%s,%s)"""
            cursor.execute(sql1, (cpf,codigo,data))
            db1.commit()
            db1.close()
            return jsonify('dados inseridos com sucesso')
    if request.method=='GET':
        if request.args.get('busca')=='sim':
            cpf=request.args.get('cpf')
            print (cpf)
            Host,User,Password,Db,Charser,Port=credenciais.credencialbanco()
            db1 = pymysql.connect(host=Host, user=User, password=Password, db=Db, charset=Charset,port=Port)
            cursor = db1.cursor()
            sql1 = "SELECT * FROM cadastro  WHERE codigo=%s"
            cursor.execute(sql1,(cpf,))
            retorno = cursor.fetchall()
            if not retorno:
                retorno='nada'
            print (retorno)
            db1.close()
            return jsonify(retorno)
    return render_template('index.html')


if __name__ == '__main__':
  #serve(app, host='10.75.243.115', port=5000)
  app.run(debug=True) # Executa a aplicação
  #app.run( host='10.75.243.115', port=5000)