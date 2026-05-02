"""
Módulo logic.py — regras de negócio do Orçamento Familiar.

Responsabilidades:
    - Persistência em JSON (carregar/guardar)
    - Validação de lançamentos
    - Cálculos de totais e saldo
    - Agregações por categoria
    - Geração de IDs sequenciais

Não tem interface com utilizador — isso é tratado em `main.py`.

Estrutura de dados esperada (ver Docs/data-schema.md):

    {
      "metadata": {
        "familia": str, "moeda": "EUR",
        "criado_em": "YYYY-MM-DD", "ultima_atualizacao": "YYYY-MM-DD"
      },
      "membros":  [ { "id": int, "nome": str, "relacao": str }, ... ],
      "receitas": [ { "id": "R001", "data": "...", ... }, ... ],
      "despesas": [ { "id": "D001", "data": "...", ... }, ... ]
    }
"""

import json
import os
import re
from datetime import date


# ============================================================================
# Estrutura por defeito (usada quando o ficheiro ainda não existe)
# ============================================================================

def _estrutura_vazia():
    """Devolve o esqueleto inicial do JSON."""
    hoje = date.today().isoformat()
    return {
        "metadata": {
            "familia": "Família Silva",
            "moeda": "EUR",
            "criado_em": hoje,
            "ultima_atualizacao": hoje
        },
        "membros": [
            {"id": 1, "nome": "João Silva",  "relacao": "pai"},
            {"id": 2, "nome": "Maria Silva", "relacao": "mãe"},
            {"id": 3, "nome": "Tomás Silva", "relacao": "filho"}
        ],
        "receitas": [],
        "despesas": []
    }


# ============================================================================
# Persistência: carregar e guardar o JSON
# ============================================================================

def carregar_dados(caminho):
    """Lê o JSON do disco. Se não existir, devolve uma estrutura vazia válida."""
    if not os.path.exists(caminho):
        return _estrutura_vazia()
    with open(caminho, "r", encoding="utf-8") as ficheiro:
        return json.load(ficheiro)


def guardar_dados(dados, caminho):
    """Grava `dados` em disco e atualiza `metadata.ultima_atualizacao`."""
    if "metadata" not in dados:
        dados["metadata"] = _estrutura_vazia()["metadata"]
    dados["metadata"]["ultima_atualizacao"] = _data_mais_recente(dados)

    with open(caminho, "w", encoding="utf-8") as ficheiro:
        json.dump(dados, ficheiro, ensure_ascii=False, indent=2)


def _data_mais_recente(dados):
    """Devolve a data mais tardia entre todos os lançamentos (ou hoje)."""
    todas_datas = []
    for receita in dados.get("receitas", []):
        if "data" in receita:
            todas_datas.append(receita["data"])
    for despesa in dados.get("despesas", []):
        if "data" in despesa:
            todas_datas.append(despesa["data"])

    if len(todas_datas) == 0:
        return date.today().isoformat()
    return max(todas_datas)


# ============================================================================
# Geração de IDs e validação
# ============================================================================

def gerar_id(tipo, dados=None):
    """
    Gera o próximo ID sequencial do tipo indicado.

    `tipo` é "R" (receita) ou "D" (despesa). O ID tem 3 dígitos:
    R001, R002, ..., D015, ...
    """
    tipo = tipo.upper()

    if dados is None:
        return f"{tipo}001"

    if tipo == "R":
        lista = dados.get("receitas", [])
    else:
        lista = dados.get("despesas", [])

    maior_numero = 0
    for item in lista:
        identificador = item.get("id", "")
        # Formato esperado: letra (R/D) seguida de dígitos. Ex.: "R012".
        if len(identificador) >= 2 and identificador[0] == tipo:
            parte_numero = identificador[1:]
            if parte_numero.isdigit():
                numero = int(parte_numero)
                if numero > maior_numero:
                    maior_numero = numero

    proximo = maior_numero + 1
    return f"{tipo}{proximo:03d}"


_PADRAO_ID = re.compile(r"^[RD]\d{3,}$")


