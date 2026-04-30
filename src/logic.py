import logic

CAMINHO = "dados.json"

def menu():
    print("\n=== Orçamento Familiar ===")
    print("1. Adicionar receita")
    print("2. Adicionar despesa")
    print("3. Listar receitas")
    print("4. Listar despesas")
    print("5. Saldo do mês")
    print("6. Resumo por categoria")
    print("7. Editar/Remover lançamento")
    print("8. Guardar e sair")
    return input("\nEscolha uma opção: ")


def main():
    dados = logic.carregar_dados(CAMINHO)

    while True:
        opcao = menu()

        if opcao == "1":
            valor = input("Valor da receita: ")
            desc = input("Descrição: ")

            if valor.replace('.', '', 1).isdigit():
                receita = {
                    "id": logic.gerar_id("R"),
                    "valor": float(valor),
                    "descricao": desc
                }

                if logic.validar_lancamento(receita):
                    dados = logic.adicionar_receita(dados, receita)
                    print("Receita adicionada.")
                else:
                    print("Erro: Dados inválidos.")
            else:
                print("Erro: Valor inválido.")

        elif opcao == "2":
            valor = input("Valor da despesa: ")
            desc = input("Descrição: ")

            if valor.replace('.', '', 1).isdigit():
                despesa = {
                    "id": logic.gerar_id("D"),
                    "valor": float(valor),
                    "descricao": desc
                }

                if logic.validar_lancamento(despesa):
                    dados = logic.adicionar_despesa(dados, despesa)
                    print("Despesa adicionada.")
                else:
                    print("Erro: Dados inválidos.")
            else:
                print("Erro: Valor inválido.")

        elif opcao == "3":
            for r in dados.get("receitas", []):
                print(f"{r['id']} - {r['descricao']}: {r['valor']}€")

        elif opcao == "4":
            for d in dados.get("despesas", []):
                print(f"{d['id']} - {d['descricao']}: {d['valor']}€")

        elif opcao == "5":
            saldo = logic.saldo(dados)
            print(f"Saldo atual: {saldo}€")

        elif opcao == "6":
            resumo = logic.agrupar_por_categoria(dados, "despesas")
            for cat, total in resumo.items():
                print(f"{cat}: {total}€")

        elif opcao == "7":
            id_lanc = input("ID do lançamento: ")
            acao = input("Editar (E) ou Remover (R)? ").lower()

            if acao == "r":
                dados = logic.remover_lancamento(dados, id_lanc)
                print("Removido.")
            elif acao == "e":
                campo = input("Campo a editar (valor/descricao): ")
                novo_valor = input("Novo valor: ")

                alteracoes = {campo: novo_valor}
                dados = logic.editar_lancamento(dados, id_lanc, alteracoes)
                print("Editado.")
            else:
                print("Ação inválida.")

        elif opcao == "8":
            logic.guardar_dados(dados, CAMINHO)
            print("Dados guardados. A sair...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
