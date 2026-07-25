@echo off
chcp 65001 >nul
title Publicar la web de Angelica
cd /d "%~dp0"

echo ============================================
echo   PUBLICANDO LA WEB EN INTERNET
echo ============================================
echo.
echo Esto puede tardar un minuto. No cierres la ventana.
echo.

echo [1/3] Creando el repositorio y subiendo la web...
gh repo create psicologia-angelica --public --source=. --push > "publicar-log.txt" 2>&1
echo    (resultado guardado en publicar-log.txt)
echo.

echo [2/3] Activando la pagina web...
gh api -X POST repos/nuestrosproyectos/psicologia-angelica/pages -f "source[branch]=main" -f "source[path]=/" >> "publicar-log.txt" 2>&1
echo.

echo [3/3] Comprobando...
gh repo view nuestrosproyectos/psicologia-angelica --json name,url >> "publicar-log.txt" 2>&1

echo.
echo ============================================
echo   RESULTADO
echo ============================================
type "publicar-log.txt"
echo.
echo ============================================
echo.
echo Tu enlace (espera 2-3 minutos a que se active):
echo.
echo    https://nuestrosproyectos.github.io/psicologia-angelica/
echo.
echo ============================================
echo.
echo Ya puedes volver al chat y escribir "ya".
echo.
pause
