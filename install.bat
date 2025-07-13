@echo off

REM Script de Instalação para o Gravador e Transcritor de Áudio

echo Verificando e instalando dependências Python...

pip install PyQt6 sounddevice soundfile numpy openai-whisper pyperclip keyboard

echo.
echo ========================================================================
echo ATENÇÃO: FFmpeg é necessário para o Whisper funcionar corretamente.
echo Por favor, instale o FFmpeg manualmente se ainda não o fez.
echo Você pode baixá-lo de: https://ffmpeg.org/download.html
echo E adicione-o ao PATH do seu sistema.
echo ========================================================================
echo.

echo Instalação concluída. Pressione qualquer tecla para sair.
pause > nul

