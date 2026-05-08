import logic
import os

# Configuração de caminhos
DB_PATH = "Src/expenses_revenues.json"

def limpar_ecra():
    """Limpa a consola dependendo do Sistema Operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def formatar_moeda(valor):
    """Transforma 1500.0 em 1.500,00 €."""
    return f"{valor:,.2f}€".replace(",", "X").replace(".", ",").replace("X", ".")

def exibir_menu():
    print("\n" + "="*30)
    print("      ORÇAMENTO FAMILIAR")
    print("="*30)
    print("1. ➕ Adicionar Receita")
    print("2. ➖ Adicionar Despesa")
    print("3. 📑 Listar Receitas")
    print("4. 📑 Listar Despesas")
    print("5. 💰 Saldo do Mês")
    print("6. 📊 Resumo por Categoria")
    print("7. ⚙️  Editar/Remover Lançamento")
    print("8. 💾 Guardar e Sair")
    print("="*30)
    return input("Escolha uma opção: ")

def main():
    # 1. Carregar dados ao iniciar
    dados = logic.carregar_dados(DB_PATH)
    
    while True:
        opcao = exibir_menu()

        if opcao in ["1", "2"]:
            tipo = "R" if opcao == "1" else "D"
            print(f"\n--- Adicionar {'Receita' if tipo == 'R' else 'Despesa'} ---")
            
            try:
                descricao = input("Descrição: ")
                valor = float(input("Valor: "))
                # Exemplo de categorias fixas sugeridas
                print("Categorias: Salário, Prémio, Alimentação, Habitação, Lazer, Outros")
                categoria = input("Categoria: ").strip().lower()

                novo_item = {
                    "id": logic.gerar_id(tipo, dados),
                    "descricao": descricao,
                    "valor": valor,
                    "categoria": categoria
                }

                if logic.validar_lancamento(novo_item):
                    if tipo == "R":
                        dados = logic.adicionar_receita(dados, novo_item)
                    else:
                        dados = logic.adicionar_despesa(dados, novo_item)
                    print("✅ Lançamento registado com sucesso!")
                else:
                    print("❌ Erro: Dados inválidos.")
            
            except ValueError:
                print("⚠️ Erro: Por favor, insira um número válido para o valor.")

        elif opcao == "3":
            print("\n--- Listagem de Receitas ---")
            for r in dados.get('receitas', []):
                print(f"ID: {r['id']} | {r['descricao']}: {formatar_moeda(r['valor'])}")

        elif opcao == "4":
            print("\n--- Listagem de Despesas ---")
            for d in dados.get('despesas', []):
                print(f"ID: {d['id']} | {d['descricao']}: {formatar_moeda(d['valor'])}")

        elif opcao == "5":
            mes = input("Mês (MM): ")
            ano = input("Ano (AAAA): ")
            saldo_final = logic.calcular_saldo(dados, mes, ano)
            print(f"\n💰 Saldo em {mes}/{ano}: {formatar_moeda(saldo_final)}")

        elif opcao == "6":
            print("\n--- Resumo por Categoria ---")
            resumo = logic.agrupar_por_categoria(dados)
            for cat, total in resumo.items():
                print(f"{cat.capitalize()}: {formatar_moeda(total)}")

        elif opcao == "8":
            logic.guardar_dados(dados, DB_PATH)
            print("💾 Dados guardados com segurança. Até à próxima!")
            break

        else:
            print("⚠️ Opção inválida. Tenta novamente.")
            
        input("\nPrime [Enter] para continuar...")
        limpar_ecra()

if __name__ == "__main__":
    main()