import requests
import base64

from Crypto.Cipher import AES
from re import findall

API  = "VERoNS9wOXh2U0BiNlRZaExbZFBgL3gkJXBYd3Yk"
HOST = "152.44.32.124"


# DECRIPTOGRAFAR
def AESdecrypt(content, key=b'1p4vo5hz1592mvvy'):
    try:
        cryptor = AES.new(key, AES.MODE_CBC, key)

        content = base64.b64decode(content)
        content = content.decode()

        content += (len(content) % 4) * '='
        content = base64.b64decode(content)

        decrypted = cryptor.decrypt(content)
        return decrypted
    except:
        return content


# OBTERLINK DE DOWNLOAD
def getLink(enc_link):
    link = f'{enc_link}'
    reg = r'(?<=#)[^\\]+'
    reg = findall(reg, link)

    if len(reg) > 0:
        link = reg[-1]

        html = requests.get(link).text
        link = findall(r'(?<="play_url":")[^"]+', html)

        if len(link) > 0:
            link = link[-1].encode().decode('unicode_escape')
        else:
            exit('\033[31;1mOcorreu um erro ao obter o link\033[m')
 
    else:
        link = enc_link

    return link
        


# API
def api(url):
    headers = {
        'Authorization': API,
        'Host': HOST
    }

    return requests.get(url, headers=headers)


# LISTAR ANIMES
def start():
    """
    Página Inícial

    Return   (dict): Json
    """

    r = api(f'http://{HOST}/api/inicial')
    return r.json()


def search(query, page=1):
    """
    Busca pelo nome do anime

    Args:
        query (str): Nome do Anime
        page  (int): Nível da Página

    Return   (dict): Json
    """

    query = requests.utils.quote(query)
    
    r = api(f'http://{HOST}/api/pesquisa/{query}?page={page}')
    return r.json()


def category(query, page=1):
    """
    Buscar anime por categoria

    Args:
        query (str): Categorias de Animes
        page  (int): Nível da Página

    Return   (dict): Json
    """

    cats = {
        'Ação': 9, 'Anjos': 50, 'Artes Marciais': 27, 'Aventura': 10,
        'Baseball': 55, 'Basquete': 56, 'Bishoujo': 48, 'Bishounen': 47,
        'Boxe': 43, 'Chinês': 70, 'Comédia': 17, 'Culinária': 66, 'Dança': 59,
        'Demônios': 62, 'Detetive': 30, 'Drama': 14, 'Dublado': 21, 'Ecchi': 1,
        'Escolar': 19, 'Espacial': 65, 'Esportes': 31, 'Fantasia': 6,
        'Ficção Científica': 8, 'Filme': 12, 'Futebol': 53, 'Guerra': 44,
        'Harem': 28, 'Histórico': 51, 'Infantil': 45, 'Jogos': 7, 'Josei': 5,
        'Lolicon': 58, 'Luta': 32, 'Magia': 22, 'Mahou Shoujo': 54, 'Mecha': 25,
        'Medieval': 69, 'Militar': 16, 'Mistério': 33, 'Musical': 35, 'Novel': 24,
        'OVA': 11, 'Paródia': 63, 'Poderes': 15, 'Policial': 26, 'Pós-apocalíptico': 67,
        'Psicológico': 36, 'Realidade Virtual': 60, 'Romance': 18, 'RPG': 13,
        'Samurai': 64, 'Seinen': 3, 'Shoujo': 34, 'Shoujoai': 40, 'Shounen': 2,
        'Shounenai': 39, 'Sobrenatural': 29, 'Submundo': 49, 'Suspense': 61, 'Terror': 4,
        'Thriller': 68, 'Tragédia': 42, 'Universo Paralelo': 23, 'Vampiros': 46,
        'Vida Diária': 20, 'Yaoi': 41, 'Yuri': 37
    }

    query = query.title()
    query = cats[query]

    r = api(f'http://{HOST}/api/categoria/{query}?page={page}')
    return r.json()


def letter(query, page=1):
    """
    Buscar anime por letra

    Args:
        query (str): Letra Inicial
        page  (int): Nível da Página

    Return   (dict): Json
    """

    letters = '@abcdefghijklmnopqrstuvwxyz'
    query = query[0].lower().strip()

    if query in letters:
        r = api(f'http://{HOST}/api/letra/{query}?page={page}')
        return r.json()

    else:
        print('Não existe essa busca na pesquisa')


def year(query, page=1):
    """
    Buscar anime por ano

    Args:
        query (str): Ano de Lançamento
        page  (int): Nível da Página

    Return   (dict): Json
    """

    years = (
        2020,2019,2018,2017,2016,2015,2014,
        2013,2012,2011,2010,2009,2008,2007,
        2006,2005,2004,2003,2002,2001,2000,
        1999,1998,1997,1996,1995,1994,1993,
        1992,1991,1990,1989,1988,1987,1986,
        1985,1983,1982,1981,1980,1979,1978,
        1977,1976,1975,1974,1972,1971,1970,
        1969,1968,1967,1966,1963,1958
    )

    if query in years:
        r = api(f'http://{HOST}/api/ano/{query}?page={page}')
        return r.json()
    
    else:
        print('Não existe esse ano na pesquisa')


# INFO ANIMES
def anime(aid):
    """
    Obtém informações sobre o anime

    Args:
        aid  (int): ID do Anime

    Return (dict): Json
    """

    r = api(f'http://{HOST}/api/anime/{aid}')
    return r.json()


def episodes(aid, ep=0):
    """
    Obtém a lista de episódios

    Args:
        aid  (int): ID do Anime
        ep  (int): Número do Episódio 

    Return (dict): Json
    """

    r = api(f'http://{HOST}/api/episodios/{aid}')
    r = r.json()

    if ep > 0:
        r = r['data'][::-1]
        return r[ep - 1]
    else:
        return r
