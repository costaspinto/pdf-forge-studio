import io, os, shutil, traceback
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinter import font as tkfont

try:
    import fitz
    from PIL import Image
except Exception as e:
    raise SystemExit(f"Missing dependency: {e}")

APP = "PDF Forge Studio"
VERSION = "2.1.1"
DEVELOPER = "Costas Pinto"

BASE = Path.home() / "Downloads" / "PDF_Forge_Studio"
OUTPUT = BASE / "Output"
BACKUPS = BASE / "Backups"
LOGS = BASE / "Logs"
for p in (OUTPUT, BACKUPS, LOGS):
    p.mkdir(parents=True, exist_ok=True)
LOG = LOGS / "pdf_forge.log"

def log_error():
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write("\n--- ERROR ---\n")
            f.write(traceback.format_exc())
    except Exception:
        pass

def unique_path(folder, filename):
    folder.mkdir(parents=True, exist_ok=True)
    p = folder / filename
    if not p.exists(): return p
    for i in range(1, 10000):
        p = folder / f"{Path(filename).stem}_{i}{Path(filename).suffix}"
        if not p.exists(): return p
    raise RuntimeError("Could not create a unique filename.")

def backup_file(path):
    return shutil.copy2(path, unique_path(BACKUPS, Path(path).name))

def human_size(n):
    v = float(n)
    for u in ("B", "KB", "MB", "GB"):
        if v < 1024 or u == "GB": return f"{v:.2f} {u}"
        v /= 1024

