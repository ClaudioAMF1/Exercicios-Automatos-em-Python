from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
import sys

def exibir_tabela_transicao(automato, tipo_automato, nome):
    """Exibe a tabela de transições de um autômato"""
    print(f"\n{'='*60}")
    print(f"TABELA DE TRANSIÇÃO - {tipo_automato}: {nome}")
    print('='*60)
    
    # Cabeçalho
    simbolos = sorted(list(automato.input_symbols))
    # Verificar se há transições vazias (epsilon)
    tem_epsilon = any("" in automato.transitions.get(estado, {}) for estado in automato.states)
    if tem_epsilon:
        simbolos.append("ε")
    
    header = "Estado".ljust(15)
    for simbolo in simbolos:
        header += simbolo.ljust(15)
    print(header)
    print("-" * len(header))
    
    # Linhas da tabela
    estados_ordenados = sorted(list(automato.states))
    for estado in estados_ordenados:
        linha = estado.ljust(15)
        
        for simbolo in simbolos:
            if simbolo == "ε":
                simbolo_busca = ""
            else:
                simbolo_busca = simbolo
                
            if estado in automato.transitions and simbolo_busca in automato.transitions[estado]:
                destinos = automato.transitions[estado][simbolo_busca]
                if isinstance(destinos, set):
                    destinos_str = "{" + ",".join(sorted(destinos)) + "}"
                else:
                    destinos_str = str(destinos)
                linha += destinos_str.ljust(15)
            else:
                linha += "-".ljust(15)
        
        # Marcar estados inicial e finais
        marcador = ""
        if estado == automato.initial_state:
            marcador += "→"
        if estado in automato.final_states:
            marcador += "*"
        linha += marcador
        
        print(linha)
    
    print("\n→ Estado inicial, * Estado final")

def contar_ocorrencias_ab(string):
    """Conta ocorrências não-sobrepostas de 'ab' em uma string"""
    count = 0
    i = 0
    while i < len(string) - 1:
        if string[i:i+2] == "ab":
            count += 1
            i += 2  # Pula os dois caracteres para evitar sobreposição
        else:
            i += 1
    return count

def testar_strings_predefinidas(automato, nome, strings_teste):
    """Testa strings predefinidas no autômato"""
    print(f"\n{'='*60}")
    print(f"TESTES PREDEFINIDOS - {nome}")
    print('='*60)
    
    aceitas = []
    rejeitadas = []
    erros = []
    
    for string in strings_teste:
        try:
            resultado = automato.accepts_input(string)
            
            # Verificação especial para AFN de "ab"
            if "3 ocorrências de 'ab'" in nome:
                ab_count = contar_ocorrencias_ab(string)
                deveria_aceitar = ab_count >= 3
                info = f" ({ab_count} 'ab')"
                
                if resultado and deveria_aceitar:
                    aceitas.append(string + info)
                elif not resultado and not deveria_aceitar:
                    rejeitadas.append(string + info)
                else:
                    # Erro na implementação
                    status = "ACEITA" if resultado else "REJEITADA"
                    esperado = "deveria aceitar" if deveria_aceitar else "deveria rejeitar"
                    erros.append(f"{string}{info}: {status} mas {esperado}")
            else:
                if resultado:
                    aceitas.append(string)
                else:
                    rejeitadas.append(string)
                    
        except Exception as e:
            erros.append(f"{string}: ERRO - {e}")
    
    print("STRINGS ACEITAS:")
    if aceitas:
        for string in aceitas:
            print(f"  ✓ '{string}'")
    else:
        print("  (nenhuma)")
    
    print("\nSTRINGS REJEITADAS:")
    if rejeitadas:
        for string in rejeitadas:
            print(f"  ✗ '{string}'")
    else:
        print("  (nenhuma)")
        
    if erros:
        print("\nERROS ENCONTRADOS:")
        for erro in erros:
            print(f"  ⚠️  '{erro}'")

def testar_automato_interativo(automato, nome):
    """Permite ao usuário testar strings no autômato"""
    print(f"\n{'='*60}")
    print(f"TESTE INTERATIVO - {nome}")
    print('='*60)
    print("Digite strings para testar (ou 'sair' para continuar):")
    
    while True:
        entrada = input("\nString: ").strip()
        if entrada.lower() == 'sair':
            break
            
        try:
            resultado = automato.accepts_input(entrada)
            status = "✓ ACEITA" if resultado else "✗ REJEITADA"
            
            # Informação extra para AFN de "ab"
            if "3 ocorrências de 'ab'" in nome:
                ab_count = contar_ocorrencias_ab(entrada)
                print(f"'{entrada}': {status} ({ab_count} ocorrências de 'ab')")
            else:
                print(f"'{entrada}': {status}")
        except Exception as e:
            print(f"Erro ao processar '{entrada}': {e}")

