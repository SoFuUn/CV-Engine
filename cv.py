import logging
import random

from datetime import datetime
from pathlib import Path
from typing import List, Union, Dict
from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "cv_generator.log"

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def finde_asset_pfad(ordner: Path, dateiname_ohne_endung: str) -> Path:
    """Sucht nach einer Datei mit der Endung .png, .jpg oder .jpeg.

    Gibt das gefundene Path-Objekt zurück, oder None, falls nichts
    existiert.
    """
    gueltige_endungen = {".png", ".jpg", ".jpeg"}

    try:
        for datei in ordner.iterdir():
            if (
                datei.stem.lower() == dateiname_ohne_endung.lower()
                and datei.suffix.lower() in gueltige_endungen
            ):
                return datei
    except FileNotFoundError:
        pass

    return ordner / f"{dateiname_ohne_endung}.png"

ASSETS_DIR = BASE_DIR / "assets"

ICON_PIN_PATH = finde_asset_pfad(ASSETS_DIR, "pin")
ICON_MAIL_PATH = finde_asset_pfad(ASSETS_DIR, "mail")
ICON_PHONE_PATH = finde_asset_pfad(ASSETS_DIR, "phone")

try:
    PORTRAIT_PATH = next(ASSETS_DIR.glob("portrait.*"))
except StopIteration:
    PORTRAIT_PATH = None
    logger.warning("No file named 'portrait.*' found in assets directory.")


