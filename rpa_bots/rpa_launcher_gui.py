import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# --------------------------------------------------------------------
# Determine base directory (works both in development and when frozen)
# --------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --------------------------------------------------------------------
# Discover RPA scripts in the same folder (exclude this launcher itself)
# --------------------------------------------------------------------
SCRIPT_EXT = ".py"
LAUNCHER_NAME = os.path.basename(__file__)

def discover_scripts():
    return sorted([
        f for f in os.listdir(BASE_DIR)
        if f.endswith(SCRIPT_EXT) and f != LAUNCHER_NAME
    ])

# --------------------------------------------------------------------
# Simple GUI launcher
# --------------------------------------------------------------------
class RPAGuiLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPA Launcher – GUI Simple")
        self.geometry("800x600")
        self.configure(bg="#1e1e2e")
        self.process = None
        self._build_ui()
        self._load_scripts()

    # ----------------------------------------------------------------
    # UI construction
    # ----------------------------------------------------------------
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1e1e2e", pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🛠️ RPA Launcher", font=("Segoe UI", 20, "bold"), bg="#1e1e2e", fg="#e2e8f0").pack()

        # Main panes
        main = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#1e1e2e")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # Left – script list
        left = tk.Frame(main, bg="#2a2a3e")
        main.add(left, width=250)
        tk.Label(left, text="Scripts disponibles", bg="#2a2a3e", fg="#94a3b8", font=("Segoe UI", 11, "bold")).pack(pady=(0,5))
        self.listbox = tk.Listbox(left, bg="#2a2a3e", fg="#e2e8f0", selectbackground="#7c3aed", activestyle="none")
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # Right – console and controls
        right = tk.Frame(main, bg="#1e1e2e")
        main.add(right)
        # Console output
        self.console = scrolledtext.ScrolledText(
            right,
            bg="#12121c",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            font=("Cascadia Code", 10),
            wrap="word",
        )
        self.console.pack(fill="both", expand=True, pady=(0,5))
        self.console.configure(state="disabled")
        # Buttons
        btn_frame = tk.Frame(right, bg="#1e1e2e")
        btn_frame.pack(fill="x", pady=5)
        self.run_btn = ttk.Button(btn_frame, text="▶ Ejecutar", command=self._run_selected, state="disabled")
        self.run_btn.pack(side="left", padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="⏹ Detener", command=self._stop_process, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        self.clear_btn = ttk.Button(btn_frame, text="🗑 Limpiar", command=self._clear_console)
        self.clear_btn.pack(side="right", padx=5)

    # ----------------------------------------------------------------
    # Load scripts
    # ----------------------------------------------------------------
    def _load_scripts(self):
        self.listbox.delete(0, tk.END)
        for script in discover_scripts():
            self.listbox.insert(tk.END, script)

    # ----------------------------------------------------------------
    # UI callbacks
    # ----------------------------------------------------------------
    def _on_select(self, event=None):
        sel = self.listbox.curselection()
        if sel:
            self.run_btn.configure(state="normal")
        else:
            self.run_btn.configure(state="disabled")

    def _log(self, msg):
        self.console.configure(state="normal")
        self.console.insert(tk.END, msg + "\n")
        self.console.see(tk.END)
        self.console.configure(state="disabled")

    def _clear_console(self):
        self.console.configure(state="normal")
        self.console.delete('1.0', tk.END)
        self.console.configure(state="disabled")

    # ----------------------------------------------------------------
    # Run / stop logic
    # ----------------------------------------------------------------
    def _run_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Sin selección", "Selecciona un script antes de ejecutar.")
            return
        script_name = self.listbox.get(sel[0])
        script_path = os.path.join(BASE_DIR, script_name)
        if not os.path.isfile(script_path):
            self._log(f"❌ Archivo no encontrado: {script_path}")
            return
        python_exec = sys.executable  # works in dev and frozen mode
        self._log(f"🚀 Ejecutando {script_name} con {python_exec}")
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        def target():
            try:
                # Run Python in unbuffered mode to get real‑time output
                self.process = subprocess.Popen(
                    [python_exec, "-u", script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    cwd=BASE_DIR,
                )
                for line in self.process.stdout:
                    # Schedule UI update in the main thread
                    self.after(0, lambda l=line: self._log(l.rstrip()))
                self.process.wait()
                rc = self.process.returncode
                self.after(0, lambda: self._log(f"✅ Proceso finalizado con código {rc}"))
            except Exception as e:
                self.after(0, lambda: self._log(f"❌ Error al ejecutar: {e}"))
            finally:
                self.after(0, self._reset_ui)

        # Start thread
        threading.Thread(target=target, daemon=True).start()

    def _stop_process(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self._log("⏹ Proceso detenido por el usuario.")
        self._reset_ui()

    def _reset_ui(self):
        self.run_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.process = None

if __name__ == "__main__":
    RPAGuiLauncher().mainloop()
