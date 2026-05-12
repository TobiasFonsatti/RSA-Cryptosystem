# Sistema de Criptografia Educacional RSA

Projeto acadêmico para demonstrar o funcionamento básico da criptografia RSA usando Python via terminal (CLI). Todos os cálculos matemáticos foram implementados do zero.

## Estrutura do Projeto
- `gerar_chaves.py`: Gera as chaves públicas e privadas.
- `criptografar.py` (Módulo A): Criptografa o texto e salva em um arquivo.
- `decifrar.py` (Módulo B): Lê o arquivo cifrado e recupera a mensagem original.

## Integrantes do Grupo
- Artur Feiteiro Ruiz (RA: 2840482421032)
- Tobias Fonsatti Gomide (RA: 2840482421046)
- Marcus Vinicius Milano Silva (RA: 2840482421001)

- **Divisão de Tarefas:** 
   - **Artur**: Interface de linha de comando, leitura e gravação dos arquivos.
   - **Tobias**: Algoritmos matemáticos básicos (Exponenciação e Inverso Modular).
   - **Marcus**: Teste de primalidade e regras de conversão de texto.

## Algoritmos Utilizados
- **Teste de Primalidade (Miller-Rabin):** Para gerar números primos aleatórios de forma eficiente.
- **Algoritmo de Euclides Estendido:** Para calcular a chave privada (inverso modular).
- **Exponenciação Modular Rápida:** Para realizar cálculos de potência sem travar a memória.

## Como Usar (Passo a Passo)

### Passo 1: Gerar as Chaves
```bash
python gerar_chaves.py
```
Siga as instruções na tela para criar sua Chave Pública e Privada. Anote os valores gerados.

### Passo 2: Criptografar a Mensagem
```bash
python criptografar.py
```
O sistema pedirá a mensagem e a sua Chave Pública. A mensagem embaralhada será salva num arquivo chamado `mensagem.rsa`.

### Passo 3: Decifrar a Mensagem
```bash
python decifrar.py
```
Digite o nome do arquivo (`mensagem.rsa`) e a sua Chave Privada. O programa fará a leitura e exibirá sua mensagem original na tela.