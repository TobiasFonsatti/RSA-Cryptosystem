import os

# Algoritmo de Exponenciação Modular Rápida (Square-and-Multiply)
# Implementado do zero para realizar c^d mod n rapidamente
def exponenciacao_modular(base, exp, mod):
    resultado = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            resultado = (resultado * base) % mod
        exp = exp >> 1 # Equivalente a exp // 2
        base = (base * base) % mod
    return resultado

def principal():
    nome_arquivo = input("Digite o arquivo cifrado: ")
    
    # Tenta buscar o arquivo primeiramente dentro da mesma pasta do script (trabalho_rsa)
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(pasta_script, nome_arquivo)
    
    if not os.path.exists(caminho_completo):
        # Se não encontrar na pasta do script, tenta usar o caminho que o usuário passou puro
        if os.path.exists(nome_arquivo):
            caminho_completo = nome_arquivo
        else:
            print("Erro: Arquivo não encontrado.")
            return
        
    chaves_str = input("Digite a chave privada (n d): ")
    try:
        # Extrai n e d separados por um espaço
        partes = chaves_str.split()
        if len(partes) != 2:
            raise ValueError
        n = int(partes[0])
        d = int(partes[1])
    except ValueError:
        print("Erro: Formato inválido. Digite os dois números separados por espaço.")
        return

    print("\nDecifrando...")
    
    # Leitura do texto cifrado no arquivo
    try:
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip()
    except Exception as erro:
        print(f"Erro ao ler arquivo: {erro}")
        return

    if not conteudo:
        print("Erro: Arquivo vazio.")
        return

    lista_cifrada = conteudo.split()
    texto_claro = ""

    # Processo de decifragem e decodificação do número para string (UTF-8)
    for c_str in lista_cifrada:
        try:
            c = int(c_str)
            
            # Decifra usando a implementação matemática do zero: m = c^d mod n
            m = exponenciacao_modular(c, d, n)
            
            # Converte o número de volta ao caractere utilizando a tabela ASCII/UTF-8
            texto_claro += chr(m)
        except ValueError:
            print("Erro: Arquivo contém valores inválidos.")
            return
            
    print(f"Mensagem original: {texto_claro}")

if __name__ == "__main__":
    principal()
