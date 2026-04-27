import logic

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
    while True:
        opcao = menu()

        if opcao == "1":
            valor = input("Valor da receita: ")
            desc = input("Descrição: ")
            # Validação simples antes de enviar para a lógica
            if valor.replace('.', '', 1).isdigit():
                logic.adicionar_item(float(valor), desc, "receita")
            else:
                print("Erro: Valor inválido.")

        elif opcao == "3":
            receitas = logic.obter_lista("receita")
            for r in receitas:
                print(f"{r['descricao']}: {r['valor']}€")

        elif opcao == "8":
            logic.guardar_dados()
            print("Dados guardados. A sair...")
            break
        
        else:
            print("Opção inválida ou ainda não implementada.")

if __name__ == "__main__":
    main()
