# Orçamento Familiar

Sistema de gestão financeira para famílias portuguesas, em Python puro. Permite registar e organizar receitas e despesas mensais, com persistência em JSON e cálculo automático de saldo.

> Trabalho de grupo · Abril 2026

---

## 👥 Autores

| Nome | Responsabilidade |
|------|------------------|
| Gonçalo | `expenses_revenues.json` — estrutura de dados |
| Tiago | `logic.py` — regras de negócio e cálculos |
| Alex | `main.py` — interface CLI |

---

## 🧰 Stack

- **Python 3.10+**
- Apenas biblioteca standard (`json`, `datetime`, `os`)
- Sem dependências externas, sem base de dados

---

## 📁 Estrutura

```
orcamento-familiar/
├── Docs/
│   └── (documentação, diagramas, manual de utilizador)
├── Src/
│   ├── main.py                  # interface CLI (Alex)
│   ├── logic.py                 # regras de negócio (Tiago)
│   └── expenses_revenues.json   # base de dados (Gonçalo)
├── README.md
└── .gitignore
```

---

## 🔁 Fluxo de dados

```
Utilizador  →  main.py  →  logic.py  →  expenses_revenues.json
   (input)     (UI/menus)   (cálculos)         (persistência)
```

O `main.py` nunca toca directamente no JSON. Tudo passa por `logic.py`.

---

## ▶️ Como correr

A partir da raiz do projeto, ou de qualquer outro directório:

```bash
python Src/main.py
# ou, equivalentemente
cd Src && python main.py
```

O `DB_PATH` é resolvido relativamente ao próprio script, por isso a app funciona seja qual for o CWD. Não é preciso instalar nada — usa apenas a biblioteca standard. O ficheiro `expenses_revenues.json` é criado automaticamente na primeira execução, caso ainda não exista.

---

## 🖥️ Menu da aplicação

```
=== Orçamento Familiar ===
1. Adicionar receita
2. Adicionar despesa
3. Listar receitas
4. Listar despesas
5. Saldo do mês
6. Resumo por categoria
7. Editar/Remover lançamento
8. Guardar e sair
```

---

## 📦 Estrutura do JSON

O ficheiro `expenses_revenues.json` está dividido em 4 secções:

```json
{
  "metadata": {
    "familia": "Família Exemplo",
    "moeda": "EUR",
    "criado_em": "2026-04-27",
    "ultima_atualizacao": "2026-04-27"
  },
  "membros": [
    { "id": 1, "nome": "João",  "relacao": "pai" },
    { "id": 2, "nome": "Maria", "relacao": "mãe" }
  ],
  "receitas": [
    {
      "id": "R001",
      "data": "2026-04-01",
      "descricao": "Salário Abril",
      "categoria": "salario",
      "membro_id": 1,
      "valor": 1450.00,
      "recorrente": true,
      "frequencia": "mensal"
    }
  ],
  "despesas": [
    {
      "id": "D001",
      "data": "2026-04-05",
      "descricao": "Renda da casa",
      "categoria": "habitacao",
      "subcategoria": "renda",
      "valor": 750.00,
      "metodo_pagamento": "transferencia",
      "recorrente": true,
      "frequencia": "mensal"
    }
  ]
}
```

### Categorias disponíveis

**Receitas:** `salario`, `subsidio_refeicao`, `subsidio_ferias`, `subsidio_natal`, `prestacoes_sociais`, `extras`

**Despesas:** `habitacao`, `utilidades`, `alimentacao`, `transportes`, `saude`, `educacao`, `lazer`, `vestuario`, `outros`

---

## ⚙️ API interna do `logic.py`

| Função | Devolve | Descrição |
|--------|---------|-----------|
| `carregar_dados(caminho)` | `dict` | Lê o JSON do disco. Se o ficheiro não existir, devolve uma estrutura vazia válida. |
| `guardar_dados(dados, caminho)` | `None` | Grava o JSON em disco (UTF-8, indent=2). Atualiza `metadata.ultima_atualizacao`. |
| `adicionar_receita(dados, receita)` | `dict` | Insere uma nova receita (auto-completa campos opcionais). |
| `adicionar_despesa(dados, despesa)` | `dict` | Insere uma nova despesa (auto-completa campos opcionais). |
| `remover_lancamento(dados, id_lanc)` | `dict` | Remove pelo ID (`R001`, `D001`, ...). |
| `editar_lancamento(dados, id_lanc, alteracoes)` | `dict` | Edita campos de um lançamento (recebe um `dict` com os campos a alterar). |
| `total_receitas(dados, mes=None, ano=None)` | `float` | Soma de receitas, opcionalmente filtrada por mês/ano (strings ou ints). |
| `total_despesas(dados, mes=None, ano=None)` | `float` | Soma de despesas, opcionalmente filtrada por mês/ano. |
| `saldo(dados, mes=None, ano=None)` | `float` | Receitas menos despesas no período indicado. |
| `calcular_saldo(dados, mes, ano)` | `float` | Alias de `saldo` — usado pelo `main.py`. |
| `calcular_media_mensal(dados, ano, tipo="despesas")` | `float` | Média mensal de receitas ou despesas num ano (divide pelos meses com lançamentos). |
| `agrupar_por_categoria(dados, tipo="despesas")` | `dict` | Total por categoria. `tipo` pode ser `"receitas"` ou `"despesas"`. |
| `resumo_mensal(dados, mes, ano)` | `dict` | Resumo completo do mês (totais e agrupamentos). |
| `validar_lancamento(lancamento)` | `bool` | Valida campos obrigatórios e formato (id `R###`/`D###`, valor positivo, descrição não vazia). |
| `gerar_id(tipo, dados=None)` | `str` | Gera o próximo ID sequencial (`R001`, `D001`, ...) consultando `dados`. |

> Estrutura completa do JSON e listas de categorias/métodos de pagamento em [`Docs/data-schema.md`](Docs/data-schema.md).

---

## 📝 Convenções de equipa

- **Branches:** `feature/main`, `feature/logic`, `feature/json`
- **Commits:** formato Conventional Commits — `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`
- **Cada um trabalha apenas no seu ficheiro.** Alterações cruzadas só em pull request.
- **Antes do merge final:** reunião curta para alinhar tipos e nomes de campos.

---

## 📅 Estado

Projecto em desenvolvimento. Versão inicial prevista para entrega académica.

---

## 📄 Licença

Projecto académico. Uso livre para fins educativos.
