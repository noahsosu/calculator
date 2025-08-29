import tkinter as tk
from tkinter import font
import math

# --- Theme settings (dark, Windows-like) ---
DARK_BG = "#23272f"
BTN_BG = "#363c4a"
BTN_BG2 = "#22252A"
BTN_FG = "#e6e6e6"
BTN_HOVER = "#444b5a"
ACCENT_BG = "#47d6ff"
ACCENT_FG = "#22252A"
DISPLAY_BG = "#23272f"
DISPLAY_FG = "#fff"

WINDOW_W = 430
WINDOW_H = 540

class ModernCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.configure(bg=DARK_BG)
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.minsize(WINDOW_W, WINDOW_H)
        self.resizable(False, False)
        self.expression = ""
        self.memory = 0
        self._build_fonts()
        self._build_display()
        self._build_memory_bar()
        self._build_buttons()

    def _build_fonts(self):
        self.display_font = font.Font(family="Segoe UI", size=40, weight="bold")
        self.button_font = font.Font(family="Segoe UI", size=18)
        self.mem_font = font.Font(family="Segoe UI", size=11)

    def _build_display(self):
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            self, textvariable=self.display_var, anchor="e",
            font=self.display_font, bg=DISPLAY_BG, fg=DISPLAY_FG,
            bd=0, padx=20, pady=14
        )
        self.display.place(x=0, y=52, width=WINDOW_W, height=80)

    def _build_memory_bar(self):
        # "Standard" and memory buttons row
        bar = tk.Frame(self, bg=DARK_BG)
        bar.place(x=0, y=0, width=WINDOW_W, height=48)
        tk.Label(bar, text="Standard", font=("Segoe UI", 16, "bold"), fg=BTN_FG, bg=DARK_BG).pack(side="left", padx=14)
        # Memory buttons
        mem_btns = ["MC", "MR", "M+", "M-", "MS", "M^"]
        for m in mem_btns:
            b = tk.Label(bar, text=m, font=self.mem_font, fg=BTN_FG, bg=DARK_BG, padx=8)
            b.pack(side="left", padx=2)

    def _build_buttons(self):
        # Button grid frame
        grid = tk.Frame(self, bg=DARK_BG)
        grid.place(x=0, y=132, width=WINDOW_W, height=WINDOW_H-132)
        btn_specs = [
            # row 1
            [("%", self._percent), ("CE", self._clear_entry), ("C", self._clear_all), ("⌫", self._backspace)],
            # row 2
            [("½", self._half), ("x²", self._square), ("⅟ₓ", self._reciprocal), ("÷", lambda: self._op_press("/"))],
            # row 3
            [("7", lambda: self._num_press("7")), ("8", lambda: self._num_press("8")), ("9", lambda: self._num_press("9")), ("×", lambda: self._op_press("*"))],
            # row 4
            [("4", lambda: self._num_press("4")), ("5", lambda: self._num_press("5")), ("6", lambda: self._num_press("6")), ("-", lambda: self._op_press("-"))],
            # row 5
            [("1", lambda: self._num_press("1")), ("2", lambda: self._num_press("2")), ("3", lambda: self._num_press("3")), ("+", lambda: self._op_press("+"))],
            # row 6
            [("±", self._negate), ("0", lambda: self._num_press("0")), (".", lambda: self._num_press(".")), ("=", self._calculate)]
        ]
        self.button_refs = []
        for r, row in enumerate(btn_specs):
            for c, (txt, cmd) in enumerate(row):
                # Accent for '=' button
                if txt == "=":
                    bg, fg, ah = ACCENT_BG, ACCENT_FG, "#81e8ff"
                else:
                    bg, fg, ah = BTN_BG, BTN_FG, BTN_HOVER
                btn = tk.Button(
                    grid, text=txt, font=self.button_font, bg=bg, fg=fg,
                    bd=0, relief="flat", activebackground=ah, activeforeground=fg,
                    command=cmd, cursor="hand2"
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5, ipadx=0, ipady=0)
                btn.bind("<Enter>", lambda e, b=btn, h=ah: b.config(bg=h))
                btn.bind("<Leave>", lambda e, b=btn, d=bg: b.config(bg=d))
                self.button_refs.append(btn)
        # Make grid cells expand evenly
        for i in range(6): grid.rowconfigure(i, weight=1)
        for i in range(4): grid.columnconfigure(i, weight=1)

    # --- Calculator Logic ---
    def _num_press(self, char):
        if self.display_var.get() == "0" or self.display_var.get() == "Error":
            self.display_var.set(char)
        else:
            self.display_var.set(self.display_var.get() + char)

    def _op_press(self, op):
        val = self.display_var.get()
        if val[-1] in "+-*/":
            val = val[:-1]
        self.display_var.set(val + op)

    def _calculate(self):
        expr = self.display_var.get().replace("×", "*").replace("÷", "/")
        try:
            # If expression ends with operator, remove it
            if expr[-1] in "+-*/":
                expr = expr[:-1]
            result = eval(expr)
            self.display_var.set(str(result))
        except Exception:
            self.display_var.set("Error")

    def _clear_entry(self):
        self.display_var.set("0")

    def _clear_all(self):
        self.display_var.set("0")

    def _backspace(self):
        val = self.display_var.get()
        if len(val) <= 1 or val == "Error":
            self.display_var.set("0")
        else:
            self.display_var.set(val[:-1])

    def _percent(self):
        try:
            val = float(self.display_var.get())
            self.display_var.set(str(val / 100))
        except Exception:
            self.display_var.set("Error")

    def _half(self):
        try:
            val = float(self.display_var.get())
            self.display_var.set(str(val / 2))
        except Exception:
            self.display_var.set("Error")

    def _square(self):
        try:
            val = float(self.display_var.get())
            self.display_var.set(str(val ** 2))
        except Exception:
            self.display_var.set("Error")

    def _reciprocal(self):
        try:
            val = float(self.display_var.get())
            if val == 0:
                raise ZeroDivisionError
            self.display_var.set(str(1 / val))
        except Exception:
            self.display_var.set("Error")

    def _negate(self):
        try:
            val = float(self.display_var.get())
            self.display_var.set(str(-val))
        except Exception:
            self.display_var.set("Error")

if __name__ == "__main__":
    ModernCalculator().mainloop()