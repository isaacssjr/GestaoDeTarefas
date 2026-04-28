# Gestão de Atividades - Sistema de Gerenciamento de Tarefas para TI

Sistema desenvolvido em Python com PyQt6 para gerenciamento de tarefas do dia a dia da TI, com suporte a múltiplas tarefas em paralelo, alertas, logs detalhados e integração com system tray.

## ✅ Funcionalidades Implementadas

- **Adicionar, gerenciar e concluir tarefas** - Interface intuitiva para criação e gestão
- **Visualização com cores por prioridade**:
  - 🟢 Baixa (Verde)
  - 🔵 Média (Azul) 
  - 🟠 Alta (Laranja)
- **Múltiplas tarefas em paralelo** - Execute várias demandas simultaneamente
- **Alerta pop-up de 30 em 30 minutos** quando há mais de uma tarefa ativa (contagem inicia ao iniciar nova tarefa com outra já ativa)
- **Log completo de atividades** com:
  - Data/hora de início e fim
  - Registro de pausas manuais
  - Cálculo automático do tempo total investido (horas e minutos)
- **Parser automático de chamados** - Cole a linha completa e o sistema extrai:
  - Ticket
  - E-mail do solicitante
  - Tipo/categoria da demanda
  - Descrição
- **Tema escuro** para conforto visual
- **System tray** - Minimiza para a bandeja do sistema (canto inferior direito)
- **Janela de logs com filtragem** por texto e data
- **Exportação para Excel** dos logs
- **Persistência de dados** - Recupera tarefas ao reiniciar
- **Auto-instalação** - Script cria .venv e instala dependências automaticamente

## 🛠️ Tecnologias

- **Python 3.8+**
- **PyQt6** - Interface gráfica moderna com system tray nativo
- **SQLite/JSON** - Armazenamento de dados
- **PyInstaller** - Compilação para .exe
- **openpyxl** - Exportação para Excel
- **plyer** - Notificações do sistema

## 📦 Instalação Automática (Windows)

1. **Execute o instalador:**
   ```cmd
   install.bat
   ```

2. O script irá automaticamente:
   - Criar ambiente virtual (.venv)
   - Instalar todas as dependências (PyQt6, plyer, openpyxl, pyinstaller)
   - Testar a instalação
   - Compilar o executável .exe
   - Oferecer criar atalho na Área de Trabalho
   - Oferecer configurar inicialização com o Windows

3. **Após instalação:**
   - Executável estará em: `dist\GestaoAtividades.exe`
   - Atalho opcional na Área de Trabalho
   - Startup opcional configurado no Windows

## 🐧 Instalação (Linux/Mac)

```bash
chmod +x install.sh
./install.sh
```

Para executar:
```bash
source .venv/bin/activate
python main.py
```

## 🚀 Execução Manual

```bash
# Criar e ativar ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

## 📋 Formato do Chamado

O sistema aceita o formato tabulado:
```
#TI2604276854gessika.vasconcelos@grupocertare.comAjuda e Suporte > Hardware (Dispositivos/Equipamentos)"Após limpeza realizada o illustrator e o corel pararam de funcionar."
```

**Campos na ordem:**
1. Ticket do chamado (#TI...)
2. E-mail do solicitante
3. Tipo/Categoria da demanda
4. Descrição (entre aspas)

Basta colar esta linha no campo indicado e o sistema extrairá automaticamente todas as informações.

## 🎨 Prioridades e Cores

| Prioridade | Cor | Código Hex |
|------------|-----|------------|
| Baixa | 🟢 Verde | #4caf50 |
| Média | 🔵 Azul | #2196f3 |
| Alta | 🟠 Laranja | #ff9800 |

## ⏱️ Controle de Tempo

- **Início**: Marca data/hora de início e começa contagem
- **Pause**: Manual - pausa a contagem e registra no histórico
- **Retomar**: Continua contagem de onde parou
- **Concluir**: Finaliza e calcula tempo total investido
- **Cálculo automático**: Horas, minutos e segundos formatados (HH:MM:SS)

## 🔔 Alertas de Múltiplas Demandas

Quando você tem **mais de uma tarefa "Em Andamento"**:
- Sistema notifica a cada 30 minutos
- Contagem inicia quando a segunda tarefa é iniciada
- Notificação via:
  - System tray (nativo do Windows/Linux)
  - Plyer (notificação do sistema operacional)
- Mensagem mostra qual tarefa está em andamento

## 📊 Logs e Relatórios

Acesse através do botão **"📊 Ver Logs"**:
- **Filtro por texto**: Busca em ticket, email, descrição
- **Filtro por data**: Período de/conclusão
- **Visualização**: Tabela com todas as tarefas concluídas
- **Exportar Excel**: Gera planilha completa com:
  - Todos os campos da tarefa
  - Tempo total em segundos e formatado
  - Histórico completo de eventos

## 💾 Persistência de Dados

- **Arquivo JSON**: `tasks_db.json` (na mesma pasta do executável)
- **Recuperação automática**: Ao reiniciar, todas as tarefas são carregadas
- **Segurança**: Tarefas em andamento ao fechar são automaticamente pausadas

## 🔧 Compilar para .exe

```bash
# Após instalar dependências
pyinstaller --onefile --windowed --name "GestaoAtividades" main.py

