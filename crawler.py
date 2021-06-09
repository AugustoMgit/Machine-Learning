import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin #ajuda na contatenação dos links. Exemplo: como o urllib não executa sem ter o link completo, https ou http, essa biblioteca coloca isso antes para poder executar
import re
import nltk
import pymysql

def inserePalavraLocalizacao(idurl, idpalavra, localizacao):
    conexao = pymysql.connect(host='localhost', user='root', password='senha', db = 'indice', autocommit = True)
    cursor = conexao.cursor()
    cursor.execute('insert into palavra_localizacao(idurl, idpalavra, localizacao) values(%s, %s, %s)',(idurl, idpalavra, localizacao))
    idpalavra_localizacao = cursor.lastrowid
    cursor.close()
    conexao.close()
    
    return idpalavra_localizacao

#inserePalavraLocalizacao(1, 2, 20)

def inserePalavra(palavra):
    conexao = pymysql.connect(host='localhost', user='root', password='Felipem160899', db = 'indice', autocommit = True)
    cursor = conexao.cursor()
    cursor.execute('insert into palavras(palavra) values (%s)', palavra)
    idpalavra = cursor.lastrowid
    cursor.close()
    conexao.close()
    
    return idpalavra

#inserePalavra('Isso') #cada palavra adicionada, irá ter um novo índice e será retornado esse novo índice, ou seja, o último índice
    
def palavraIndexada(palavra):
    retorno = -1 #que não existe a palavra no índice
    conexao = pymysql.connect(host='localhost', user='root', password='Felipem160899', db = 'indice')
    cursor = conexao.cursor()
    cursor.execute('select idpalavra from palavras where palavra = %s', palavra)
    if cursor.rowcount > 0:
        print("Palavra já cadastrada")
        retorno = cursor.fetchone()[0]#retorna o idpalavra, por causa do [0]
    #else:
     #   print("Palavra não cadastrada")
    cursor.close()
    conexao.close()
    print(retorno)
    return retorno

palavraIndexada('teste')
#palavraIndexada('linguagem')

