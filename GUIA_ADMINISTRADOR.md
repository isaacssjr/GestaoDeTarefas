# 🛠️ Guia do Administrador de TI

## Para quem vai distribuir o sistema

---

## 📦 O Que Você Precisa Distribuir

### Opção 1: Enviar o Instalador (Recomendado)

**Arquivos para enviar ao cliente:**
```
📁 GestaoDeAtividades/
├── install.bat          ← Este é o único que o cliente executa!
├── gestao_atividades.py ← Código fonte
├── requirements.txt     ← Dependências
└── README.md            ← Documentação completa
```

**Vantagens:**
- ✅ Cliente só precisa dar dois cliques
- ✅ Instala tudo automaticamente
- ✅ Gera o .exe na máquina do cliente
- ✅ Mais seguro (não envia executável pronto)

**Desvantagens:**
- ❌ Precisa ter Python instalado na máquina
- ❌ Leva 2-3 minutos para instalar

---

### Opção 2: Enviar o Executável Pronto

**Passos para gerar o .exe:**

1. **No SEU computador, execute:**
```bash
# Instale as dependências
pip install -r requirements.txt

# Compile o executável
pyinstaller --onefile --windowed --name "GestaoDeAtividades" gestao_atividades.py
```

2. **O executável estará em:**
```
📁 dist/
└── GestaoDeAtividades.exe
```

3. **Arquivos para enviar ao cliente:**
```
📁 GestaoDeAtividades/
├── GestaoDeAtividades.exe  ← Executável pronto
├── tarefas.json            ← (opcional) dados iniciais vazios
└── GUIA_RAPIDO_CLIENTE.md  ← Instruções de uso
```

**Vantagens:**
- ✅ Não precisa de Python instalado
- ✅ Já está pronto para usar
- ✅ Mais rápido para o cliente

**Desvantagens:**
- ❌ Arquivo maior (~15-20 MB)
- ❌ Alguns antivírus podem alertar (falso positivo)

---

## 🚀 Processo de Instalação (Opção 1 - Recomendada)

### Passo a Passo para o Cliente

**1. Envie os arquivos**
- Compacte a pasta em `.zip`
- Envie por e-mail/Teams/WhatsApp

**2. Instrua o cliente:**
> "Extraia o arquivo ZIP e dê dois cliques em `install.bat`"

**3. O instalador fará:**
- ✅ Verifica se Python está instalado
- ✅ Cria ambiente virtual (.venv)
- ✅ Instala dependências (plyer, pyinstaller, openpyxl)
- ✅ Compila o executável
- ✅ Pergunta se adiciona ao startup do Windows
- ✅ Pergunta se executa agora

**4. Após instalação:**
- O executável fica em: `dist/GestaoDeAtividades.exe`
- Os dados ficam em: `tarefas.json`

---

## ⚙️ Personalizações Possíveis

### Mudar Intervalo do Alerta (30 min)

**Arquivo:** `gestao_atividades.py`  
**Linha:** ~430

```python
intervalo_alerta = 1800  # 30 minutos (em segundos)
```

**Valores sugeridos:**
- `900` = 15 minutos
- `1800` = 30 minutos (padrão)
- `3600` = 1 hora
- `7200` = 2 horas

---

### Mudar Cores das Prioridades

**Arquivo:** `gestao_atividades.py`  
**Linhas:** ~172-177

```python
self.cores_prioridade = {
    Prioridade.BAIXA: "#90EE90",      # Verde claro
    Prioridade.MEDIA: "#87CEEB",      # Azul claro
    Prioridade.ALTA: "#FFA500",       # Laranja
    Prioridade.URGENTE: "#FF6B6B"     # Vermelho
}
```

**Cores em hexadecimal:** Use qualquer cor em formato `#RRGGBB`

---

### Mudar Tamanho da Janela

**Arquivo:** `gestao_atividades.py`  
**Linha:** ~164

```python
self.root.geometry("1200x700")  # Largura x Altura
```

---

### Mudar Nome do Executável

**No arquivo:** `install.bat`  
**Linha:** ~52

```batch
pyinstaller --onefile --windowed --name "SEU_NOME_AQUI" gestao_atividades.py
```

---

## 🔧 Startup Automático do Windows

### Como Funciona

