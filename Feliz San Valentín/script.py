import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import colorchooser, filedialog
import math
import random
import time
import threading
from PIL import ImageGrab  
import speech_recognition as sr  

# Intentamos importar pygame para la música interactiva
try:
    import pygame
    pygame.mixer.init()
    MUSIC_AVAILABLE = True
except ImportError:
    MUSIC_AVAILABLE = False

# Función para analizar la música y extraer tiempos de beat usando librosa
def analyze_audio_beats(audio_file):
    try:
        import librosa
    except ImportError as e:
        print("librosa no está instalado.")
        return [], 0
    try:
        y, sr = librosa.load(audio_file)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        return beat_times, tempo
    except Exception as e:
        print("Error al analizar audio:", e)
        return [], 0

def generate_heart_points(scale, center_x, center_y, num_points=400):
    """Genera los puntos (x, y) para dibujar un corazón usando ecuaciones paramétricas."""
    points = []
    for i in range(num_points):
        t = math.pi * 2 * i / num_points
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        x *= scale
        y *= -scale  
        points.extend([center_x + x, center_y + y])
    return points

class SanValentinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("¡Feliz San Valentín!")
        self.canvas_width = 800
        self.canvas_height = 600
        self.root.resizable(False, False)

        # Variable para llevar el registro del último múltiplo de 10 felicitado.
        self.last_congrats_multiple = 0
        # Flag para mostrar el mensaje final cuando termine la música.
        self.music_finished_shown = False

        # Lista de mensajes de alago
        self.congrats_messages = [
            "¡Eres increíble!",
            "¡Sigue así, eres una crack!",
            "¡Lo haces genial!",
            "¡Eres muy buena en todo lo que haces!",
            "¡Tu talento es asombroso!"
        ]

        # Configuración de estilos con ttk para lograr botones modernos y elegantes
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        self.style.configure("TButton",
                             font=("Helvetica", 12, "bold"),
                             foreground="white",
                             background="#0078D7",
                             padding=6)
        self.style.map("TButton", background=[("active", "#005999")])
        self.style.configure("TLabel", font=("Helvetica", 12))

        # --- CONTROL PRINCIPAL ---
        control_frame = ttk.Frame(root)
        control_frame.pack(pady=5)

        ttk.Label(control_frame, text="Mensaje:").grid(row=0, column=0, padx=5, sticky="e")
        self.message_var = tk.StringVar(value="¡Feliz San Valentín!")
        self.entry = ttk.Entry(control_frame, textvariable=self.message_var, font=("Helvetica", 14), width=30)
        self.entry.grid(row=0, column=1, padx=5)
        self.msg_button = ttk.Button(control_frame, text="Actualizar Mensaje", command=self.start_text_animation)
        self.msg_button.grid(row=0, column=2, padx=5)

        # --- CONTROLES AVANZADOS DEL MENSAJE ---
        adv_frame = ttk.Frame(root)
        adv_frame.pack(pady=5)

        ttk.Label(adv_frame, text="Fuente:").grid(row=0, column=0, padx=5, sticky="e")
        self.font_options = ["Helvetica", "Arial", "Times", "Courier"]
        self.selected_font = tk.StringVar(value=self.font_options[0])
        tk.OptionMenu(adv_frame, self.selected_font, *self.font_options).grid(row=0, column=1, padx=5)

        ttk.Label(adv_frame, text="Tamaño:").grid(row=0, column=2, padx=5, sticky="e")
        self.font_size = tk.IntVar(value=30)
        tk.Spinbox(adv_frame, from_=12, to=72, textvariable=self.font_size, width=5).grid(row=0, column=3, padx=5)

        ttk.Label(adv_frame, text="Color:").grid(row=0, column=4, padx=5, sticky="e")
        self.message_color = "#ffffff"
        ttk.Button(adv_frame, text="Elegir color", command=self.choose_color).grid(row=0, column=5, padx=5)

        ttk.Label(adv_frame, text="Predefinido:").grid(row=0, column=6, padx=5, sticky="e")
        self.predef_messages = ["¡Te amo!", "Eres mi sol", "Contigo todo es mejor", "Mi corazón es tuyo"]
        self.selected_predef = tk.StringVar(value=self.predef_messages[0])
        tk.OptionMenu(adv_frame, self.selected_predef, *self.predef_messages, command=self.use_predef_message).grid(row=0, column=7, padx=5)

        # --- CONTROLES DE MÚSICA ---
        self.music_frame = ttk.Frame(root)
        self.music_frame.pack(pady=5)
        if MUSIC_AVAILABLE:
            ttk.Button(self.music_frame, text="Play", command=self.music_play).grid(row=0, column=0, padx=3)
            ttk.Button(self.music_frame, text="Pause", command=self.music_pause).grid(row=0, column=1, padx=3)
            ttk.Button(self.music_frame, text="Resume", command=self.music_resume).grid(row=0, column=2, padx=3)
            ttk.Button(self.music_frame, text="Stop", command=self.music_stop).grid(row=0, column=3, padx=3)
            ttk.Button(self.music_frame, text="Vol +", command=self.volume_up).grid(row=0, column=4, padx=3)
            ttk.Button(self.music_frame, text="Vol -", command=self.volume_down).grid(row=0, column=5, padx=3)
        else:
            ttk.Label(self.music_frame, text="Música no disponible (pygame no instalado)").pack()

        # --- CONTROLES DE MICROFONO ---
        mic_frame = ttk.Frame(root)
        mic_frame.pack(pady=5)
        ttk.Button(mic_frame, text="Activar Micrófono", command=self.start_microphone_recognition).pack()

        self.score = 0
        self.score_label = ttk.Label(root, text=f"Puntaje: {self.score}", font=("Helvetica", 14))
        self.score_label.pack(pady=5)

        # --- CANVAS PRINCIPAL ---
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Botón para capturar pantalla
        screenshot_frame = ttk.Frame(root)
        screenshot_frame.pack(pady=5)
        ttk.Button(screenshot_frame, text="Capturar Pantalla", command=self.capture_screenshot).pack()

        # Vinculación de eventos
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.root.bind("<space>", self.launch_fireworks)
        self.root.bind("r", self.restart_animation)
        self.root.bind("<Control-Shift-s>", self.show_surprise_message)

        # Animación del fondo
        self.bg_start_time = time.time()
        self.animate_background()

        # Calcular los puntos del corazón y comenzar su animación
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        self.base_scale = 10
        self.full_points = generate_heart_points(self.base_scale, self.center_x, self.center_y, num_points=400)
        # Crear la línea del corazón con un índice inicial de 4 para que tenga al menos dos puntos
        self.heart_line = self.canvas.create_line(0, 0, 0, 0, fill="red", width=2, smooth=True)
        self.animate_heart_drawing(4)

        # Inicialmente, el mensaje no está en pantalla
        self.text_item = None

        self.falling_objects = []
        self.animate_falling_objects()
        self.animate_extra_particles()

        self.start_flowers()
        self.animate_beat()

        # --- NUEVAS ANIMACIONES ADICIONALES ---
        self.animate_confetti()
        self.animate_petals()

        # Si la música está disponible, cargar y reproducir la canción SIN loop.
        if MUSIC_AVAILABLE:
            self.music_file = "audio/BIRDS OD A FEARHER.mp3"
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.set_volume(0.5)
                # Reproducir la canción UNA VEZ para que eventualmente finalice
                pygame.mixer.music.play()
                try:
                    self.beat_times, self.tempo = analyze_audio_beats(self.music_file)
                    print("Tempo detectado:", self.tempo)
                except Exception as e:
                    print("Error al analizar audio:", e)
                    self.beat_times = []
            except Exception as e:
                print("Error al cargar música:", e)
            # Comenzar a comprobar si la música terminó
            self.check_music_finished()

    # ---------- MÉTODOS PARA COMPROBAR FINAL DE MÚSICA ----------
    def check_music_finished(self):
        if MUSIC_AVAILABLE:
            if not pygame.mixer.music.get_busy() and not self.music_finished_shown:
                self.music_finished_shown = True
                self.display_final_message()
        self.root.after(1000, self.check_music_finished)

    def display_final_message(self):
        final_msg = ("Gracias por compartir este momento mágico.")
        final_text = self.canvas.create_text(self.center_x, self.center_y,
                                              text=final_msg,
                                              fill="gold",
                                              font=("Helvetica", 26, "bold"),
                                              justify="center")
        self.root.after(5000, lambda: self.canvas.delete(final_text))

    # ---------- PERSONALIZACIÓN DEL MENSAJE ----------
    def choose_color(self):
        color_tuple = colorchooser.askcolor(title="Elige un color")
        if color_tuple[1]:
            self.message_color = color_tuple[1]

    def use_predef_message(self, value):
        self.message_var.set(value)

    def start_text_animation(self):
        if self.text_item is not None:
            self.canvas.delete(self.text_item)
        msg = self.message_var.get()
        font_family = self.selected_font.get()
        size = self.font_size.get()
        self.custom_font = (font_family, size, "bold")
        self.text_item = self.canvas.create_text(self.center_x, self.center_y,
                                                  text="",
                                                  fill=self.message_color,
                                                  font=self.custom_font)
        self.typewriter_text(0)

    def typewriter_text(self, index):
        if index <= len(self.message_var.get()):
            current_text = self.message_var.get()[:index]
            self.canvas.itemconfig(self.text_item, text=current_text)
            self.root.after(100, self.typewriter_text, index + 1)
        else:
            self.root.after(2000, self.delete_text_effect)

    def delete_text_effect(self):
        current_text = self.canvas.itemcget(self.text_item, "text")
        if current_text:
            new_text = current_text[:-1]
            self.canvas.itemconfig(self.text_item, text=new_text)
            self.root.after(100, self.delete_text_effect)
        else:
            self.canvas.delete(self.text_item)
            self.text_item = None

    # ---------- ANIMACIONES PRINCIPALES ----------
    def animate_background(self):
        t = time.time() - self.bg_start_time
        r = int((math.sin(t) * 0.5 + 0.5) * 120)
        g = int((math.sin(t + 2*math.pi/3) * 0.5 + 0.5) * 120)
        b = int((math.sin(t + 4*math.pi/3) * 0.5 + 0.5) * 120)
        color = f'#{r:02x}{g:02x}{b:02x}'
        self.canvas.config(bg=color)
        self.root.after(50, self.animate_background)

    def animate_heart_drawing(self, index):
        if index <= len(self.full_points):
            current_points = self.full_points[:index]
            self.canvas.coords(self.heart_line, *current_points)
            self.root.after(20, self.animate_heart_drawing, index + 2)
        else:
            self.canvas.delete(self.heart_line)
            self.heart = self.canvas.create_polygon(self.full_points,
                                                    fill="red",
                                                    outline="pink",
                                                    width=2)
            self.animate_heart_fill()
            self.start_sparkles()

    def animate_heart_fill(self):
        bbox = self.canvas.bbox(self.heart)
        if not bbox:
            return
        x1, y1, x2, y2 = bbox
        cover = self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=self.canvas.cget("bg"),
                                             outline="")
        def move_cover():
            self.canvas.move(cover, 0, -5)
            _, cy1, _, _ = self.canvas.bbox(cover)
            if cy1 > y1:
                self.root.after(50, move_cover)
            else:
                self.canvas.delete(cover)
        move_cover()

    def start_sparkles(self):
        self.animate_sparkles()

    def animate_sparkles(self):
        num_points = len(self.full_points) // 2
        idx = random.randrange(num_points)
        x = self.full_points[idx * 2]
        y = self.full_points[idx * 2 + 1]
        size = random.randint(3, 6)
        sparkle = self.canvas.create_oval(x - size, y - size, x + size, y + size,
                                          fill="white", outline="")
        self.root.after(500, lambda: self.canvas.delete(sparkle))
        self.root.after(200, self.animate_sparkles)

    # ---------- FLORES EN LOS LATERALES ----------
    def start_flowers(self):
        self.schedule_next_flower()

    def schedule_next_flower(self):
        delay = random.randint(1500, 3000)
        self.root.after(delay, self.create_random_flower)

    def create_random_flower(self):
        side = random.choice(["left", "right"])
        x = random.randint(30, 150) if side == "left" else random.randint(self.canvas_width - 150, self.canvas_width - 30)
        y = random.randint(50, self.canvas_height - 50)
        self.draw_flower_gradually(x, y, petal_color="magenta",
                                   center_color="yellow",
                                   petal_radius=8,
                                   center_radius=4,
                                   num_petals=6)
        self.schedule_next_flower()

    def draw_flower_gradually(self, x, y, petal_color, center_color,
                               petal_radius, center_radius, num_petals,
                               current=0, petal_ids=None):
        if petal_ids is None:
            petal_ids = []
        if current < num_petals:
            angle = 2 * math.pi * current / num_petals
            petal_center_x = x + petal_radius * 2 * math.cos(angle)
            petal_center_y = y + petal_radius * 2 * math.sin(angle)
            petal_id = self.canvas.create_oval(petal_center_x - petal_radius,
                                                 petal_center_y - petal_radius,
                                                 petal_center_x + petal_radius,
                                                 petal_center_y + petal_radius,
                                                 fill=petal_color,
                                                 outline="")
            petal_ids.append(petal_id)
            self.root.after(200, self.draw_flower_gradually,
                             x, y, petal_color, center_color,
                             petal_radius, center_radius, num_petals,
                             current + 1, petal_ids)
        else:
            self.canvas.create_oval(x - center_radius, y - center_radius,
                                    x + center_radius, y + center_radius,
                                    fill=center_color,
                                    outline="")

    # ---------- OBJETOS QUE CAEN (CORAZONES / CONFETI) ----------
    def animate_falling_objects(self):
        if random.random() < 0.05:
            x = random.randint(20, self.canvas_width - 20)
            y = -20
            size = random.randint(12, 20)
            color = random.choice(["red", "magenta", "pink", "orange", "yellow"])
            obj = self.canvas.create_text(x, y, text="❤", fill=color, font=("Arial", size))
            speed = random.uniform(1, 3)
            self.falling_objects.append((obj, speed))
        for item in self.falling_objects.copy():
            obj, speed = item
            self.canvas.move(obj, 0, speed)
            coords = self.canvas.coords(obj)
            if coords and coords[1] > self.canvas_height + 20:
                self.canvas.delete(obj)
                self.falling_objects.remove(item)
        self.root.after(50, self.animate_falling_objects)

    # ---------- PARTÍCULAS EXTRA (CONFETI / PÉTALOS) ----------
    def animate_extra_particles(self):
        x = random.randint(0, self.canvas_width)
        y = random.randint(0, self.canvas_height)
        size = random.randint(2, 4)
        particle = self.canvas.create_oval(x - size, y - size, x + size, y + size,
                                           fill="white", outline="")
        self.root.after(300, lambda: self.canvas.delete(particle))
        self.root.after(100, self.animate_extra_particles)

    # ---------- NUEVAS ANIMACIONES: CONFETI EXTRA ----------
    def animate_confetti(self):
        if random.random() < 0.1:
            x = random.randint(0, self.canvas_width)
            y = -10
            size = random.randint(5, 15)
            color = random.choice(["red", "blue", "green", "yellow",
                                   "magenta", "cyan", "orange", "pink", "purple"])
            confetti = self.canvas.create_rectangle(x, y, x + size, y + size,
                                                    fill=color, outline="")
            self.animate_confetti_particle(confetti)
        self.root.after(50, self.animate_confetti)

    def animate_confetti_particle(self, particle):
        coords = self.canvas.coords(particle)
        if not coords:
            return
        x1, y1, x2, y2 = coords
        dx = random.randint(-2, 2)
        dy = random.randint(3, 6)
        self.canvas.move(particle, dx, dy)
        if y1 > self.canvas_height:
            self.canvas.delete(particle)
        else:
            self.root.after(50, self.animate_confetti_particle, particle)

    # ---------- NUEVAS ANIMACIONES: CASCADA DE PÉTALOS ----------
    def animate_petals(self):
        if random.random() < 0.05:
            x = random.randint(0, self.canvas_width)
            y = -10
            width = random.randint(8, 20)
            height = random.randint(4, 10)
            color = random.choice(["pink", "lightpink", "hotpink"])
            petal = self.canvas.create_oval(x, y, x + width, y + height,
                                            fill=color, outline="")
            self.animate_petal_particle(petal)
        self.root.after(150, self.animate_petals)

    def animate_petal_particle(self, petal):
        coords = self.canvas.coords(petal)
        if not coords:
            return
        x1, y1, x2, y2 = coords
        dx = random.randint(-2, 2)
        dy = random.randint(2, 5)
        self.canvas.move(petal, dx, dy)
        if y1 > self.canvas_height:
            self.canvas.delete(petal)
        else:
            self.root.after(50, self.animate_petal_particle, petal)

    # ---------- EFECTO LATIDO REACTIVO CON ANÁLISIS DE AUDIO ----------
    def animate_beat(self):
        t = time.time()
        beat_factor = 1 + 0.05 * math.sin(t * 6)
        new_scale = self.base_scale * beat_factor
        points = generate_heart_points(new_scale, self.center_x, self.center_y, num_points=400)
        if hasattr(self, "heart"):
            self.canvas.coords(self.heart, *points)
        else:
            self.canvas.coords(self.heart_line, *points)
        color_intensity = int((math.sin(t * 2) * 0.5 + 0.5) * 255)
        new_color = f'#{color_intensity:02x}0000'
        if hasattr(self, "heart"):
            self.canvas.itemconfig(self.heart, fill=new_color)
        else:
            self.canvas.itemconfig(self.heart_line, fill=new_color)
        if MUSIC_AVAILABLE and hasattr(self, "beat_times") and self.beat_times:
            current_music_time = pygame.mixer.music.get_pos() / 1000.0
            for beat in self.beat_times:
                if abs(beat - current_music_time) < 0.05:
                    if hasattr(self, "heart"):
                        self.canvas.itemconfig(self.heart, fill="white")
                    else:
                        self.canvas.itemconfig(self.heart_line, fill="white")
                    for _ in range(5):
                        size = random.randint(2, 4)
                        sparkle = self.canvas.create_oval(self.center_x - size, self.center_y - size,
                                                           self.center_x + size, self.center_y + size,
                                                           fill="yellow", outline="")
                        self.root.after(300, lambda s=sparkle: self.canvas.delete(s))
                    break
        self.root.after(100, self.animate_beat)

    # ---------- FUEGOS ARTIFICIALES ----------
    def launch_fireworks(self, event):
        x0 = event.x if event else self.center_x
        y0 = event.y if event else self.center_y
        num_particles = 30
        particles = []
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            dx = speed * math.cos(angle)
            dy = speed * math.sin(angle)
            size = random.randint(3, 6)
            color = random.choice(["red", "yellow", "magenta", "orange", "white"])
            p = self.canvas.create_oval(x0 - size, y0 - size, x0 + size, y0 + size,
                                         fill=color, outline="")
            particles.append((p, dx, dy, size))
        self.animate_firework_particles(particles, 0)

    def animate_firework_particles(self, particles, step):
        if step < 20:
            for (p, dx, dy, size) in particles:
                self.canvas.move(p, dx, dy)
            self.root.after(50, self.animate_firework_particles, particles, step + 1)
        else:
            for p, _, _, _ in particles:
                self.canvas.delete(p)

    # ---------- INTERACCIÓN DEL MOUSE Y TECLADO ----------
    def on_canvas_click(self, event):
        for _ in range(10):
            dx = random.randint(-20, 20)
            dy = random.randint(-20, 20)
            size = random.randint(3, 6)
            sparkle = self.canvas.create_oval(event.x + dx - size, event.y + dy - size,
                                               event.x + dx + size, event.y + dy + size,
                                               fill="white", outline="")
            self.root.after(500, lambda s=sparkle: self.canvas.delete(s))
        clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for obj, speed in self.falling_objects.copy():
            if obj in clicked_items:
                self.canvas.delete(obj)
                self.falling_objects.remove((obj, speed))
                self.score += 1
                self.score_label.config(text=f"Puntaje: {self.score}")
                if self.score != 0 and self.score % 10 == 0 and (self.score // 10) > self.last_congrats_multiple:
                    self.last_congrats_multiple = self.score // 10
                    self.show_congrats_message()

    def on_mouse_move(self, event):
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        size = random.randint(2, 4)
        particle = self.canvas.create_oval(event.x + dx - size, event.y + dy - size,
                                             event.x + dx + size, event.y + dy + size,
                                             fill="white", outline="")
        self.root.after(300, lambda: self.canvas.delete(particle))

    def restart_animation(self, event=None):
        self.score = 0
        self.last_congrats_multiple = 0
        self.score_label.config(text=f"Puntaje: {self.score}")
        for item in self.falling_objects.copy():
            self.canvas.delete(item[0])
            self.falling_objects.remove(item)
        print("Animación reiniciada.")

    def show_surprise_message(self, event=None):
        msg = "¡Eres increíble!"
        surprise_text = self.canvas.create_text(self.center_x, self.center_y - 100,
                                                  text=msg, fill="gold",
                                                  font=("Helvetica", 24, "bold"))
        self.root.after(2000, lambda: self.canvas.delete(surprise_text))

    def show_congrats_message(self):
        msg = random.choice(self.congrats_messages)
        congrats_text = self.canvas.create_text(self.center_x, self.center_y - 50,
                                                 text=msg, fill="green",
                                                 font=("Helvetica", 20, "bold"))
        self.root.after(3000, lambda: self.canvas.delete(congrats_text))

    # ---------- CAPTURA DE PANTALLA CON DIÁLOGO ----------
    def capture_screenshot(self):
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        bbox = (x, y, x + w, y + h)
        img = ImageGrab.grab(bbox=bbox)
        filename = filedialog.asksaveasfilename(
            title="Guardar captura",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All Files", "*.*")]
        )
        if filename:
            img.save(filename)
            print(f"Captura guardada en {filename}")

    # ---------- CONTROLES DE MÚSICA ----------
    def music_play(self):
        if MUSIC_AVAILABLE:
            try:
                # Reproducir la canción UNA VEZ para que eventualmente finalice
                pygame.mixer.music.play()
            except Exception as e:
                print("Error al reproducir música:", e)

    def music_pause(self):
        if MUSIC_AVAILABLE:
            pygame.mixer.music.pause()

    def music_resume(self):
        if MUSIC_AVAILABLE:
            pygame.mixer.music.unpause()

    def music_stop(self):
        if MUSIC_AVAILABLE:
            pygame.mixer.music.stop()

    def volume_up(self):
        if MUSIC_AVAILABLE:
            vol = pygame.mixer.music.get_volume()
            vol = min(vol + 0.1, 1.0)
            pygame.mixer.music.set_volume(vol)

    def volume_down(self):
        if MUSIC_AVAILABLE:
            vol = pygame.mixer.music.get_volume()
            vol = max(vol - 0.1, 0.0)
            pygame.mixer.music.set_volume(vol)

    # ---------- RECONOCIMIENTO DE VOZ CON MICROFONO ----------
    def start_microphone_recognition(self):
        threading.Thread(target=self.recognize_speech, daemon=True).start()

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Escuchando...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Texto reconocido:", text)
            self.message_var.set(text)
            self.start_text_animation()
        except sr.UnknownValueError:
            print("No se entendió lo que dijiste.")
            self.message_var.set("No se entendió lo que dijiste.")
            self.start_text_animation()
        except sr.RequestError as e:
            print("Error al conectar con el servicio de reconocimiento:", e)
            self.message_var.set("Error de conexión al servicio.")
            self.start_text_animation()

def main():
    root = tk.Tk()
    app = SanValentinApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
