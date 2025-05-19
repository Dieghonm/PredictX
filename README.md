# Projeto Final

1. Subir no GITHUB todos os jupyter notebooks/códigos que você desenvolveu nesse ultimo módulo
1. Gerar um arquivo python (.py) com todas as funções necessárias para rodar no streamlit a escoragem do arquivo de treino
    - Criar um .py
    - Criar um carregador de csv no streamlit 
    - Subir um csv no streamlit 
    - Criar um pipeline de pré processamento dos dados
    - Utilizar o modelo treinado para escorar a base 
        - nome_arquivo = 'model_final.pkl'
1. Gravar um vídeo da tela do streamlit em funcionamento (usando o próprio streamlit (temos aula disso) ou qlqr outra forma de gravação).
1. Subir no Github o vídeo de funcionamento da ferramenta como README.md.
1. Subir no Github os códigos desenvolvidos. 
1. Enviar links do github para o tutor corrigir.



readme parcial 2

Aqui está um modelo de README parcial para o seu projeto de análise de dados, seguindo boas práticas e incluindo as funcionalidades que você desenvolveu:

```markdown
# 📊 Análise de Dados Automatizada

## Visão Geral
Este projeto fornece uma interface intuitiva para análise exploratória de dados, tratamento de dados faltantes, detecção de outliers e preparação de datasets para modelagem.

## 🔧 Funcionalidades Principais

### 1. Pré-processamento de Dados
- **Verificação de Dados Duplicados**
  - Identificação automática de linhas duplicadas
  - Visualização de estatísticas de duplicação
  - Opções flexíveis para tratamento (manter primeira/última ocorrência ou remover todas)

- **Tratamento de Valores Faltantes**
  - Análise percentual de missing values por coluna
  - Métodos de preenchimento:
    - Zero, Média, Mediana, Moda
    - Valor personalizado
  - Opção de remoção de linhas com missing values

### 2. Análise de Outliers
- Detecção automática usando método IQR
- Visualização gráfica dos outliers
- Sugestão automática de limiares para corte
- Opção de remoção controlada de outliers

### 3. Configuração do Modelo
- **Seleção da Variável Alvo**
  - Análise de valores únicos
  - Alertas para colunas com alta cardinalidade

- **Divisão dos Dados**
  - Métodos disponíveis:
    - Por porcentagem (train/val/test)
    - Por coluna específica (categórica ou temporal)
  - Controle fino dos conjuntos de dados
  - Divisão temporal com seleção por intervalos de datas

## 🛠️ Como Usar

### Pré-requisitos
- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Matplotlib/Seaborn

### Instalação
```bash
git clone [seu-repositorio]
cd [diretorio-do-projeto]
pip install -r requirements.txt
```

### Execução
```bash
streamlit run app.py
```

## Estrutura do Projeto
```
/src
│
├── /functions
│   ├── data_handling.py       # Funções básicas de manipulação de dados
│   ├── missing_values.py      # Tratamento de valores faltantes  
│   ├── outliers_handling.py   # Detecção e tratamento de outliers
│   ├── duplicates_handling.py # Controle de dados duplicados
│   ├── target_selection.py    # Seleção da variável alvo
│   └── data_splitting.py      # Divisão dos conjuntos de dados
│
├── /paginas
│   ├── data_page.py           # Página de carregamento de dados
│   └── configuracoes_page.py  # Página de configurações (este módulo)
│
└── app.py                     # Aplicação principal
```

## Próximos Passos (Roadmap)
- [ ] Integração com mais tipos de modelos
- [ ] Exportação de relatórios automáticos
- [ ] Análise automática de feature importance
- [ ] Suporte a dados geoespaciais
```

### Dicas para completar o README:

1. Adicione uma seção de **"Exemplo de Uso"** com screenshots das interfaces
2. Inclua um **diagrama de fluxo** das funcionalidades
3. Adicione badges do CI/CD se estiver usando
4. Inclua uma seção de **FAQ** com problemas comuns
5. Adicione um **guia de contribuição** se for projeto aberto

Você quer que eu desenvolva alguma seção específica com mais detalhes? Ou ajustar algo neste modelo?




Rodar localmente - streamlit run src/app.py