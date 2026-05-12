# Roteiro Definitivo: O Criptossistema RSA (Tudo Detalhado)

Este documento foi reescrito para explicar **TUDO**. Ele é dividido em duas partes. A **Parte 1** explica detalhadamente a engenharia por trás (os algoritmos matemáticos difíceis). A **Parte 2** mostra como o fluxo principal usa essas ferramentas.

---

# PARTE 1: Os Motores Matemáticos (O que rola em segundo plano)
Antes de gerar chaves ou criptografar, nosso sistema depende de 5 algoritmos matemáticos complexos. Se perguntarem "como a mágica acontece", a resposta está aqui.

### 1. Exponenciação Modular Rápida (Square-and-Multiply)
**O Problema:** No RSA, precisamos calcular coisas como $65^{65537} \pmod{3233}$. Um computador normal trava ou estoura a memória tentando calcular o resultado de $65^{65537}$ (daria um número com milhares de dígitos) para só depois dividir.
**A Solução:** Esse algoritmo calcula a potência de forma fragmentada e inteligente.
**Como funciona:**
- Em vez de multiplicar mil vezes, ele olha para o expoente em formato binário (zeros e uns).
- A cada passo, ele "desloca" os bits do expoente para a direita (`exp >> 1`), cortando o trabalho pela metade.
- A cada passo, ele eleva a base ao quadrado. Se o bit atual do expoente for 1 (ímpar), ele multiplica o resultado pela base.
- **O grande truque:** Logo após QUALQUER multiplicação, ele aplica o `% mod`. Isso garante que o número na memória nunca passe do tamanho do `mod`, não importa o tamanho do expoente. Fica super rápido e leve.

```python
def exponenciacao_modular(base, exp, mod):
    resultado = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            resultado = (resultado * base) % mod
        exp = exp >> 1 # Divisão inteira por 2 (deslocamento de bits)
        base = (base * base) % mod
    return resultado
```

### 2. Teste de Primalidade de Miller-Rabin
**O Problema:** Precisamos de números primos enormes. Testar se um número gigante é primo dividindo-o por todos os números até chegar nele levaria mais tempo que a idade do universo.
**A Solução:** Miller-Rabin é um teste *probabilístico*.
**Como funciona:**
- Ele pega o número `n` que queremos testar e subtrai 1 (`n-1`). Como `n-1` é par, ele divide por 2 várias vezes até sobrar um número ímpar `d`. (Isso se chama fatorar a potência de 2).
- Depois, ele faz `k` "rodadas" de testes matemáticos (no código, `k=5`). Em cada rodada, ele escolhe uma base aleatória `a` e faz uma conta usando a nossa `exponenciacao_modular`.
- Se o número falhar na conta da rodada, temos **certeza de 100%** de que ele é falso/composto (retorna `False`).
- Se ele passar na rodada, testamos de novo. Se passar nas 5 rodadas, a probabilidade de ele ser um "falso primo" é tão absurdamente baixa que o consideramos primo com segurança.

```python
def miller_rabin(n, k=5):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False

    # Fatora n - 1 = 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = exponenciacao_modular(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = exponenciacao_modular(x, 2, n)
            if x == n - 1: break
        else: return False
    return True
```

### 3. Algoritmo de Euclides Clássico (Cálculo de MDC)
**O Problema:** Precisamos garantir que nossa Chave Pública (`e`) não tenha nenhum divisor em comum com o número secreto `phi`. Ou seja, o Maior Divisor Comum (MDC) tem que ser 1.
**A Solução:** O algoritmo de Euclides.
**Como funciona:** É elegantemente simples. Ele assume que o MDC de `A` e `B` é o mesmo que o MDC de `B` e do **resto da divisão** de `A` por `B`. Ele fica num loop trocando as variáveis (`a = b`, `b = resto`) até que o resto seja zero. Quando dá zero, a variável `a` guarda o MDC perfeito.

```python
def mdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a
```