def validar_lancamento(lancamento):
    """
    Valida campos obrigatórios mínimos de um lançamento.

    Regras:
      - tem de ser um dicionário
      - "id" no formato R### ou D### (mínimo 3 dígitos)
      - "descricao" presente e não vazia
      - "valor" numérico (int ou float) maior que zero
      - "categoria" presente e não vazia
    """
    if not isinstance(lancamento, dict):
        return False

    identificador = lancamento.get("id", "")
    if not isinstance(identificador, str):
        return False
    if _PADRAO_ID.match(identificador) is None:
        return False

    descricao = lancamento.get("descricao", "")
    if not isinstance(descricao, str) or descricao.strip() == "":
        return False

    valor = lancamento.get("valor", None)
    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        return False
    if valor <= 0:
        return False

    categoria = lancamento.get("categoria", "")
    if not isinstance(categoria, str) or categoria.strip() == "":
        return False

    return True


# ============================================================================
# Auto-completar campos opcionais (quando o main.py cria items "magros")
# ============================================================================

def _completar_receita(dados, receita):
    """Preenche campos opcionais de uma receita com defaults sensatos."""
    if "data" not in receita:
        receita["data"] = date.today().isoformat()

    if "membro_id" not in receita:
        membros = dados.get("membros", [])
        if len(membros) > 0:
            receita["membro_id"] = membros[0]["id"]
        else:
            receita["membro_id"] = 1

    if "recorrente" not in receita:
        receita["recorrente"] = False
    if "frequencia" not in receita:
        receita["frequencia"] = "unica"

    return receita


def _completar_despesa(despesa):
    """Preenche campos opcionais de uma despesa com defaults sensatos."""
    if "data" not in despesa:
        despesa["data"] = date.today().isoformat()
    if "subcategoria" not in despesa:
        despesa["subcategoria"] = ""
    if "metodo_pagamento" not in despesa:
        despesa["metodo_pagamento"] = "dinheiro"
    if "recorrente" not in despesa:
        despesa["recorrente"] = False
    if "frequencia" not in despesa:
        despesa["frequencia"] = "unica"
    return despesa


# ============================================================================
# CRUD: criar, remover, editar
# ============================================================================

def adicionar_receita(dados, receita):
    """Insere uma receita em `dados['receitas']` e devolve `dados` atualizado."""
    receita_completa = _completar_receita(dados, receita)
    if "receitas" not in dados:
        dados["receitas"] = []
    dados["receitas"].append(receita_completa)
    return dados


def adicionar_despesa(dados, despesa):
    """Insere uma despesa em `dados['despesas']` e devolve `dados` atualizado."""
    despesa_completa = _completar_despesa(despesa)
    if "despesas" not in dados:
        dados["despesas"] = []
    dados["despesas"].append(despesa_completa)
    return dados


def remover_lancamento(dados, id_lanc):
    """
    Remove o lançamento com o ID indicado.

    Procura tanto em receitas como em despesas. Se não encontrar, devolve
    `dados` inalterado.
    """
    id_lanc = id_lanc.strip().upper()

    receitas_filtradas = []
    for receita in dados.get("receitas", []):
        if receita.get("id") != id_lanc:
            receitas_filtradas.append(receita)
    dados["receitas"] = receitas_filtradas

    despesas_filtradas = []
    for despesa in dados.get("despesas", []):
        if despesa.get("id") != id_lanc:
            despesas_filtradas.append(despesa)
    dados["despesas"] = despesas_filtradas

    return dados


def editar_lancamento(dados, id_lanc, alteracoes):
    """
    Edita os campos indicados em `alteracoes` (dict) no lançamento com `id_lanc`.

    Procura primeiro em receitas, depois em despesas. Se não encontrar,
    devolve `dados` inalterado.
    """
    id_lanc = id_lanc.strip().upper()

    for receita in dados.get("receitas", []):
        if receita.get("id") == id_lanc:
            for chave in alteracoes:
                receita[chave] = alteracoes[chave]
            return dados

    for despesa in dados.get("despesas", []):
        if despesa.get("id") == id_lanc:
            for chave in alteracoes:
                despesa[chave] = alteracoes[chave]
            return dados

    return dados


# ============================================================================
# Filtros e cálculos de totais
# ============================================================================

def _normalizar_mes_ano(mes, ano):
    """
    Normaliza mes/ano para strings (`'03'`, `'2026'`).

    Aceita ints (3 -> '03') e strings ('3' ou '03' -> '03').
    """
    mes_str = str(mes).zfill(2)
    ano_str = str(ano)
    return mes_str, ano_str