class CV(FPDF):
    def __init__(self, sidebar_x: float, sidebar_w: float, sidebar_h: float, tech_profile: dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sidebar_x = sidebar_x
        self.sidebar_w = sidebar_w
        self.sidebar_h = sidebar_h
        self.tech_profile = tech_profile or {}
        
        self.add_page()
        self.add_picture()

    def add_page(self, *args, **kwargs):
        super().add_page(*args, **kwargs)
        
        if self.page == 1:
            self.draw_sidebar() 
            
        elif self.page == 2:
            self.draw_sidebar()
            
            self.add_technical_skills(
                languages=self.tech_profile.get("programming_languages", []),
                tools=self.tech_profile.get("tools_frameworks", []),
                focus=self.tech_profile.get("focus_areas", [])
            )

    def add_header_name(self, name: str, job_title: str, certificate: str) -> None:
        self.set_left_margin(10)
        self.set_xy(10, 20)

        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "B", 26)
        self.cell(130, 14, name, ln=True, align="L")
        
        self.set_text_color(150, 0, 0)
        self.set_font("Arial", "B", 15)
        self.cell(130, 8, job_title, ln=True, align="L")
        
        self.set_text_color(80, 80, 80)
        self.set_font("Arial", "I", 10)
        self.cell(130, 6, certificate, ln=True, align="L")
        
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y() + 2, 135, self.get_y() + 2)
        self.ln(5)

    def add_profile_summary(self, text: str) -> None:
        self.set_font("Arial", "I", 10)
        self.set_text_color(50, 50, 50)
        
        available_width = self.sidebar_x - 15 - 5 
        self.set_x(10)
        self.multi_cell(available_width, 5, text, align="L")
        self.ln(8)

    def draw_sidebar(self) -> None:
        tile_size = 15 
        half_tile = tile_size / 2
        self.set_draw_color(0, 0, 0)
        with self.local_context(fill_opacity=1):
            with self.rect_clip(self.sidebar_x, 0, self.sidebar_w, self.sidebar_h):
                for y in range(-int(half_tile), 310, int(half_tile)):
                    row_even = (y // int(half_tile)) % 2 == 0
                    
                    for x in range(self.sidebar_x - int(half_tile), 220, tile_size):
                        current_x = x if row_even else x - half_tile
                        
                        red_val = random.randint(75, 100) 
                        self.set_fill_color(red_val, 0, 0)
                        self.set_draw_color(red_val - 10, 0, 0)
                        self.set_line_width(0.5)
                        
                        cx = current_x + half_tile
                        cy = y + half_tile
                        
                        points = [
                            [cx, cy - half_tile],
                            [cx + half_tile, cy],
                            [cx, cy + half_tile],
                            [cx - half_tile, cy]
                        ]
                        self.polygon(points, "F")

    def add_picture(self) -> None:
        img_w, img_h = 50, 50
        img_x = self.sidebar_x + (self.sidebar_w / 2) - (img_w / 2)
        img_y = 15
        
        border_thickness = 1.5
        self.set_fill_color(255, 255, 255)
        self.rect(img_x - border_thickness, 
                  img_y - border_thickness, 
                  img_w + (2 * border_thickness), 
                  img_h + (2 * border_thickness), 
                  "F")

        if PORTRAIT_PATH and PORTRAIT_PATH.exists():
            try:
                self.image(PORTRAIT_PATH, x=img_x, y=img_y, w=img_w, h=img_h)
                return
            except Exception as e:
                logger.error(f"Failed to load image: {e}")
        
        # Fallback-Visualisierung bei fehlendem Bild
        self.set_fill_color(200, 200, 200)
        self.rect(img_x, img_y, img_w, img_h, "F")
        self.set_text_color(0, 0, 0)
        self.set_xy(img_x, img_y + (img_h / 2))
        self.set_font("Arial", "I", 8)
        self.cell(img_w, 5, "Bild fehlt", align="C")

    def add_contact_info(self, address: List[str], email: List[str], phone: List[str], languages: List[Dict[str, int]] = None) -> None:
        start_y = 80 
        next_y = self.add_sidebar_contact_element(ICON_PIN_PATH, address, start_y)
        next_y = self.add_sidebar_contact_element(ICON_MAIL_PATH, email, next_y)
        next_y = self.add_sidebar_contact_element(ICON_PHONE_PATH, phone, next_y)

        self.set_xy(self.sidebar_x, next_y + 15)
        self.set_font("Arial", "B", 12)
        self.cell(self.sidebar_w, 10, "Languages:", align="C", ln=True)
        
        self.draw_skill_level("German - Native language", 5, self.get_y() + 5)
        self.draw_skill_level("English", 5, self.get_y() + 5)
    
    def add_sidebar_contact_element(self, icon_path: Path, text_lines: List[str], y_pos: float) -> float:
        sidebar_center = self.sidebar_x + (self.sidebar_w / 2)
        icon_size = 9
        
        if icon_path.exists():
            try:
                self.image(icon_path, x=sidebar_center - (icon_size / 2), y=y_pos, w=icon_size)
            except OSError as e:
                logger.error(f"Could not render icon {icon_path}: {e}")
                self._draw_fallback_icon(sidebar_center, y_pos, icon_size)
        else:
            self._draw_fallback_icon(sidebar_center, y_pos, icon_size)

        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "", 10)
        
        current_y = y_pos + icon_size + 2
        for line in text_lines:
            self.set_xy(self.sidebar_x, current_y)
            self.cell(self.sidebar_w, 5, line, align="C", ln=True)
            current_y += 4
            
        return current_y + 15

    def _draw_fallback_icon(self, center_x: float, y_pos: float, size: float) -> None:
        """Interne Hilfsmethode."""
        self.set_draw_color(255, 255, 255)
        self.circle(center_x, y_pos + (size / 2), 1, style="D")

    def draw_skill_level(self, label: str, level: int, y_pos: float) -> None:
        sidebar_center = self.sidebar_x + (self.sidebar_w / 2)
        
        self.set_xy(self.sidebar_x, y_pos)
        self.set_font("Arial", "", 10)
        self.set_text_color(255, 255, 255)
        self.cell(self.sidebar_w, 5, f"{label}:", align="C", ln=True)
        
        star_width = 5 
        total_stars_width = 5 * star_width
        start_x_stars = sidebar_center - (total_stars_width / 2)
        stars_y = self.get_y() + 1
        
        for i in range(1, 6):
            style = "F" if i <= level else "D"
            self.set_draw_color(255, 255, 255)
            self.set_fill_color(255, 255, 255)
            self.set_line_width(0.2)
            
            curr_x = start_x_stars + (i - 1) * star_width + (star_width / 2)
            r = 1.5
            points = [
                (curr_x, stars_y),
                (curr_x + r, stars_y + r),
                (curr_x, stars_y + 2 * r),
                (curr_x - r, stars_y + r)
            ]
            self.polygon(points, style=style)
            
        self.ln(8)

    def add_section(self, title: str, content: List[Union[str, dict]]) -> None:
        required_space = 40
        if self.get_y() + required_space > self.page_break_trigger:
            self.add_page()

        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "B", 14)
        self.cell(0, 6, title, ln=True)
        self.ln(2)
        
        self.set_font("Arial", "", 11)
        for index, text in enumerate(content):
            if isinstance(text, dict):
                if self.get_y() + 25 > self.page_break_trigger:
                    self.add_page()

                self.add_experience(text["period"], text["title"], text["company"])
                if index != len(content) - 1:
                    self.ln(5)
            else:
                self.cell(120, 6, text, ln=True)
        self.ln(10)

    def add_experience(self, period: str, title: str, company: str) -> None:
        self.set_font("Arial", "B", 11)
        start_y = self.get_y()
        self.cell(35, 6, period, ln=False)

        available_width = self.sidebar_x - 34
        self.set_xy(33, start_y)
        self.multi_cell(available_width, 6, title, align="L")
        
        if company:
            self.set_x(33)
            self.set_font("Arial", "I", 10)
            self.multi_cell(available_width, 6, company, align='L')
        
        self.ln(2)

    def add_technical_skills(self, languages: List[Dict[str, int]], tools: List[str], focus: List[str]) -> None:
        """Rendert die erweiterten technischen Fähigkeiten in der rechten Sidebar,

        ohne den Haupttext zu verschieben.
        """
        ursprung_x = self.get_x()
        ursprung_y = self.get_y()

        sidebar_rechts_x = 140
        sidebar_w = 70
        current_y = 25
        
        if languages:
            self.set_xy(sidebar_rechts_x, current_y)
            self.set_font("Arial", "B", 12)
            self.set_text_color(255, 255, 255)
            self.cell(sidebar_w, 8, "Programming languages:", align="C", ln=True)
            current_y = self.get_y() + 2
            
            for lang in languages:
                alter_x = self.sidebar_x
                self.sidebar_x = sidebar_rechts_x
                
                self.draw_skill_level(lang["name"], lang["level"], current_y)
                current_y = self.get_y()
                
                self.sidebar_x = alter_x
            
            current_y += 5

        if tools:
            self.set_xy(sidebar_rechts_x, current_y)
            self.set_font("Arial", "B", 12)
            self.set_text_color(255, 255, 255)
            self.cell(sidebar_w, 8, "Tools & Frameworks:", align="C", ln=True)
            
            self.set_font("Arial", "", 10)
            current_y = self.get_y() + 2
            
            for tool in tools:
                self.set_x(sidebar_rechts_x)
                self.cell(sidebar_w, 5, tool, align="C", ln=True)
            
            current_y = self.get_y() + 10

        if focus:
            self.set_xy(sidebar_rechts_x, current_y)
            self.set_font("Arial", "B", 12)
            self.set_text_color(255, 255, 255)
            self.cell(sidebar_w, 8, "Spezialgebiete:", align="C", ln=True)
            
            self.set_font("Arial", "I", 9)
            current_y = self.get_y() + 2
            
            for area in focus:
                self.set_x(sidebar_rechts_x)
                self.multi_cell(sidebar_w, 4, area, align="C")
                self.ln(2)

        self.set_xy(ursprung_x, ursprung_y)

    def footer(self) -> None:
        old_auto_page_break = self.auto_page_break
        self.set_auto_page_break(False)
        
        self.set_y(-18) 
        self.set_font("Arial", "I", 8)
        self.set_text_color(150, 150, 150)
        
        self.set_draw_color(220, 220, 220)
        self.set_line_width(0.2)
        self.line(10, self.get_y(), 135, self.get_y())
        self.ln(2)

        datum_heute = datetime.now().strftime("%d.%m.%Y")
        self.set_x(10)
        self.cell(125, 4, f"Stand: {datum_heute} | Erstellt mit Python (fpdf2)", ln=True, align="L")
        github_url = "https://github.com/SoFuUn/CV-Engine"
        self.set_x(10)
        self.cell(125, 4, f"Code: {github_url}", ln=True, align="L")
        
        self.set_auto_page_break(old_auto_page_break, margin=15)
    
    def ensure_page2(self) -> None:
        """Überprüft, ob bereits eine zweite Seite existiert.

        Wenn nicht, wird sie manuell erstellt, damit das technische Profil
        immer gedruckt wird.
        """
        if self.page < 2:
            logger.info("Haupttext passt auf eine Seite. Erzwinge Seite 2 für das technische Profil.")
            
            self.add_page()