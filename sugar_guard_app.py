import json
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

DATA_FILE = Path.home() / ".sugar_guard_data.json"


@dataclass
class CravingEntry:
    timestamp: str
    intensity: int
    trigger: str
    action: str
    note: str


class DataStore:
    def __init__(self, path: Path):
        self.path = path
        self.data = {
            "onboarding": {
                "name": "",
                "goal": "",
                "start_date": str(date.today()),
                "max_sweets_per_day": 1,
            },
            "daily": {},
            "cravings": [],
            "wins": [],
        }
        self.load()

    def load(self):
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                pass

    def save(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_today(self):
        key = str(date.today())
        if key not in self.data["daily"]:
            self.data["daily"][key] = {
                "meals_done": 0,
                "water_glasses": 0,
                "sleep_hours": 7,
                "stress": 5,
                "sweets_portions": 0,
                "movement_minutes": 0,
                "notes": "",
            }
        return self.data["daily"][key]


class SugarGuardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sugar Guard — plan na wilczy głód i cukier")
        self.geometry("980x720")
        self.store = DataStore(DATA_FILE)
        self.urge_remaining = 0

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.header_var = tk.StringVar()
        self.stats_var = tk.StringVar()

        self.build_ui()
        self.refresh_dashboard()

    def build_ui(self):
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="Sugar Guard", font=("Helvetica", 22, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(
            frame,
            text=(
                "Aplikacja wspierająca ograniczenie cukru przez mikro-nawyki, "
                "kontrolę głodu i szybkie procedury SOS"
            ),
        )
        subtitle.pack(anchor="w", pady=(2, 12))

        status = ttk.Frame(frame)
        status.pack(fill="x", pady=(0, 10))
        ttk.Label(status, textvariable=self.header_var, font=("Helvetica", 11, "bold")).pack(anchor="w")
        ttk.Label(status, textvariable=self.stats_var).pack(anchor="w")

        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both", expand=True)

        self.dashboard_tab = ttk.Frame(notebook, padding=12)
        self.sos_tab = ttk.Frame(notebook, padding=12)
        self.plan_tab = ttk.Frame(notebook, padding=12)
        self.history_tab = ttk.Frame(notebook, padding=12)

        notebook.add(self.dashboard_tab, text="Dziś")
        notebook.add(self.sos_tab, text="SOS głód")
        notebook.add(self.plan_tab, text="Plan")
        notebook.add(self.history_tab, text="Historia")

        self.build_dashboard_tab()
        self.build_sos_tab()
        self.build_plan_tab()
        self.build_history_tab()

    def build_dashboard_tab(self):
        today = self.store.get_today()

        left = ttk.LabelFrame(self.dashboard_tab, text="Dzienny check-in", padding=10)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.sleep_var = tk.IntVar(value=today["sleep_hours"])
        self.stress_var = tk.IntVar(value=today["stress"])
        self.meals_var = tk.IntVar(value=today["meals_done"])
        self.water_var = tk.IntVar(value=today["water_glasses"])
        self.sweets_var = tk.IntVar(value=today["sweets_portions"])
        self.move_var = tk.IntVar(value=today["movement_minutes"])
        self.note_var = tk.StringVar(value=today["notes"])

        self.add_spin(left, "Sen (h):", self.sleep_var, 0, 14)
        self.add_spin(left, "Stres (1-10):", self.stress_var, 1, 10)
        self.add_spin(left, "Posiłki zjedzone:", self.meals_var, 0, 8)
        self.add_spin(left, "Szklanki wody:", self.water_var, 0, 20)
        self.add_spin(left, "Porcje słodyczy:", self.sweets_var, 0, 10)
        self.add_spin(left, "Ruch (min):", self.move_var, 0, 240)

        ttk.Label(left, text="Notatka: wyzwalacze / co pomogło").pack(anchor="w", pady=(8, 2))
        ttk.Entry(left, textvariable=self.note_var).pack(fill="x")

        ttk.Button(left, text="Zapisz dzień", command=self.save_today).pack(anchor="w", pady=(10, 0))

        right = ttk.LabelFrame(self.dashboard_tab, text="Strategie skuteczności", padding=10)
        right.pack(side="left", fill="both", expand=True)

        strategies = [
            "1) Jedz co 3-4h: białko + błonnik + tłuszcz (stabilna glikemia).",
            "2) Gdy ciągnie do cukru: 500 ml wody + 10 przysiadów + oddech 4-7-8.",
            "3) Zasada 10 minut: odłóż decyzję i obserwuj falę głodu.",
            "4) Usuwaj ekspozycję: słodycze poza domem/polem widzenia.",
            "5) Miej zamienniki: jogurt naturalny + owoce, orzechy, gorzka czekolada.",
            "6) Sen < 7h zwiększa apetyt — priorytet snu to priorytet kontroli łaknienia.",
        ]
        for s in strategies:
            ttk.Label(right, text=f"• {s}", wraplength=380, justify="left").pack(anchor="w", pady=2)

    def build_sos_tab(self):
        info = (
            "Tryb kryzysowy na wilczy głód: zapisujesz impuls i uruchamiasz protokół "
            "odroczenia. Celem jest przerwanie automatu 'bodziec → cukier'."
        )
        ttk.Label(self.sos_tab, text=info, wraplength=800, justify="left").pack(anchor="w", pady=(0, 10))

        form = ttk.Frame(self.sos_tab)
        form.pack(fill="x")

        self.intensity_var = tk.IntVar(value=7)
        self.trigger_var = tk.StringVar(value="Zmęczenie")
        self.action_var = tk.StringVar(value="Woda + 10 min spaceru")
        self.craving_note_var = tk.StringVar()
        self.timer_var = tk.StringVar(value="Timer SOS: gotowy")

        self.add_spin(form, "Siła głodu (1-10):", self.intensity_var, 1, 10)

        ttk.Label(form, text="Wyzwalacz").pack(anchor="w", pady=(6, 2))
        trigger_combo = ttk.Combobox(
            form,
            textvariable=self.trigger_var,
            values=["Zmęczenie", "Stres", "Nuda", "Po pracy", "Spotkanie towarzyskie", "Inny"],
            state="readonly",
        )
        trigger_combo.pack(anchor="w")

        ttk.Label(form, text="Akcja zastępcza").pack(anchor="w", pady=(6, 2))
        action_combo = ttk.Combobox(
            form,
            textvariable=self.action_var,
            values=[
                "Woda + 10 min spaceru",
                "Herbata + 5 min oddechu",
                "Jogurt naturalny + cynamon",
                "20 przysiadów + prysznic",
                "Telefon do bliskiej osoby",
            ],
            state="readonly",
            width=32,
        )
        action_combo.pack(anchor="w")

        ttk.Label(form, text="Krótka notatka").pack(anchor="w", pady=(6, 2))
        ttk.Entry(form, textvariable=self.craving_note_var, width=50).pack(anchor="w")

        buttons = ttk.Frame(form)
        buttons.pack(anchor="w", pady=(10, 4))
        ttk.Button(buttons, text="Zapisz impuls", command=self.log_craving).pack(side="left", padx=(0, 6))
        ttk.Button(buttons, text="Start SOS 10 min", command=self.start_urge_timer).pack(side="left")

        ttk.Label(form, textvariable=self.timer_var, font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(8, 2))
        ttk.Label(
            form,
            text="Protokół: 1) oddychaj 4-7-8, 2) wypij wodę, 3) zmień otoczenie, 4) wróć do decyzji po timerze.",
            wraplength=800,
        ).pack(anchor="w")

    def build_plan_tab(self):
        ob = self.store.data["onboarding"]

        container = ttk.LabelFrame(self.plan_tab, text="Plan osobisty", padding=10)
        container.pack(fill="x", pady=(0, 10))

        self.name_var = tk.StringVar(value=ob.get("name", ""))
        self.goal_var = tk.StringVar(value=ob.get("goal", "Chcę ograniczyć cukier i napady głodu"))
        self.max_sweets_var = tk.IntVar(value=ob.get("max_sweets_per_day", 1))

        ttk.Label(container, text="Imię").pack(anchor="w")
        ttk.Entry(container, textvariable=self.name_var).pack(anchor="w", fill="x")

        ttk.Label(container, text="Cel (konkretny)").pack(anchor="w", pady=(6, 0))
        ttk.Entry(container, textvariable=self.goal_var).pack(anchor="w", fill="x")

        self.add_spin(container, "Maks porcji słodyczy/dzień", self.max_sweets_var, 0, 5)

        ttk.Button(container, text="Zapisz plan", command=self.save_plan).pack(anchor="w", pady=(10, 0))

        habits = ttk.LabelFrame(self.plan_tab, text="Nawyki o najwyższym wpływie", padding=10)
        habits.pack(fill="both", expand=True)

        checklist_text = (
            "☐ Stałe pory posiłków (3-4 główne)",
            "☐ Białko w każdym posiłku (jaja, ryby, strączki, nabiał)",
            "☐ Min. 25 g błonnika dziennie",
            "☐ 7-8h snu",
            "☐ 30 min ruchu",
            "☐ Słodycze tylko po pełnym posiłku, nigdy na pusty żołądek",
            "☐ Plan awaryjny na wieczór: herbata + książka + prysznic",
        )
        for line in checklist_text:
            ttk.Label(habits, text=line).pack(anchor="w", pady=2)

    def build_history_tab(self):
        self.history_box = tk.Text(self.history_tab, height=30, wrap="word")
        self.history_box.pack(fill="both", expand=True)
        ttk.Button(self.history_tab, text="Odśwież historię", command=self.refresh_history).pack(anchor="w", pady=(8, 0))
        self.refresh_history()

    def add_spin(self, parent, label, variable, minv, maxv):
        row = ttk.Frame(parent)
        row.pack(anchor="w", pady=2)
        ttk.Label(row, text=label, width=26).pack(side="left")
        ttk.Spinbox(row, from_=minv, to=maxv, textvariable=variable, width=6).pack(side="left")

    def save_today(self):
        today = self.store.get_today()
        today.update(
            {
                "sleep_hours": self.sleep_var.get(),
                "stress": self.stress_var.get(),
                "meals_done": self.meals_var.get(),
                "water_glasses": self.water_var.get(),
                "sweets_portions": self.sweets_var.get(),
                "movement_minutes": self.move_var.get(),
                "notes": self.note_var.get().strip(),
            }
        )

        if today["sweets_portions"] <= self.store.data["onboarding"].get("max_sweets_per_day", 1):
            self.store.data["wins"].append(f"{date.today()}: Cel słodyczy utrzymany ✅")

        self.store.save()
        self.refresh_dashboard()
        self.refresh_history()
        messagebox.showinfo("Zapisano", "Dzień został zapisany.")

    def save_plan(self):
        self.store.data["onboarding"].update(
            {
                "name": self.name_var.get().strip(),
                "goal": self.goal_var.get().strip(),
                "max_sweets_per_day": self.max_sweets_var.get(),
            }
        )
        self.store.save()
        self.refresh_dashboard()
        messagebox.showinfo("Plan", "Plan został zapisany.")

    def log_craving(self):
        entry = CravingEntry(
            timestamp=datetime.now().isoformat(timespec="minutes"),
            intensity=self.intensity_var.get(),
            trigger=self.trigger_var.get(),
            action=self.action_var.get(),
            note=self.craving_note_var.get().strip(),
        )
        self.store.data["cravings"].append(asdict(entry))
        self.store.save()
        self.refresh_history()
        messagebox.showinfo("Zapis", "Impuls zapisany. Teraz uruchom 10-minutowe SOS.")

    def start_urge_timer(self):
        self.urge_remaining = 10 * 60
        self.tick_timer()

    def tick_timer(self):
        if self.urge_remaining <= 0:
            self.timer_var.set("Timer SOS: fala minęła. Zdecyduj świadomie.")
            self.bell()
            return

        minutes, seconds = divmod(self.urge_remaining, 60)
        self.timer_var.set(f"Timer SOS: {minutes:02d}:{seconds:02d}")
        self.urge_remaining -= 1
        self.after(1000, self.tick_timer)

    def calculate_streak(self):
        days = sorted(self.store.data["daily"].keys())
        streak = 0
        max_sweets = self.store.data["onboarding"].get("max_sweets_per_day", 1)
        d = date.today()

        while str(d) in days and self.store.data["daily"][str(d)]["sweets_portions"] <= max_sweets:
            streak += 1
            d = d - timedelta(days=1)

        return streak

    def refresh_dashboard(self):
        ob = self.store.data["onboarding"]
        today = self.store.get_today()
        streak = self.calculate_streak()

        name = ob.get("name") or "Hej"
        goal = ob.get("goal") or "ograniczamy cukier"
        self.header_var.set(f"{name}! Cel: {goal}")

        stat = (
            f"Dziś: słodycze {today['sweets_portions']}/{ob.get('max_sweets_per_day', 1)} | "
            f"woda {today['water_glasses']} szkl. | ruch {today['movement_minutes']} min | "
            f"seria dni w limicie: {streak}"
        )
        self.stats_var.set(stat)

    def refresh_history(self):
        self.history_box.delete("1.0", tk.END)
        lines = ["=== Historia impulsów ===\n"]

        cravings = self.store.data["cravings"][-20:]
        if not cravings:
            lines.append("Brak wpisów.\n")
        else:
            for item in cravings:
                lines.append(
                    f"{item['timestamp']} | siła {item['intensity']}/10 | {item['trigger']} | "
                    f"akcja: {item['action']} | notatka: {item['note']}\n"
                )

        lines.append("\n=== Wygrane dni ===\n")
        wins = self.store.data["wins"][-20:]
        if not wins:
            lines.append("Jeszcze bez wygranych wpisów.\n")
        else:
            lines.extend(f"{w}\n" for w in wins)

        self.history_box.insert(tk.END, "".join(lines))


if __name__ == "__main__":
    app = SugarGuardApp()
    app.mainloop()
