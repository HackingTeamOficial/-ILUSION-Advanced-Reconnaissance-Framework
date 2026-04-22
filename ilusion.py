#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║     ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗             ║
║     ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝             ║
║     ███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗           ║
║     ██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║           ║
║     ██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝           ║
║     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝            ║
║                                                                       ║
║           Comunidad de Hackers - Herramienta de Reconocimiento       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import random
import os
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import re

# ─── ANSI COLOR CODES ───────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

# Greens (matrix style)
G_DARK  = "\033[38;5;22m"
G_MID   = "\033[38;5;40m"
G_BRIGHT= "\033[38;5;46m"
G_NEON  = "\033[38;5;82m"

# Accents
CYAN    = "\033[38;5;51m"
WHITE   = "\033[38;5;255m"
GRAY    = "\033[38;5;240m"
RED     = "\033[38;5;196m"
YELLOW  = "\033[38;5;226m"
MAGENTA = "\033[38;5;201m"

# Background
BG_BLACK= "\033[40m"

# ─── HELPERS ────────────────────────────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewrite(text, delay=0.018, color=""):
    for ch in text:
        sys.stdout.write(color + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def glitch_line(text, color=G_BRIGHT, glitch_color=RED, iterations=3, delay=0.07):
    """Simula efecto glitch en una línea."""
    glitch_chars = "!@#$%^&*<>?/|\\[]{}~±§"
    for _ in range(iterations):
        glitched = ""
        for ch in text:
            if ch != ' ' and random.random() < 0.15:
                glitched += random.choice(glitch_chars)
            else:
                glitched += ch
        sys.stdout.write(f"\r{glitch_color}{BOLD}{glitched}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"\r{color}{BOLD}{text}{RESET}\n")
    sys.stdout.flush()

def random_hex_stream(width=60, lines=3, delay=0.04):
    """Imprime un stream de hex estilo boot."""
    for _ in range(lines):
        row = ""
        for _ in range(width // 3):
            row += f"{random.randint(0,255):02X} "
        color = random.choice([G_DARK, G_MID, G_BRIGHT, GRAY])
        print(f"{color}{DIM}{row}{RESET}")
        time.sleep(delay)

def matrix_rain_line(width=70):
    """Una línea estilo Matrix rain."""
    chars = "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ01アイウエオカキ"
    line = "".join(random.choice(chars) if random.random() > 0.3 else " " for _ in range(width))
    colors = [G_DARK, G_MID, G_BRIGHT, G_NEON]
    out = ""
    for ch in line:
        out += random.choice(colors) + ch
    print(out + RESET)

def separator(char="─", width=70, color=G_MID):
    print(f"{color}{char * width}{RESET}")

def center_text(text, width=70, color=WHITE, bg=""):
    padding = (width - len(text)) // 2
    print(f"{' ' * padding}{bg}{color}{BOLD}{text}{RESET}")

# ─── ASCII ART ───────────────────────────────────────────────────────────────
SKULL = [
    r"    ░░░░░░░░░░░░░░░░░    ",
    r"   ░░  ░░░░░░░░░░  ░░   ",
    r"  ░░  ░░      ░░  ░░  ░░ ",
    r" ░░░░░░        ░░░░░░░░░ ",
    r" ░░ ██  ░░░░  ██  ░░░░░ ",
    r" ░░░░░░  ░░  ░░░░░░░░░░ ",
    r"  ░░░░░░░░░░░░░░░░░░░░  ",
    r"   ░░░ ░░░░░░░ ░░░░░░   ",
    r"    ░░░░░░░░░░░░░░░░     ",
]

HACKING_ART = [
    "  ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗  ",
    "  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝  ",
    "  ███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗ ",
    "  ██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║ ",
    "  ██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝ ",
    "  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ",
]

TEAM_ART = [
    "        ████████╗███████╗ █████╗ ███╗   ███╗        ",
    "           ██╔══╝██╔════╝██╔══██╗████╗ ████║        ",
    "           ██║   █████╗  ███████║██╔████╔██║        ",
    "           ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║        ",
    "           ██║   ███████╗██║  ██║██║ ╚═╝ ██║        ",
    "           ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝        ",
]

COMUNIDAD_ART = [
    " ██████╗ ██████╗ ███╗   ███╗██╗   ██╗███╗   ██╗██╗██████╗  █████╗ ██████╗ ",
    "██╔════╝██╔═══██╗████╗ ████║██║   ██║████╗  ██║██║██╔══██╗██╔══██╗██╔══██╗",
    "██║     ██║   ██║██╔████╔██║██║   ██║██╔██╗ ██║██║██║  ██║███████║██║  ██║",
    "██║     ██║   ██║██║╚██╔╝██║██║   ██║██║╚██╗██║██║██║  ██║██╔══██║██║  ██║",
    "╚██████╗╚██████╔╝██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║██████╔╝██║  ██║██████╔╝",
    " ╚═════╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═════╝ ",
]

DE_HACKERS_ART = [
    "     ██████╗ ███████╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ ███████╗",
    "     ██╔══██╗██╔════╝    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔════╝",
    "     ██║  ██║█████╗      ███████║███████║██║     █████╔╝ █████╗  ██████╔╝███████╗",
    "     ██║  ██║██╔══╝      ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗╚════██║",
    "     ██████╔╝███████╗    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║███████║",
    "     ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝",
]

# ─── INFO PANEL ──────────────────────────────────────────────────────────────
INFO_LINES = [
    ("[ SISTEMA ]", f"Linux x86_64 | Python {sys.version.split()[0]}"),
    ("[ STATUS  ]", "OPERATIVO ▶ ONLINE"),
    ("[ NIVEL   ]", "ELITE ████████████ 100%"),
    ("[ RED     ]", "TOR ACTIVO | VPN ACTIVO | ANONIMO"),
    ("[ MISIÓN  ]", "Aprender · Explorar · Compartir"),
]

QUOTES = [
    "\"La información quiere ser libre.\"  — Stewart Brand",
    "\"Hack the planeta.\"  — Hackers (1995)",
    "\"Cuestiona todo. Rompe límites. Comparte conocimiento.\"",
    "\"La seguridad no es un producto, es un proceso.\"  — B. Schneier",
]

# ─── MAIN BANNER ─────────────────────────────────────────────────────────────
def show_banner():
    clear()

    # Boot sequence
    print(f"\n{G_MID}{DIM}  [*] Iniciando sistema...{RESET}")
    time.sleep(0.3)
    random_hex_stream(width=66, lines=2, delay=0.03)
    print(f"{G_MID}{DIM}  [*] Cargando módulos...{RESET}")
    time.sleep(0.2)
    random_hex_stream(width=66, lines=2, delay=0.03)
    print(f"{G_NEON}{BOLD}  [✓] Sistema listo.{RESET}\n")
    time.sleep(0.3)

    # Matrix rain header
    for _ in range(4):
        matrix_rain_line(72)
        time.sleep(0.04)

    print()
    separator("═", 72, G_NEON)
    separator(" ", 72)

    # HACKING
    for i, line in enumerate(HACKING_ART):
        colors = [G_DARK, G_MID, G_BRIGHT, G_NEON, G_BRIGHT, G_MID]
        glitch = (i == 0)
        if glitch:
            glitch_line(line, color=G_NEON, glitch_color=RED, iterations=2, delay=0.05)
        else:
            print(f"{colors[i % len(colors)]}{BOLD}{line}{RESET}")
        time.sleep(0.05)

    # TEAM
    print()
    for i, line in enumerate(TEAM_ART):
        colors = [G_MID, G_BRIGHT, G_NEON, G_BRIGHT, G_MID, G_DARK]
        print(f"{colors[i % len(colors)]}{BOLD}{line}{RESET}")
        time.sleep(0.04)

    separator(" ", 72)
    separator("─", 72, G_MID)
    separator(" ", 72)

    # COMUNIDAD
    for i, line in enumerate(COMUNIDAD_ART):
        shade = [G_DARK, G_MID, G_BRIGHT, G_BRIGHT, G_MID, G_DARK]
        print(f"{shade[i % len(shade)]}{BOLD}{line}{RESET}")
        time.sleep(0.04)

    print()

    # DE HACKERS
    for i, line in enumerate(DE_HACKERS_ART):
        shade = [G_MID, G_BRIGHT, G_NEON, G_NEON, G_BRIGHT, G_MID]
        print(f"{shade[i % len(shade)]}{BOLD}{line}{RESET}")
        time.sleep(0.04)

    separator(" ", 72)
    separator("═", 72, G_NEON)

    # Matrix rain footer
    print()
    for _ in range(3):
        matrix_rain_line(72)
        time.sleep(0.04)

    # Info panel
    print()
    separator("┌" + "─"*70 + "┐", 1, G_MID)
    for label, value in INFO_LINES:
        pad = 70 - len(label) - len(value) - 4
        print(f"{G_MID}│ {CYAN}{BOLD}{label}{RESET}  {G_BRIGHT}{value}{' ' * pad}{G_MID}│{RESET}")
    separator("└" + "─"*70 + "┘", 1, G_MID)

    # Quote
    print()
    quote = random.choice(QUOTES)
    center_text(quote, 72, YELLOW)
    print()

    # Skull decorativo pequeño
    for line in SKULL:
        center_text(line, 72, G_MID)

    print()
    separator("═", 72, G_NEON)
    center_text("[ ACCESO AUTORIZADO — BIENVENIDO, HACKER ]", 72, G_NEON)
    separator("═", 72, G_NEON)

    # Prompt final animado
    print()
    typewrite("  root@illusion:~$ ", delay=0.07, color=G_BRIGHT)
    time.sleep(0.3)
    typewrite(f"  [✓] Entorno ILUSION cargado correctamente.", delay=0.03, color=G_NEON)
    print()

# ─── TOOL DETECTION ──────────────────────────────────────────────────────────
class ToolDetector:
    def __init__(self):
        self.go_path = os.path.expanduser("~/go/bin")
        self.kali_tools = [
            "nmap", "masscan", "subfinder", "amass", "naabu", "httpx", 
            "nuclei", "fuff", "dnsx", "shuffledns", "hakrawler", 
            "assetfinder", "dalfox", "subjack", "gowitness", "waymore",
            "dirsearch", "sqlmap", "crt", "gau", "gf", "qsreplace",
            "unfurl", "jq", "curl", "wget", "dig", "nslookup"
        ]
        self.tools = {}
        self.detect_all()
    
    def detect_tool(self, tool_name):
        """Detect if a tool is available in the system"""
        import shutil
        paths_to_check = [
            os.path.join(self.go_path, tool_name),
            f"/usr/bin/{tool_name}",
            f"/usr/local/bin/{tool_name}",
            f"/bin/{tool_name}",
            shutil.which(tool_name)
        ]
        
        for path in paths_to_check:
            if path and os.path.isfile(path) and os.access(path, os.X_OK):
                return path
        
        try:
            result = subprocess.run(
                ["which", tool_name], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def detect_all(self):
        """Detect all tools and their status"""
        print(f"\n{G_CYAN}[*] Detecting available tools...{RESET}\n")
        
        import shutil
        
        for tool in self.kali_tools:
            path = self.detect_tool(tool)
            self.tools[tool] = {
                "available": path is not None,
                "path": path if path else "Not found",
                "status": f"{G_BRIGHT}✓{RESET}" if path else f"{RED}✗{RESET}"
            }
            status_icon = f"{G_BRIGHT}✓{RESET}" if path else f"{RED}✗{RESET}"
            print(f"  {status_icon} {tool:<15} {path if path else RED + 'Not installed' + RESET}")
        
        available_count = sum(1 for t in self.tools.values() if t["available"])
        print(f"\n{YELLOW}[*] {available_count}/{len(self.tools)} tools available{RESET}\n")

G_CYAN = CYAN

# ─── MAIN RECON CLASS ────────────────────────────────────────────────────────
class IlusionRecon:
    def __init__(self, target, scope, output_dir, threads=100, verbose=False):
        self.target = target
        self.scope = scope.split(',') if scope else []
        self.output_dir = Path(output_dir)
        self.threads = threads
        self.verbose = verbose
        self.tool_detector = ToolDetector()
        self.tools = self.tool_detector.tools
        self.start_time = datetime.now()
        self.results = {
            "subdomains": [],
            "ports": [],
            "urls": [],
            "vulnerabilities": [],
            "screenshots": [],
            "secrets": []
        }
        
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary output directories"""
        dirs = [
            "recon",
            "recon/subdomains",
            "recon/ports",
            "recon/web",
            "recon/urls",
            "recon/vulnerabilities",
            "recon/screenshots",
            "recon/secrets",
            "reports"
        ]
        for d in dirs:
            (self.output_dir / d).mkdir(parents=True, exist_ok=True)
    
    def log(self, message, level="info"):
        """Log messages with colors"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "info": CYAN,
            "success": G_BRIGHT,
            "warning": YELLOW,
            "error": RED,
            "header": MAGENTA
        }
        color = colors.get(level, WHITE)
        print(f"{color}[{timestamp}] {message}{RESET}")
    
    def run_command(self, cmd, output_file=None, timeout=300, check=True):
        """Run a command and optionally save output"""
        if self.verbose:
            self.log(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}", "info")
        
        try:
            if isinstance(cmd, str):
                cmd = cmd.split()
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if output_file and result.returncode == 0:
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
            
            return result
            
        except subprocess.TimeoutExpired:
            self.log(f"Command timed out: {cmd[0]}", "error")
            return None
        except Exception as e:
            self.log(f"Error running command: {e}", "error")
            return None
    
    def is_in_scope(self, subdomain):
        """Check if subdomain is in scope"""
        if not self.scope:
            return True
        
        for s in self.scope:
            s = s.strip().replace('*.', '')
            if s in subdomain or subdomain.endswith(s):
                return True
        return False
    
    def phase1_reconnaissance(self):
        """Phase 1: Subdomain Enumeration"""
        self.log("=" * 60, "header")
        self.log("PHASE 1: RECONNAISSANCE - Subdomain Enumeration", "header")
        self.log("=" * 60, "header")
        
        all_subdomains = set()
        
        # 1.1 Passive Reconnaissance - Subfinder
        if self.tools['subfinder']['available']:
            self.log("Running Subfinder (Passive Sources)...", "info")
            output = self.output_dir / "recon/subdomains/subfinder.txt"
            result = self.run_command(
                ["subfinder", "-d", self.target, "-o", str(output)],
                timeout=180
            )
            if result and result.returncode == 0:
                with open(output) as f:
                    for line in f:
                        sub = line.strip()
                        if sub and self.is_in_scope(sub):
                            all_subdomains.add(sub)
        
        # 1.2 Assetfinder
        if self.tools['assetfinder']['available']:
            self.log("Running Assetfinder...", "info")
            result = self.run_command(
                ["assetfinder", "--subs-only", self.target],
                timeout=120
            )
            if result and result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.strip() and self.is_in_scope(line.strip()):
                        all_subdomains.add(line.strip())
        
        # 1.3 Certificate Analysis (crt.sh)
        self.log("Running Certificate Analysis (crt.sh)...", "info")
        try:
            result = subprocess.run(
                ["curl", "-s", f"https://crt.sh/?q=%25.{self.target}&output=json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                for entry in data:
                    name = entry.get('name_value', '')
                    for sub in name.split('\n'):
                        sub = sub.strip()
                        if sub and self.is_in_scope(sub) and '*' not in sub:
                            all_subdomains.add(sub)
        except Exception as e:
            self.log(f"Certificate analysis failed: {e}", "warning")
        
        # 1.4 Amass (Active + Passive)
        if self.tools['amass']['available']:
            self.log("Running Amass (Active + Passive)...", "info")
            output = self.output_dir / "recon/subdomains/amass.txt"
            self.run_command(
                ["amass", "enum", "-passive", "-d", self.target, "-o", str(output)],
                timeout=300
            )
            if output.exists():
                with open(output) as f:
                    for line in f:
                        sub = line.strip()
                        if sub and self.is_in_scope(sub):
                            all_subdomains.add(sub)
        
        # 1.5 DNS Resolution with dnsx
        self.log("Resolving subdomains with dnsx...", "info")
        resolved = set()
        if self.tools['dnsx']['available'] and all_subdomains:
            input_file = self.output_dir / "recon/subdomains/all_raw.txt"
            output = self.output_dir / "recon/subdomains/dnsx_resolved.txt"
            
            with open(input_file, 'w') as f:
                f.write('\n'.join(all_subdomains))
            
            result = self.run_command(
                ["dnsx", "-l", str(input_file), "-o", str(output), "-resp"],
                timeout=300
            )
            
            if output.exists():
                with open(output) as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 2 and parts[1] != '':
                            resolved.add(parts[0])
        
        self.results['subdomains'] = list(resolved if resolved else all_subdomains)
        self.log(f"Found {len(self.results['subdomains'])} unique subdomains", "success")
        
        # Save final subdomain list
        with open(self.output_dir / "recon/subdomains/final_subdomains.txt", 'w') as f:
            f.write('\n'.join(sorted(self.results['subdomains'])))
        
        return self.results['subdomains']
    
    def phase2_port_scanning(self):
        """Phase 2: Port Scanning"""
        self.log("=" * 60, "header")
        self.log("PHASE 2: PORT SCANNING", "header")
        self.log("=" * 60, "header")
        
        open_ports = []
        subdomains = self.results.get('subdomains', [])
        
        if not subdomains:
            self.log("No subdomains found. Skipping port scan.", "warning")
            return open_ports
        
        # 2.1 Naabu (Fast port scan)
        if self.tools['naabu']['available']:
            self.log("Running Naabu (Top 100 ports)...", "info")
            input_file = self.output_dir / "recon/subdomains/final_subdomains.txt"
            output = self.output_dir / "recon/ports/naabu_results.txt"
            
            result = self.run_command(
                ["naabu", "-hl", str(input_file), "-o", str(output), "-p", "top-100", "-silent"],
                timeout=600
            )
            
            if output.exists():
                with open(output) as f:
                    open_ports = [line.strip() for line in f if line.strip()]
        
        # 2.2 Masscan (Full scan on selected hosts)
        if self.tools['masscan']['available']:
            self.log("Running Masscan (1-10000 ports on top hosts)...", "info")
            output = self.output_dir / "recon/ports/masscan_results.txt"
            top_subs = subdomains[:20]
            
            for sub in top_subs:
                self.run_command(
                    ["masscan", f"{sub}", "--ports", "1-10000", "-oJ", str(output)],
                    timeout=120
                )
        
        # 2.3 Nmap (Detailed scan)
        if self.tools['nmap']['available'] and open_ports:
            self.log("Running Nmap (Service Detection)...", "info")
            
            self.run_command(
                ["nmap", "-sV", "-p", ",".join(set([p.split(':')[-1] for p in open_ports])), 
                 "-iL", str(self.output_dir / "recon/subdomains/final_subdomains.txt"),
                 "-oA", str(self.output_dir / "recon/ports/nmap_scan")],
                timeout=900
            )
        
        self.results['ports'] = open_ports
        self.log(f"Found {len(open_ports)} open ports", "success")
        
        return open_ports
    
    def phase3_web_discovery(self):
        """Phase 3: Web Discovery"""
        self.log("=" * 60, "header")
        self.log("PHASE 3: WEB DISCOVERY", "header")
        self.log("=" * 60, "header")
        
        alive_hosts = []
        subdomains = self.results.get('subdomains', [])
        
        if not subdomains:
            self.log("No subdomains found. Skipping web discovery.", "warning")
            return []
        
        # 3.1 httpx - Check which hosts have web services
        if self.tools['httpx']['available']:
            self.log("Running httpx (Web Probing)...", "info")
            input_file = self.output_dir / "recon/subdomains/final_subdomains.txt"
            output = self.output_dir / "recon/web/httpx_alive.txt"
            
            result = self.run_command(
                ["httpx", "-l", str(input_file), "-o", str(output), "-silent", 
                 "-status-code", "-title", "-tech-detect"],
                timeout=600
            )
            
            if output.exists():
                with open(output) as f:
                    alive_hosts = [line.strip() for line in f if line.strip()]
        
        self.results['urls'] = alive_hosts
        self.log(f"Found {len(alive_hosts)} alive web hosts", "success")
        
        # 3.2 Gowitness - Screenshots
        if self.tools['gowitness']['available'] and alive_hosts:
            self.log("Running Gowitness (Screenshots)...", "info")
            screenshot_dir = self.output_dir / "recon/screenshots"
            
            self.run_command(
                ["gowitness", "scan", "-f", str(self.output_dir / "recon/web/httpx_alive.txt"),
                 "-d", str(screenshot_dir), "--threads", "10"],
                timeout=1200
            )
        
        # 3.3 Directory Scanning
        if self.tools['fuff']['available'] and alive_hosts:
            self.log("Running ffuf (Directory Fuzzing)...", "info")
            for host in alive_hosts[:10]:
                host_name = urlparse(f"http://{host}").netloc.replace(':', '_')
                output = self.output_dir / "recon/web" / f"ffuf_{host_name}.txt"
                
                self.run_command(
                    ["fuff", "-u", f"http://{host}/FUZZ", "-w", 
                     "/usr/share/wordlists/dirb/common.txt", "-o", str(output)],
                    timeout=300
                )
        
        # 3.4 Dirsearch
        if self.tools['dirsearch']['available'] and alive_hosts:
            self.log("Running Dirsearch...", "info")
            for host in alive_hosts[:5]:
                host_name = urlparse(f"http://{host}").netloc.replace(':', '_')
                
                self.run_command(
                    ["dirsearch", "-u", f"http://{host}", "-o", 
                     str(self.output_dir / "recon/web" / f"dirsearch_{host_name}.json")],
                    timeout=600
                )
        
        return alive_hosts
    
    def phase4_archive_analysis(self):
        """Phase 4: Archive Analysis"""
        self.log("=" * 60, "header")
        self.log("PHASE 4: ARCHIVE ANALYSIS", "header")
        self.log("=" * 60, "header")
        
        all_urls = []
        
        # 4.1 Waymore
        if self.tools['waymore']['available']:
            self.log("Running Waymore (URL Extraction)...", "info")
            output = self.output_dir / "recon/urls/waymore_urls.txt"
            
            self.run_command(
                ["waymore", "-i", self.target, "-oU", str(output)],
                timeout=600
            )
            
            if output.exists():
                with open(output) as f:
                    all_urls.extend([u.strip() for u in f if u.strip()])
        
        # 4.2 GAU (Get All URLs)
        if self.tools['gau']['available']:
            self.log("Running GAU...", "info")
            output = self.output_dir / "recon/urls/gau_urls.txt"
            
            self.run_command(
                ["gau", "--subs", self.target, "-o", str(output)],
                timeout=600
            )
            
            if output.exists():
                with open(output) as f:
                    all_urls.extend([u.strip() for u in f if u.strip()])
        
        # 4.3 JS Files Analysis
        if all_urls:
            self.log("Extracting JavaScript files...", "info")
            js_files = [u for u in all_urls if '.js' in u.lower()]
            
            with open(self.output_dir / "recon/urls/js_files.txt", 'w') as f:
                f.write('\n'.join(js_files))
            
            self.log(f"Found {len(js_files)} JavaScript files", "success")
            
            # 4.4 Secrets in JS
            if self.tools['gf']['available']:
                self.log("Searching for secrets in JavaScript...", "info")
                for js_file in js_files[:20]:
                    result = self.run_command(
                        ["curl", "-s", js_file],
                        timeout=30
                    )
                    if result and result.stdout:
                        patterns = [
                            (r'(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)["\']?\s*[:=]\s*["\'][^"\']{10,}["\']', 'API_KEY'),
                            (r'(?i)password["\']?\s*[:=]\s*["\'][^"\']+["\']', 'PASSWORD'),
                            (r'(?i)bearer\s+[a-zA-Z0-9\-_\.]+', 'BEARER_TOKEN'),
                            (r'ghp_[a-zA-Z0-9]{36}', 'GITHUB_TOKEN'),
                            (r'xox[baprs]-[a-zA-Z0-9]{10,}', 'SLACK_TOKEN'),
                        ]
                        
                        for pattern, ptype in patterns:
                            matches = re.findall(pattern, result.stdout)
                            if matches:
                                for match in matches:
                                    self.results['secrets'].append({
                                        'type': ptype,
                                        'url': js_file,
                                        'match': match
                                    })
        
        self.results['urls'] = list(set(all_urls))
        self.log(f"Found {len(self.results['urls'])} total URLs", "success")
        
        with open(self.output_dir / "recon/urls/all_urls.txt", 'w') as f:
            f.write('\n'.join(sorted(self.results['urls'])))
        
        return all_urls
    
    def phase5_vulnerability_scanning(self):
        """Phase 5: Vulnerability Scanning"""
        self.log("=" * 60, "header")
        self.log("PHASE 5: VULNERABILITY SCANNING", "header")
        self.log("=" * 60, "header")
        
        vulnerabilities = []
        alive_urls = self.results.get('urls', [])
        
        if not alive_urls:
            self.log("No URLs found. Skipping vulnerability scan.", "warning")
            return vulnerabilities
        
        # 5.1 Nuclei - Template-based scanning
        if self.tools['nuclei']['available']:
            self.log("Running Nuclei (Template Scanning)...", "info")
            
            self.run_command(
                ["nuclei", "-l", str(self.output_dir / "recon/web/httpx_alive.txt"),
                 "-o", str(self.output_dir / "recon/vulnerabilities/nuclei_results.txt"),
                 "-t", "cves/", "-t", "vulnerabilities/", "-silent", "-stats"],
                timeout=1800
            )
            
            nuclei_output = self.output_dir / "recon/vulnerabilities/nuclei_results.txt"
            if nuclei_output.exists():
                with open(nuclei_output) as f:
                    for line in f:
                        vulnerabilities.append({
                            'tool': 'nuclei',
                            'finding': line.strip()
                        })
        
        # 5.2 Dalfox - XSS Scanning
        if self.tools['dalfox']['available']:
            self.log("Running Dalfox (XSS Scanning)...", "info")
            
            for url in alive_urls[:50]:
                output = self.output_dir / "recon/vulnerabilities/dalfox_temp.txt"
                
                result = self.run_command(
                    ["dalfox", "url", url, "-o", str(output)],
                    timeout=120
                )
                
                if output.exists():
                    with open(output) as f:
                        for line in f:
                            vulnerabilities.append({
                                'tool': 'dalfox',
                                'finding': line.strip()
                            })
        
        # 5.3 SQLMap
        if self.tools['sqlmap']['available']:
            self.log("Running SQLMap (SQL Injection Testing)...", "info")
            
            for url in alive_urls[:20]:
                self.run_command(
                    ["sqlmap", "-u", url, "--batch", "--random-agent",
                     "-o", "--smart", "--level=1", "--risk=1",
                     "-o", str(self.output_dir / "recon/vulnerabilities/sqlmap_results.txt")],
                    timeout=600
                )
        
        # 5.4 SSRF Testing
        self.log("Testing for SSRF vulnerabilities...", "info")
        ssrf_payloads = [
            "http://127.0.0.1",
            "http://localhost",
            "http://169.254.169.254/latest/meta-data/",
        ]
        
        for url in alive_urls[:30]:
            parsed = urlparse(url)
            test_url = f"{parsed.scheme}://{parsed.netloc}/{ssrf_payloads[0]}"
            
            result = self.run_command(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", test_url],
                timeout=30
            )
            
            if result and result.stdout.strip() in ['200', '301', '302', '400']:
                vulnerabilities.append({
                    'tool': 'manual',
                    'type': 'SSRF_POSSIBLE',
                    'url': url,
                    'payload': ssrf_payloads[0]
                })
        
        self.results['vulnerabilities'] = vulnerabilities
        self.log(f"Found {len(vulnerabilities)} potential vulnerabilities", "success")
        
        return vulnerabilities
    
    def generate_report(self):
        """Generate final report"""
        self.log("=" * 60, "header")
        self.log("GENERATING FINAL REPORT", "header")
        self.log("=" * 60, "header")
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        report = f"""
{G_NEON}{'=' * 80}{RESET}
{G_NEON}                    ILUSION - RECONNAISSANCE REPORT{G_BRIGHT}{RESET}
{G_NEON}{'=' * 80}{RESET}

Target:           {self.target}
Scope:            {', '.join(self.scope) if self.scope else 'All subdomains'}
Scan Date:        {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
Duration:         {duration}

{G_NEON}{'=' * 80}{RESET}
{G_NEON}                           SUMMARY STATISTICS{G_BRIGHT}{RESET}
{G_NEON}{'=' * 80}{RESET}

{G_BRIGHT}Subdomains Found:{RESET}     {len(self.results['subdomains'])}
{G_BRIGHT}Ports Discovered:{RESET}     {len(self.results['ports'])}
{G_BRIGHT}Alive Web Hosts:{RESET}      {len(self.results['urls'])}
{G_BRIGHT}Vulnerabilities:{RESET}      {len(self.results['vulnerabilities'])}
{G_BRIGHT}Secrets Found:{RESET}        {len(self.results['secrets'])}

{G_NEON}{'=' * 80}{RESET}
{G_NEON}                           SUBDOMAINS{G_BRIGHT}{RESET}
{G_NEON}{'=' * 80}{RESET}

"""
        
        if self.results['subdomains']:
            for sub in sorted(self.results['subdomains'])[:100]:
                report += f"  {G_BRIGHT}•{RESET} {sub}\n"
            if len(self.results['subdomains']) > 100:
                report += f"\n  {YELLOW}... and {len(self.results['subdomains']) - 100} more{RESET}\n"
        
        report += f"""


{G_NEON}{'=' * 80}{RESET}
{G_NEON}                           VULNERABILITIES{G_BRIGHT}{RESET}
{G_NEON}{'=' * 80}{RESET}

"""
        
        if self.results['vulnerabilities']:
            for i, vuln in enumerate(self.results['vulnerabilities'][:50], 1):
                report += f"  {MAGENTA}[{i}]{RESET} {vuln.get('tool', 'Unknown').upper()}\n"
                report += f"      {vuln.get('finding', vuln.get('type', 'N/A'))}\n"
                if 'url' in vuln:
                    report += f"      URL: {vuln['url']}\n"
                report += "\n"
        else:
            report += "  No vulnerabilities found.\n"
        
        report += f"""


{G_NEON}{'=' * 80}{RESET}
{G_NEON}                           SECRETS FOUND{G_BRIGHT}{RESET}
{G_NEON}{'=' * 80}{RESET}

"""
        
        if self.results['secrets']:
            for secret in self.results['secrets']:
                report += f"  {RED}Type:{RESET} {secret.get('type', 'Unknown')}\n"
                report += f"  {RED}URL:{RESET} {secret.get('url', 'N/A')}\n"
                report += f"  {RED}Match:{RESET} {secret.get('match', 'N/A')[:50]}...\n\n"
        else:
            report += "  No secrets found.\n"
        
        report += f"""


{G_NEON}{'=' * 80}{RESET}
{G_NEON}                           OUTPUT FILES{G_BRIGHT}{RESET}
{G_NEON}{'=' * 80}{RESET}

  Recon Data:    {self.output_dir}/recon/
  Reports:       {self.output_dir}/reports/
  Screenshots:   {self.output_dir}/recon/screenshots/

{G_NEON}{'=' * 80}{RESET}
{G_NEON}             Generated by ILUSION Recon Framework{G_BRIGHT}{RESET}
{G_NEON}{'=' * 80}{RESET}
"""
        
        # Save reports
        report_file = self.output_dir / "reports/full_report.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        # JSON report
        json_report = {
            "target": self.target,
            "scan_date": self.start_time.isoformat(),
            "duration_seconds": duration.total_seconds(),
            "subdomains": self.results['subdomains'],
            "ports": self.results['ports'],
            "urls": self.results['urls'],
            "vulnerabilities": self.results['vulnerabilities'],
            "secrets": self.results['secrets']
        }
        
        json_file = self.output_dir / "reports/report.json"
        with open(json_file, 'w') as f:
            json.dump(json_report, f, indent=2)
        
        # CSV for vulnerabilities
        csv_file = self.output_dir / "reports/vulnerabilities.csv"
        if self.results['vulnerabilities']:
            with open(csv_file, 'w') as f:
                f.write("Tool,Type,URL,Finding\n")
                for v in self.results['vulnerabilities']:
                    f.write(f"{v.get('tool', '')},{v.get('type', '')},{v.get('url', '')},{v.get('finding', '')}\n")
        
        self.log(f"Report saved to: {report_file}", "success")
        self.log(f"JSON data saved to: {json_file}", "success")
        
        print(report)
        
        return report
    
    def print_pipeline_flow(self):
        """Print the pipeline flow diagram"""
        pipeline = f"""
{G_CYAN}┌──────────────────────────────────────────────────────────────────────────────┐
│                           {YELLOW}SCAN PIPELINE FLOW{G_CYAN}                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────┐              │
│  │                    {WHITE}INPUT: Target Domain{G_CYAN}                     │              │
│  └─────────────────────────────────────────────────────────────┘              │
│                              ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐              │
│  │           {G_BRIGHT}PHASE 1: RECONNAISSANCE{G_CYAN}                            │              │
│  │                                                             │              │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │              │
│  │  │Passive  │  │Active   │  │Certificate│  │ DNS     │        │              │
│  │  │Sources  │  │Bruteforce│ │Analysis  │  │Analysis │        │              │
│  │  │(subfinder)│ │(amass) │  │(crt.sh) │  │(dnsx)  │        │              │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │              │
│  │        ↓           ↓           ↓           ↓               │              │
│  │  ┌─────────────────────────────────────────────────┐      │              │
│  │  │              Subdomain Validation                │      │              │
│  │  │              (dnsx resolution)                   │      │              │
│  │  └─────────────────────────────────────────────────┘      │              │
│  └─────────────────────────────────────────────────────────────┘              │
│                              ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐              │
│  │           {G_BRIGHT}PHASE 2: PORT SCANNING{G_CYAN}                             │              │
│  │                                                             │              │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │              │
│  │  │ naabu   │  │ masscan │  │  nmap   │                     │              │
│  │  │ (top100)│  │ (1-10k) │  │ (detailed)│                     │              │
│  │  └─────────┘  └─────────┘  └─────────┘                     │              │
│  └─────────────────────────────────────────────────────────────┘              │
│                              ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐              │
│  │           {G_BRIGHT}PHASE 3: WEB DISCOVERY{G_CYAN}                            │              │
│  │                                                             │              │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │              │
│  │  │  httpx  │  │gowitness│  │  ffuf   │  │dirsearch│        │              │
│  │  │ (probe) │  │(screens)│  │ (fuzz) │  │ (dirs) │        │              │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │              │
│  └─────────────────────────────────────────────────────────────┘              │
│                              ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐              │
│  │           {G_BRIGHT}PHASE 4: ARCHIVE ANALYSIS{G_CYAN}                         │              │
│  │                                                             │              │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │              │
│  │  │ waymore │  │   gau   │  │ JS Files│  │ Secrets │        │              │
│  │  │  urls   │  │         │  │ Analysis│  │ Finder │        │              │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │              │
│  └─────────────────────────────────────────────────────────────┘              │
│                              ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐              │
│  │           {G_BRIGHT}PHASE 5: VULNERABILITY SCANNING{G_CYAN}                    │              │
│  │                                                             │              │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │              │
│  │  │  nuclei │  │ dalfox  │  │ sqlmap  │  │  manual │        │              │
│  │  │(templates)│ │  (XSS) │  │ (SQLi) │  │  scans  │        │              │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │              │
│  │                                                             │              │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │              │
│  │  │  SSRF   │  │  SSTI   │  │  CORS   │  │ Takeover│        │              │
│  │  │  scan   │  │  scan   │  │  scan   │  │  scan   │        │              │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │              │
│  └─────────────────────────────────────────────────────────────┘              │
│                              ↓                                               │
│  ┌─────────────────────────────────────────────────────────────┐              │
│  │                    {WHITE}REPORT GENERATION{G_CYAN}                         │              │
│  │                                                             │              │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │              │
│  │  │  TXT Full  │  │    JSON    │  │    CSV     │            │              │
│  │  │  Report    │  │  Export    │  │  Vuln CSV  │            │              │
│  │  └────────────┘  └────────────┘  └────────────┘            │              │
│  └─────────────────────────────────────────────────────────────┘              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘{RESET}
"""
        print(pipeline)
    
    def run(self):
        """Run the complete reconnaissance pipeline"""
        self.print_pipeline_flow()
        
        self.log(f"Starting reconnaissance on: {self.target}", "header")
        self.log(f"Output directory: {self.output_dir}", "info")
        self.log(f"Threads: {self.threads}", "info")
        self.log(f"Scope: {', '.join(self.scope) if self.scope else 'All subdomains'}", "info")
        
        try:
            # Phase 1: Reconnaissance
            self.phase1_reconnaissance()
            
            # Phase 2: Port Scanning (uncomment to enable)
            # self.phase2_port_scanning()
            
            # Phase 3: Web Discovery (uncomment to enable)
            # self.phase3_web_discovery()
            
            # Phase 4: Archive Analysis (uncomment to enable)
            # self.phase4_archive_analysis()
            
            # Phase 5: Vulnerability Scanning (uncomment to enable)
            # self.phase5_vulnerability_scanning()
            
            # Generate Report
            self.generate_report()
            
            self.log("Reconnaissance completed successfully!", "success")
            
        except KeyboardInterrupt:
            self.log("Scan interrupted by user", "warning")
            self.generate_report()
            sys.exit(0)
        except Exception as e:
            self.log(f"Error during reconnaissance: {e}", "error")
            if self.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)

def main():
    # Show the cool banner first
    show_banner()
    
    parser = argparse.ArgumentParser(
        description='\nILUSION - Advanced Bug Bounty Reconnaissance Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 illusion.py example.com -s example.com,*.example.com
  python3 illusion.py https://example.com -o /tmp/ilus_recon -t 100 -v
  python3 illusion.py example.com --all

Phases:
  [1] Reconnaissance    - Subdomain enumeration
  [2] Port Scanning    - Service discovery
  [3] Web Discovery    - Screenshots, fuzzing
  [4] Archive Analysis - URL extraction, JS analysis
  [5] Vuln Scanning     - Nuclei, Dalfox, SQLMap
  [6] Reporting        - Generate reports
        """
    )
    
    parser.add_argument('target', help='Target domain (e.g., example.com)')
    parser.add_argument('-s', '--scope', help='Scope domains (comma separated)')
    parser.add_argument('-o', '--output', default='/tmp/illusion_recon', help='Output directory')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--no-subs', action='store_true', help='Skip subdomain enumeration')
    parser.add_argument('--no-ports', action='store_true', help='Skip port scanning')
    parser.add_argument('--no-web', action='store_true', help='Skip web discovery')
    parser.add_argument('--no-vuln', action='store_true', help='Skip vulnerability scanning')
    parser.add_argument('--all', action='store_true', help='Run all phases')
    
    args = parser.parse_args()
    
    # Parse target
    target = args.target
    if target.startswith('http://') or target.startswith('https://'):
        target = urlparse(target).netloc
    
    # Run reconnaissance
    recon = IlusionRecon(
        target=target,
        scope=args.scope,
        output_dir=args.output,
        threads=args.threads,
        verbose=args.verbose
    )
    
    recon.run()

if __name__ == "__main__":
    main()
