#!/usr/bin/python3

from lib.utils import shargs
from lib.stylors import *
from lib.apnime import *

def listData(data):
    print('\033c')
    menu = f'{nn} {sb}{cg}Selecione um anime da lista:'

    if 'dataT' in data:
        index = ''
        data = data['dataT']

    else:
        link = data['links']
        meta = data['meta']
        data = data['data']

        page = meta['current_page']

        index = f'{sb}{sng}{cr}[{page}]{nn} {sb}{sng}{cb}'

        if link['prev'] and link['next']:
            index += f'[ < Prev | Next > ]'

        elif  link['next']:
            index += f'[ Next > ]'

        elif link['prev']:
            index += f'[ < Prev ]'

    for i, f in enumerate(data, start=1):

        i = f"{sb}{cr}{i:<2}{nn}"

        title = findall(r'^.+?(?= \[|$)', f['title'])[0]
        title = f"{sb}{cb}{title}{nn}"

        year  = f"{sb}{co}{f['year']}{nn}"
        
        print(f'[ {i} ] [ {year} ] - {title}')

    print()

    while True:
        try:
            ep = input(f'{index}{menu}{nn} ')

            if ep == '>' and link['next']:
                return link['next']

            elif ep == '<' and link['prev']:
                return link['prev']

            ep = int(ep)
            
        except ValueError:
            print(f'{sb}{cr}Erro, isso não é um número{nn}')
            continue

        if 1 <= ep <= len(data):
            return data[ep -1]
        else:
            print(f'{sb}{cr}Digite um número entre 1 á {len(data)}{nn}')


def main(*args):
    """
    Uso: ./main.py command [query] [page]
        command Comando [ help | start | search | category | letter | year ]
        query   Busca
        page    Número da Página
    """
    
    commands = ('help', 'start', 'search',
                'category', 'letter', 'year')

    count = len(args)

    if count >= 1:
        cmd = args[0]

        if cmd in commands:
            if cmd == 'help' and count >= 2:
                func = globals()[args[1]]
                help(func)
                exit()

            elif cmd == 'start':
                global start
                return start()
            
            elif count >= 2:
                args = list(args)

                args[1] = ' '.join(args[1:])
                del args[2:]

                func = globals()[cmd]
                return func(*args[1:3])

    help(main)
    exit()


data = shargs(main)

while True:

    try:
        
        aid = listData(data)

        while 'http' in aid:
            data = api(aid).json()
            aid = listData(data)


        info_list = (
            (1, 'Informações do Anime'),
            (2, 'Lista de Episódios')
        )

        while True:

            print()

            for index, label in info_list:
                print(f'\t[{sb}{cr}{index:^3}{nn}] - {sb}{cg}{label}{nn}')

            print()
            choice = input(f'{sb}{cg}>> {nn}')

            if choice == '1':
                anf = anime(aid['id'])['data']
                title = findall(r'(.+?) \[.+?\]', anf['title'])

                if len(title) > 0:
                    anf['title'] = title[0]

                print(f"\n{nn}{sb}Título: {nn}{si}{anf['title']}{nn}")
                print(f"\n{nn}{sb}Sinopse: {nn}{si}{anf['synopsis']}{nn}\n")

                num = 1
                
                for cat in anf['categories']:

                    if num < 5:
                        sep = {'end':' '}
                        num += 1

                    else:
                        sep = {'end':'\n\n'}
                        num = 1

                    print(f"{sb}{cd}{bb}[ {cat['title']} ]{nn}", **sep)

                print('\n', nn)

            elif choice == '2':
                eps = episodes(aid['id'])

                title = findall(r'(.+?) \[.+?\]', aid['title'])

                if len(title) > 0:
                    anf['title'] = title[0]

                m3u = open(f"{aid['title']}.m3u", 'w')
                m3u.write('#EXTM3U\n')

                m3u.mode = 'a'

                for ep in eps['data']:
                    print(f"{sb}{cb} --> {ep['name']} {nn}")

                qualy = None
                eps_selects = input(f'\n{sb}{cg}Selecione o(s) episódio(s) desejado(s):{nn} ')

                if eps_selects:
                    eps_selects = findall(r'\d+', eps_selects)
                else:
                    eps_selects = range(1, len(eps['data'])+1)

                for ep in eps_selects:
                    ep = int(ep)
                    ep = eps['data'][::-1][ep-1]

                    if ep['hashd'] and qualy is None:
                        while True:
                            qualy = input(f'{sb}{cg}HD/SD?{nn} ').lower()

                            if qualy in ('sd', 'hd'):
                                print(f'{sb}{cr}Valor Inválido!!!{nn}')
                                continue

                            break

                    if qualy != 'hd':
                        qualy = 'sd'

                    link = AESdecrypt(ep[qualy])
                    link = getLink(link)

                    m3u.write(f"\n\n#EXTINF:-1, APNIME - {aid['title']} - {ep['name']}\n{link}")
                    print(f"{sb}{co}{aid['title']} {cd}- {su}{cb}{ep['name']} adcicionado a lista{nn}")
                    
                exit('\nPlaylist Criada')

            else:
                print(f'{sb}{cr}Valor inválido!!!{nn}')
    except KeyboardInterrupt:
        exit_choice = input(f'\n{nn}{sb}{cr}Deseja sair [Y/n]: {nn}')

        if exit_choice in ('Y', 'y', ''):
            exit('\033c')
