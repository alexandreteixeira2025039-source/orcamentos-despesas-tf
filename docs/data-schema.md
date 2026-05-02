# Esquema de dados — `expenses_revenues.json`

Documentação da estrutura do ficheiro de persistência usado pelo Orçamento Familiar.

O ficheiro é um único objeto JSON com quatro secções de topo: `metadata`, `membros`, `receitas` e `despesas`.

```json
{
  "metadata": {  },
  "membros":  [  ],
  "receitas": [  ],
  "despesas": [  ]
}
```

Codificação: **UTF-8 sem BOM**. Valores monetários sempre em **EUR**, com **ponto** como separador decimal (convenção JSON) e duas casas decimais.

---

## 1. `metadata`

Objeto com informação geral sobre o ficheiro.

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `familia` | string | ✅ | Nome da família a quem pertence o orçamento. | `"Família Silva"` |
| `moeda` | string | ✅ | Código ISO 4217 da moeda. Atualmente apenas `"EUR"`. | `"EUR"` |
| `criado_em` | string (data `YYYY-MM-DD`) | ✅ | Data de criação do ficheiro. | `"2026-02-01"` |
| `ultima_atualizacao` | string (data `YYYY-MM-DD`) | ✅ | Data do lançamento mais recente. Atualizado em cada gravação. | `"2026-04-30"` |

---

## 2. `membros`

Array de objetos. Cada elemento da família que pode ser titular de receitas. Mínimo: 1 elemento.

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `id` | int | ✅ | Identificador único do membro (sequencial, começa em 1). | `1` |
| `nome` | string | ✅ | Nome completo. | `"João Silva"` |
| `relacao` | string | ✅ | Relação familiar. Sugestões: `pai`, `mãe`, `filho`, `filha`, `avo`, `avó`, `outro`. | `"pai"` |

Exemplo:

```json
{ "id": 1, "nome": "João Silva", "relacao": "pai" }
```

---

## 3. `receitas`

Array de lançamentos de entrada de dinheiro. Cada lançamento referencia um `membro` através de `membro_id`.

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `id` | string | ✅ | Identificador único, formato `R` + 3 dígitos (`R001`–`R999`). Sequencial. | `"R001"` |
| `data` | string (data `YYYY-MM-DD`) | ✅ | Data em que a receita foi recebida. | `"2026-02-28"` |
| `descricao` | string | ✅ | Descrição livre, breve. | `"Salário Fevereiro - João"` |
| `categoria` | string | ✅ | Uma de: `salario`, `subsidio_refeicao`, `subsidio_ferias`, `subsidio_natal`, `prestacoes_sociais`, `extras`. | `"salario"` |
| `membro_id` | int | ✅ | `id` do membro a quem a receita pertence. Tem de existir em `membros`. | `1` |
| `valor` | float | ✅ | Montante em euros, **positivo**, com 2 casas decimais. | `1100.00` |
| `recorrente` | bool | ✅ | `true` se a receita se repete; `false` se for pontual. | `true` |
| `frequencia` | string | ✅ | Periodicidade. Para `recorrente=true`: `mensal`, `anual`. Para `recorrente=false`: `unica`. | `"mensal"` |

### Categorias de receitas permitidas

| Categoria | Significado |
|-----------|-------------|
| `salario` | Vencimento mensal de um membro. |
| `subsidio_refeicao` | Subsídio de refeição (cartão ou em dinheiro). |
| `subsidio_ferias` | Subsídio de férias (geralmente pago uma ou duas vezes por ano). |
| `subsidio_natal` | Subsídio de Natal. |
| `prestacoes_sociais` | Abono de família, RSI, prestações da Segurança Social, etc. |
| `extras` | Prémios, reembolsos, presentes em dinheiro, biscates pontuais. |

Exemplo:

```json
{
  "id": "R001",
  "data": "2026-02-28",
  "descricao": "Salário Fevereiro - João",
  "categoria": "salario",
  "membro_id": 1,
  "valor": 1100.00,
  "recorrente": true,
  "frequencia": "mensal"
}
```

---

## 4. `despesas`

