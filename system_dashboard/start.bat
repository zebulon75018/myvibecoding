@echo off
echo ==================================
echo   Dashboard Systeme - Installation
echo ==================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Demander si on cree un environnement virtuel
set /p VENV="Voulez-vous creer un environnement virtuel ? (recommande) [O/n] "
if /i "%VENV%"=="o" (
    echo.
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [OK] Environnement virtuel active
)

REM Installer les dependances
echo.
echo [INFO] Installation des dependances...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERREUR] Erreur lors de l'installation des dependances
    pause
    exit /b 1
)

echo [OK] Dependances installees avec succes

REM Lancer l'application
echo.
echo ==================================
echo   Demarrage du Dashboard
echo ==================================
echo.
echo [INFO] L'application sera accessible a : http://localhost:5000
echo        Appuyez sur Ctrl+C pour arreter le serveur
echo.
timeout /t 2 >nul

python app.py
pause
