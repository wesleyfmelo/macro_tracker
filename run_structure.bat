@echo off
echo ===================================================
echo Criando estrutura de arquivos do Macro Tracker (OO)
echo ===================================================

:: 1. Criar Diretórios
mkdir data
mkdir reports
mkdir src
mkdir src\fetchers
mkdir src\pipeline
mkdir src\reporting
mkdir src\reporting\templates
mkdir app
mkdir app\components
mkdir app\pages

echo [OK] Pastas criadas com sucesso.

:: 2. Criar Arquivos de Configuração da Raiz
type nul > .env
type nul > README.md
type nul > requirements.txt

:: Criar .gitignore padrão para Python e SQLite
(
echo .venv/
echo __pycache__/
echo *.pyc
echo .env
echo data/*.db
echo reports/*.pdf
) > .gitignore

echo [OK] Arquivos da raiz e .gitignore criados.

:: 3. Criar Arquivos do Código Fonte (src/)
type nul > src\__init__.py

type nul > src\fetchers\__init__.py
type nul > src\fetchers\base.py
type nul > src\fetchers\bcb.py
type nul > src\fetchers\ibge.py
type nul > src\fetchers\scrapers.py

type nul > src\pipeline\__init__.py
type nul > src\pipeline\db.py
type nul > src\pipeline\pipeline.py
type nul > src\pipeline\processor.py

type nul > src\reporting\__init__.py
type nul > src\reporting\generator.py
type nul > src\reporting\templates\report.html
type nul > src\reporting\templates\styles.css

echo [OK] Modulos da pasta src/ e subpastas criados.

:: 4. Criar Arquivos da Interface (app/)
type nul > app\__init__.py
type nul > app\main.py
type nul > app\config.py

type nul > app\components\__init__.py
type nul > app\components\cards.py
type nul > app\components\charts.py

type nul > app\pages\__init__.py
type nul > app\pages\1_📊_Mercado_Financeiro.py
type nul > app\pages\2_🏭_Economia_Real.py
type nul > app\pages\3_🧠_Sondagens_e_Expectativas.py
type nul > app\pages\4_📄_Emissao_de_Relatorio.py

echo [OK] Estrutura do Streamlit (app/) criada.

echo ===================================================
echo Estrutura concluida com sucesso!
echo ===================================================
pause