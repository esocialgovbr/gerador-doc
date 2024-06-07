class Geral:
    RODAPE_TABELA = (
        '</tbody>\n'
        '</table>\n')

    LINK = '<a href="#{}">{}</a>'


class Tabela:
    CELULA = '<td rowspan="" colspan=""{classe}>{conteudo}</td>\n'

    CELULA_CABECALHO = (
        '<td class="grupo" rowspan="" colspan=""{dimensao}>{conteudo}</td>\n')

    ANEXO = (
        '<div class="message" style="font-size: .8em">\n'
        '<div class="message-body">\n{}'
        '</div>\n'
        '</div>\n')

    LINHA_INDICE = (
        '<li>'
        '<a href="#{numero}">Tabela {numero} - {titulo}</a>'
        '</li>\n')

    CABECALHO = (
        '<table id="{}"'
        ' class="table is-fullwidth is-bordered tabela quebra-anterior">\n'
        '<thead>\n'
        '<tr>\n'
        '<th id="t_{}" colspan="{}">Tabela {} - {}</th>\n'
        '</tr>\n'
        '<tr class="grupo">\n'
        '{}'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n')


class Regra:
    LINHA = (
        '<tr>\n'
        '<td id="{id}"><a title="Ver ocorrências"><strong>{nome}</strong></a></td>\n'
        '<td>{texto}</td>\n'
        '</tr>\n')

    LINHA_MODAL = (
        '<div class="modal" id="{nome}">\n'
        '<div class="modal-background"></div>\n'
        '<div class="modal-card">\n'
        '<header class="modal-card-head">\n'
        '<p class="modal-card-title"><a href="regras.html#{nome}">{nome}</a></p>\n'
        '<button class="delete" aria-label="close"></button>\n'
        '</header>\n'
        '<div class="modal-card-body">\n'
        '<p>{texto}</p>\n'
        '</div>\n'
        '</div>\n'
        '</div>\n')

    LINHA_REFERENCIA = (
        '<li><a href="index.html#{id}">{trilha}</a></li>')

    LINHA_MODAL_REFERENCIA = (
        '<div class="modal" id="r_{nome}">\n'
        '<div class="modal-background"></div>\n'
        '<div class="modal-card">\n'
        '<header class="modal-card-head">\n'
        '<p class="modal-card-title">{nome}</p>\n'
        '<button class="delete" aria-label="close"></button>\n'
        '</header>\n'
        '<div class="modal-card-body">\n'
        '<ul>{texto}</ul>\n'
        '</div>\n'
        '</div>\n'
        '</div>\n')

    CABECALHO = (
        '<table class="table is-fullwidth is-bordered regras">\n'
        '<tbody>\n'
        '<tr>\n'
        '<th>Nome</th>\n'
        '<th>Descrição</th>\n'
        '</tr>\n')


class Resumo:
    LINHA_TEXTO = (
        'Nível: {nivel}\n'
        'Nome: {nome}\n'
        'Pai: {pai}\n'
        'Descrição: {descricao}\n'
        'Ocorrência: {ocorrencia}\n'
        'Chave: {chave}\n'
        'Condição: {condicao}\n\n')

    LINHA = (
        '<tr>\n'
        '<td id="r_{link_completo}">'
        '<a href="#{link_completo}">{nome}</a>'
        '</td>\n'
        '<td>{pai}</td>\n'
        '<td>{nivel}</td>\n'
        '<td>{descricao}</td>\n'
        '<td>{ocorrencia}</td>\n'
        '<td>{chave}</td>\n'
        '<td>{condicao}</td>\n'
        '</tr>\n')

    LINHA_INDICE = (
        '<li>'
        '<a href="#{nome}">{codigo} - {descricao}</a>'
        '</li>\n')

    REFERENCIA = (
        '<tr>\n'
        '<td>...</td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '<td><strong>Ver:</strong> '
        '<a href="#r_{id_pai}">'
        '{nome_pai}</a> &gt; '
        '<a href="#r_{id}">'
        '{nome}</a></td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '</tr>\n')

    CABECALHO = (
        '\n'
        '<h3 id="{}" class="title has-text-centered quebra-anterior">{} - {}</h3>\n'
        '<table class="table is-fullwidth is-bordered resumo">\n'
        '<tbody>\n'
        '<tr>\n'
        '<th colspan="7">Tabela de Resumo dos '
        'Registros</th>\n'
        '</tr>\n'
        '<tr class="grupo">\n'
        '<td>'
        '<strong>Grupo</strong></td>\n'
        '<td>'
        '<strong>Grupo Pai</strong></td>\n'
        '<td>'
        '<strong>Nível</strong></td>\n'
        '<td>'
        '<strong>Descrição</strong></td>\n'
        '<td>'
        '<strong>Ocor.</strong></td>\n'
        '<td>'
        '<strong>Chave</strong></td>\n'
        '<td>'
        '<strong>Condição</strong></td>\n'
        '</tr>\n')

    LEGENDA = (
        '\n'
        '<p class="is-size-6" style="margin-top: -1rem; margin-bottom: 2rem;">* Campo chave do evento</p>\n')


class Completo:
    LINHA_TEXTO = (
        'Nome: {nome}\n'
        'Pai: {pai}\n'
        'Elem.: {tipo_elemento}\n'
        'Tipo: {tipo}\n'
        'Ocorrência: {ocorrencia}\n'
        'Tamanho: {tamanho}\n'
        'Dec.: {decimais}\n'
        'Descrição: {descricao}\n\n'
    )

    LINHA = (
        '<tr{marcador_grupo}>\n'
        '<td class="seletor" onclick="copiarCaminho.call(this)"'
        ' title="{caminho}"'
        ' id="{caminho}">{indice}</td>\n'
        '<td>'
        '{nome}'
        '</td>\n'
        '<td>{pai}</td>\n'
        '<td>{tipo_elemento}</td>\n'
        '<td>{tipo}</td>\n'
        '<td>{ocorrencia}</td>\n'
        '<td>{tamanho}</td>\n'
        '<td>{decimais}</td>\n'
        '<td>{descricao}</td>\n'
        '</tr>\n')

    REFERENCIA = (
        '<tr>\n'
        '<td>...</td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '<td></td>\n'
        '<td><strong>Ver:</strong> '
        '<a href="#{id_pai}">{nome_pai}</a> &gt; '
        '<a href="#{id}">{nome}</a></td>\n'
        '</tr>\n')

    CABECALHO = (
        '\n'
        '<h4 class="subtitle has-text-centered">'
        'Registros do evento {} - {}</h4>\n'
        '<table class="table is-fullwidth is-bordered completo">\n'
        '<tbody>\n'
        '<tr>\n'
        '<th class="seletor">#</th>\n'
        '<th>Grupo/Campo</th>\n'
        '<th>Grupo Pai</th>\n'
        '<th>Elem.</th>\n'
        '<th>Tipo</th>\n'
        '<th>Ocor.</th>\n'
        '<th>Tamanho</th>\n'
        '<th>Dec.</th>\n'
        '<th>Descrição</th>\n'
        '</tr>\n')