def _filtrar_por_mes_ano(lancamentos, mes, ano):
    """
    Filtra lançamentos pela data ('YYYY-MM-DD').

    Se `mes` ou `ano` forem None, devolve a lista inteira (sem filtro).
    """
    if mes is None or ano is None:
        return lancamentos

    mes_str, ano_str = _normalizar_mes_ano(mes, ano)
    prefixo = f"{ano_str}-{mes_str}"

    resultado = []
    for item in lancamentos:
        data = item.get("data", "")
        if data.startswith(prefixo):
            resultado.append(item)
    return resultado


def total_receitas(dados, mes=None, ano=None):
    """Soma das receitas, opcionalmente filtrada por mês/ano."""
    receitas = _filtrar_por_mes_ano(dados.get("receitas", []), mes, ano)
    soma = 0.0
    for receita in receitas:
        soma = soma + receita.get("valor", 0)
    return round(soma, 2)


def total_despesas(dados, mes=None, ano=None):
    """Soma das despesas, opcionalmente filtrada por mês/ano."""
    despesas = _filtrar_por_mes_ano(dados.get("despesas", []), mes, ano)
    soma = 0.0
    for despesa in despesas:
        soma = soma + despesa.get("valor", 0)
    return round(soma, 2)


def saldo(dados, mes=None, ano=None):
    """Receitas menos despesas no período indicado (None = considera tudo)."""
    receitas = total_receitas(dados, mes, ano)
    despesas = total_despesas(dados, mes, ano)
    return round(receitas - despesas, 2)


def calcular_saldo(dados, mes, ano):
    """Alias de `saldo`. Existe para compatibilidade com `main.py`."""
    return saldo(dados, mes, ano)


def calcular_media_mensal(dados, ano, tipo="despesas"):
    """
    Devolve a média mensal de receitas ou despesas para o ano indicado.

    `tipo` pode ser "receitas" ou "despesas". Por defeito calcula a média
    de despesas. A média é calculada apenas sobre os meses em que houve
    pelo menos um lançamento (não divide por 12 fixo).
    """
    if tipo == "receitas":
        lista = dados.get("receitas", [])
    else:
        lista = dados.get("despesas", [])

    totais_por_mes = {}
    for item in lista:
        data = item.get("data", "")
        if not data.startswith(str(ano)):
            continue
        mes = data[5:7]
        if mes in totais_por_mes:
            totais_por_mes[mes] = totais_por_mes[mes] + item.get("valor", 0)
        else:
            totais_por_mes[mes] = item.get("valor", 0)

    if len(totais_por_mes) == 0:
        return 0.0

    soma = 0.0
    for mes in totais_por_mes:
        soma = soma + totais_por_mes[mes]
    return round(soma / len(totais_por_mes), 2)


# ============================================================================
# Agregações por categoria
# ============================================================================

def agrupar_por_categoria(dados, tipo="despesas"):
    """
    Devolve um dicionário {categoria: total} para o `tipo` indicado.

    `tipo` é "receitas" ou "despesas". Por defeito agrega despesas.
    """
    if tipo == "receitas":
        lista = dados.get("receitas", [])
    else:
        lista = dados.get("despesas", [])

    agregado = {}
    for item in lista:
        categoria = item.get("categoria", "outros")
        valor = item.get("valor", 0)
        if categoria in agregado:
            agregado[categoria] = agregado[categoria] + valor
        else:
            agregado[categoria] = valor

    # Arredondar no fim, para evitar erros de vírgula flutuante
    for categoria in agregado:
        agregado[categoria] = round(agregado[categoria], 2)
    return agregado


def resumo_mensal(dados, mes, ano):
    """
    Resumo completo de um mês: totais e agrupamentos.

    Devolve um dicionário com:
      - mes, ano
      - total_receitas, total_despesas, saldo
      - receitas_por_categoria, despesas_por_categoria
    """
    mes_str, ano_str = _normalizar_mes_ano(mes, ano)

    receitas_filtradas = _filtrar_por_mes_ano(dados.get("receitas", []), mes, ano)
    despesas_filtradas = _filtrar_por_mes_ano(dados.get("despesas", []), mes, ano)

    sub_dados = {
        "receitas": receitas_filtradas,
        "despesas": despesas_filtradas
    }

    return {
        "mes": mes_str,
        "ano": ano_str,
        "total_receitas": total_receitas(dados, mes, ano),
        "total_despesas": total_despesas(dados, mes, ano),
        "saldo": saldo(dados, mes, ano),
        "receitas_por_categoria": agrupar_por_categoria(sub_dados, "receitas"),
        "despesas_por_categoria": agrupar_por_categoria(sub_dados, "despesas")
    }
