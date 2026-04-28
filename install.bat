@echo off
REM ============================================================================
REM Gestao de Atividades - Instalador Automatico
REM Este script cria o ambiente virtual, instala dependencias e compila o .exe
REM ============================================================================

echo.
echo ========================================
echo  Gestao de Atividades - Instalador
echo ========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.8 ou superior em https://python.org
    pause
    exit /b 1
)

echo [1/5] Python encontrado!
python --version

REM Criar diretorio de instalacao
set INSTALL_DIR=%~dp0
cd /d "%INSTALL_DIR%"

REM Criar ambiente virtual se nao existir
if not exist ".venv" (
    echo.
    echo [2/5] Criando ambiente virtual...
    python -m venv .venv
) else (
    echo.
    echo [2/5] Ambiente virtual ja existe!
)

REM Ativar ambiente virtual
echo [3/5] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instalar dependencias (suprimindo saidas desnecessarias)
echo.
echo [4/5] Instalando dependencias...
call .venv\Scripts\python.exe -m pip install --upgrade pip --quiet 2>nul
call .venv\Scripts\pip.exe install -r requirements.txt --quiet 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ERRO ao instalar dependencias. Tentando novamente...
    call .venv\Scripts\pip.exe install plyer pyinstaller openpyxl
)

REM Compilar executavel
echo.
echo [5/5] Compilando executavel .exe...
pyinstaller --onefile --windowed --name "GestaoDeAtividades" --icon=NONE gestao_atividades.py

REM Verificar se compilacao foi bem sucedida
if exist "dist\GestaoDeAtividades.exe" (
    echo.
    echo ========================================
    echo  INSTALACAO CONCLUIDA COM SUCESSO!
    echo ========================================
    echo.
    echo O executavel foi criado em: %INSTALL_DIR%dist\GestaoDeAtividades.exe
    echo.
    echo Para iniciar o programa:
    echo   1. Execute: dist\GestaoDeAtividades.exe
    echo   2. Ou crie um atalho na area de trabalho
    echo.
    
    REM Perguntar se deseja criar atalho na inicializacao
    set /p CREATE_STARTUP="Deseja adicionar o programa para iniciar com o Windows? (S/N): "
    if /i "%CREATE_STARTUP%"=="S" (
        echo.
        echo Adicionando ao startup do Windows...
        
        REM Criar atalho no startup
        set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
        powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_DIR%\GestaoDeAtividades.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%dist\GestaoDeAtividades.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%dist'; $Shortcut.Save()"
        
        echo Atalho criado no startup do Windows!
    )
    
    echo.
    echo ========================================
    echo  Para rodar o sistema agora:
    echo ========================================
    echo.
    echo Opcao 1: Executar o .exe compilado
    echo   dist\GestaoDeAtividades.exe
    echo.
    echo Opcao 2: Rodar como script Python
    echo   python gestao_atividades.py
    echo.
    pause
    
    REM Perguntar se deseja rodar agora
    set /p RUN_NOW="Deseja executar o programa agora? (S/N): "
    if /i "%RUN_NOW%"=="S" (
        echo.
        echo Iniciando Gestao de Atividades...
        start "" "dist\GestaoDeAtividades.exe"
    )
) else (
    echo.
    echo ========================================
    echo  ERRO na compilacao!
    echo ========================================
    echo.
    echo Verifique se todas as dependencias foram instaladas corretamente.
    echo.
    pause
)

REM Desativar ambiente virtual
deactivate >nul 2>&1

exit /b 0
