@echo off
chcp 65001 >nul

REM Muda para o diretorio onde o script esta localizado
cd /d "%~dp0"

echo ==========================================
echo   Gestao de Atividades TI - Instalador
echo ==========================================
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado! Instale o Python 3.8+.
    pause
    exit /b 1
)

echo [1/5] Criando ambiente virtual (.venv)...
if not exist .venv (
    python -m venv .venv
) else (
    echo Ambiente virtual ja existe.
)

echo [2/5] Ativando ambiente e atualizando pip...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet

echo [3/5] Instalando dependencias...
call .venv\Scripts\python.exe -m pip install -r requirements.txt

echo [4/5] Testando a aplicacao...
call .venv\Scripts\python.exe -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK!')"

echo [5/5] Gerando executavel .exe...
call .venv\Scripts\pyinstaller --onefile --windowed --name "GestaoAtividades" main.py --clean

if exist dist\GestaoAtividades.exe (
    echo.
    echo ==========================================
    echo   SUCESSO!
    echo ==========================================
    echo Executavel criado em: dist\GestaoAtividades.exe
    echo.
    
    echo Deseja criar atalho na Area de Trabalho?
    set /p createShortcut="(S/N): "
    if /i "%createShortcut%"=="S" (
        powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\GestaoAtividades.lnk'); $Shortcut.TargetPath = '%CD%\dist\GestaoAtividades.exe'; $Shortcut.WorkingDirectory = '%CD%\dist'; $Shortcut.Save()"
        echo Atalho criado!
    )
    
    echo.
    echo Deseja configurar para iniciar com o Windows?
    set /p setupStartup="(S/N): "
    if /i "%setupStartup%"=="S" (
        powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\GestaoAtividades.lnk'); $Shortcut.TargetPath = '%CD%\dist\GestaoAtividades.exe'; $Shortcut.WorkingDirectory = '%CD%\dist'; $Shortcut.Save()"
        echo Configurado para iniciar com o Windows!
    )
    
    echo.
    echo Para executar agora, digite:
    echo   dist\GestaoAtividades.exe
) else (
    echo Erro ao compilar. Verifique mensagens acima.
)

echo.
pause
