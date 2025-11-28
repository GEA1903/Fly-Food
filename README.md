# 🚁 Food Delivery Route Optimizer

Sistema de otimização de rotas para entregas utilizando distância Manhattan, desenvolvido para encontrar o caminho mais eficiente entre um ponto de origem e múltiplos pontos de entrega.

## 📋 Descrição

Este projeto implementa um algoritmo que calcula a rota de menor distância para um sistema de entregas em uma matriz/grid. O sistema identifica:
- **R**: Ponto de origem (restaurante)
- **A, B, C, D...**: Pontos de entrega (clientes)
- **0**: Espaços vazios

O algoritmo utiliza permutações para testar todas as rotas possíveis e encontrar a sequência ótima de entregas, minimizando a distância total percorrida.

## 🚀 Funcionalidades

- ✅ Leitura de matrizes a partir de arquivo de texto
- ✅ Leitura de matrizes a partir de strings
- ✅ Cálculo de distância Manhattan entre pontos
- ✅ Algoritmo exaustivo para encontrar a rota ótima
- ✅ Suporte para múltiplos pontos de entrega
- ✅ Validação de entrada e tratamento de erros

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/food-delivery-optimizer.git

# Entre no diretório do projeto
cd food-delivery-optimizer

# Não há dependências externas necessárias - usa apenas bibliotecas padrão do Python
```

## 🔧 Uso

### Exemplo Básico

```python
from main import FoodDelivery

# Criar uma instância do otimizador
solver = FoodDelivery()

# Definir a matriz (pode incluir dimensões na primeira linha)
matriz_exemplo = """4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0"""

# Carregar e processar a matriz
solver.ler_matriz_string(matriz_exemplo)

# Calcular a melhor rota
rota, distancia = solver.melhor_rota()

# Exibir resultados
print(f"Melhor rota: {rota}")
print(f"Distância total: {distancia} dronômetros")
```

### Leitura de Arquivo

```python
solver = FoodDelivery(nome_arquivo='matriz.txt')
solver.ler_matriz()
rota, distancia = solver.melhor_rota()
```

### Formato do Arquivo `matriz.txt`

```
0000D
0A000
0000C
R0B00
```

Ou com dimensões especificadas:

```
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```

## 📊 Como Funciona

1. **Leitura da Matriz**: O sistema identifica o ponto de origem (R) e todos os pontos de entrega (letras A-Z)

2. **Cálculo de Distância**: Utiliza a distância Manhattan:
   ```
   distância = |x1 - x2| + |y1 - y2|
   ```

3. **Otimização**: Testa todas as permutações possíveis de rotas para encontrar a sequência com menor distância total

4. **Resultado**: Retorna a sequência ótima de entregas e a distância mínima

## 🎯 Exemplo de Saída

```
Melhor rota encontrada: A B C D
Menor distância total: 14 dronômetros
```

## ⚙️ Métodos Principais

| Método | Descrição |
|--------|-----------|
| `ler_matriz()` | Lê matriz de arquivo texto |
| `ler_matriz_string(matriz_string)` | Lê matriz de string |
| `distancia(p1, p2)` | Calcula distância Manhattan |
| `melhor_rota()` | Retorna rota ótima e distância |

## ⚠️ Complexidade

O algoritmo utiliza permutações, portanto tem complexidade **O(n!)**, onde n é o número de pontos de entrega. É ideal para:
- ✅ Até 10 pontos de entrega (< 1 segundo)
- ⚠️ 11-12 pontos (alguns segundos)
- ❌ 13+ pontos (pode ser lento)

Para grandes quantidades de pontos, considere implementar algoritmos heurísticos como:
- Algoritmo guloso (vizinho mais próximo)
- Algoritmo genético
- Simulated annealing

## 🧪 Validações

O sistema valida:
- ✅ Existência de ponto de origem (R)
- ✅ Dimensões consistentes da matriz
- ✅ Pontos duplicados
- ✅ Múltiplos pontos de origem

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