def main():
    print("IMPLEMENTAÇÃO DE AUTÔMATOS FINITOS")
    print("="*50)
    
    # ===== AFD 1: Exatamente 4 símbolos =====
    print("\n1. AFD - Strings com exatamente 4 símbolos")
    
    afd_4_simbolos = DFA(
        states={'q0', 'q1', 'q2', 'q3', 'q4', 'qreject'},
        input_symbols={'a', 'b'},
        transitions={
            'q0': {'a': 'q1', 'b': 'q1'},
            'q1': {'a': 'q2', 'b': 'q2'},
            'q2': {'a': 'q3', 'b': 'q3'},
            'q3': {'a': 'q4', 'b': 'q4'},
            'q4': {'a': 'qreject', 'b': 'qreject'},
            'qreject': {'a': 'qreject', 'b': 'qreject'}
        },
        initial_state='q0',
        final_states={'q4'}
    )
    
    afd_4_simbolos.show_diagram(path="afd_4_simbolos.png")
    exibir_tabela_transicao(afd_4_simbolos, "AFD", "Exatamente 4 símbolos")
    
    # Testes predefinidos para AFD 4 símbolos
    strings_teste_4 = [
        "",          # 0 símbolos - deve rejeitar
        "a",         # 1 símbolo - deve rejeitar
        "ab",        # 2 símbolos - deve rejeitar
        "abc",       # símbolo inválido
        "aba",       # 3 símbolos - deve rejeitar
        "abab",      # 4 símbolos - deve aceitar
        "aabb",      # 4 símbolos - deve aceitar
        "aaaa",      # 4 símbolos - deve aceitar
        "bbbb",      # 4 símbolos - deve aceitar
        "ababa",     # 5 símbolos - deve rejeitar
        "aaaaaa",    # 6 símbolos - deve rejeitar
        "baab",      # 4 símbolos - deve aceitar
    ]
    testar_strings_predefinidas(afd_4_simbolos, "AFD - Exatamente 4 símbolos", strings_teste_4)
    testar_automato_interativo(afd_4_simbolos, "AFD - Exatamente 4 símbolos")
    
    # ===== AFD 2: Começa com "aba" =====
    print("\n2. AFD - Strings que começam com 'aba'")
    
    afd_comeca_aba = DFA(
        states={'q0', 'q1', 'q2', 'q3', 'qreject'},
        input_symbols={'a', 'b'},
        transitions={
            'q0': {'a': 'q1', 'b': 'qreject'},
            'q1': {'a': 'qreject', 'b': 'q2'},
            'q2': {'a': 'q3', 'b': 'qreject'},
            'q3': {'a': 'q3', 'b': 'q3'},
            'qreject': {'a': 'qreject', 'b': 'qreject'}
        },
        initial_state='q0',
        final_states={'q3'}
    )
    
    afd_comeca_aba.show_diagram(path="afd_comeca_aba.png")
    exibir_tabela_transicao(afd_comeca_aba, "AFD", "Começa com 'aba'")
    
    # Testes predefinidos para AFD começa com "aba"
    strings_teste_aba = [
        "",          # string vazia - deve rejeitar
        "a",         # só 'a' - deve rejeitar
        "ab",        # 'ab' sem completar - deve rejeitar
        "aba",       # exatamente "aba" - deve aceitar
        "abaa",      # "aba" + 'a' - deve aceitar
        "abab",      # "aba" + 'b' - deve aceitar
        "abaaba",    # "aba" + "aba" - deve aceitar
        "abaaaabb",  # "aba" + qualquer coisa - deve aceitar
        "baba",      # não começa com "aba" - deve rejeitar
        "aab",       # não é "aba" - deve rejeitar
        "abb",       # não é "aba" - deve rejeitar
        "ba",        # começa com 'b' - deve rejeitar
        "aa",        # não tem 'b' na posição 2 - deve rejeitar
    ]
    testar_strings_predefinidas(afd_comeca_aba, "AFD - Começa com 'aba'", strings_teste_aba)
    testar_automato_interativo(afd_comeca_aba, "AFD - Começa com 'aba'")
    
    # ===== AFN 1: Mínimo 3 ocorrências de "ab" =====
    print("\n3. AFN - Mínimo 3 ocorrências de 'ab'")
    
    afn_3_ab = NFA(
        states={"q0", "q1", "q2", "q3", "wait_b0", "wait_b1", "wait_b2"},
        input_symbols={"a", "b"},
        transitions={
            # Estado inicial: 0 ocorrências de "ab"
            "q0": {
                "a": {"wait_b0"},  # Viu 'a', esperando 'b' para primeira ocorrência
                "b": {"q0"}        # 'b' sozinho não forma padrão, permanece em q0
            },
            # Esperando 'b' após ver 'a' (0 ocorrências completas)
            "wait_b0": {
                "a": {"wait_b0"},  # Outro 'a', ainda esperando 'b'
                "b": {"q1"}        # Completou primeira ocorrência "ab"
            },
            # Estado: 1 ocorrência de "ab" completa
            "q1": {
                "a": {"wait_b1"},  # Viu 'a', esperando 'b' para segunda ocorrência
                "b": {"q1"}        # 'b' sozinho, permanece em q1
            },
            # Esperando 'b' após ver 'a' (1 ocorrência completa)
            "wait_b1": {
                "a": {"wait_b1"},  # Outro 'a', ainda esperando 'b'
                "b": {"q2"}        # Completou segunda ocorrência "ab"
            },
            # Estado: 2 ocorrências de "ab" completas
            "q2": {
                "a": {"wait_b2"},  # Viu 'a', esperando 'b' para terceira ocorrência
                "b": {"q2"}        # 'b' sozinho, permanece em q2
            },
            # Esperando 'b' após ver 'a' (2 ocorrências completas)
            "wait_b2": {
                "a": {"wait_b2"},  # Outro 'a', ainda esperando 'b'
                "b": {"q3"}        # Completou terceira ocorrência "ab" - ACEITA!
            },
            # Estado final: 3+ ocorrências de "ab"
            "q3": {
                "a": {"q3"},       # Aceita qualquer entrada adicional
                "b": {"q3"}
            }
        },
        initial_state="q0",
        final_states={"q3"}
    )
    
    afn_3_ab.show_diagram(path="afn_3_ab.png")
    exibir_tabela_transicao(afn_3_ab, "AFN", "Mínimo 3 ocorrências de 'ab'")
    
    # Testes predefinidos para AFN 3 ocorrências de "ab"
    strings_teste_3ab = [
        "",             # string vazia - deve rejeitar
        "ab",           # 1 ocorrência - deve rejeitar
        "abab",         # 2 ocorrências - deve rejeitar
        "ababab",       # 3 ocorrências - deve aceitar
        "abababab",     # 4 ocorrências - deve aceitar
        "aabababab",    # 3 ocorrências - deve aceitar
        "ababababa",    # 4 ocorrências - deve aceitar
        "bababab",      # 3 ocorrências - deve aceitar
        "aaa",          # 0 ocorrências - deve rejeitar
        "bbb",          # 0 ocorrências - deve rejeitar
        "abcabc",       # símbolos inválidos
        "baabababab",   # 4 ocorrências - deve aceitar
        "aaabbbaaab",   # 1 ocorrência - deve rejeitar
        "aababab",      # apenas 2 ocorrências - deve rejeitar
        "abababb",      # apenas 2 ocorrências - deve rejeitar
    ]
    testar_strings_predefinidas(afn_3_ab, "AFN - Mínimo 3 ocorrências de 'ab'", strings_teste_3ab)
    testar_automato_interativo(afn_3_ab, "AFN - Mínimo 3 ocorrências de 'ab'")
    
    # ===== AFN 2: Mínimo 3 a's OU 3 b's OU 3 c's =====
    print("\n4. AFN - Mínimo 3 a's OU 3 b's OU 3 c's")
    
    afn_3_abc = NFA(
        states={
            "start", "a0", "a1", "a2", "a3_plus", 
            "b0", "b1", "b2", "b3_plus",
            "c0", "c1", "c2", "c3_plus"
        },
        input_symbols={"a", "b", "c"},
        transitions={
            "start": {"": {"a0", "b0", "c0"}},
            "a0": {"a": {"a1"}, "b": {"a0"}, "c": {"a0"}},
            "a1": {"a": {"a2"}, "b": {"a1"}, "c": {"a1"}},
            "a2": {"a": {"a3_plus"}, "b": {"a2"}, "c": {"a2"}},
            "a3_plus": {"a": {"a3_plus"}, "b": {"a3_plus"}, "c": {"a3_plus"}},
            "b0": {"a": {"b0"}, "b": {"b1"}, "c": {"b0"}},
            "b1": {"a": {"b1"}, "b": {"b2"}, "c": {"b1"}},
            "b2": {"a": {"b2"}, "b": {"b3_plus"}, "c": {"b2"}},
            "b3_plus": {"a": {"b3_plus"}, "b": {"b3_plus"}, "c": {"b3_plus"}},
            "c0": {"a": {"c0"}, "b": {"c0"}, "c": {"c1"}},
            "c1": {"a": {"c1"}, "b": {"c1"}, "c": {"c2"}},
            "c2": {"a": {"c2"}, "b": {"c2"}, "c": {"c3_plus"}},
            "c3_plus": {"a": {"c3_plus"}, "b": {"c3_plus"}, "c": {"c3_plus"}}
        },
        initial_state="start",
        final_states={"a3_plus", "b3_plus", "c3_plus"}
    )
    
    afn_3_abc.show_diagram(path="afn_3_abc.png")
    exibir_tabela_transicao(afn_3_abc, "AFN", "Mínimo 3 a's OU 3 b's OU 3 c's")
    
    # Testes predefinidos para AFN 3 a's OU 3 b's OU 3 c's
    strings_teste_3abc = [
        "",              # string vazia - deve rejeitar
        "aaa",           # 3 a's - deve aceitar
        "bbb",           # 3 b's - deve aceitar
        "ccc",           # 3 c's - deve aceitar
        "ab",            # 1 a, 1 b - deve rejeitar
        "abc",           # 1 de cada - deve rejeitar
        "aabb",          # 2 a's, 2 b's - deve rejeitar
        "abcabc",        # 2 de cada - deve rejeitar
        "aaab",          # 3 a's, 1 b - deve aceitar
        "abbb",          # 1 a, 3 b's - deve aceitar
        "accc",          # 1 a, 3 c's - deve aceitar
        "aaaabbbbcccc",  # 4 de cada - deve aceitar
        "abcabcabc",     # 3 de cada - deve aceitar
        "aabcc",         # 2 a's, 1 b, 2 c's - deve rejeitar
        "aaacccbbb",     # 3 de cada - deve aceitar
        "abcdefg",       # símbolos inválidos
        "cba",           # 1 de cada invertido - deve rejeitar
        "cccaaa",        # 3 c's, 3 a's - deve aceitar
    ]
    testar_strings_predefinidas(afn_3_abc, "AFN - Mínimo 3 a's OU 3 b's OU 3 c's", strings_teste_3abc)
    testar_automato_interativo(afn_3_abc, "AFN - Mínimo 3 a's OU 3 b's OU 3 c's")
    
    # ===== AFN-ε 1: a's antes de b's (linguagem a*b*) =====
    print("\n5. AFN-ε - a's que antecedem b's (linguagem a*b*)")
    
    afn_epsilon_melhorado = NFA(
        states={"q0", "q1"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {
                "a": {"q0"},     # Lê a's (permanece em q0)
                "": {"q1"}       # Transição vazia para estado que lê b's
            },
            "q1": {
                "b": {"q1"}      # Lê b's (permanece em q1)
            }
        },
        initial_state="q0",
        final_states={"q0", "q1"}  # Ambos são finais: aceita a*, b* e a*b*
    )
    
    afn_epsilon_melhorado.show_diagram(path="afn_epsilon_ab.png")
    exibir_tabela_transicao(afn_epsilon_melhorado, "AFN-ε", "a's que antecedem b's")
    
    # Testes predefinidos para AFN-ε a's antes de b's (linguagem a*b*)
    strings_teste_ab_ordem = [
        "",          # string vazia (ε) - deve aceitar
        "a",         # a¹ - deve aceitar
        "aa",        # a² - deve aceitar
        "aaa",       # a³ - deve aceitar
        "b",         # b¹ - deve aceitar
        "bb",        # b² - deve aceitar
        "bbb",       # b³ - deve aceitar
        "ab",        # a¹b¹ - deve aceitar
        "aab",       # a²b¹ - deve aceitar
        "abb",       # a¹b² - deve aceitar
        "aabb",      # a²b² - deve aceitar
        "aaabbb",    # a³b³ - deve aceitar
        "aaaa",      # a⁴ - deve aceitar
        "bbbb",      # b⁴ - deve aceitar
        "ba",        # b¹a¹ - deve REJEITAR (b antes de a)
        "bba",       # b²a¹ - deve REJEITAR
        "aba",       # a¹b¹a¹ - deve REJEITAR (a depois de b)
        "abab",      # intercalado - deve REJEITAR
        "aabba",     # a²b²a¹ - deve REJEITAR
        "baaab",     # começa com b, depois a's - deve REJEITAR
    ]
    testar_strings_predefinidas(afn_epsilon_melhorado, "AFN-ε - a's que antecedem b's", strings_teste_ab_ordem)
    testar_automato_interativo(afn_epsilon_melhorado, "AFN-ε - a's que antecedem b's")
    
    # ===== AFN-ε 2: Strings que contêm "ab" ou "ba" =====
    print("\n6. AFN-ε - Strings que contêm 'ab' ou 'ba'")
    
    afn_epsilon_ab_ou_ba = NFA(
        states={"q0", "q1", "q2", "q3", "q4", "qf"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {
                "": {"q1", "q3"},  # Escolha não-determinística entre procurar "ab" ou "ba"
                "a": {"q0"},       # Pode ignorar símbolos até encontrar padrão
                "b": {"q0"}
            },
            # Ramo para encontrar "ab"
            "q1": {
                "a": {"q2"},       # Viu 'a', espera 'b'
                "b": {"q1"}        # Continua procurando
            },
            "q2": {
                "b": {"qf"},       # Completou "ab"
                "a": {"q2"}        # Viu outro 'a', ainda pode completar "ab"
            },
            # Ramo para encontrar "ba"  
            "q3": {
                "b": {"q4"},       # Viu 'b', espera 'a'
                "a": {"q3"}        # Continua procurando
            },
            "q4": {
                "a": {"qf"},       # Completou "ba"
                "b": {"q4"}        # Viu outro 'b', ainda pode completar "ba"
            },
            # Estado final
            "qf": {
                "a": {"qf"},       # Aceita qualquer coisa depois
                "b": {"qf"}
            }
        },
        initial_state="q0",
        final_states={"qf"}
    )
    
    afn_epsilon_ab_ou_ba.show_diagram(path="afn_epsilon_ab_ou_ba.png")
    exibir_tabela_transicao(afn_epsilon_ab_ou_ba, "AFN-ε", "Contém 'ab' ou 'ba'")
    
    # Testes predefinidos para AFN-ε contém "ab" ou "ba"
    strings_teste_ab_ou_ba = [
        "",          # string vazia - deve rejeitar
        "a",         # só 'a' - deve rejeitar
        "b",         # só 'b' - deve rejeitar
        "aa",        # só a's - deve rejeitar
        "bb",        # só b's - deve rejeitar
        "ab",        # contém "ab" - deve aceitar
        "ba",        # contém "ba" - deve aceitar
        "aab",       # contém "ab" - deve aceitar
        "aba",       # contém "ab" e "ba" - deve aceitar
        "bab",       # contém "ba" e "ab" - deve aceitar
        "abab",      # contém "ab" múltiplas vezes - deve aceitar
        "baba",      # contém "ba" múltiplas vezes - deve aceitar
        "aabb",      # contém "ab" - deve aceitar
        "bbaa",      # contém "ba" - deve aceitar
        "xaby",      # símbolos inválidos
        "cabbage",   # símbolos inválidos
        "aaabbb",    # contém "ab" - deve aceitar
        "bbbaaa",    # contém "ba" - deve aceitar
        "abcdef",    # símbolos inválidos
        "baab",      # contém "ba" e "ab" - deve aceitar
    ]
    testar_strings_predefinidas(afn_epsilon_ab_ou_ba, "AFN-ε - Contém 'ab' ou 'ba'", strings_teste_ab_ou_ba)
    testar_automato_interativo(afn_epsilon_ab_ou_ba, "AFN-ε - Contém 'ab' ou 'ba'")
    
    print("\n" + "="*60)
    print("RESUMO DOS AUTÔMATOS IMPLEMENTADOS:")
    print("="*60)
    print("AFD:")
    print("  1. Strings com exatamente 4 símbolos")
    print("  2. Strings que começam com 'aba'")
    print("\nAFN:")
    print("  3. Strings com mínimo 3 ocorrências de 'ab'")
    print("  4. Strings com mínimo 3 a's OU 3 b's OU 3 c's")
    print("\nAFN-ε:")
    print("  5. Strings onde a's antecedem b's")
    print("  6. Strings que contêm 'ab' ou 'ba'")
    print("\nDiagramas salvos como arquivos PNG.")

if __name__ == "__main__":
    main()