# Executável será gerado em: dist/GestaoAtividades.exe
```

## 📁 Estrutura do Projeto

```
/workspace
├── main.py              # Aplicação principal
├── requirements.txt     # Dependências Python
├── install.bat          # Instalador Windows
├── install.sh           # Instalador Linux/Mac
├── .gitignore          # Arquivos ignorados pelo Git
├── README.md           # Esta documentação
└── tasks_db.json       # Banco de dados (gerado automaticamente)
```

## 🎯 Casos de Uso

### Cenário 1: Única demanda
1. Cole a linha do chamado
2. Selecione prioridade
3. Clique em "Adicionar Tarefa"
4. Clique em "▶️ Iniciar" na tabela
5. Trabalhe na demanda
6. Clique em "✅ Concluir" quando finalizar

### Cenário 2: Múltiplas demandas em paralelo
1. Adicione e inicie a primeira tarefa
2. Adicione e inicie a segunda tarefa
3. Sistema notificará a cada 30 minutos sobre demandas paralelas
4. Use "⏸️ Pausar" para focar em uma específica
5. Retome quando necessário

### Cenário 3: Pausa para atendimento urgente
1. Tarefa A está "Em Andamento"
2. Surge urgência → Clique "⏸️ Pausar" na tarefa A
3. Adicione e inicie tarefa urgente
4. Ao finalizar, retome tarefa A com "▶️ Retomar"

## ⚙️ Configurações Avançadas

### Iniciar com Windows (manual)
O instalador oferece esta opção. Para configurar manualmente:
1. Pressione `Win + R`
2. Digite `shell:startup`
3. Crie atalho para `dist\GestaoAtividades.exe`

### Personalizar intervalo de alerta
Edite no `main.py`:
```python
self.notification_interval = 1800  # 30 minutos em segundos
```

## 📝 Notas Importantes

- **Primeira execução**: Pode levar alguns segundos para carregar
- **System tray**: No Linux, requer suporte a system tray no desktop environment
- **Notificações**: Requer permissões de notificação no sistema operacional
- **Excel**: Abre automaticamente no programa padrão após exportação

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"
- Instale Python 3.8+ marcando "Add to PATH" durante instalação

### Erro: "ModuleNotFoundError: PyQt6"
- Execute `install.bat` novamente ou `pip install -r requirements.txt`

### Sistema não minimiza para tray
- Verifique se há ícones ocultos no canto inferior direito do Windows
- Clique na setinha ^ para mostrar ícones ocultos

### Dados não persistem
- Verifique permissões de escrita na pasta do executável
- Não execute como Administrador desnecessariamente

## 📄 Licença

Uso interno - Gestão de Atividades TI

---

**Versão**: 1.0.0  
**Desenvolvido para**: Departamento de TI  
**Tecnologia**: Python + PyQt6
