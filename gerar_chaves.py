import random

# Algoritmo de Exponenciação Modular Rápida (Square-and-Multiply)
def exponenciacao_modular(base, exp, mod):
    resultado = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            resultado = (resultado * base) % mod
        exp = exp >> 1 # Divisão inteira por 2 (deslocamento de bits)
        base = (base * base) % mod
    return resultado

# Teste de Primalidade de Miller-Rabin
def miller_rabin(n, k=5):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False

    # Encontra r e d tal que n - 1 = 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Roda o teste k vezes para maior precisão matemática
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = exponenciacao_modular(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = exponenciacao_modular(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Abstração do teste de primalidade
def e_primo(num):
    return miller_rabin(num)

# Gera primo aleatório de até 4 dígitos usando Miller-Rabin
def gerar_primo_aleatorio():
    while True:
        num = random.randint(100, 9999)
        if e_primo(num):
            return num

# Calcula o Máximo Divisor Comum (Algoritmo de Euclides Clássico)
def mdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Algoritmo de Euclides Estendido
# Retorna mdc(a,b) e os coeficientes x, y tais que a*x + b*y = mdc(a,b)
def algoritmo_estendido_euclides(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = algoritmo_estendido_euclides(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Calcula o Inverso Modular (Chave Privada 'd')
def inverso_modular(e, phi):
    gcd, x, y = algoritmo_estendido_euclides(e, phi)
    if gcd != 1:
        raise Exception('Inverso modular não existe.')
    # Garantir que o d seja positivo
    return x % phi

def principal():
    print("=== GERADOR DE CHAVES RSA ===")
    print("1 - Digitar meus próprios primos")
    print("2 - Gerar primos aleatórios")
    opcao = input("Escolha: ")

    if opcao == '1':
        try:
            p = int(input("\nDigite p: "))
            q = int(input("Digite q: "))
            
            sao_primos = e_primo(p) and e_primo(q)
            print(f"\np={p} e q={q} são primos? {'Sim' if sao_primos else 'Não'}")
            
            if not sao_primos:
                print("Erro: p e q devem ser primos.")
                return
            if p == q:
                print("Erro: p e q não podem ser iguais.")
                return
        except ValueError:
            print("Erro: Digite apenas inteiros.")
            return
            
    elif opcao == '2':
        p = gerar_primo_aleatorio()
        q = gerar_primo_aleatorio()
        while p == q:
            q = gerar_primo_aleatorio()
        print(f"\np={p} e q={q} são primos? Sim")
    else:
        print("Opção inválida.")
        return

    # Cálculos Matemáticos RSA
    n = p * q
    phi = (p - 1) * (q - 1)

    # Definir o expoente público 'e'
    e = 17
    if mdc(e, phi) != 1:
        e = 3
        while mdc(e, phi) != 1:
            e += 2

    # Definir o expoente privado 'd'
    d = inverso_modular(e, phi)

    print(f"n = {n}")
    print(f"phi(n) = {phi}")
    print(f"e = {e} (mdc({e},{phi})=1)")
    print(f"d = {d}")

    print(f"\nCHAVE PÚBLICA: ({n}, {e})")
    print(f"CHAVE PRIVADA: ({n}, {d})")

if __name__ == "__main__":
    principal()
