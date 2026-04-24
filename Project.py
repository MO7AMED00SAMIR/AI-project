import tkinter as tk
from tkinter import messagebox, ttk
import collections
import random
import math

WORD_LIST = [
    "apple","about","above","actor","admin","again","agree","animal","answer",
    "banana","basic","beauty","because","before","better","between","bottle",
    "camera","carbon","center","chance","change","charge","choice","client",
    "computer","control","create","culture","current",
    "data","design","device","digital","doctor","driver","during",
    "effect","engine","enough","example","expert",
    "family","feature","future",
    "garden","global","ground",
    "health","history","human",
    "image","impact","inside","island",
    "language","letter","level","little",
    "machine","market","memory","method","mobile","modern",
    "network","number",
    "object","office","option","output",
    "people","person","player","policy","power","program","project","python",
    "quality","question",
    "result","reason","record","report","resource",
    "science","server","simple","system",
    "teacher","theory","travel","training",
    "update","user","useful",
    "value","vision",
    "window","worker","world"
]

# ─── Colors ─────────────────────────────────────────────────────
BG_DARK     = "#0d1117"
BG_CARD     = "#161b22"
BG_PANEL    = "#1c2230"
ACCENT      = "#58a6ff"
ACCENT2     = "#3fb950"
DANGER      = "#f85149"
WARNING     = "#d29922"
TEXT_MAIN   = "#e6edf3"
TEXT_DIM    = "#8b949e"
BORDER      = "#30363d"


class HangmanAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman AI  •  Smart Edition")
        self.root.geometry("680x780")
        self.root.resizable(True, True)
        self.root.minsize(680, 780)
        self.root.configure(bg=BG_DARK)

        self.mode         = None
        self.word         = ""
        self.pattern      = []
        self.guessed_letters = set()
        self.wrong_letters   = set()
        self.possible_words  = []
        self.used_words      = set()
        self.attempts        = 6
        self.game_active     = False

        self._build_styles()
        self.start_frame = tk.Frame(root, bg=BG_DARK)
        self.game_frame  = tk.Frame(root, bg=BG_DARK)
        self.start_frame.pack(fill="both", expand=True)

        self._build_start_screen()
        self._build_game_screen()

    # ═══════════════════════════════════════════════════
    #  STYLES
    # ═══════════════════════════════════════════════════
    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame",  background=BG_CARD,  relief="flat")
        style.configure("Panel.TFrame", background=BG_PANEL, relief="flat")

        # Primary button
        style.configure("Primary.TButton",
            background=ACCENT, foreground="#0d1117",
            font=("Consolas", 11, "bold"),
            padding=(18, 10), relief="flat", borderwidth=0)
        style.map("Primary.TButton",
            background=[("active", "#79c0ff"), ("disabled", "#21262d")],
            foreground=[("disabled", TEXT_DIM)])

        # Success button
        style.configure("Success.TButton",
            background=ACCENT2, foreground="#0d1117",
            font=("Consolas", 11, "bold"),
            padding=(18, 10), relief="flat", borderwidth=0)
        style.map("Success.TButton",
            background=[("active", "#56d364"), ("disabled", "#21262d")],
            foreground=[("disabled", TEXT_DIM)])

        # Danger button
        style.configure("Danger.TButton",
            background=DANGER, foreground="#0d1117",
            font=("Consolas", 11, "bold"),
            padding=(18, 10), relief="flat", borderwidth=0)
        style.map("Danger.TButton",
            background=[("active", "#ff6e6e")])

        # Ghost button
        style.configure("Ghost.TButton",
            background=BG_PANEL, foreground=TEXT_DIM,
            font=("Consolas", 10),
            padding=(14, 8), relief="flat", borderwidth=0)
        style.map("Ghost.TButton",
            background=[("active", BORDER)],
            foreground=[("active", TEXT_MAIN)])

    # ═══════════════════════════════════════════════════
    #  START SCREEN
    # ═══════════════════════════════════════════════════
    def _build_start_screen(self):
        f = self.start_frame

        # Top spacer
        tk.Frame(f, bg=BG_DARK, height=60).pack()

        # Logo area
        logo_frame = tk.Frame(f, bg=BG_DARK)
        logo_frame.pack()

        tk.Label(logo_frame, text="⬡", font=("Arial", 48),
                 fg=ACCENT, bg=BG_DARK).pack()
        tk.Label(logo_frame, text="HANGMAN AI",
                 font=("Consolas", 32, "bold"),
                 fg=TEXT_MAIN, bg=BG_DARK).pack()
        tk.Label(logo_frame, text="Smart Letter-Guessing Engine",
                 font=("Consolas", 12),
                 fg=TEXT_DIM, bg=BG_DARK).pack(pady=(4, 0))

        tk.Frame(f, bg=BORDER, height=1, width=400).pack(pady=40)

        # Mode cards
        cards_row = tk.Frame(f, bg=BG_DARK)
        cards_row.pack(pady=10)

        self._mode_card(cards_row,
            icon="🤖", title="AI Guess Mode",
            desc="Enter a word — the AI\nwill try to guess it.",
            cmd=self.start_ai_mode, col=0)

        self._mode_card(cards_row,
            icon="🧑", title="User Guess Mode",
            desc="A random word is chosen —\nyou guess the letters.",
            cmd=self.start_user_mode, col=1)

        tk.Frame(f, bg=BORDER, height=1, width=400).pack(pady=40)
        tk.Label(f, text="Built with Python  •  Tkinter",
                 font=("Consolas", 9),
                 fg=TEXT_DIM, bg=BG_DARK).pack()

    def _mode_card(self, parent, icon, title, desc, cmd, col):
        card = tk.Frame(parent, bg=BG_CARD,
                        highlightbackground=BORDER,
                        highlightthickness=1,
                        width=240, height=200)
        card.grid(row=0, column=col, padx=16)
        card.pack_propagate(False)

        tk.Label(card, text=icon, font=("Arial", 36),
                 bg=BG_CARD).pack(pady=(28, 4))
        tk.Label(card, text=title, font=("Consolas", 13, "bold"),
                 fg=TEXT_MAIN, bg=BG_CARD).pack()
        tk.Label(card, text=desc, font=("Consolas", 10),
                 fg=TEXT_DIM, bg=BG_CARD, justify="center").pack(pady=8)
        ttk.Button(card, text="Select", style="Primary.TButton",
                   command=cmd).pack(pady=(0, 18))

    # ═══════════════════════════════════════════════════
    #  GAME SCREEN
    # ═══════════════════════════════════════════════════
    def _build_game_screen(self):
        f = self.game_frame

        # ── Header bar ─────────────────────────────────
        header = tk.Frame(f, bg=BG_CARD, height=52,
                          highlightbackground=BORDER,
                          highlightthickness=1)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="⬡ HANGMAN AI",
                 font=("Consolas", 14, "bold"),
                 fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=12)

        ttk.Button(header, text="← Back",
                   style="Ghost.TButton",
                   command=self._go_back).pack(side="right", padx=12, pady=8)

        self.mode_badge = tk.Label(header, text="",
                                   font=("Consolas", 10, "bold"),
                                   fg=BG_DARK, bg=ACCENT,
                                   padx=10, pady=3)
        self.mode_badge.pack(side="right", padx=8, pady=14)

        # ── Main content ───────────────────────────────
        content = tk.Frame(f, bg=BG_DARK)
        content.pack(fill="both", expand=True, padx=20, pady=16)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        # Left panel: hangman drawing + status
        left = tk.Frame(content, bg=BG_DARK)
        left.pack(side="left", fill="y")

        # Canvas card
        canvas_card = tk.Frame(left, bg=BG_CARD,
                               highlightbackground=BORDER,
                               highlightthickness=1)
        canvas_card.pack()

        self.canvas = tk.Canvas(canvas_card, width=220, height=240,
                                bg=BG_CARD, highlightthickness=0)
        self.canvas.pack(padx=16, pady=16)

        # Attempts indicator
        att_frame = tk.Frame(left, bg=BG_DARK)
        att_frame.pack(fill="x", pady=(12, 0))

        tk.Label(att_frame, text="ATTEMPTS LEFT",
                 font=("Consolas", 9), fg=TEXT_DIM, bg=BG_DARK).pack()

        self.attempts_row = tk.Frame(att_frame, bg=BG_DARK)
        self.attempts_row.pack(pady=4)

        self.heart_labels = []
        for i in range(6):
            lbl = tk.Label(self.attempts_row, text="♥",
                           font=("Arial", 18),
                           fg=DANGER, bg=BG_DARK)
            lbl.grid(row=0, column=i, padx=2)
            self.heart_labels.append(lbl)

        # Word pattern
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=16)

        self.word_label = tk.Label(left, text="",
                                   font=("Consolas", 26, "bold"),
                                   fg=ACCENT, bg=BG_DARK)
        self.word_label.pack()

        self.word_hint = tk.Label(left, text="",
                                  font=("Consolas", 10),
                                  fg=TEXT_DIM, bg=BG_DARK)
        self.word_hint.pack(pady=(4, 0))

        # Right panel: input + keyboard + log
        right = tk.Frame(content, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True, padx=(20, 0))

        # Input area
        input_card = tk.Frame(right, bg=BG_CARD,
                              highlightbackground=BORDER,
                              highlightthickness=1)
        input_card.pack(fill="x")

        tk.Label(input_card, text="INPUT",
                 font=("Consolas", 9, "bold"),
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=14, pady=(10, 2))

        self.word_entry = tk.Entry(input_card,
            font=("Consolas", 13), justify="center",
            bg=BG_PANEL, fg=TEXT_MAIN,
            insertbackground=ACCENT,
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT)
        self.word_entry.pack(fill="x", padx=14, pady=(0, 8), ipady=7)
        self.word_entry.insert(0, "Type your word here…")
        self.word_entry.bind("<FocusIn>",  self._clear_placeholder)
        self.word_entry.bind("<FocusOut>", self._restore_placeholder)

        self.guess_entry = tk.Entry(input_card,
            font=("Consolas", 13), justify="center",
            bg=BG_PANEL, fg=TEXT_MAIN,
            insertbackground=ACCENT,
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT)
        self.guess_entry.pack(fill="x", padx=14, pady=(0, 10), ipady=7)
        self.guess_entry.bind("<Return>", lambda e: self.user_guess())

        btn_row = tk.Frame(input_card, bg=BG_CARD)
        btn_row.pack(fill="x", padx=14, pady=(0, 14))

        self.start_btn = ttk.Button(btn_row, text="▶ Start",
            style="Success.TButton", command=self.start_game)
        self.start_btn.pack(side="left", padx=(0, 6))

        self.next_btn = ttk.Button(btn_row, text="⚡ AI Guess",
            style="Primary.TButton",
            command=self.next_guess, state="disabled")
        self.next_btn.pack(side="left", padx=(0, 6))

        self.guess_btn = ttk.Button(btn_row, text="✓ Guess",
            style="Primary.TButton",
            command=self.user_guess, state="disabled")
        self.guess_btn.pack(side="left", padx=(0, 6))

        ttk.Button(btn_row, text="↺ Restart",
            style="Ghost.TButton",
            command=self.restart_game).pack(side="right")

        # Virtual keyboard
        kb_card = tk.Frame(right, bg=BG_CARD,
                           highlightbackground=BORDER,
                           highlightthickness=1)
        kb_card.pack(fill="x", pady=(12, 0))

        tk.Label(kb_card, text="KEYBOARD",
                 font=("Consolas", 9, "bold"),
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=14, pady=(10, 4))

        self.key_buttons = {}
        kb_inner = tk.Frame(kb_card, bg=BG_CARD)
        kb_inner.pack(padx=10, pady=(0, 12))

        rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        for r, row in enumerate(rows):
            row_frame = tk.Frame(kb_inner, bg=BG_CARD)
            row_frame.pack(pady=2)
            for c, letter in enumerate(row):
                btn = tk.Button(row_frame, text=letter.upper(),
                    width=3, font=("Consolas", 9, "bold"),
                    bg=BG_PANEL, fg=TEXT_MAIN,
                    activebackground=ACCENT,
                    relief="flat", bd=0,
                    cursor="hand2",
                    command=lambda l=letter: self._kb_press(l))
                btn.grid(row=0, column=c, padx=2, pady=1, ipady=4)
                self.key_buttons[letter] = btn

        # Log
        log_card = tk.Frame(right, bg=BG_CARD,
                            highlightbackground=BORDER,
                            highlightthickness=1)
        log_card.pack(fill="both", expand=True, pady=(12, 0))

        tk.Label(log_card, text="GAME LOG",
                 font=("Consolas", 9, "bold"),
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=14, pady=(10, 4))

        self.log_box = tk.Text(log_card,
            height=6, bg=BG_PANEL, fg=TEXT_MAIN,
            font=("Consolas", 10),
            relief="flat", bd=0, state="disabled",
            insertbackground=ACCENT)
        self.log_box.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        self.log_box.tag_config("good",    foreground=ACCENT2)
        self.log_box.tag_config("bad",     foreground=DANGER)
        self.log_box.tag_config("info",    foreground=ACCENT)
        self.log_box.tag_config("neutral", foreground=TEXT_DIM)

        self._draw_base()

    # ═══════════════════════════════════════════════════
    #  NAV HELPERS
    # ═══════════════════════════════════════════════════
    def show_game(self):
        self.start_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def _go_back(self):
        self.restart_game()
        self.game_frame.pack_forget()
        self.start_frame.pack(fill="both", expand=True)

    def _clear_placeholder(self, e):
        if self.word_entry.get() == "Type your word here…":
            self.word_entry.delete(0, "end")
            self.word_entry.config(fg=TEXT_MAIN)

    def _restore_placeholder(self, e):
        if self.word_entry.get() == "":
            self.word_entry.insert(0, "Type your word here…")
            self.word_entry.config(fg=TEXT_DIM)

    # ═══════════════════════════════════════════════════
    #  MODES
    # ═══════════════════════════════════════════════════
    def start_ai_mode(self):
        self.mode = "AI"
        self.show_game()
        self.mode_badge.config(text=" 🤖 AI MODE ", bg=ACCENT)
        self.word_entry.config(state="normal")
        self.guess_entry.config(state="disabled")
        self.guess_btn.config(state="disabled")
        self._log("Enter a secret word, then press ▶ Start.", "info")

    def start_user_mode(self):
        self.mode = "USER"
        self.show_game()
        self.mode_badge.config(text=" 🧑 USER MODE ", bg=ACCENT2)
        self.word_entry.config(state="disabled")
        self._start_user_game()

    # ═══════════════════════════════════════════════════
    #  USER MODE
    # ═══════════════════════════════════════════════════
    def _get_random_word(self):
        available = [w for w in WORD_LIST if w not in self.used_words]
        if not available:
            self.used_words.clear()
            available = WORD_LIST
        word = random.choice(available)
        self.used_words.add(word)
        return word

    def _start_user_game(self):
        self.word = self._get_random_word()
        self.pattern = ["_"] * len(self.word)
        self.guessed_letters.clear()
        self.wrong_letters.clear()
        self.attempts = 6
        self.game_active = True
        self.guess_btn.config(state="normal")
        self._reset_keyboard()
        self._update_ui()
        self._draw_hangman()
        self._log(f"New word chosen — {len(self.word)} letters. Good luck!", "info")

    # ═══════════════════════════════════════════════════
    #  AI MODE
    # ═══════════════════════════════════════════════════
    def start_game(self):
        if self.mode != "AI":
            return

        raw = self.word_entry.get().strip().lower()
        if raw == "type your word here…" or not raw:
            messagebox.showerror("Error", "Please enter a word first.")
            return
        if not raw.isalpha():
            messagebox.showerror("Error", "Word must contain letters only.")
            return

        self.word = raw
        self.pattern = ["_"] * len(self.word)
        self.guessed_letters.clear()
        self.wrong_letters.clear()
        self.attempts = 6
        self.game_active = True

        # Build candidate list — words of same length
        self.possible_words = [w for w in WORD_LIST if len(w) == len(self.word)]

        self.word_entry.config(state="disabled")
        self.next_btn.config(state="normal")
        self._reset_keyboard()
        self._update_ui()
        self._draw_hangman()

        if self.possible_words:
            self._log(f"Word entered ({len(self.word)} letters). AI found {len(self.possible_words)} candidates.", "info")
        else:
            self._log(f"Word entered ({len(self.word)} letters). Not in my list — using frequency analysis.", "neutral")

    def _ai_pick_letter(self):
        """
        Smart letter-picking strategy:
        1. Filter possible_words by current pattern & wrong letters.
        2. If candidates exist → pick by frequency across them.
        3. If no candidates (word not in list) → use English letter
           frequency adjusted by pattern position hints.
        """
        # Global English letter frequency (fallback)
        ENGLISH_FREQ = "etaoinrshlducmfwgypbvkjxqz"

        unguessed = [c for c in ENGLISH_FREQ if c not in self.guessed_letters]
        if not unguessed:
            return None

        # Filter candidate words from list
        filtered = []
        for w in self.possible_words:
            match = True
            for i, ch in enumerate(self.pattern):
                if ch != "_" and w[i] != ch:
                    match = False
                    break
            if not match:
                continue
            if any(wl in w for wl in self.wrong_letters):
                continue
            filtered.append(w)

        self.possible_words = filtered

        if filtered:
            # Frequency count across candidates
            freq = collections.Counter()
            for w in filtered:
                for ch in set(w):
                    if ch not in self.guessed_letters:
                        freq[ch] += 1
            if freq:
                return freq.most_common(1)[0][0]

        # ── Fallback: word not in list ──────────────────────────
        # Use positional frequency: scan ALL words for letter
        # distribution at known blank positions
        blank_positions = [i for i, ch in enumerate(self.pattern) if ch == "_"]
        freq = collections.Counter()
        for w in WORD_LIST:
            if len(w) != len(self.word):
                continue
            # Must not contain any wrong letter
            if any(wl in w for wl in self.wrong_letters):
                continue
            # Must match known pattern positions
            ok = all(self.pattern[i] == "_" or w[i] == self.pattern[i]
                     for i in range(len(self.pattern)))
            if not ok:
                continue
            for pos in blank_positions:
                ch = w[pos]
                if ch not in self.guessed_letters:
                    freq[ch] += 1

        if freq:
            return freq.most_common(1)[0][0]

        # Last resort: pure English frequency
        return unguessed[0]

    def next_guess(self):
        if self.mode != "AI" or not self.game_active:
            return

        letter = self._ai_pick_letter()
        if letter is None:
            self._log("AI has no more letters to try.", "neutral")
            return

        self._process_guess(letter)

    # ═══════════════════════════════════════════════════
    #  USER GUESS
    # ═══════════════════════════════════════════════════
    def user_guess(self):
        if self.mode != "USER" or not self.game_active:
            return
        letter = self.guess_entry.get().strip().lower()
        self.guess_entry.delete(0, "end")
        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid", "Please enter a single letter.")
            return
        if letter in self.guessed_letters:
            self._log(f"'{letter.upper()}' already guessed!", "neutral")
            return
        self._process_guess(letter)

    def _kb_press(self, letter):
        if self.mode == "USER" and self.game_active:
            if letter in self.guessed_letters:
                return
            self._process_guess(letter)

    # ═══════════════════════════════════════════════════
    #  CORE LOGIC
    # ═══════════════════════════════════════════════════
    def _process_guess(self, letter):
        self.guessed_letters.add(letter)

        if letter in self.word:
            for i, ch in enumerate(self.word):
                if ch == letter:
                    self.pattern[i] = letter
            hits = self.word.count(letter)
            self._log(f"✔  '{letter.upper()}' found — {hits} occurrence(s)!", "good")
            self._color_key(letter, "good")
        else:
            self.wrong_letters.add(letter)
            self.attempts -= 1
            self._log(f"✘  '{letter.upper()}' not in word. {self.attempts} attempts left.", "bad")
            self._color_key(letter, "bad")

        self._update_ui()
        self._draw_hangman()
        self._check_end()

    def _check_end(self):
        if "_" not in self.pattern:
            self.game_active = False
            self.next_btn.config(state="disabled")
            self.guess_btn.config(state="disabled")
            self._log(f"🎉 Word revealed: {self.word.upper()}", "good")
            self.root.after(300, lambda: messagebox.showinfo(
                "🎉 You Win!", f"The word was: {self.word.upper()}\nCongratulations!"))
        elif self.attempts <= 0:
            self.game_active = False
            self.next_btn.config(state="disabled")
            self.guess_btn.config(state="disabled")
            self.word_label.config(text=self.word.upper(), fg=DANGER)
            self._log(f"💀 Game Over! Word was: {self.word.upper()}", "bad")
            self.root.after(300, lambda: messagebox.showinfo(
                "Game Over 💀", f"The word was: {self.word.upper()}\nBetter luck next time!"))

    # ═══════════════════════════════════════════════════
    #  RESTART
    # ═══════════════════════════════════════════════════
    def restart_game(self):
        self.word = ""
        self.pattern = []
        self.guessed_letters.clear()
        self.wrong_letters.clear()
        self.possible_words = []
        self.attempts = 6
        self.game_active = False

        self.word_entry.config(state="normal")
        self.word_entry.delete(0, "end")
        self.word_entry.insert(0, "Type your word here…")
        self.word_entry.config(fg=TEXT_DIM)

        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, "end")

        self.next_btn.config(state="disabled")
        self.guess_btn.config(state="disabled")

        self.word_label.config(text="? ? ? ? ?", fg=ACCENT)
        self.word_hint.config(text="")

        self._reset_keyboard()
        self._clear_log()

        # Reset hearts
        for lbl in self.heart_labels:
            lbl.config(fg=DANGER)

        self.canvas.delete("all")
        self._draw_base()

        if self.mode == "USER":
            self._start_user_game()

    # ═══════════════════════════════════════════════════
    #  UI UPDATE
    # ═══════════════════════════════════════════════════
    def _update_ui(self):
        # Word display
        display = "  ".join(ch if ch != "_" else "＿" for ch in self.pattern)
        self.word_label.config(text=display, fg=ACCENT)

        hint_parts = []
        known = sum(1 for c in self.pattern if c != "_")
        hint_parts.append(f"{known}/{len(self.pattern)} letters found")
        if self.wrong_letters:
            hint_parts.append(f"Wrong: {', '.join(sorted(self.wrong_letters)).upper()}")
        self.word_hint.config(text="  •  ".join(hint_parts))

        # Hearts
        for i, lbl in enumerate(self.heart_labels):
            lbl.config(fg=DANGER if i < self.attempts else TEXT_DIM)

    # ═══════════════════════════════════════════════════
    #  KEYBOARD
    # ═══════════════════════════════════════════════════
    def _reset_keyboard(self):
        for btn in self.key_buttons.values():
            btn.config(bg=BG_PANEL, fg=TEXT_MAIN, state="normal")

    def _color_key(self, letter, state):
        btn = self.key_buttons.get(letter)
        if btn:
            if state == "good":
                btn.config(bg=ACCENT2, fg=BG_DARK, state="disabled")
            else:
                btn.config(bg=DANGER,  fg=BG_DARK, state="disabled")

    # ═══════════════════════════════════════════════════
    #  LOG
    # ═══════════════════════════════════════════════════
    def _log(self, msg, tag="neutral"):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"  {msg}\n", tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def _clear_log(self):
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")

    # ═══════════════════════════════════════════════════
    #  HANGMAN DRAWING
    # ═══════════════════════════════════════════════════
    def _draw_base(self):
        c = self.canvas
        # Ground
        c.create_line(20, 220, 200, 220, fill=BORDER, width=3)
        # Pole
        c.create_line(60, 220, 60, 20,  fill=TEXT_DIM, width=3)
        # Top beam
        c.create_line(60, 20, 150, 20,  fill=TEXT_DIM, width=3)
        # Brace
        c.create_line(60, 50, 90, 20,   fill=TEXT_DIM, width=2)
        # Rope
        c.create_line(150, 20, 150, 48, fill=TEXT_DIM, width=2)

    def _draw_hangman(self):
        self.canvas.delete("all")
        self._draw_base()

        wrong = 6 - self.attempts
        color = DANGER if wrong == 6 else TEXT_MAIN

        if wrong >= 1:  # Head
            self.canvas.create_oval(132, 48, 168, 84,
                outline=color, width=2, fill="")
        if wrong >= 2:  # Body
            self.canvas.create_line(150, 84, 150, 148,
                fill=color, width=2)
        if wrong >= 3:  # Left arm
            self.canvas.create_line(150, 100, 120, 128,
                fill=color, width=2)
        if wrong >= 4:  # Right arm
            self.canvas.create_line(150, 100, 180, 128,
                fill=color, width=2)
        if wrong >= 5:  # Left leg
            self.canvas.create_line(150, 148, 120, 190,
                fill=color, width=2)
        if wrong == 6:  # Right leg — game over
            self.canvas.create_line(150, 148, 180, 190,
                fill=color, width=2)
            # X eyes
            self.canvas.create_line(140, 58, 147, 65, fill=DANGER, width=2)
            self.canvas.create_line(147, 58, 140, 65, fill=DANGER, width=2)
            self.canvas.create_line(153, 58, 160, 65, fill=DANGER, width=2)
            self.canvas.create_line(160, 58, 153, 65, fill=DANGER, width=2)


# ─── Run ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = HangmanAI(root)
    root.mainloop()