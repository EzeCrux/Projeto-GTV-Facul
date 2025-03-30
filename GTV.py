import itertools
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
from tabulate import tabulate

def obter_variaveis(expressao):
    return sorted(set(re.findall(r'\b[A-Za-z]\b', expressao)))

def gerar_tabela(variaveis):
    return list(itertools.product([False, True], repeat=len(variaveis)))

def avaliar_expressao(expressao, variaveis, valores):
    try:
        contexto = dict(zip(variaveis, valores))
        return eval(expressao, {"__builtins__": None}, contexto)
    except Exception:
        return None

def formatar_expressao(expressao):
    substituicoes = {
        "→": " or not ", "=>": " or not ",
        "↔": " == ", "<=>": " == ",
        "⊕": " ^ ",
        "¬": " not ", "!": " not ",
        "∧": " and ", "&": " and ",
        "∨": " or ", "|": " or "
    }
    for simbolo, operador in substituicoes.items():
        expressao = expressao.replace(simbolo, operador)
    return expressao

def classificar_tabela(resultados):
    if all(resultados):
        return "Tautologia (Sempre verdadeiro)"
    elif not any(resultados):
        return "Contradição (Sempre falso)"
    else:
        return "Contingência (Às vezes verdadeiro, às vezes falso)"

def gerar_expressao_aleatoria():
    variaveis = random.sample("ABCDEFG", random.randint(2, 4))
    operadores = ["∧", "∨", "→", "↔", "⊕"]
    expressao = random.choice(variaveis)
    for _ in range(random.randint(1, 3)):
        expressao += f" {random.choice(operadores)} {random.choice(variaveis)}"
    entrada_expressao.delete(0, tk.END)
    entrada_expressao.insert(0, expressao)

def mostrar_instrucoes():
    janela_instrucoes = tk.Toplevel(janela)
    janela_instrucoes.title("Como Usar")
    janela_instrucoes.geometry("450x400")
    
    texto_instrucoes = (
        "Instruções de Uso:\n\n"
        "- Digite uma expressão lógica usando variáveis de A-Z.\n"
        "- Use os seguintes operadores:\n"
        "  ∧  (E) - Conjunção\n"
        "  ∨  (OU) - Disjunção\n"
        "  →  ou =>  (IMPLICAÇÃO)\n"
        "  ↔  ou <=>  (BI-IMPLICAÇÃO)\n"
        "  ⊕  (XOR) - OU Exclusivo\n"
        "  ¬  ou !  (NÃO) - Negação\n\n"
        "- Pressione 'Gerar Tabela' para visualizar a tabela verdade.\n"
        "- Pressione 'Expressão Aleatória' para gerar um exemplo automático.\n"
        "- Copie os símbolos abaixo para facilitar a inserção de expressões."
    )
    
    label = tk.Label(janela_instrucoes, text=texto_instrucoes, justify=tk.LEFT, anchor="w")
    label.pack(pady=10, padx=10, fill=tk.BOTH)
    
    frame_copiar = tk.Frame(janela_instrucoes)
    frame_copiar.pack(pady=5)
    
    entrada_caracteres = tk.Entry(frame_copiar, width=40, justify="center")
    entrada_caracteres.pack(side=tk.LEFT, padx=5)
    entrada_caracteres.insert(0, "∧ ∨ → ↔ ⊕ ¬ ! & | => <=>")
    
    def copiar_simbolos():
        janela_instrucoes.clipboard_clear()
        janela_instrucoes.clipboard_append(entrada_caracteres.get())
        messagebox.showinfo("Copiado", "Símbolos copiados para a área de transferência!")
    
    botao_copiar = tk.Button(frame_copiar, text="Copiar", command=copiar_simbolos)
    botao_copiar.pack(side=tk.LEFT, padx=5)

def gerar_tabela_verdade():
    expressao = entrada_expressao.get()
    expressao_formatada = formatar_expressao(expressao)
    variaveis = obter_variaveis(expressao)
    
    if not variaveis:
        messagebox.showwarning("Erro", "Nenhuma variável foi detectada na expressão! Certifique-se de usar letras de A-Z para representar as variáveis.")
        return
    
    tabela = gerar_tabela(variaveis)
    resultados = []
    linhas = []
    
    for linha in tabela:
        resultado = avaliar_expressao(expressao_formatada, variaveis, linha)
        if resultado is None:
            messagebox.showerror("Erro", "A expressão inserida é inválida. Verifique os operadores e o uso correto dos parênteses.")
            return
        resultados.append(resultado)
        linhas.append(list(map(int, linha)) + [int(resultado)])
    
    tipo_tabela = classificar_tabela(resultados)
    
    tabela_str = tabulate(linhas, headers=variaveis + ["Resultado"], tablefmt="grid")
    tabela_str += f"\n\nClassificação da Tabela: {tipo_tabela}\n"
    
    saida_texto.config(state=tk.NORMAL)
    saida_texto.delete(1.0, tk.END)
    saida_texto.insert(tk.END, tabela_str)
    saida_texto.config(state=tk.DISABLED)

janela = tk.Tk()
janela.title("Gerador de Tabela Verdade")

tk.Label(janela, text="Digite a expressão lógica:").pack(pady=5)
entrada_expressao = tk.Entry(janela, width=40)
entrada_expressao.pack(pady=5)

botao_gerar = tk.Button(janela, text="Gerar Tabela", command=gerar_tabela_verdade)
botao_gerar.pack(pady=5)

botao_aleatorio = tk.Button(janela, text="Expressão Aleatória", command=gerar_expressao_aleatoria)
botao_aleatorio.pack(pady=5)

botao_instrucoes = tk.Button(janela, text="Como Usar", command=mostrar_instrucoes)
botao_instrucoes.pack(pady=5)

saida_texto = scrolledtext.ScrolledText(janela, width=60, height=15, state=tk.DISABLED)
saida_texto.pack(pady=5)

janela.mainloop()
