import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime, timedelta
import json
import os
import sys
import threading
import time
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

# Tenta importar plyer para notificações, se não tiver, usa fallback
try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Atividades - TI")
        self.root.geometry("1000x700")
        
        # Configurações de Tema Escuro
        self.colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'input_bg': '#3c3f41',
            'input_fg': '#ffffff',
            'btn_bg': '#4a90e2',
            'btn_fg': '#ffffff',
            'header_bg': '#1e1e1e',
            'tree_bg': '#323232',
            'tree_sel': '#505050',
            'low': '#4caf50',      # Verde
            'medium': '#2196f3',   # Azul
            'high': '#ff9800',     # Laranja
            'urgent': '#f44336'    # Vermelho
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos customizados
        style.configure("Treeview", background=self.colors['tree_bg'], 
                        fieldbackground=self.colors['tree_bg'], 
                        foreground=self.colors['fg'],
                        rowheight=25)
        style.configure("Treeview.Heading", background=self.colors['header_bg'], 
                        foreground=self.colors['fg'], font=('Arial', 10, 'bold'))
        style.map("Treeview", background=[('selected', self.colors['tree_sel'])])
        
        style.configure("TButton", background=self.colors['btn_bg'], foreground=self.colors['btn_fg'])
        style.configure("TLabel", background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure("TEntry", fieldbackground=self.colors['input_bg'], foreground=self.colors['input_fg'])
        style.configure("TCombobox", fieldbackground=self.colors['input_bg'], foreground=self.colors['input_fg'])

        # Dados
        self.tasks = {}  # ID -> dados da tarefa
        self.active_tasks = set() # IDs das tarefas em andamento
        self.timers = {} # ID -> timer thread
        self.paused_times = defaultdict(list) # ID -> lista de períodos pausados
        
        # Variáveis de controle de notificação
        self.last_notification_time = {} # ID -> ultimo aviso
        self.notification_interval = 1800 # 30 minutos em segundos

        self.setup_ui()
        self.load_data()
        self.start_global_timer()
        
        # Configurar fechamento para tray
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.tray_icon = None
        self.setup_tray()

    def setup_tray(self):
        # Implementação simplificada de tray (requer pystray ou similar, aqui faremos minimizar normal)
        # Para um exe standalone robusto, ideal usar pystray, mas vamos focar na funcionalidade core
        pass

    def minimize_to_tray(self):
        self.root.withdraw()
        # Em uma implementação completa com pystray, criaria o ícone aqui.
        # Como fallback, mostramos um messagebox ou apenas minimizamos.
        # Para este MVP, vamos criar um botão "Restaurar" se estiver minimizado ou usar o ícone na taskbar padrão.
        # Nota: Tkinter puro não tem tray nativo fácil sem bibliotecas extras.
        # Vamos adicionar um botão na UI para "Minimizar para Bandeja" que simula o comportamento
        # ou apenas minimiza a janela.
        if HAS_PLYER:
             notification.notify(
                title="Gestão de Atividades",
                message="Sistema minimizado. Verifique a bandeja do sistema.",
                timeout=3
            )
        # Recriar ícone simples se necessário, por enquanto deixamos minimizado na taskbar
        # Para funcionar perfeitamente em tray, seria necessário instalar 'pystray' e 'Pillow'
        # Vou adicionar a lógica de restauração via duplo clique na taskbar se possível, 
        # mas o comportamento padrão do Windows já agrupa.
        
        # Criar uma janela temporária invisível para segurar o foco? Não, vamos simplificar.
        # O usuário pode restaurar clicando no ícone na barra de tarefas.

    def restore_from_tray(self, event=None):
        self.root.deiconify()
        self.root.focus_force()

    def setup_ui(self):
        # Frame Superior - Entrada de Dados
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # Título
        lbl_title = ttk.Label(top_frame, text="Nova Demanda", font=("Arial", 14, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=6, sticky=tk.W, pady=(0, 10))
        
        # Campo Único do Chamado
        ttk.Label(top_frame, text="Cole a linha do chamado aqui:").grid(row=1, column=0, sticky=tk.W)
        self.entry_call = ttk.Entry(top_frame, width=80)
        self.entry_call.grid(row=1, column=1, columnspan=4, padx=5, pady=5)
        self.entry_call.bind('<KeyRelease>', self.parse_call_auto)
        
        # Botão Limpar
        btn_clear = ttk.Button(top_frame, text="🗑️ Limpar", command=self.clear_form)
        btn_clear.grid(row=1, column=5, padx=5)

        # Campos Ocultos/Preenchidos Automaticamente (para visualização)
        info_frame = ttk.LabelFrame(top_frame, text="Dados Extraídos", padding="5")
        info_frame.grid(row=2, column=0, columnspan=6, sticky=tk.EW, pady=5)
        
        self.lbl_ticket = ttk.Label(info_frame, text="Ticket: -", foreground=self.colors['medium'])
        self.lbl_ticket.grid(row=0, column=0, padx=10, sticky=tk.W)
        
        self.lbl_email = ttk.Label(info_frame, text="Email: -")
        self.lbl_email.grid(row=0, column=1, padx=10, sticky=tk.W)
        
        self.lbl_cat = ttk.Label(info_frame, text="Cat: -")
        self.lbl_cat.grid(row=0, column=2, padx=10, sticky=tk.W)

        # Prioridade
        ttk.Label(top_frame, text="Prioridade:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.combo_priority = ttk.Combobox(top_frame, values=["Baixa", "Média", "Alta", "Urgente"], state="readonly", width=17)
        self.combo_priority.current(1)
        self.combo_priority.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Botão Adicionar
        btn_add = ttk.Button(top_frame, text="➕ Adicionar Tarefa", command=self.add_task)
        btn_add.grid(row=3, column=2, columnspan=2, padx=20)

        # Lista de Tarefas
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Ticket', 'Descrição', 'Prioridade', 'Status', 'Tempo Total')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != 'Descrição' else 300)
            
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Status', width=100, anchor='center')
        self.tree.column('Tempo Total', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind correto para seleção
        self.tree.bind('<<TreeviewSelect>>', self.on_task_select)
        # Bind duplo clique para iniciar/pausar rápido
        self.tree.bind('<Double-1>', self.on_double_click_action)

        # Painel de Ações
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        self.btn_start = ttk.Button(action_frame, text="▶️ Iniciar/Retomar", command=self.start_task, state=tk.DISABLED)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        self.btn_pause = ttk.Button(action_frame, text="⏸️ Pausar", command=self.pause_task, state=tk.DISABLED)
        self.btn_pause.pack(side=tk.LEFT, padx=5)
        
        self.btn_finish = ttk.Button(action_frame, text="✅ Concluir", command=self.finish_task, state=tk.DISABLED)
        self.btn_finish.pack(side=tk.LEFT, padx=5)
        
        self.btn_delete = ttk.Button(action_frame, text="❌ Excluir", command=self.delete_task, state=tk.DISABLED)
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        
        self.btn_logs = ttk.Button(action_frame, text="📊 Ver Logs", command=self.open_logs_window)
        self.btn_logs.pack(side=tk.RIGHT, padx=5)

        self.selected_item_id = None

    def parse_call_auto(self, event=None):
        """Parse da linha do chamado automaticamente"""
        text = self.entry_call.get().strip()
        if not text:
            self.clear_labels()
            return

        # Tenta separar por tabulação primeiro, senão por espaços múltiplos ou padrões
        parts = text.split('\t')
        
        # Se não tiver tabs, tenta um split mais inteligente baseado no formato esperado
        if len(parts) < 4:
            # Formato esperado: #ID email categoria "descricao"
            # Regex simples ou split manual
            import re
            # Tenta achar o ticket (#TI...)
            match = re.match(r'(#\w+)\s+(\S+)\s+(.*?)\s+"(.*)"', text)
            if match:
                parts = [match.group(1), match.group(2), match.group(3), match.group(4)]
            else:
                # Fallback: split por espaços se nada der certo (pode quebrar categorias com espaço)
                parts = text.split()

        if len(parts) >= 4:
            ticket = parts[0]
            email = parts[1]
            category = parts[2]
            desc = parts[3].strip('"') # Remove aspas se houver
            
            self.lbl_ticket.config(text=f"Ticket: {ticket}")
            self.lbl_email.config(text=f"Email: {email}")
            self.lbl_cat.config(text=f"Cat: {category}")
            
            # Salva dados temporários no entry ou variável auxiliar
            self.current_parsed_data = {
                'ticket': ticket,
                'email': email,
                'category': category,
                'desc': desc
            }
        else:
            self.clear_labels()
            if hasattr(self, 'current_parsed_data'):
                del self.current_parsed_data

    def clear_labels(self):
        self.lbl_ticket.config(text="Ticket: -")
        self.lbl_email.config(text="Email: -")
        self.lbl_cat.config(text="Cat: -")
        if hasattr(self, 'current_parsed_data'):
            del self.current_parsed_data

    def clear_form(self):
        self.entry_call.delete(0, tk.END)
        self.combo_priority.current(1)
        self.clear_labels()
        if hasattr(self, 'current_parsed_data'):
            del self.current_parsed_data

    def add_task(self):
        if not hasattr(self, 'current_parsed_data'):
            messagebox.showwarning("Atenção", "Cole a linha do chamado e aguarde a extração dos dados.")
            return
        
        data = self.current_parsed_data
        priority = self.combo_priority.get()
        
        task_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        task = {
            'id': task_id,
            'ticket': data['ticket'],
            'email': data['email'],
            'category': data['category'],
            'description': data['desc'],
            'priority': priority,
            'status': 'Aguardando', # Aguardando, Em Andamento, Pausado, Concluido
            'start_time': None,
            'pause_time': None,
            'total_seconds': 0,
            'history': [] # Log de eventos
        }
        
        self.tasks[task_id] = task
        self.save_data()
        self.refresh_tree()
        self.clear_form()
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for tid, task in self.tasks.items():
            # Formatar tempo
            hrs = int(task['total_seconds'] // 3600)
            mins = int((task['total_seconds'] % 3600) // 60)
            secs = int(task['total_seconds'] % 60)
            time_str = f"{hrs:02}:{mins:02}:{secs:02}"
            
            # Cores por prioridade
            tag = 'low'
            if task['priority'] == 'Média': tag = 'medium'
            elif task['priority'] == 'Alta': tag = 'high'
            elif task['priority'] == 'Urgente': tag = 'urgent'
            
            self.tree.insert('', tk.END, iid=tid, values=(
                tid[-4:], # Mostra ultimos 4 digitos do ID
                task['ticket'],
                task['description'][:40] + "...",
                task['priority'],
                task['status'],
                time_str
            ), tags=(tag,))
            
        # Configurar tags de cor
        self.tree.tag_configure('low', background=self.colors['low'], foreground='white')
        self.tree.tag_configure('medium', background=self.colors['medium'], foreground='white')
        self.tree.tag_configure('high', background=self.colors['high'], foreground='white')
        self.tree.tag_configure('urgent', background=self.colors['urgent'], foreground='white')

    def on_task_select(self, event):
        selection = self.tree.selection()
        if selection:
            self.selected_item_id = selection[0]
            task = self.tasks.get(self.selected_item_id)
            if task:
                self.btn_start.config(state=tk.NORMAL if task['status'] in ['Aguardando', 'Pausado'] else tk.DISABLED)
                self.btn_pause.config(state=tk.NORMAL if task['status'] == 'Em Andamento' else tk.DISABLED)
                self.btn_finish.config(state=tk.NORMAL if task['status'] in ['Em Andamento', 'Pausado'] else tk.DISABLED)
                self.btn_delete.config(state=tk.NORMAL if task['status'] in ['Aguardando', 'Concluido'] else tk.DISABLED)
        else:
            self.selected_item_id = None
            self.btn_start.config(state=tk.DISABLED)
            self.btn_pause.config(state=tk.DISABLED)
            self.btn_finish.config(state=tk.DISABLED)
            self.btn_delete.config(state=tk.DISABLED)

    def on_double_click_action(self, event):
        # Atalho: Duplo clique inicia se estiver parado, pausa se estiver rodando
        self.on_task_select(event) # Garante seleção
        if self.selected_item_id:
            task = self.tasks[self.selected_item_id]
            if task['status'] in ['Aguardando', 'Pausado']:
                self.start_task()
            elif task['status'] == 'Em Andamento':
                self.pause_task()

    def start_task(self):
        if not self.selected_item_id: return
        task = self.tasks[self.selected_item_id]
        
        if task['status'] == 'Aguardando':
            task['start_time'] = datetime.now()
            task['history'].append(f"Início: {task['start_time'].strftime('%d/%m %H:%M')}")
        elif task['status'] == 'Pausado':
            task['history'].append(f"Retomado: {datetime.now().strftime('%d/%m %H:%M')}")
            
        task['status'] = 'Em Andamento'
        self.active_tasks.add(self.selected_item_id)
        self.save_data()
        self.refresh_tree()
        self.on_task_select(None) # Atualiza botões
        
        # Inicia timer específico se necessário (lógica simplificada: global timer cuida)
        self.check_multiple_tasks()

    def pause_task(self):
        if not self.selected_item_id: return
        task = self.tasks[self.selected_item_id]
        
        if task['status'] == 'Em Andamento':
            now = datetime.now()
            # Calcular tempo decorrido desde o último start
            # Precisamos armazenar o 'last_start_time' no objeto task
            if not hasattr(task, 'last_start_time'):
                 task['last_start_time'] = task['start_time'] if task['start_time'] else now
            
            delta = (now - task['last_start_time']).total_seconds()
            task['total_seconds'] += delta
            task['pause_time'] = now
            task['history'].append(f"Pausa: {now.strftime('%d/%m %H:%M')} (Acumulado: {self.format_time(task['total_seconds'])})")
            task['status'] = 'Pausado'
            
            if self.selected_item_id in self.active_tasks:
                self.active_tasks.remove(self.selected_item_id)
                
            self.save_data()
            self.refresh_tree()
            self.on_task_select(None)

    def finish_task(self):
        if not self.selected_item_id: return
        task = self.tasks[self.selected_item_id]
        
        if task['status'] == 'Em Andamento':
            now = datetime.now()
            if not hasattr(task, 'last_start_time'):
                task['last_start_time'] = task['start_time']
            delta = (now - task['last_start_time']).total_seconds()
            task['total_seconds'] += delta
            
        task['status'] = 'Concluido'
        task['end_time'] = datetime.now()
        task['history'].append(f"Concluído: {task['end_time'].strftime('%d/%m %H:%M')}")
        
        if self.selected_item_id in self.active_tasks:
            self.active_tasks.remove(self.selected_item_id)
            
        self.save_data()
        self.refresh_tree()
        self.on_task_select(None)
        messagebox.showinfo("Concluído", f"Tarefa {task['ticket']} finalizada!\nTempo total: {self.format_time(task['total_seconds'])}")

    def delete_task(self):
        if not self.selected_item_id: return
        if messagebox.askyesno("Excluir", "Tem certeza que deseja excluir esta tarefa?"):
            del self.tasks[self.selected_item_id]
            if self.selected_item_id in self.active_tasks:
                self.active_tasks.remove(self.selected_item_id)
            self.save_data()
            self.refresh_tree()
            self.on_task_select(None)

    def format_time(self, seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02}:{m:02}:{s:02}"

    def check_multiple_tasks(self):
        # Verifica se há mais de uma tarefa em andamento e notifica
        if len(self.active_tasks) > 1:
            now = time.time()
            for tid in self.active_tasks:
                last_notif = self.last_notification_time.get(tid, 0)
                if now - last_notif >= self.notification_interval:
                    task = self.tasks[tid]
                    msg = f"Atenção: Você tem múltiplas tarefas em andamento!\nUma delas é: {task['ticket']} - {task['description'][:30]}"
                    
                    if HAS_PLYER:
                        notification.notify(
                            title="Gestão de Atividades - Múltiplas Demandas",
                            message=msg,
                            timeout=10
                        )
                    else:
                        # Fallback messagebox (bloqueante, usar com cuidado ou thread)
                        # Melhor não usar messagebox bloqueante aqui para não travar o fluxo
                        pass 
                    
                    self.last_notification_time[tid] = now

    def start_global_timer(self):
        def update_loop():
            while True:
                time.sleep(1)
                # Atualiza tempos das tarefas em andamento na memória (visualmente)
                # E verifica notificações
                now = datetime.now()
                updated = False
                for tid in list(self.active_tasks):
                    if tid in self.tasks:
                        task = self.tasks[tid]
                        if not hasattr(task, 'last_start_time'):
                            task['last_start_time'] = task['start_time']
                        
                        # Apenas para exibição no treeview em tempo real, não salva no disco a cada segundo
                        # O save é feito ao pausar/concluir
                        pass
                
                self.check_multiple_tasks()
                
                # Atualiza UI a cada segundo se houver tarefas ativas
                if self.active_tasks:
                    self.root.after(0, self.refresh_tree)

        t = threading.Thread(target=update_loop, daemon=True)
        t.start()

    def save_data(self):
        # Serializa dados, convertendo datetime para string
        data_save = {}
        for k, v in self.tasks.items():
            d = v.copy()
            # Remove atributos temporários de cálculo se houver
            if 'last_start_time' in d: del d['last_start_time']
            data_save[k] = d
            
        with open("tasks_db.json", "w", encoding='utf-8') as f:
            json.dump(data_save, f, indent=4, ensure_ascii=False)

    def load_data(self):
        if os.path.exists("tasks_db.json"):
            try:
                with open("tasks_db.json", "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data
                    # Recalcula active_tasks baseado no status
                    for k, v in self.tasks.items():
                        if v['status'] == 'Em Andamento':
                            # Se estava em andamento ao fechar, considera como Pausado para segurança
                            # ou mantém, mas precisa ajustar o last_start_time
                            v['status'] = 'Pausado' 
                            v['history'].append("Sistema reiniciado (ajuste de tempo necessário)")
                    self.refresh_tree()
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")

    def open_logs_window(self):
        win = tk.Toplevel(self.root)
        win.title("Histórico de Logs")
        win.geometry("900x600")
        win.configure(bg=self.colors['bg'])
        
        # Filtros
        filter_frame = ttk.Frame(win, padding="10")
        filter_frame.pack(fill=tk.X)
        
        ttk.Label(filter_frame, text="Filtrar por Texto:").pack(side=tk.LEFT)
        entry_filter = ttk.Entry(filter_frame, width=30)
        entry_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="De:").pack(side=tk.LEFT, padx=(10,0))
        date_start = ttk.Entry(filter_frame, width=10)
        date_start.insert(0, "DD/MM/AAAA")
        date_start.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Até:").pack(side=tk.LEFT)
        date_end = ttk.Entry(filter_frame, width=10)
        date_end.insert(0, "DD/MM/AAAA")
        date_end.pack(side=tk.LEFT, padx=5)
        
        def apply_filter():
            for item in tree_logs.get_children():
                tree_logs.delete(item)
            
            txt = entry_filter.get().lower()
            # Implementação simples de filtro de texto
            for tid, task in self.tasks.items():
                if task['status'] != 'Concluido': continue
                
                match = True
                if txt:
                    s = f"{task['ticket']} {task['description']} {task['email']}".lower()
                    if txt not in s: match = False
                
                if match:
                    hrs = int(task['total_seconds'] // 3600)
                    mins = int((task['total_seconds'] % 3600) // 60)
                    time_str = f"{hrs:02}:{mins:02}"
                    
                    tree_logs.insert('', tk.END, values=(
                        task['ticket'],
                        task['email'],
                        task['priority'],
                        task['history'][-1] if task['history'] else '-', # Data fim
                        time_str,
                        task['description'][:30]
                    ))

        ttk.Button(filter_frame, text="Filtrar", command=apply_filter).pack(side=tk.LEFT, padx=10)
        
        btn_export = ttk.Button(filter_frame, text="📥 Exportar Excel", command=lambda: self.export_excel(win))
        btn_export.pack(side=tk.RIGHT)

        # Treeview Logs
        cols = ('Ticket', 'Email', 'Prioridade', 'Data Fim', 'Tempo Total', 'Descrição')
        tree_logs = ttk.Treeview(win, columns=cols, show='headings')
        for c in cols:
            tree_logs.heading(c, text=c)
            tree_logs.column(c, width=100)
        tree_logs.column('Descrição', width=300)
        tree_logs.column('Email', width=200)
        
        tree_logs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        apply_filter() # Carrega tudo inicialmente

    def export_excel(self, parent_win):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not filename: return
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Logs de Atividades"
        
        # Header
        headers = ["Ticket", "Email", "Categoria", "Descrição", "Prioridade", "Status", "Tempo Total (s)", "Tempo Formatado", "Histórico"]
        ws.append(headers)
        
        # Fill
        for task in self.tasks.values():
            hrs = int(task['total_seconds'] // 3600)
            mins = int((task['total_seconds'] % 3600) // 60)
            time_str = f"{hrs:02}:{mins:02}"
            
            ws.append([
                task['ticket'],
                task['email'],
                task['category'],
                task['description'],
                task['priority'],
                task['status'],
                task['total_seconds'],
                time_str,
                "\n".join(task['history'])
            ])
            
        # Style
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
            
        wb.save(filename)
        messagebox.showinfo("Sucesso", "Log exportado com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
