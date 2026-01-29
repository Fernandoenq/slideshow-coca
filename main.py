import os
import random
import tkinter as tk
from PIL import Image, ImageTk
from screeninfo import get_monitors

# --- CONFIGURAÇÃO ---
CAMINHO_DA_PASTA = r'C:\Users\jrval\OneDrive\Documentos\apagar depois\1'
TEMPO_EXPOSICAO = 1000 
MONITOR_ALVO = 0  # 0 para o principal, 1 para o segundo, etc.

class SlideShow:
    def __init__(self, root, monitor_index):
        self.root = root
        self.root.title("SlideShow Oficial")
        
        # 1. Pega as coordenadas do monitor escolhido
        monitores = get_monitors()
        monitor = monitores[monitor_index] if monitor_index < len(monitores) else monitores[0]

        # 2. Posiciona a janela no monitor certo antes de meter o Full Screen
        self.largura = monitor.width
        self.altura = monitor.height
        self.root.geometry(f"{self.largura}x{self.altura}+{monitor.x}+{monitor.y}")

        # 3. O PULO DO GATO: Full Screen nativo (sem tirar o ícone da barra de tarefas)
        self.root.attributes('-fullscreen', True)
        
        # Se quiser sair do Full Screen mas deixar aberto, o Esc resolve:
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        
        self.root.configure(background='black')
        self.label = tk.Label(root, background='black')
        self.label.pack(expand=True, fill='both')

        self.mostrar_proxima()

    def obter_imagens(self):
        extensoes = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        if not os.path.exists(CAMINHO_DA_PASTA):
            return []
        return [os.path.join(CAMINHO_DA_PASTA, f) for f in os.listdir(CAMINHO_DA_PASTA) 
                if f.lower().endswith(extensoes)]

    def mostrar_proxima(self):
        fotos = self.obter_imagens()
        if fotos:
            foto_aleatoria = random.choice(fotos)
            try:
                img = Image.open(foto_aleatoria)
                # Redimensiona pra ficar na estica na tela
                img.thumbnail((self.largura, self.altura), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.label.config(image=self.photo)
            except:
                pass
        
        # O loop não para nunca, mesmo minimizado
        self.root.after(TEMPO_EXPOSICAO, self.mostrar_proxima)

if __name__ == "__main__":
    root = tk.Tk()
    app = SlideShow(root, MONITOR_ALVO)
    root.mainloop()