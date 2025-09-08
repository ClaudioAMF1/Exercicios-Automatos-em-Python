# Primeiro, certifique-se de ter as bibliotecas instaladas:
# pip install automata-lib graphviz

from automata.fa.dfa import DFA
from graphviz import Digraph
import os

# Função para gerar o diagrama Graphviz de um DFA
def generate_dfa_image(dfa, filename, title="DFA"):
    dot = Digraph(comment=title, format='png', engine='dot')
    dot.attr(rankdir='LR') # Left to Right

    # Adicionar um estado inicial 'invisible'
    dot.attr('node', shape='none')
    dot.node('start', label='')
    dot.attr('node', shape='circle')

    # Adicionar estados
    for state in dfa.states:
        if state in dfa.final_states:
            dot.node(str(state), str(state), shape='doublecircle')
        else:
            dot.node(str(state), str(state))

    # Conectar o início ao estado inicial
    dot.edge('start', str(dfa.initial_state))

    # Adicionar transições
    for from_state, transitions in dfa.transitions.items():
        for symbol, to_state in transitions.items():
            dot.edge(str(from_state), str(to_state), label=symbol)

    # Renderizar e salvar a imagem
    output_path = os.path.join(os.getcwd(), "output_dfa_images")
    os.makedirs(output_path, exist_ok=True)
    full_path = os.path.join(output_path, filename)
    dot.render(full_path, view=False, cleanup=True) # view=False para não abrir automaticamente
    print(f"Imagem '{filename}.png' gerada em '{output_path}'")


# Função para exibir a tabela de transição formatada
def display_transition_table(dfa, title):
    print(f"\n--- Tabela de Transição para {title} ---")
    states_list = sorted(list(dfa.states), key=str)
    input_symbols_list = sorted(list(dfa.input_symbols))

    # Cabeçalho
    header = ["Estado"] + input_symbols_list
    print(f"{header[0]:<10}" + "".join(f"{s:^8}" for s in header[1:]))
    print("-" * (10 + len(input_symbols_list) * 8))

    # Linhas de dados
    for state in states_list:
        row = f"{str(state):<10}" # Convertido para str para consistência
        for symbol in input_symbols_list:
            next_state = dfa.transitions.get(state, {}).get(symbol, "-")
            if next_state == "-":
                 row += f"{'-':^8}"
            else:
                 row += f"{str(next_state):^8}" # Convertido para str para consistência
        print(row)
    print("-" * (10 + len(input_symbols_list) * 8))
    
    # LINHA CORRIGIDA AQUI!
    final_states_str = ", ".join(sorted([str(s) for s in dfa.final_states]))
    
    print(f"Estado Inicial: {dfa.initial_state}")
    print(f"Estados Finais: {{{final_states_str}}}")

# Função para testar o autômato interativamente
def test_dfa_interactively(dfa, title):
    print(f"\n--- Teste Interativo para {title} ---")
    while True:
        user_input = input("Digite uma sequência de símbolos (ou 'sair' para terminar): ").strip()
        if user_input.lower() == 'sair':
            break
        if dfa.accepts_input(user_input):
            print(f"'{user_input}' -> ACEITA")
        else:
            print(f"'{user_input}' -> REJEITA")
    print("Teste encerrado.")

# --- Definição do Autômato 1 (Original) ---
dfa1_original = DFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': 'q1', 'b': 'q2'}, 'q1': {'a': 'q3', 'b': 'q4'},
        'q2': {'a': 'q5', 'b': 'q6'}, 'q3': {'a': 'q3', 'b': 'q3'},
        'q4': {'a': 'q4', 'b': 'q4'}, 'q5': {'a': 'q5', 'b': 'q5'},
        'q6': {'a': 'q6', 'b': 'q6'}
    },
    initial_state='q0',
    final_states={'q0', 'q1', 'q3', 'q6'} # Corrigido: q0 é final
)
dfa1_minimizado = dfa1_original.minify()

print("\n" + "="*50)
print("             MINIMIZAÇÃO DE AUTÔMATOS             ")
print("="*50)

print("\n--- Autômato 1 Original ---")
display_transition_table(dfa1_original, "Autômato 1 Original")
generate_dfa_image(dfa1_original, "dfa1_original", "Autômato 1 Original")

print("\n--- Autômato 1 Minimizado ---")
display_transition_table(dfa1_minimizado, "Autômato 1 Minimizado")
generate_dfa_image(dfa1_minimizado, "dfa1_minimizado", "Autômato 1 Minimizado")
test_dfa_interactively(dfa1_minimizado, "Autômato 1 Minimizado")


# --- Definição do Autômato 2 (Original com Sink State para completar) ---
dfa2_original_completo = DFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q_sink'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': 'q1', 'b': 'q_sink'},
        'q1': {'a': 'q_sink', 'b': 'q2'},
        'q2': {'a': 'q5', 'b': 'q_sink'},
        'q3': {'a': 'q3', 'b': 'q3'},
        'q4': {'a': 'q3', 'b': 'q6'},
        'q5': {'a': 'q5', 'b': 'q4'},
        'q6': {'a': 'q6', 'b': 'q_sink'},
        'q_sink': {'a': 'q_sink', 'b': 'q_sink'}
    },
    initial_state='q0',
    final_states={'q1', 'q4'}
)
dfa2_minimizado = dfa2_original_completo.minify()

print("\n\n" + "="*50)
print("--- Autômato 2 Original (Completo) ---")
display_transition_table(dfa2_original_completo, "Autômato 2 Original")
generate_dfa_image(dfa2_original_completo, "dfa2_original", "Autômato 2 Original")

print("\n--- Autômato 2 Minimizado ---")
display_transition_table(dfa2_minimizado, "Autômato 2 Minimizado")
generate_dfa_image(dfa2_minimizado, "dfa2_minimizado", "Autômato 2 Minimizado")
test_dfa_interactively(dfa2_minimizado, "Autômato 2 Minimizado")

print("\n" + "="*50)
print("Fim da Análise.")
print("As imagens foram salvas na pasta 'output_dfa_images'.")
print("="*50)