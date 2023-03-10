from leiaute import Leiaute
from modelos import Regra
from modelos import Geral
from modelos import Tabela
from modelos import Resumo
import cinto_utilidades as cinto

import locale
import os
import re
import sys
import datetime
from time import perf_counter
from xml.etree.ElementTree import parse
sys.dont_write_bytecode = True
locale.setlocale(locale.LC_TIME, "pt_BR")

if len(sys.argv) < 2:
    print('Uso: python xsd_html.py CAMINHOS_LEIAUTES')
    exit()

for indice in range(1, len(sys.argv)):
    print('Caminho: ', sys.argv[indice])

    caminho_xsd = os.path.join(sys.argv[indice], '{}')
    caminho_ativos = os.path.join(os.getcwd(), 'ativos', '{}')
    caminho_doc = os.path.join(sys.argv[indice], 'doc', '{}')
    caminho_saida = os.path.join(sys.argv[indice], 'doc', 'saida', '{}')
    caminho_texto = os.path.join(sys.argv[indice], 'doc', 'txt', '{}')

    parametros = cinto.obter_arquivo(caminho_doc.format('parametros_texto_inicial')).read().split('\n')
    menu = cinto.obter_arquivo(caminho_doc.format('menu')).read()

    for parametro in parametros:
        if 'VERSAO' in parametro:
            _, versao = parametro.split(' = ')
            versao_m = re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), versao, 1)

        if 'PUBLICACAO' in parametro:
            _, publicacao = parametro.split(' = ')
            publicacao_reduzida = publicacao.replace('consolidada', 'cons.').replace('nº ', '')

        if 'DATA' in parametro:
            _, data = parametro.split(' = ')

            data_atual = datetime.date.today().strftime('%B de %Y').capitalize()

            if data != data_atual:
                print('A data informada no parâmetro de configuração é diferente da data atual.')

        if 'DETALHES' in parametro:
            _, detalhes_publicacao = parametro.split(' = ')

    inicio = cinto.obter_arquivo(caminho_ativos.format('inicio.html')).read()
    fim = cinto.obter_arquivo(caminho_ativos.format('fim.html')).read().replace(
        'MENU', menu)

    regras = {}

    arquivo = cinto.obter_arquivo(caminho_xsd.format('regras.txt'))
    id = None

    for linha in arquivo.readlines():
        if id is None:
            id = linha.rstrip()
            regras[id] = []
        else:
            if linha.strip() == '':
                id = None
            else:
                texto = linha.rstrip().translate(str.maketrans({
                    '>': '&gt;',
                    '<': '&lt;',
                }))

                for regra in set(re.findall(r'(REGRA_\w+)', texto)):
                    texto = texto.replace(
                        regra, Geral.LINK.format(regra, regra))

                regras[id].append(texto)
    arquivo.close()

    inicio_tempo = perf_counter()

    # LEIAUTES
    leiautes = []
    identificadores = [item for item in os.listdir(
        sys.argv[indice]) if item.startswith('evt')]

    tipos_globais = {tipo.get('name'): tipo
                    for tipo in parse(caminho_xsd.format('tipos.xsd')).getroot()}

    for identificador in identificadores:
        raiz = parse(caminho_xsd.format(identificador)).getroot()
        leiautes.append(Leiaute(raiz, tipos_globais))

    leiautes.sort(key=lambda item: item.codigo)

    conteudo = inicio.replace(
        'SUBTITULO',  f'eSocial {versao} - Leiautes {publicacao_reduzida}').replace(
        'TITULO', f'eSocial {versao} - Leiautes').replace(
        'TEXTO_1', (
            '<h1 class="title has-text-centered is-3">LEIAUTES DO eSOCIAL'
            '<br /><br />'
            '{}</h1>'
            f'{detalhes_publicacao}'
            .format(f'{versao_m} {publicacao}'))).replace(
        'TEXTO_2', f'<h1 class="title has-text-centered is-3">{data}</h1>')

    conteudo_indice = ''
    for leiaute in leiautes:
        conteudo_indice += Resumo.LINHA_INDICE.format(
            nome=leiaute.nome, codigo=leiaute.codigo, descricao=leiaute.descricao)

        with cinto.obter_arquivo(caminho_texto.format(f'{leiaute.codigo}.txt'), 'w') as f:
            f.write(leiaute.gerar_texto())

    conteudo += '<h2 class="title has-text-centered is-3">Sumário</h2>\n'
    conteudo += '<ul class="sumario">\n'
    conteudo += conteudo_indice
    conteudo += '</ul>\n'

    html = ''
    for regra in regras:
        texto = '<br />\n'.join(regras[regra])
        html += Regra.LINHA_MODAL.format(nome=regra, texto=texto)

    html += ''.join([item.gerar_html() for item in leiautes])

    conteudo += html
    conteudo += fim

    with cinto.obter_arquivo(caminho_saida.format('index.html'), 'w') as f:
        f.write(conteudo)

    referencias_regras = {}

    for leiaute in leiautes:
        for regra in leiaute.referencias_regras:
            if regra not in referencias_regras:
                referencias_regras[regra] = []

            referencias_regras[regra].extend(leiaute.referencias_regras[regra])

    # REGRAS
    conteudo = inicio.replace(
        'SUBTITULO',  f'eSocial {versao} - Regras {publicacao_reduzida}').replace(
        'TITULO', f'eSocial {versao} - Regras').replace(
        'TEXTO_1', '<h1 class="title has-text-centered is-3">ANEXO II DOS LEIAUTES DO eSOCIAL<br />REGRAS DE VALIDAÇÃO</h1>').replace(
        'TEXTO_2', '<h1 class="title has-text-centered is-3">{}</h1>'.format(
            f'{versao_m} {publicacao}'))

    conteudo += '_referencias_' + Regra.CABECALHO
    conteudo_modal = ''

    for regra in regras:
        texto = '<br />\n'.join(regras[regra])
        conteudo += Regra.LINHA.format(
            id=regra, nome=regra, texto=texto)

        texto_modal = '\n'.join([Regra.LINHA_REFERENCIA.format(
            id=ocorrencia[0], trilha=ocorrencia[1]) for ocorrencia in referencias_regras[regra]])

        conteudo_modal += Regra.LINHA_MODAL_REFERENCIA.format(
            nome=regra, texto=texto_modal)

    conteudo = conteudo.replace('_referencias_', conteudo_modal)

    conteudo += Geral.RODAPE_TABELA
    conteudo += fim

    with cinto.obter_arquivo(caminho_saida.format('regras.html'), 'w') as f:
        f.write(conteudo)

    # TABELAS
    tabelas = []
    conteudo_tabela = ''
    conteudo_indice = ''

    itens_caminho = os.path.split(sys.argv[indice])

    if (itens_caminho[-1].endswith('simplificacao')):
        caminho_tabelas = os.path.join(sys.argv[indice], 'tabelas', '{}')
    else:
        caminho_tabelas = os.path.join(os.path.dirname(sys.argv[indice]), 'tabelas', '{}')


    for tabela in sorted(os.listdir(caminho_tabelas.replace('{}', ''))):
        texto_tabela = []
        anexos_tabela = []
        itens_cabecalho = []
        linhas_cabecalho = 1

        with cinto.obter_arquivo(caminho_tabelas.format(tabela)) as arquivo_tabela:
            rowspan_linha = {}

            fim_da_tabela = False
            texto_largura_fixa = False
            indices_texto = []

            for indice_linha, linha in enumerate(arquivo_tabela):
                if indice_linha == 2 and linha.startswith('^'):
                    linhas_cabecalho = 2

                if '__' in linha:
                    linha = re.sub('__(.*?)__', '<i>\\1</i>', linha)
                if '##' in linha:
                    linha = re.sub('##(.*?)##', '<b>\\1</b>', linha)

                itens_linha = []

                if linha.rstrip() == '===':
                    fim_da_tabela = True
                    continue
                elif fim_da_tabela:
                    if (linha.startswith('>')):
                        if not texto_largura_fixa:
                            anexos_tabela.append(
                                '<pre>{}'.format(linha.rstrip()[1:]))
                            texto_largura_fixa = True
                        else:
                            anexos_tabela.append(linha.rstrip()[1:])
                    else:
                        if texto_largura_fixa:
                            texto_largura_fixa = False
                            anexos_tabela.append('</pre>')
                        anexos_tabela.append(
                            '<p>{}</p>'.format(linha.rstrip()))
                    continue
                elif indice_linha == 0:
                    if '#' in linha:
                        titulo, dimensoes = linha.rstrip().split('#')
                        dimensoes = dimensoes.split(' ')
                    else:
                        titulo = linha.rstrip()
                        dimensoes = None
                    continue
                else:
                    extensao_colspan = 0

                    for indice_item, item in enumerate(linha.rstrip().split('|')):
                        if indice_linha == 1:
                            rowspan_linha[indice_item] = 0

                            if '>' in item:
                                itens_linha.append('')
                                extensao_colspan += 1
                            else:
                                if '<' in item:
                                    item = item[1:]
                                    indices_texto.append(indice_item)

                                if dimensoes is not None:
                                    dimensao = ' style="width: {}%"'.format(
                                        dimensoes[indice_item])
                                else:
                                    dimensao = ''
                                itens_linha.append(
                                    Tabela.CELULA_CABECALHO.format(
                                        dimensao=dimensao,
                                        conteudo=item))
                        else:
                            if item.startswith('^'):
                                itens_linha.append('')
                                rowspan_linha[indice_item] += 1
                            elif item.startswith('>'):
                                itens_linha.append('')
                                extensao_colspan += 1

                                if rowspan_linha[indice_item] > 0:
                                    indice = indice_linha \
                                        - rowspan_linha[indice_item] - 2

                                    valor = texto_tabela[indice][indice_item]
                                    valor = valor.replace(
                                        'rowspan=""', 'rowspan="{}"'.format(
                                            rowspan_linha[indice_item] + 1))

                                    texto_tabela[indice][indice_item] = valor
                                    rowspan_linha[indice_item] = 0

                            else:
                                if extensao_colspan != 0:
                                    indice = indice_item - extensao_colspan - 1
                                    valor = itens_linha[indice].replace(
                                        'colspan=""', 'colspan="{}"'.format(
                                            extensao_colspan + 1))

                                    itens_linha[indice] = valor
                                    extensao_colspan = 0

                                if rowspan_linha[indice_item] > 0:
                                    indice = indice_linha \
                                        - rowspan_linha[indice_item] - 2

                                    valor = texto_tabela[indice][indice_item]
                                    valor = valor.replace(
                                        'rowspan=""', 'rowspan="{}"'.format(
                                            rowspan_linha[indice_item] + 1))

                                    texto_tabela[indice][indice_item] = valor

                                rowspan_linha[indice_item] = 0

                                classe = ''
                                if indice_item in indices_texto:
                                    classe = ' class="texto"'

                                itens_linha.append(Tabela.CELULA.format(
                                    classe=classe,
                                    conteudo=item))

                    if extensao_colspan > 0:
                        item = itens_linha[indice_item - extensao_colspan]
                        item = item.replace('colspan=""', 'colspan="{}"'.format(
                            extensao_colspan + 1))
                        itens_linha[indice_item - extensao_colspan] = item

                    if indice_linha <= linhas_cabecalho:
                        itens_cabecalho.append(itens_linha)

                texto_tabela.append(itens_linha)

            for i in range(indice_item):
                if rowspan_linha[i] > 0:
                    texto = texto_tabela[indice_linha - rowspan_linha[i] - 1][i]
                    texto = texto.replace('rowspan=""', 'rowspan="{}"'.format(
                        rowspan_linha[i] + 1))
                    texto_tabela[indice_linha - rowspan_linha[i] - 1][i] = texto

            cabecalho = Tabela.CABECALHO

            if tabela[:-4] == '04':
                cabecalho = Tabela.CABECALHO.replace(
                    'thead', 'thead style="display: table-row-group;"', 1)

            conteudo_cabecalho = []

            for itens in itens_cabecalho:
                conteudo_cabecalho.append(''.join(itens).replace(
                    ' class="grupo"', '').replace(
                    ' rowspan=""', '').replace(' colspan=""', ''))

            linha_cabecalho = '</tr>\n<tr>\n'.join(
                conteudo_cabecalho)

            conteudo_tabela += cabecalho.format(
                tabela[:-4], tabela[:-4], indice_item + 1, tabela[:-4], titulo, linha_cabecalho)

            for indice_linha, linha in enumerate(texto_tabela[linhas_cabecalho:]):
                if 'class="grupo"' in linha[0]:
                    conteudo_tabela += '<tr class="grupo">\n'
                else:
                    conteudo_tabela += '<tr>\n'

                for item in linha:
                    if '--C3--' in item:
                        item = item.replace(
                            '--C3--', '').replace(
                                '<td', '<td class="sub-cabecalho"')

                    if item != '':
                        conteudo_tabela += item.replace(
                            ' class="grupo"', '').replace(
                            ' rowspan=""', '').replace(' colspan=""', '')

                conteudo_tabela += '</tr>\n'

            conteudo_tabela += Geral.RODAPE_TABELA

            if len(anexos_tabela) > 0:
                conteudo_tabela += Tabela.ANEXO.format(
                    ''.join([anexo + '\n' for anexo in anexos_tabela]))

        conteudo_indice += Tabela.LINHA_INDICE.format(
            numero=tabela[:-4], titulo=titulo)

        tabelas.append(tabela[:-4])

    conteudo = inicio.replace(
        'SUBTITULO',  f'eSocial {versao} - Tabelas {publicacao_reduzida}').replace(
        'TITULO', f'eSocial {versao} - Tabelas').replace(
        'TEXTO_1', '<h1 class="title has-text-centered is-3">ANEXO I DOS LEIAUTES DO eSOCIAL<br />TABELAS</h1>').replace(
        'TEXTO_2', '<h1 class="title has-text-centered is-3">{}</h1>'.format(
            f'{versao_m} {publicacao}'))

    conteudo += '<h2 class="title has-text-centered is-3">Sumário</h2>\n'
    conteudo += '<ul class="sumario">\n'
    conteudo += conteudo_indice
    conteudo += '</ul>\n'
    conteudo += conteudo_tabela
    conteudo += fim

    with cinto.obter_arquivo(caminho_saida.format('tabelas.html'), 'w') as f:
        f.write(conteudo)

    # VERIFICAÇÃO DE LINKS

    links = []
    [links.append(item)
        for item in re.findall(r'"\#(\S+)"', html) if item not in links]

    ids = []
    [ids.append(item)
        for item in re.findall(r'id="(\S+)"', html) if item not in ids]
    ids = ids + tabelas

    ausentes = [link for link in links if link not in ids]

    if ausentes:
        print('Links quebrados:')
        [print(link) for link in ausentes]

    print('Tempo de execução: ', perf_counter() - inicio_tempo, '\n')
