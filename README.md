🧠 ILUSION — Advanced Reconnaissance Framework

<img width="1280" height="686" alt="photo_5_2026-04-22_23-55-43" src="https://github.com/user-attachments/assets/34d45282-c8c2-4a4c-a935-a0e992efd2af" />

██╗██╗     ██╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗
██║██║     ██║   ██║██╔════╝██║██╔═══██╗████╗  ██║
██║██║     ██║   ██║███████╗██║██║   ██║██╔██╗ ██║
██║██║     ██║   ██║╚════██║██║██║   ██║██║╚██╗██║
██║███████╗╚██████╔╝███████║██║╚██████╔╝██║ ╚████║
╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝

Framework avanzado de reconocimiento para Bug Bounty, Pentesting y Red Team Linux Y Windows 

🚀 Descripción

ILUSION es una herramienta de automatización de reconocimiento diseñada para descubrir superficie de ataque de forma rápida, eficiente y escalable.

Integra múltiples herramientas de seguridad en una sola pipeline, permitiendo:

Enumeración de subdominios
Descubrimiento de servicios
Análisis web
Extracción de endpoints
Detección de vulnerabilidades

🎯 Características
🔄 Pipeline automatizada end-to-end
⚡ Alto rendimiento (multithreading)
🧩 Modular y extensible
🧠 Análisis inteligente de datos
💻 Interfaz CLI con estilo hacker
📊 Generación de reportes (TXT, JSON, CSV)
🧬 Arquitectura

Target → Recon → Ports → Web → URLs → Vulns → Report

Fases:
Fase	Descripción
Reconnaissance	Enumeración de subdominios
Port Scanning	Descubrimiento de servicios
Web Discovery	Hosts activos + fuzzing
Archive Analysis	URLs + JS + secretos
Vulnerability Scanning	CVEs, XSS, SQLi, SSRF
Reporting	Generación de reportes

🧰 Herramientas Integradas

🔍 Reconocimiento
subfinder
amass
assetfinder
crt.sh

🌐 Red
naabu
masscan
nmap

🕸️ Web
httpx
ffuf
dirsearch
gowitness

🧪 Análisis
waymore
gau
gf

💥 Vulnerabilidades
nuclei
dalfox
sqlmap

📦 Instalación
1. Clonar repositorio
git clone https://github.com/HackingTeamOficial/-ILUSION-Advanced-Reconnaissance-Framework.git
cd ilusion
2. Dar permisos
chmod +x illusion.py
3. Instalar dependencias

Asegúrate de tener instaladas las herramientas necesarias (Kali Linux recomendado).

⚡ Uso

python3 illusion.py

Scan básico
sudo python3 illusion.py example.com -s example.com,*.example.com

Scan completo
sudo python3 illusion.py example.com --all

Scan avanzado
sudo python3 illusion.py https://example.com -o /tmp/ilus_recon \ -t 100 \ -v

⚙️ Opciones

Flag	Descripción

-s, --scope	Definir scope
-o, --output	Directorio de salida
-t, --threads	Número de hilos
-v, --verbose	Modo detallado
--all	Ejecutar todas las fases
--no-subs	Omitir subdominios
--no-ports	Omitir puertos
--no-web	Omitir web discovery
--no-vuln	Omitir vulnerabilidades

📊 Output
/recon/
 ├── subdomains/
 ├── ports/
 ├── web/
 ├── urls/
 ├── vulnerabilities/
 └── screenshots/

/reports/
 ├── full_report.txt
 ├── report.json
 └── vulnerabilities.csv

🧪 Ejemplo de Resultados
Subdomains Found:     342
Ports Discovered:     89
Alive Web Hosts:      56
Vulnerabilities:      17
Secrets Found:        3

🧠 Casos de Uso
Bug Bounty
Pentesting Web
Red Team
Asset Discovery
Attack Surface Mapping

⚠️ Disclaimer

Esta herramienta debe utilizarse únicamente en entornos autorizados.

Programas de Bug Bounty
Infraestructura propia
Laboratorios de pruebas

El uso indebido puede ser ilegal.

🛠️ Roadmap

Integración con APIs de Bug Bounty
Dashboard visual
Modo continuo (monitoring)
IA para priorización de vulnerabilidades
Exportación a SIEM

🤝 Contribuciones

Las contribuciones son bienvenidas.

Fork del repositorio
Crear rama (feature/nueva-funcionalidad)
Commit
Pull Request

📜 Licencia

Hacking Team

🏁 Autor
root@illusion:~$ whoami
> AnonSec777 | Haxor | Hack The Planet
>
> 💻🔥 Somos una comunidad de hacking y ciberseguridad donde aprender es parte del juego 🔥💻

🧑‍💻 Aquí encontrarás gente que está empezando y otros que ya están en nivel avanzado, todos compartiendo herramientas, trucos, metodologías y experiencias reales.

🛠 Desde pentesting hasta OSINT, explotación o defensa, tocamos todo lo necesario para crecer en este mundo.

🎯 Nos gusta aprender haciendo: laboratorios, retos, pruebas reales y colaboración constante.

🧠 Nuestros logotipos representan quiénes somos: una comunidad unida por la curiosidad, el conocimiento y las ganas de romper (y entender) sistemas.

🚀 Si te mola la ciberseguridad y quieres subir de nivel rodeado de gente que está en lo mismo que tú… este es tu sitio.

🌐 Página Web:
https://ethical-hacking-team-oficial.vercel.app/

💻 GitHub:
https://github.com/HackingTeamOficial

📲 Telegram:
https://t.me/PlantillasNucleiHackingTeam
https://t.me/HackingTeamGrupoOfficial
https://t.me/+0hHSaKO7eI9mNWY8 (Difusión)
https://t.me/+llcmNGzz6JIyMmI0 (Biblioteca)
https://t.me/TermuxHackingTeam

🐦 X (Twitter):
@HackingTeam777

🦋 Bluesky:
https://bsky.app/profile/hackingteam.bsky.social

💬 Discord:
https://discord.gg/V4nPFbQX

📘 Facebook:
https://www.facebook.com/groups/hackingteam2022/?ref=share
https://www.facebook.com/groups/HackingTeamCyber/?ref=share

🎥 YouTube:
https://www.youtube.com/@HackingTeamOficial/videos

🎵 TikTok:
https://www.tiktok.com/@hackingteamprohackers
https://www.tiktok.com/@hacking.kdea?_t=ZS-8vTtlaQrDTL&_r=1