O instalador cria um atalho em:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\GestaoDeAtividades.lnk
```

### Para Remover Manualmente

**No computador do cliente:**
1. Pressione `Win + R`
2. Digite: `shell:startup`
3. Delete o atalho `GestaoDeAtividades.lnk`

### Para Adicionar Manualmente

**Script PowerShell:**
```powershell
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\GestaoDeAtividades.lnk")
$Shortcut.TargetPath = "C:\Caminho\Para\dist\GestaoDeAtividades.exe"
$Shortcut.WorkingDirectory = "C:\Caminho\Para\dist"
$Shortcut.Save()
```

---

## 💾 Backup dos Dados

### Onde Estão os Dados

**Arquivo:** `tarefas.json`  
**Local:** Mesma pasta onde o .exe foi executado

### Estrutura do JSON

```json
{
  "tarefas": [
    {
      "id": 1,
      "titulo": "...",
      "descricao": "...",
      "ticket": "...",
      "email": "...",
      "categoria": "...",
      "prioridade": "ALTA",
      "status": "CONCLUIDA",
      "data_criacao": "2025-01-15T10:30:00",
      "sessoes": [
        {
          "inicio": "2025-01-15T10:35:00",
          "fim": "2025-01-15T11:45:00",
          "duracao_segundos": 4200
        }
      ],
      "tempo_total_segundos": 4200
    }
  ]
}
```

### Procedimento de Backup

**Para fazer backup:**
1. Feche o sistema (botão direito no ícone → Sair)
2. Copie o arquivo `tarefas.json`
3. Guarde em local seguro

**Para restaurar:**
1. Feche o sistema
2. Substitua o `tarefas.json` pelo backup
3. Abra o sistema novamente

---

## 🔄 Atualização de Versão

### Quando Lançar Nova Versão

**Passos:**

1. **Atualize o código no Git:**
```bash
git add .
git commit -m "Versão 1.1 - Descrição das mudanças"
git push
```

2. **Gere novo instalador:**
- Atualize o número da versão no `README.md`
- Atualize o `GUIA_RAPIDO_CLIENTE.md` se necessário

3. **Distribua:**
- Envie novo `install.bat` + arquivos atualizados
- Ou envie novo `.exe` (se usar Opção 2)

4. **Instrua os clientes:**
> "Uma nova versão está disponível. Por favor, execute o install.bat novamente para atualizar."

---

## 🐛 Solução de Problemas Técnicos

### "Python não encontrado"

**Causa:** Python não está instalado ou não está no PATH

**Solução:**
1. Baixe Python em https://python.org
2. Na instalação, marque: **"Add Python to PATH"**
3. Reinicie o terminal/computador
4. Execute `install.bat` novamente

---

### "Erro ao compilar .exe"

**Causas possíveis:**
- Dependências não instaladas
- PyInstaller desatualizado
- Antivírus bloqueando

**Solução:**
```bash
# Atualize pip e dependências
python -m pip install --upgrade pip
pip install --upgrade pyinstaller plyer openpyxl

# Tente compilar manualmente
pyinstaller --onefile --windowed --name "GestaoDeAtividades" gestao_atividades.py
```

---

### "Antivírus bloqueou o .exe"

**Causa:** Falso positivo comum em executáveis Python

**Soluções:**
1. Adicione exceção no antivírus para a pasta do sistema
2. Assine o executável com certificado digital (opção avançada)
3. Use a Opção 1 (instalador) em vez de enviar .exe pronto

---

### "Ícone não aparece na bandeja"

**Causas:**
- Windows escondendo ícones
- Sistema não iniciou corretamente

**Solução:**
1. Clique na setinha `^` perto do relógio
2. Arraste o ícone para a barra principal
3. Se não aparecer, reinicie o sistema

---

## 📊 Monitoramento de Uso

### Logs do Sistema

O sistema gera logs em tempo de execução no console (se rodar como script).

**Para ver logs:**
```bash
python gestao_atividades.py
```

### Métricas Úteis

Você pode analisar o `tarefas.json` para saber:
- Total de tarefas por usuário
- Tempo médio por chamado
- Chamados por categoria
- Produtividade da equipe

**Exemplo de análise (Python):**
```python
import json

with open('tarefas.json', 'r') as f:
    dados = json.load(f)

total = len(dados['tarefas'])
concluidas = len([t for t in dados['tarefas'] if t['status'] == 'CONCLUIDA'])
tempo_total = sum(t['tempo_total_segundos'] for t in dados['tarefas'])

print(f"Total: {total}")
print(f"Concluídas: {concluidas}")
print(f"Tempo total: {tempo_total / 3600:.2f} horas")
```

---

## 📞 Suporte aos Usuários

### Checklist de Atendimento

Quando um usuário relatar problema:

- [ ] O ícone aparece perto do relógio?
- [ ] O sistema abre ao clicar duas vezes?
- [ ] Recebe notificações?
- [ ] Consegue criar tarefas?
- [ ] O arquivo `tarefas.json` existe?

### Perguntas Frequentes

**"Como faço backup?"**
> Copie o arquivo `tarefas.json` da pasta onde o sistema está instalado.

**"Posso usar em outro PC?"**
> Sim! Copie o `.exe` (da pasta dist) e o `tarefas.json` para o novo PC.

**"Quero mudar o alerta de 30 minutos"**
> Contate o administrador de TI para ajustar no código.

**"O sistema está lento"**
> Feche completamente (botão direito → Sair) e abra novamente.

---

## 🎯 Melhores Práticas

### Para Distribuição

✅ **Faça:**
- Teste em uma máquina limpa antes de distribuir
- Envie o `GUIA_RAPIDO_CLIENTE.md` junto
- Mantenha backup centralizado dos `tarefas.json` dos usuários
- Versione adequadamente no Git

❌ **Não faça:**
- Não envie .exe sem testar antes
- Não modifique o código sem testar todas as funções
- Não esqueça de atualizar a documentação

### Para Manutenção

✅ **Rotina recomendada:**
- Semanal: Verifique issues no Git
- Mensal: Faça backup dos dados dos usuários
- Trimestral: Revise métricas de uso
- Anual: Avalie melhorias e novas versões

---

## 📚 Recursos Adicionais

### Links Úteis

- **Repositório Git**: https://github.com/isaacssjr/GestaoDeTarefas
- **Python Download**: https://python.org
- **PyInstaller Docs**: https://pyinstaller.org
- **Tkinter Docs**: https://docs.python.org/3/library/tkinter.html

### Ferramentas Recomendadas

- **VS Code**: Editor de código para modificações
- **7-Zip**: Para compactar arquivos para envio
- **Notepad++**: Para editar arquivos JSON manualmente

---

**Documentação criada para facilitar sua gestão!**

*Dúvidas? Consulte o README.md ou o código fonte.*