def inserePagina(url):
    conexao = pymysql.connect(host='localhost', user='root', password='Felipem160899', db = 'indice', autocommit = True, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    cursor.execute('insert into urls (url) values (%s)', url)
    idpagina = cursor.lastrowid
    
    cursor.close()
    conexao.close()
    return idpagina
#retorna o id que foi inserido
#inserePagina("teste2")

def paginaIndexada(url):
    retorno = -1 #pagina não existe
    conexao = pymysql.connect(host='localhost', user='root', password='Felipem160899', db = 'indice', use_unicode = True, charset = 'utf8mb4')
    cursorURL = conexao.cursor() #faz consultas sql
    cursorURL.execute('select idurl from urls where url = %s', url )
    if cursorURL.rowcount > 0:
        #print("URL cadastrada")
        idurl = cursorURL.fetchone()[0] #retorna registro, no caso o primeiro->[0]
        cursorPalavra = conexao.cursor()
        cursorPalavra.execute("select idurl from palavra_localizacao where idurl = %s", idurl)
        if cursorPalavra.rowcount > 0:
            #print("URL com palavras")
            retorno = -2
        else:
            #print("URL sem palavras")
            retorno = idurl
        cursorPalavra.close()
    #else:
        #print("URL não cadastrada")
    cursorURL.close()
    conexao.close()
    
    return retorno
#paginaIndexada('teste')

def separaPalavras(texto):
    stop= nltk.corpus.stopwords.words('portuguese')
    stemmer = nltk.stem.RSLPStemmer()
    splitter = re.compile('\\W+')
    lista_palavras=[]
    lista=[p for p in splitter.split(texto) if p!='']
    for p in lista: 
        if p.lower() not in stop: #se p nÃ£o estiver na lista stop1, ele nÃ£o adiciona
            if len(p) > 1:
                lista_palavras.append(stemmer.stem(p).lower()) 
    return lista_palavras
                 
#teste = separaPalavras("Este lugar é apavorante")

def getTexto(sopa):
    for tags in sopa(['script', 'style']):
        tags.decompose() #remove todo o conteúdo da tag
    return' '.join(sopa.stripped_strings)


def indexador(url, sopa):
    indexada = paginaIndexada(url) #irá receber -1 ou -2 ou a idurl
    if indexada == -2:#já existe a url 
        print("url já cadastrada")
        return #para por aqui, não executa mais nada, pois a página já está cadastrada
    elif indexada == -1:
        print("página não existente. Logo, vou inserir")
        idnova_pagina = inserePagina(url)   
    elif indexada > 0: #existe a página mas não existe palavra
        idnova_pagina = indexada
    
    print("Indexando" + url)
    
    texto = getTexto(sopa)
    palavras = inserePalavra(texto)
    for i in range(len(palavras)):
        idpalavra = palavraIndexada(palavras[i])
        if idpalavra == -1:
            idpalavra = inserePalavra(palavras[i])
        inserePalavraLocalizacao(idnova_pagina, idpalavra, i)
        

#OBS: urlib quer a url completa : https://sdfsfdf.com
def crawl(paginas, profundidade):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)#desabilita o aviso de segurança
    for i in range(profundidade):
        #à medida que percorre o for, irá adicionando novos links na variável novaspaginas. Isso é permitido pelo set()
        novaspaginas=set() #set = conjunto dos link, não permite valor repetidos
        for pagina in paginas:
            http=urllib3.PoolManager()
                #tenta carregar  a página e se der algum erro, cai no except
            try:
                dados_pagina=http.request('GET', pagina)
            #ao dar erro
            except:
                print("Erro ao abrir a página " + pagina)
                continue #volta para o for, não continua para baixo quando der erro de carregar página
                    
            #captura de todos os dados da página    
            sopa=BeautifulSoup(dados_pagina.data,"lxml") #lxml = parser= extração de dados do arquivo html
            indexador(pagina, sopa)
            links=sopa.find_all('a')
            contador=1
            contador1=1
            for link in links:
                    #str converte para string e link.content diz qual o título do link
                    #print(str(link.contents) + " - " + str(link.get('href'))) #str(link.get('href')) = pega o link da página e transforma em string 
                    #print(link.attrs)#mostra todos os atributos de cada link: ex: href
                    #print('\n')
                    #irá contar quantos atributos href tem no total de todos os links
                if('href' in link.attrs):
                        #contatena o link, ou seja, faz a correção dos links colocando http ou https
                        #Ex: se no link que foi passado é diferente do original, ele corrige, colocando o https na frente, pois o link original contem https na frente
                        #url = urljoin(paginaPadrão, paginaAserConcertar)
                    url=urljoin(pagina, str(link.get('href')))
                        
                        #if url != link.get('href'):
                        #    print(url)
                        #    print(link.get('href'))
                            
                
                        #se a url for inválida. se rotronar valor diferente de -1 ele encontrou uma url válida, logo, não usa ela. continue não executa mais nada que tem para baixo e executa outro link
                        #se a url encaixar nessa condição, passa para a próxima página
                    if url.find("'") != -1: 
                        continue
                    print(url)
                        #percorre os links e encotra a #. split quebra a string quando encontrar a # em uma posição[0]
                        #isso vai servir para diferenciar link interno e externo, ou seja, depois do # de um link, significa que será direcionado dentro da página, link facilitador
                    url=url.split('#')[0] 
                        #print(url)
                        #print('/n')
                        
                        #pega somente os links que começam com http
                    if url[0:4]=='http':
                        novaspaginas.add(url)
                    contador=contador+1
                #total de páginas
                contador1=contador1+1
            print("Total de páginas ", contador1)
            #páginas que tem o href
            #apenas as tags que tem href levam a outras páginas
            
            #adiciona o link na variável páginas
            paginas=novaspaginas
        print(contador)
teste=set()
teste.add("a")
teste.add("b")
listapaginas=['https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o']
crawl(listapaginas,2)
