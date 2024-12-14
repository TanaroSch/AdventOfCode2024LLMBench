@echo off
setlocal enabledelayedexpansion

echo Starting execution sequence...

:: Step 1: Try to activate either Conda environment
echo Attempting to activate Conda environment...
call conda activate AdventOfCode 2>nul
if errorlevel 1 (
    echo AdventOfCode environment not found, trying AoC...
    call conda activate AoC 2>nul
    if errorlevel 1 (
        echo Error: Failed to activate either AdventOfCode or AoC environment
        echo Available environments:
        conda env list
        exit /b 1
    )
    echo Successfully activated AoC environment.
) else (
    echo Successfully activated AdventOfCode environment.
)

:: Step 2: Run Python script for table generation
echo Running visualize_results.py...
python visualize_results.py
if errorlevel 1 (
    echo Error: Failed to execute visualize_results.py
    exit /b 1
)
echo visualize_results.py completed successfully.

:: Step 3: Run first Python script
echo Running update_readme.py...
python update_readme.py
if errorlevel 1 (
    echo Error: Failed to execute update_readme.py
    exit /b 1
)
echo update_readme.py completed successfully.

echo All operations completed successfully!
pause