### 4. Algoritmo Estendido de Euclides
**O Problema:** O MDC resolve parte do problema, mas precisamos achar coeficientes matemáticos complexos para gerar nossa Chave Privada. Precisamos resolver uma equação (Identidade de Bézout) que diz: $A*x + B*y = MDC(A,B)$.
**A Solução:** Uma versão "turbinada" do algoritmo de Euclides.
**Como funciona:** Ele funciona de forma recursiva. Ele mergulha fundo, dividindo até chegar em 0 (igual ao Euclides normal). Mas ao subir de volta, ele vem calculando os "restos" ao contrário, preenchendo o valor de duas novas variáveis, `x` e `y`. O `x` final será essencial no próximo passo.

```python
def algoritmo_estendido_euclides(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = algoritmo_estendido_euclides(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y
```

### 5. Inverso Modular (Como o 'd' nasce)
**O Problema:** A nossa chave privada `d` é definida como o **Inverso Modular** de `e`. Matematicamente, isso significa que $e * d \equiv 1 \pmod{phi}$. Precisamos achar esse número mágico que "anula" a chave pública.
**A Solução e Como funciona:** 
- A gente chama o Algoritmo Estendido de Euclides passando `e` e `phi`.
- Lembra daquela equação lá de cima ($A*x + B*y = MDC$)? No nosso caso, o MDC é 1. Então temos $e*x + phi*y = 1$.
- Se calcularmos essa equação em "módulo phi" (removendo os múltiplos de phi), o lado `phi*y` vira 0.
- O que sobra? Sobra que **$e * x = 1$**. 
- Bingo! Aquele coeficiente `x` que o Euclides Estendido cuspiu no final é exatamente a nossa chave privada mágica `d`. Nós apenas usamos `% phi` nele caso ele venha negativo, para deixá-lo positivo.

```python
def inverso_modular(e, phi):
    gcd, x, y = algoritmo_estendido_euclides(e, phi)
    if gcd != 1:
        raise Exception('Inverso modular não existe.')
    return x % phi # O 'x' vira o nosso 'd'
```

---

# PARTE 2: O Fluxo na Prática (Juntando as peças)

Agora que você já tem domínio total das "ferramentas", veja como é simples a casa que construímos com elas:

## Etapa A: `gerar_chaves.py`
1. **P e Q:** Geramos ou recebemos números. Usamos o **Miller-Rabin** nele. Se for True, temos nossos primos.
2. **N e Phi:** Calculamos o módulo público $n = p \times q$. Calculamos o segredo de estado $phi = (p - 1) \times (q - 1)$.
3. **Chave Pública (e):** Escolhemos $e=17$. Chamamos a função **MDC Clássico** para conferir se o `MDC(17, phi) == 1`. Se não for, tentamos $19, 21, 23...$ até achar um.
4. **Chave Privada (d):** Chamamos a função **Inverso Modular** passando `e` e `phi`. Por baixo dos panos, ela usa o **Euclides Estendido** para nos devolver o `d` mágico.
5. **Resultado:** Temos as chaves $(n, e)$ e $(n, d)$.

## Etapa B: `criptografar.py`
1. Lemos a mensagem de texto (ex: "A").
2. Convertemos as letras para números de tabela (ASCII/UTF). Ex: "A" vira 65.
3. Usamos a Chave Pública e a **Exponenciação Modular Rápida** para calcular: $Cifra = 65^e \pmod{n}$.
4. Salvamos esses "números ininteligíveis" no `mensagem.rsa`.

## Etapa C: `decifrar.py`
1. Lemos os números ininteligíveis do `mensagem.rsa`.
2. Usamos a Chave Privada e a **Exponenciação Modular Rápida** novamente para calcular a volta: $TextoClaro = Cifra^d \pmod{n}$. (O poder do `d` aqui desfaz exatamente a confusão gerada pelo `e`).
3. Pegamos o número que sai dessa conta (ex: 65) e re-convertemos para Letra, recuperando a mensagem original "A".
