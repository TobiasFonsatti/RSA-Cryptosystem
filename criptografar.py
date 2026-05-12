import os

# Algoritmo de Exponenciação Modular Rápida (Square-and-Multiply)
# Implementado do zero para evitar dependências e gerenciar Big Integers
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
    texto = input("Digite a mensagem: ")
    if not texto:
        print("Erro: Mensagem vazia.")
        return
        
    chaves_str = input("Digite a chave pública (n e): ")
    try:
        # Extrai n e e separados por um espaço
        partes = chaves_str.split()
        if len(partes) != 2:
            raise ValueError
        n = int(partes[0])
        e = int(partes[1])
    except ValueError:
        print("Erro: Formato inválido. Digite os dois números separados por espaço.")
        return

    print("\nCifrando...")
    cifra = []
    
    # Processo de codificação UTF-8 para inteiro e criptografia
    for caractere in texto:
        m = ord(caractere) # Tabela de caracteres para int
        if m >= n:
            print(f"Erro: Caractere {caractere} (ASCII {m}) >= n ({n}). Use primos maiores.")
            return
            
        # Criptografa usando nossa própria implementação matemática: c = m^e mod n
        c = exponenciacao_modular(m, e, n)
        cifra.append(c)
        
    print(f"Mensagem cifrada: {cifra}")
    
    # Salvar em arquivo .rsa para o Módulo B ler
    # Garante que o arquivo seja salvo na mesma pasta do script (trabalho_rsa)
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    nome_arquivo = "mensagem.rsa"
    caminho_completo = os.path.join(pasta_script, nome_arquivo)
    
    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.write(" ".join(str(x) for x in cifra))
        print(f"Salvo em: {caminho_completo}")
    except Exception as erro:
        print(f"Erro ao salvar arquivo: {erro}")

if __name__ == "__main__":
    principal()
