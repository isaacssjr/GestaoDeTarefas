@echo off
chcp 65001 >nul
echo ==========================================
echo   Instalador - Gestao de Atividades TI
echo ==========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado! Instale o Python 3.x e marque 'Add to PATH'.
    pause
    exit /b 1
)

echo [1/4] Configurando ambiente virtual...
if not exist .venv (
    python -m venv .venv
)

echo [2/4] Ativando ambiente e atualizando pip...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet

echo [3/4] Instalando dependencias (plyer, openpyxl, pyinstaller)...
call .venv\Scripts\python.exe -m pip install -r requirements.txt --quiet

echo [4/4] Gerando executavel .exe...
call .venv\Scripts\pyinstaller --onefile --windowed --name "GestaoAtividades" --icon=NONE gestao_atividades.py --clean --quiet

if exist dist\GestaoAtividades.exe (
    echo.
    echo SUCESSO! Executavel criado em: dist\GestaoAtividades.exe
    echo.
    echo Deseja criar um atalho na Area de Trabalho?
    set /p createShortcut="(S/N): "
    if /i "%createShortcut%"=="S" (
        echo Set WshShell = CreateObject("WScript.Shell") > shortcut.vbs
        echo WshShell.CreateShortcut("%USERPROFILE%\Desktop\GestaoAtividades.lnk").TargetPath = "%CD%\dist\GestaoAtividades.exe" >> shortcut.vbs
        echo WshShell.WorkingDirectory = "%CD%\dist" >> shortcut.vbs
        echo WshShell.Save >> shortcut.vbs
        cscript //nologo shortcut.vbs
        del shortcut.vbs
        echo Atalho criado!
    )
    
    echo.
    echo Para iniciar agora, digite:
    echo   dist\GestaoAtividades.exe
) else (
    echo Erro ao compilar. Verifique se houve mensagens de erro acima.
)

echo.
pause
