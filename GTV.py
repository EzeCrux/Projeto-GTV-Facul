import itertools
import re
import tkinter as tk
from tkinter import messagebox, scrolledtext
import random

def obter_variaveis(expressao):
    return sorted(set(re.findall(r'[A-Za-z]', expressao)))

def gerar_tabela(variaveis):
    return list(itertools.product([False, True], repeat=len(variaveis)))

def avaliar_expressao(expressao, variaveis, valores):
    try:
        contexto = dict(zip(variaveis, valores))
        return eval(expressao, {}, contexto)
    except Exception:
        return None

def formatar_expressao(expressao):
    substituicoes = {
        "→": "or not",
        "↔": "==",
        "⊕": "!=",
        "¬": "not ",
        "∧": " and ",
        "v": " or "
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
    operadores = ["∧", "v", "→", "↔", "⊕"]
    expressao = random.choice(variaveis)
    for _ in range(random.randint(1, 3)):
        expressao += f" {random.choice(operadores)} {random.choice(variaveis)}"
    entrada_expressao.delete(0, tk.END)
    entrada_expressao.insert(0, expressao)

def mostrar_instrucoes():
    janela_instrucoes = tk.Toplevel(janela)
    janela_instrucoes.title("Como Usar")
    janela_instrucoes.geometry("400x300")
    
    texto_instrucoes = (
        "Instruções de Uso:\n"
        "- Digite uma expressão lógica usando as variáveis A-Z.\n"
        "- Use os seguintes operadores:\n"
        "  ∧ (E), v (OU), → (IMPLICAÇÃO), ↔ (BI-IMPLICAÇÃO), ⊕ (XOR), ¬ (NÃO)\n"
        "- Pressione 'Gerar Tabela' para visualizar a tabela verdade.\n"
        "- Pressione 'Expressão Aleatória' para gerar um exemplo automático."
    )
    
    label = tk.Label(janela_instrucoes, text=texto_instrucoes, justify=tk.LEFT)
    label.pack(pady=10, padx=10)
    
    entrada_caracteres = tk.Entry(janela_instrucoes, width=30)
    entrada_caracteres.pack(pady=5)
    entrada_caracteres.insert(0, "∧ v → ↔ ⊕ ¬")
    
    botao_copiar = tk.Button(janela_instrucoes, text="Copiar", command=lambda: janela_instrucoes.clipboard_append(entrada_caracteres.get()))
    botao_copiar.pack(pady=5)

def gerar_tabela_verdade():
    expressao = entrada_expressao.get()
    expressao_formatada = formatar_expressao(expressao)
    variaveis = obter_variaveis(expressao)
    
    if not variaveis:
        messagebox.showwarning("Erro", "Nenhuma variável foi detectada na expressão! Certifique-se de usar letras de A-Z para representar as variáveis.")
        return
    
    if any(op not in "∧v→↔⊕¬() " and not op.isalpha() for op in expressao):
        messagebox.showerror("Erro", "Expressão inválida! Verifique se os operadores e parênteses estão corretos. Sugestão: Use parênteses para agrupar corretamente.")
        return
    
    tabela = gerar_tabela(variaveis)
    resultados = []
    tabela_str = "\n" + " | ".join(variaveis) + " | Resultado\n"
    tabela_str += "=" * (len(variaveis) * 6 + 12) + "\n"
    
    for linha in tabela:
        resultado = avaliar_expressao(expressao_formatada, variaveis, linha)
        if resultado is None:
            messagebox.showerror("Erro", "A expressão inserida é inválida. Verifique os operadores e o uso correto dos parênteses. Sugestão: Tente usar parênteses para evitar ambiguidade.")
            return
        resultados.append(resultado)
        linha_str = " | ".join(f" {int(v)} " for v in linha) + f" |  {int(resultado)} \n"
        tabela_str += linha_str
    
    tipo_tabela = classificar_tabela(resultados)
    tabela_str += "=" * (len(variaveis) * 6 + 12) + "\n"
    tabela_str += f"\nClassificação da Tabela: {tipo_tabela}\n"
    
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