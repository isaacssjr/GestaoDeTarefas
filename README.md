# 📋 Gestão de Atividades

Sistema completo para gerenciamento de múltiplas demandas de TI com controle de tempo, prioridades e notificações.

---

## 🚀 INSTALAÇÃO RÁPIDA (Para Clientes)

### Passo a Passo Simplificado

**1️⃣ Baixe o Instalador**
- Receba o arquivo `install.bat` do administrador de TI

**2️⃣ Execute o Instalador**
- Clique duas vezes em `install.bat`
- Aguarde a instalação automática (pode levar 2-3 minutos)
- O sistema fará tudo sozinho: cria ambiente, instala dependências e gera o executável

**3️⃣ Pronto!**
- Ao final, o instalador perguntará se deseja:
  - ✅ Adicionar ao startup do Windows (inicia automaticamente quando ligar o PC)
  - ✅ Executar o programa agora

**4️⃣ Como Usar**
- O ícone aparecerá no canto inferior direito (perto do relógio)
- Clique no ícone para abrir o sistema
- Minimizar = vai para a bandeja do sistema (não fecha!)

---

## 📖 Guia Completo do Usuário

### O Que Este Sistema Resolve

Se você trabalha com TI e tem dificuldade em gerenciar múltiplas demandas simultâneas, este sistema foi feito para você! Ele ajuda a:

- **Não esquecer tarefas** que foram iniciadas mas ficaram em segundo plano
- **Controlar o tempo** investido em cada demanda
- **Visualizar prioridades** de forma clara e colorida
- **Receber alertas** quando estiver com muitas tarefas em andamento
- **Gerar histórico** completo de todas as atividades

### ✨ Funcionalidades Principais

#### 1. Gestão Completa de Tarefas
- ✅ Criar novas tarefas com título, descrição e número do chamado
- ✅ Definir prioridade (Baixa, Média, Alta, Urgente)
- ✅ Iniciar, Pausar, Retomar e Concluir tarefas
- ✅ Excluir tarefas indesejadas

#### 2. Visualização Inteligente
- 🟢 **Verde**: Tarefas de baixa prioridade
- 🔵 **Azul**: Tarefas de média prioridade  
- 🟠 **Laranja**: Tarefas de alta prioridade
- 🔴 **Vermelho**: Tarefas urgentes

#### 3. Múltiplas Demandas em Paralelo
- Trabalhe em várias tarefas simultaneamente
- Sistema identifica automaticamente quando há mais de uma tarefa em andamento
- Alerta visual na interface sobre multitarefa

#### 4. Notificações Automáticas
- ⏰ **Alerta a cada 30 minutos** quando há múltiplas tarefas em andamento
- Notificação push nativa do Windows (ou messagebox de fallback)
- Ajuda a não esquecer tarefas secundárias

#### 5. Controle de Tempo Preciso
- ⏱️ Registro automático de data/hora de início e fim
- ⏸️ Função **Pause/Resume** para interrupções
- 📊 Cálculo automático do tempo total investido
- 📝 Log completo de todas as sessões de trabalho

#### 6. Integração com Chamados
- 📞 Campo dedicado para colar a linha do chamado
- Formata automaticamente: Ticket | E-mail | Categoria | Descrição
- Reutiliza informações do cliente

#### 7. Histórico e Relatórios
- 📜 Visualize todas as tarefas concluídas
- 🔍 Filtre por texto ou período (data início/fim)
- 📤 Exporte relatórios em Excel (.xlsx)
- 💾 Dados salvos automaticamente em `tarefas.json`

---

## 🎯 Guia Rápido de Uso

### Criando Sua Primeira Tarefa

1. **Clique em "➕ Nova Tarefa"**
2. **Cole a linha do chamado** no campo dedicado
   - Exemplo: `#TI2604276854	gessika.vasconcelos@grupocertare.com	Ajuda e Suporte > Hardware		"Após limpeza..."`
   - O sistema extrai automaticamente: Ticket, E-mail, Categoria e Descrição
3. **Defina a prioridade** (Baixa, Média, Alta, Urgente)
4. **Clique em "OK"**

### Trabalhando nas Tarefas

1. **Selecione uma tarefa** na lista "Tarefas Ativas"
2. **Clique em "▶️ Iniciar"** para começar a trabalhar
3. Quando precisar fazer outra coisa:
   - **"⏸️ Pausar"**: Para interromper e contar o tempo
   - **"⏯️ Retomar"**: Para continuar de onde parou
4. **Ao finalizar**: **"✅ Concluir"**

### Trabalhando com Múltiplas Tarefas

Você pode iniciar quantas tarefas quiser! O sistema vai:
- Mostrar um **alerta vermelho** no topo quando houver multitarefa
- Enviar **notificação a cada 30 minutos** lembrando das tarefas em andamento
- Manter o **controle de tempo individual** de cada uma

### Consultando o Histórico e Exportando Relatórios

1. **Clique em "📜 Ver Histórico"** no menu
2. **Use os filtros**:
   - 🔍 **Buscar por texto**: Digite qualquer palavra (cliente, ticket, descrição)
   - 📅 **Período**: Selecione data inicial e final
3. **Clique em "Filtrar"** para aplicar
4. **Para exportar**: Clique em "📤 Exportar Excel"
   - O arquivo será salvo na mesma pasta do programa

---

## 💡 Dicas Importantes

### Ícone na Bandeja do Sistema
- Quando minimizar, o sistema fica **oculto perto do relógio**
- Para voltar: clique duplo no ícone ou clique direito → "Abrir"
- Para fechar completamente: clique direito → "Sair"

### Startup Automático
- Se habilitado na instalação, inicia junto com o Windows
- Para remover: delete o atalho em `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

### Backup dos Dados
- Seus dados ficam em `tarefas.json` (na mesma pasta do .exe)
- **Dica**: Copie este arquivo regularmente para backup!
- Pode sincronizar via OneDrive/Google Drive se quiser usar em múltiplos PCs

### Notificações
- O alerta de 30 minutos só aparece se houver **2+ tarefas em andamento**
- Receba notificações mesmo com o sistema minimizado

---

## 🛠️ Solução de Problemas Comuns

| Problema | Solução |
|----------|---------|
| **Ícone não aparece na bandeja** | Clique na setinha ^ perto do relógio para mostrar ícones ocultos |
| **Não recebo notificações** | Verifique se o volume está ativo; o sistema usa notificações nativas do Windows |
| **Quero mudar o alerta de 30 min** | Contate o administrador de TI para ajustar no código |
| **Como faço backup?** | Copie o arquivo `tarefas.json` para outro local |
| **Posso usar em outro PC?** | Sim! Leve o `.exe` + `tarefas.json` juntos |

---

## 📞 Suporte Técnico

**Para Administradores de TI:**

O código fonte está disponível no repositório:
- **GitHub**: [isaacssjr/GestaoDeTarefas](https://github.com/isaacssjr/GestaoDeTarefas)

**Personalizações possíveis:**
- Alterar intervalo do alerta (linha ~430 do código)
- Mudar cores das prioridades (linhas ~172-177)
- Ajustar tamanho da janela (linha ~164)

**Requisitos Técnicos:**
- Windows 10 ou superior
- Python 3.8+ (apenas para recompilar/editar)
- Espaço em disco: ~50MB (após instalação)

---

## 🔄 Versão

**Versão atual**: 1.0  
**Última atualização**: 2025  
**Licença**: MIT  

**Desenvolvido com ❤️ para profissionais de TI que precisam de organização**
