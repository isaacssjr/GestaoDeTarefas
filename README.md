# 📋 Gerenciador de Tarefas TI

Sistema completo para gerenciamento de múltiplas demandas de TI com controle de tempo, prioridades e notificações.

## 🎯 O Que Este Sistema Resolve

Se você trabalha com TI e tem dificuldade em gerenciar múltiplas demandas simultâneas, este sistema foi feito para você! Ele ajuda a:

- **Não esquecer tarefas** que foram iniciadas mas ficaram em segundo plano
- **Controlar o tempo** investido em cada demanda
- **Visualizar prioridades** de forma clara e colorida
- **Receber alertas** quando estiver com muitas tarefas em andamento
- **Gerar histórico** completo de todas as atividades

## ✨ Funcionalidades Principais

### 1. Gestão Completa de Tarefas
- ✅ Criar novas tarefas com título, descrição e número do chamado
- ✅ Definir prioridade (Baixa, Média, Alta, Urgente)
- ✅ Iniciar, Pausar, Retomar e Concluir tarefas
- ✅ Excluir tarefas indesejadas

### 2. Visualização Inteligente
- 🟢 **Verde**: Tarefas de baixa prioridade
- 🔵 **Azul**: Tarefas de média prioridade  
- 🟠 **Laranja**: Tarefas de alta prioridade
- 🔴 **Vermelho**: Tarefas urgentes

### 3. Múltiplas Demandas em Paralelo
- Trabalhe em várias tarefas simultaneamente
- Sistema identifica automaticamente quando há mais de uma tarefa em andamento
- Alerta visual na interface sobre multitarefa

### 4. Notificações Automáticas
- ⏰ **Alerta a cada 30 minutos** quando há múltiplas tarefas em andamento
- Notificação push nativa do Windows (ou messagebox de fallback)
- Ajuda a não esquecer tarefas secundárias

### 5. Controle de Tempo Preciso
- ⏱️ Registro automático de data/hora de início e fim
- ⏸️ Função **Pause/Resume** para interrupções
- 📊 Cálculo automático do tempo total investido
- 📝 Log completo de todas as sessões de trabalho

### 6. Integração com Chamados
- 📞 Campo dedicado para número do chamado
- Reutiliza o número em novas tarefas
- Pronto para integração com APIs de sistemas de chamado

## 🚀 Como Usar no Seu Windows

### Pré-requisitos
- Windows 10 ou superior
- Python 3.8+ (opcional, se quiser rodar como script)

### Opção 1: Rodar como Script Python

```bash
# 1. Clone ou baixe este repositório
# 2. No terminal, navegue até a pasta
cd caminho/para/pasta

# 3. Instale dependências opcionais (recomendado)
pip install plyer

# 4. Execute
python gestor_tarefas_ti.py
```

### Opção 2: Compilar para Executável .exe

```bash
# 1. Instale o Python (se ainda não tiver)
# Baixe em: https://python.org

# 2. Instale as dependências
pip install plyer pyinstaller

# 3. Compile o executável
pyinstaller --onefile --windowed --name "GerenciadorTarefasTI" gestor_tarefas_ti.py

# 4. Seu executável estará na pasta 'dist'
```

## 📖 Guia Rápido de Uso

### Criando Sua Primeira Tarefa

1. **Clique em "➕ Nova Tarefa"**
2. Preencha:
   - **Título**: Nome curto da demanda
   - **Descrição**: Detalhes do que precisa ser feito
   - **Chamado**: Número/ID do chamado (opcional)
   - **Prioridade**: Selecione o nível de urgência
3. Clique em **OK**

### Trabalhando nas Tarefas

1. **Selecione uma tarefa** na lista "Tarefas Ativas"
2. Clique em **"▶️ Iniciar"** para começar a trabalhar
3. Quando precisar fazer outra coisa:
   - **"⏸️ Pausar"**: Para interromper e contar o tempo
   - **"⏯️ Retomar"**: Para continuar de onde parou
4. Ao finalizar: **"✅ Concluir"**

### Trabalhando com Múltiplas Tarefas

Você pode iniciar quantas tarefas quiser! O sistema vai:
- Mostrar um **alerta vermelho** no topo quando houver multitarefa
- Enviar **notificação a cada 30 minutos** lembrando das tarefas em andamento
- Manter o **controle de tempo individual** de cada uma

### Consultando o Histórico

- Todas as tarefas concluídas aparecem na lista **"📜 Histórico Concluído"**
- Mostra tempo total investido e data de conclusão
- Útil para reportar horas gastas por projeto/chamado

## 🔧 Personalizações

O sistema é flexível! Você pode ajustar no código:

### Mudar Intervalo do Alerta
Abra o arquivo `gestor_tarefas_ti.py` e na linha ~430 altere:
```python
intervalo_alerta = 1800  # 30 minutos (em segundos)
# Mude para 900 = 15 min, 3600 = 1 hora, etc.
```

### Mudar Cores das Prioridades
Nas linhas ~172-177:
```python
self.cores_prioridade = {
    Prioridade.BAIXA: "#90EE90",      # Verde claro
    Prioridade.MEDIA: "#87CEEB",      # Azul claro
    Prioridade.ALTA: "#FFA500",       # Laranja
    Prioridade.URGENTE: "#FF6B6B"     # Vermelho
}
```

### Tamanho da Janela
Linha ~164:
```python
self.root.geometry("1200x700")  # Largura x Altura
```

## 💾 Onde os Dados São Salvos

- Arquivo: `tarefas.json` (na mesma pasta do executável)
- Formato: JSON (legível e fácil de fazer backup)
- **Dica**: Faça backup deste arquivo regularmente!

## 🛠️ Solução de Problemas

### "Não aparece notificação push"
- Instale o plyer: `pip install plyer`
- Ou use o fallback (messagebox) que funciona sem instalação extra

### "Quero mudar o intervalo de 30 minutos"
- Edite o arquivo `.py` antes de compilar
- Procure por `intervalo_alerta` e mude o valor

### "Como faço backup das minhas tarefas?"
- Basta copiar o arquivo `tarefas.json` para outro local

### "Posso usar em mais de um computador?"
- Sim! Leve o `.exe` + `tarefas.json` juntos
- Ou use um serviço de nuvem (OneDrive, Google Drive) para sincronizar o JSON

## 📊 Comparação: Python vs Outras Tecnologias

| Tecnologia | Vantagens | Desvantagens |
|------------|-----------|--------------|
| **Python + Tkinter** | ✅ Já vem instalado<br>✅ Fácil de modificar<br>✅ Leve | ❌ Precisa do Python para editar |
| **Batch/PowerShell** | ✅ Nativo do Windows | ❌ Sem GUI profissional<br>❌ Difícil gerenciar estado |
| **C#/WPF** | ✅ Nativo Windows<br>✅ Performance | ❌ Precisa compilar<br>❌ Mais complexo |
| **Electron** | ✅ Web technologies | ❌ Consome muita RAM<br>❌ Executável grande |

**Veredito**: Python é perfeito para este caso! 🎯

## 🔄 Próximas Melhorias (Sugestões)

- [ ] Exportar relatório em PDF/Excel
- [ ] Integração com API de chamados (ServiceNow, Jira, etc.)
- [ ] Tags/categorias para tarefas
- [ ] Lembretes de prazo
- [ ] Modo escuro
- [ ] Sincronização em nuvem

---

**Desenvolvido com ❤️ para profissionais de TI que precisam de organização**

*Versão: 1.0 | License: MIT*