Array de lançamentos de saída de dinheiro. As despesas **não** estão associadas a um membro específico — pertencem ao orçamento familiar.

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `id` | string | ✅ | Identificador único, formato `D` + 3 dígitos (`D001`–`D999`). Sequencial. | `"D001"` |
| `data` | string (data `YYYY-MM-DD`) | ✅ | Data do pagamento. | `"2026-02-01"` |
| `descricao` | string | ✅ | Descrição livre, breve. | `"Renda Fevereiro"` |
| `categoria` | string | ✅ | Uma de: `habitacao`, `utilidades`, `alimentacao`, `transportes`, `saude`, `educacao`, `lazer`, `vestuario`, `outros`. | `"habitacao"` |
| `subcategoria` | string | ⚠️ recomendado | Detalhe livre dentro da categoria (ex.: `renda`, `electricidade`, `supermercado`). Pode ficar vazio se não fizer sentido. | `"renda"` |
| `valor` | float | ✅ | Montante em euros, **positivo**, com 2 casas decimais. | `720.00` |
| `metodo_pagamento` | string | ✅ | Um de: `transferencia`, `mb_way`, `multibanco`, `dinheiro`, `cartao_credito`. | `"transferencia"` |
| `recorrente` | bool | ✅ | `true` se a despesa se repete; `false` se for pontual. | `true` |
| `frequencia` | string | ✅ | Periodicidade. Para `recorrente=true`: `mensal`, `anual`. Para `recorrente=false`: `unica` (ou `anual` para encargos anuais isolados). | `"mensal"` |

### Categorias de despesas permitidas

| Categoria | Exemplos de subcategoria |
|-----------|--------------------------|
| `habitacao` | `renda`, `condominio`, `iptv`, `manutencao` |
| `utilidades` | `electricidade`, `agua`, `gas`, `internet`, `telemovel` |
| `alimentacao` | `supermercado`, `padaria`, `cafetaria`, `mercearia` |
| `transportes` | `combustivel`, `passe`, `credito_automovel`, `seguro`, `iuc`, `reparacao`, `portagem` |
| `saude` | `farmacia`, `consulta`, `oculos`, `dentista` |
| `educacao` | `material_escolar`, `propinas`, `atividades_extracurriculares`, `explicacoes`, `excursao` |
| `lazer` | `restaurante`, `cinema`, `streaming`, `desporto`, `viagens`, `presentes` |
| `vestuario` | `adulto`, `crianca`, `calcado`, `acessorios` |
| `outros` | `cuidados_pessoais`, `animais`, `eletrodomesticos`, `reparacoes_domesticas` |

### Métodos de pagamento permitidos

| Valor | Significado |
|-------|-------------|
| `transferencia` | Transferência bancária (homebanking). |
| `mb_way` | Pagamento via MB WAY. |
| `multibanco` | Cartão de débito num terminal Multibanco. |
| `dinheiro` | Numerário. |
| `cartao_credito` | Cartão de crédito. |

Exemplo:

```json
{
  "id": "D001",
  "data": "2026-02-01",
  "descricao": "Renda Fevereiro",
  "categoria": "habitacao",
  "subcategoria": "renda",
  "valor": 720.00,
  "metodo_pagamento": "transferencia",
  "recorrente": true,
  "frequencia": "mensal"
}
```

---

## Regras transversais

1. **IDs únicos e sequenciais.** Não pode haver dois lançamentos com o mesmo `id`. Os IDs são gerados pela função `logic.gerar_id(tipo)`.
2. **Datas no formato `YYYY-MM-DD`.** Sem hora.
3. **Valores positivos.** As despesas não usam sinal negativo — o sinal é dado pelo array em que o lançamento aparece (`receitas` vs. `despesas`).
4. **`metadata.ultima_atualizacao`** deve ser sempre igual à data mais recente entre todos os lançamentos.
5. **Integridade referencial:** todo `membro_id` numa receita tem de existir em `membros`.
6. **Encoding:** UTF-8 sem BOM. Acentos preservados (`ã`, `ç`, `é`, ...).

---

## Versão e histórico

- **v1.0** — esquema inicial (Abril 2026), suporta despesas e receitas com membros, categorização fixa e periodicidade simples.