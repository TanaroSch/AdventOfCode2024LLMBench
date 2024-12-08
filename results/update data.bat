@echo off
setlocal enabledelayedexpansion

echo Starting execution sequence...

:: Step 1: Run Node.js script
echo Running generate_table.js...
node generate_table.js
if errorlevel 1 (
    echo Error: Failed to execute generate_table.js
    exit /b 1
)
echo Node.js script completed successfully.

:: Step 2: Activate Conda environment
echo Activating Conda environment "AdventOfCode"...
call conda activate AdventOfCode
if errorlevel 1 (
    echo Error: Failed to activate Conda environment "AdventOfCode"
    exit /b 1
)
echo Conda environment activated successfully.

:: Step 3: Run first Python script
echo Running update_readme.py...
python update_readme.py
if errorlevel 1 (
    echo Error: Failed to execute update_readme.py
    exit /b 1
)
echo update_readme.py completed successfully.

:: Step 4: Run second Python script
echo Running visualize_results.py...
python visualize_results.py
if errorlevel 1 (
    echo Error: Failed to execute visualize_results.py
    exit /b 1
)
echo visualize_results.py completed successfully.

echo All operations completed successfully!
pause