class Forge(tk.Tk):
    BG = "#F5F6F8"
    WHITE = "#FFFFFF"
    BLACK = "#111111"
    MUTED = "#626A73"
    LINE = "#DDE1E6"
    HOVER = "#EEF1F4"
    BLUE = "#111111"

    def __init__(self):
        super().__init__()
        self.title(f"{APP}  |  {VERSION}")
        self.geometry("1180x760")
        self.minsize(1000, 680)
        self.configure(bg=self.BG)
        self.option_add("*Font", "TkDefaultFont")
        self._fonts = {}
        self.style = ttk.Style(self)
        try: self.style.theme_use("clam")
        except tk.TclError: pass
        self.style.configure("TProgressbar", troughcolor=self.LINE, background=self.BLACK)
        self.build()
        self.dashboard()

    def F(self, size=10, weight="normal"):
        """Return a cached Tk font object. Font objects avoid Tcl parsing
        issues with family names containing spaces on some Tk/Python builds."""
        key = (size, weight)
        if key not in self._fonts:
            self._fonts[key] = tkfont.Font(family="Segoe UI", size=size, weight=weight)
        return self._fonts[key]

    def build(self):
        top = tk.Frame(self, bg=self.WHITE, height=76, highlightthickness=1,
                       highlightbackground=self.LINE)
        top.pack(fill="x"); top.pack_propagate(False)

        brand = tk.Frame(top, bg=self.WHITE)
        brand.pack(side="left", padx=28)
        tk.Label(brand, text="PF", bg=self.BLACK, fg=self.WHITE,
                 font=self.F(12, "bold"), width=3, height=1).pack(side="left", padx=(0,12), pady=18)
        box = tk.Frame(brand, bg=self.WHITE); box.pack(side="left")
        tk.Label(box, text=APP, bg=self.WHITE, fg=self.BLACK,
                 font=self.F(16, "bold")).pack(anchor="w")
        tk.Label(box, text="Offline document workspace", bg=self.WHITE, fg=self.MUTED,
                 font=self.F(8)).pack(anchor="w")

        tk.Label(top, text=f"Developed by {DEVELOPER}   •   v{VERSION}",
                 bg=self.WHITE, fg=self.MUTED, font=self.F(9)).pack(side="right", padx=28)

        body = tk.Frame(self, bg=self.BG)
        body.pack(fill="both", expand=True)

        self.nav = tk.Frame(body, bg=self.WHITE, width=245, highlightthickness=1,
                            highlightbackground=self.LINE)
        self.nav.pack(side="left", fill="y"); self.nav.pack_propagate(False)

        self.content = tk.Frame(body, bg=self.BG)
        self.content.pack(side="left", fill="both", expand=True)

        items = [
            ("Dashboard", self.dashboard),
            ("Compress PDF", self.compress_page),
            ("Merge PDFs", self.merge),
            ("Split PDF", self.split),
            ("Extract Pages", self.extract),
            ("Rotate PDF", self.rotate),
            ("PDF to Images", self.pdf_images),
            ("Images to PDF", self.images_pdf),
            ("PDF Information", self.info),
        ]
        tk.Label(self.nav, text="TOOLS", bg=self.WHITE, fg=self.MUTED,
                 font=self.F(8, "bold")).pack(anchor="w", padx=22, pady=(25,10))
        for text, cmd in items:
            self.nav_button(text, cmd)

        tk.Frame(self.nav, bg=self.LINE, height=1).pack(fill="x", padx=18, pady=18)
        tk.Label(self.nav, text="STORAGE", bg=self.WHITE, fg=self.MUTED,
                 font=self.F(8, "bold")).pack(anchor="w", padx=22, pady=(0,10))
        self.nav_button("Open Output", lambda: os.startfile(OUTPUT))
        self.nav_button("Open Backups", lambda: os.startfile(BACKUPS))
        self.nav_button("About", self.about)

        foot = tk.Frame(self.nav, bg=self.WHITE)
        foot.pack(side="bottom", fill="x", padx=22, pady=20)
        tk.Label(foot, text="LOCAL ONLY", bg=self.WHITE, fg="#18864B",
                 font=self.F(8, "bold")).pack(anchor="w")
        tk.Label(foot, text="Files are processed on this PC.",
                 bg=self.WHITE, fg=self.MUTED, font=self.F(8)).pack(anchor="w", pady=3)

    def nav_button(self, text, command):
        b = tk.Button(self.nav, text=text, command=command, anchor="w",
                      bg=self.WHITE, fg=self.BLACK, activebackground=self.HOVER,
                      activeforeground=self.BLACK, relief="flat", bd=0,
                      padx=22, pady=10, cursor="hand2",
                      font=self.F(10))
        b.pack(fill="x", padx=8, pady=1)

    def clear(self):
        for x in self.content.winfo_children(): x.destroy()

    def heading(self, title, subtitle):
        f = tk.Frame(self.content, bg=self.BG)
        f.pack(fill="x", padx=42, pady=(36,22))
        tk.Label(f, text=title, bg=self.BG, fg=self.BLACK,
                 font=self.F(26, "bold")).pack(anchor="w")
        tk.Label(f, text=subtitle, bg=self.BG, fg=self.MUTED,
                 font=self.F(10)).pack(anchor="w", pady=(6,0))

    def card(self, parent, title=None):
        f = tk.Frame(parent, bg=self.WHITE, highlightthickness=1, highlightbackground=self.LINE)
        if title:
            tk.Label(f, text=title, bg=self.WHITE, fg=self.BLACK,
                     font=self.F(11, "bold")).pack(anchor="w", padx=20, pady=(18,10))
        return f

    def button(self, parent, text, command, primary=False):
        b = tk.Button(parent, text=text, command=command,
                      bg=self.BLACK if primary else self.WHITE,
                      fg=self.WHITE if primary else self.BLACK,
                      activebackground="#333333" if primary else self.HOVER,
                      activeforeground=self.WHITE if primary else self.BLACK,
                      relief="flat", bd=0, highlightthickness=1,
                      highlightbackground=self.BLACK if not primary else self.BLACK,
                      padx=18, pady=9, cursor="hand2",
                      font=self.F(9, "bold"))
        return b

    def dashboard(self):
        self.clear()
        self.heading("PDF Forge Studio", "Clean, local-first tools for everyday PDF work.")

        hero = self.card(self.content)
        hero.pack(fill="x", padx=42, pady=(0,18))
        tk.Label(hero, text="Work with PDFs without sending documents to a cloud service.",
                 bg=self.WHITE, fg=self.BLACK, font=self.F(13, "bold")).pack(anchor="w", padx=24, pady=(22,5))
        tk.Label(hero, text="Original files are never overwritten by PDF Forge Studio. Outputs and backups are stored separately.",
                 bg=self.WHITE, fg=self.MUTED, font=self.F(9)).pack(anchor="w", padx=24, pady=(0,20))

        grid = tk.Frame(self.content, bg=self.BG)
        grid.pack(fill="both", expand=True, padx=42, pady=(0,28))
        tools = [
            ("Compress PDF", "Reduce scanned PDF size.", self.compress_page),
            ("Merge PDFs", "Combine multiple documents.", self.merge),
            ("Split PDF", "Create one PDF per page.", self.split),
            ("Extract Pages", "Create a PDF from selected pages.", self.extract),
            ("Rotate PDF", "Rotate pages by 90° increments.", self.rotate),
            ("PDF to Images", "Export pages as PNG files.", self.pdf_images),
            ("Images to PDF", "Create a PDF from images.", self.images_pdf),
            ("PDF Information", "Inspect size, pages and metadata.", self.info),
        ]
        for i,(title,desc,cmd) in enumerate(tools):
            r,c=divmod(i,2)
            grid.grid_columnconfigure(c, weight=1)
            card=self.card(grid); card.grid(row=r,column=c,sticky="nsew",padx=6,pady=6)
            tk.Label(card,text=title,bg=self.WHITE,fg=self.BLACK,font=self.F(11, "bold")).pack(anchor="w",padx=20,pady=(18,4))
            tk.Label(card,text=desc,bg=self.WHITE,fg=self.MUTED,font=self.F(9)).pack(anchor="w",padx=20,pady=(0,12))
            self.button(card,"Open",cmd,primary=True).pack(anchor="w",padx=20,pady=(0,18))

    def compress_page(self):
        self.clear()
        self.heading("Compress PDF","Generate a smaller copy while keeping the source document intact.")
        box=self.card(self.content,"Select document"); box.pack(fill="x",padx=42,pady=6)
        var=tk.StringVar(value="No file selected")
        tk.Label(box,textvariable=var,bg=self.WHITE,fg=self.MUTED,font=self.F(9)).pack(side="left",fill="x",expand=True,padx=20,pady=17)
        def choose():
            f=filedialog.askopenfilename(title="Select PDF",filetypes=[("PDF","*.pdf")])
            if f: var.set(f)
        self.button(box,"Choose PDF",choose,primary=True).pack(side="right",padx=20,pady=10)

        box2=self.card(self.content,"Compression profile"); box2.pack(fill="x",padx=42,pady=10)
        preset=tk.StringVar(value="MEDIUM")
        vals=[("HIGH","200 DPI / JPEG 90","Best visual quality"),
              ("MEDIUM","150 DPI / JPEG 80","Recommended for documents"),
              ("SMALL","120 DPI / JPEG 70","Smaller file"),
              ("VERY SMALL","100 DPI / JPEG 60","Maximum reduction")]
        for name,spec,desc in vals:
            row=tk.Frame(box2,bg=self.WHITE); row.pack(fill="x",padx=20,pady=3)
            tk.Radiobutton(row,text=name,variable=preset,value=name,bg=self.WHITE,fg=self.BLACK,
                           selectcolor=self.WHITE,activebackground=self.WHITE,font=self.F(9, "bold")).pack(side="left")
            tk.Label(row,text=f"{spec}  —  {desc}",bg=self.WHITE,fg=self.MUTED,font=self.F(9)).pack(side="left",padx=10)

        status=tk.StringVar(value="Ready")
        tk.Label(self.content,textvariable=status,bg=self.BG,fg=self.MUTED,font=self.F(9)).pack(anchor="w",padx=42,pady=(12,2))
        bar=ttk.Progressbar(self.content,mode="determinate",maximum=100,style="TProgressbar")
        bar.pack(fill="x",padx=42,pady=(0,10))

        def run():
            src=var.get()
            if src=="No file selected": messagebox.showwarning("Select a PDF","Choose a PDF first."); return
            try:
                backup_file(src)
                dpi,quality={"HIGH":(200,90),"MEDIUM":(150,80),"SMALL":(120,70),"VERY SMALL":(100,60)}[preset.get()]
                out=unique_path(OUTPUT,f"{Path(src).stem}_{preset.get().replace(' ','_')}.pdf")
                source=fitz.open(src); result=fitz.open()
                total=len(source)
                for i,page in enumerate(source,1):
                    pix=page.get_pixmap(dpi=dpi,colorspace=fitz.csRGB,alpha=False)
                    img=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
                    buf=io.BytesIO(); img.save(buf,"JPEG",quality=quality,optimize=True)
                    p=result.new_page(width=page.rect.width,height=page.rect.height)
                    p.insert_image(p.rect,stream=buf.getvalue())
                    bar["value"]=i*100/total
                    status.set(f"Processing page {i} of {total}…")
                    self.update_idletasks()
                result.save(out,garbage=4,deflate=True,clean=True)
                result.close(); source.close()
                old=Path(src).stat().st_size; new=out.stat().st_size
                reduction=(1-new/old)*100 if old else 0
                status.set("Completed")
                messagebox.showinfo("Compression complete",
                                    f"Created:\n{out}\n\nOriginal: {human_size(old)}\nCompressed: {human_size(new)}\nReduction: {reduction:.1f}%")
            except Exception:
                log_error(); handle=messagebox.showerror("Compression failed",f"See error log:\n{LOG}")
        self.button(self.content,"Compress PDF",run,primary=True).pack(anchor="e",padx=42,pady=12)

    def merge(self):
        files=filedialog.askopenfilenames(title="Select PDFs",filetypes=[("PDF","*.pdf")])
        if not files:return
        try:
            out=unique_path(OUTPUT,"merged.pdf"); result=fitz.open()
            sources=[]
            for f in files:
                d=fitz.open(f); result.insert_pdf(d); sources.append(d)
            result.save(out,garbage=4,deflate=True)
            for d in sources:d.close()
            result.close(); messagebox.showinfo("Complete",f"Created:\n{out}")
        except Exception: log_error(); messagebox.showerror("Merge failed",f"See:\n{LOG}")

    def split(self):
        src=filedialog.askopenfilename(title="Select PDF",filetypes=[("PDF","*.pdf")])
        if not src:return
        try:
            doc=fitz.open(src); folder=OUTPUT/(Path(src).stem+"_pages"); folder.mkdir(exist_ok=True)
            for i in range(len(doc)):
                out=unique_path(folder,f"page_{i+1}.pdf"); one=fitz.open(); one.insert_pdf(doc,from_page=i,to_page=i)
                one.save(out,garbage=4,deflate=True); one.close()
            doc.close(); messagebox.showinfo("Complete",f"Pages saved to:\n{folder}")
        except Exception: log_error(); messagebox.showerror("Split failed",f"See:\n{LOG}")

    def extract(self):
        src=filedialog.askopenfilename(title="Select PDF",filetypes=[("PDF","*.pdf")])
        if not src:return
        try:
            doc=fitz.open(src); s=simpledialog.askstring("Extract Pages",f"Enter pages like 1,3,5-7\nTotal: {len(doc)}")
            if not s: doc.close(); return
            pages=[]
            for x in s.replace(" ","").split(","):
                if "-" in x:
                    a,b=map(int,x.split("-",1)); pages.extend(range(a,b+1))
                else: pages.append(int(x))
            pages=sorted(set(x for x in pages if 1<=x<=len(doc)))
            if not pages: raise ValueError("No valid pages.")
            out=unique_path(OUTPUT,f"{Path(src).stem}_extracted.pdf"); result=fitz.open()
            for p in pages: result.insert_pdf(doc,from_page=p-1,to_page=p-1)
            result.save(out,garbage=4,deflate=True); result.close(); doc.close()
            messagebox.showinfo("Complete",f"Created:\n{out}")
        except Exception: log_error(); messagebox.showerror("Extraction failed",f"See:\n{LOG}")

    def rotate(self):
        src=filedialog.askopenfilename(title="Select PDF",filetypes=[("PDF","*.pdf")])
        if not src:return
        try:
            angle=simpledialog.askinteger("Rotate","Angle: 90, 180 or 270",initialvalue=90)
            if angle not in (90,180,270):return
            doc=fitz.open(src)
            for p in doc:p.set_rotation((p.rotation+angle)%360)
            out=unique_path(OUTPUT,f"{Path(src).stem}_rotated.pdf"); doc.save(out,garbage=4,deflate=True); doc.close()
            messagebox.showinfo("Complete",f"Created:\n{out}")
        except Exception: log_error(); messagebox.showerror("Rotation failed",f"See:\n{LOG}")

    def pdf_images(self):
        src=filedialog.askopenfilename(title="Select PDF",filetypes=[("PDF","*.pdf")])
        if not src:return
        try:
            dpi=simpledialog.askinteger("PDF to Images","DPI (150 recommended)",initialvalue=150,minvalue=50,maxvalue=600)
            if not dpi:return
            doc=fitz.open(src); folder=OUTPUT/(Path(src).stem+"_images"); folder.mkdir(exist_ok=True)
            for i,p in enumerate(doc,1):
                pix=p.get_pixmap(dpi=dpi,colorspace=fitz.csRGB,alpha=False); pix.save(str(folder/f"page_{i}.png"))
            doc.close(); messagebox.showinfo("Complete",f"Images saved to:\n{folder}")
        except Exception: log_error(); messagebox.showerror("Conversion failed",f"See:\n{LOG}")

    def images_pdf(self):
        files=filedialog.askopenfilenames(title="Select images",filetypes=[("Images","*.jpg *.jpeg *.png *.webp *.bmp")])
        if not files:return
        try:
            ims=[Image.open(f).convert("RGB") for f in files]; out=unique_path(OUTPUT,"images_to_pdf.pdf")
            ims[0].save(out,"PDF",save_all=True,append_images=ims[1:])
            for im in ims: im.close()
            messagebox.showinfo("Complete",f"Created:\n{out}")
        except Exception: log_error(); messagebox.showerror("Conversion failed",f"See:\n{LOG}")

    def info(self):
        src=filedialog.askopenfilename(title="Select PDF",filetypes=[("PDF","*.pdf")])
        if not src:return
        try:
            doc=fitz.open(src)
            msg=f"File: {Path(src).name}\nSize: {human_size(Path(src).stat().st_size)}\nPages: {len(doc)}\nEncrypted: {'Yes' if doc.is_encrypted else 'No'}\n\nMetadata:\n{doc.metadata}"
            doc.close(); messagebox.showinfo("PDF Information",msg)
        except Exception: log_error(); messagebox.showerror("Read failed",f"See:\n{LOG}")

    def about(self):
        self.clear(); self.heading("About","Application information and storage locations.")
        c=self.card(self.content); c.pack(fill="x",padx=42,pady=10)
        tk.Label(c,text=APP,bg=self.WHITE,fg=self.BLACK,font=self.F(22, "bold")).pack(anchor="w",padx=24,pady=(24,4))
        tk.Label(c,text=f"Version {VERSION}",bg=self.WHITE,fg=self.MUTED,font=self.F(10)).pack(anchor="w",padx=24)
        tk.Label(c,text=f"Developer: {DEVELOPER}\n\nOutput: {OUTPUT}\nBackups: {BACKUPS}\nLogs: {LOG}\n\nNo cloud upload functionality is included.",bg=self.WHITE,fg=self.MUTED,font=self.F(10),justify="left").pack(anchor="w",padx=24,pady=20)

if __name__=="__main__":
    try:
        Forge().mainloop()
    except Exception:
        log_error()
        try: messagebox.showerror(APP,f"Startup failed.\n\nSee:\n{LOG}")
        except Exception: pass
