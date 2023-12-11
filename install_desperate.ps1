# Install Python 3.10
winget install -e --id Python.Python.3.10

# Attempt to install Python requirements
Try {
    pip install -r .\requirements.txt
} Catch {
    Write-Host "An error occurred during pip install. Please relog your account and try running the script again."
    Exit
}

# Download and install CMake
$cmakeInstaller = "https://github.com/Kitware/CMake/releases/download/v3.28.0/cmake-3.28.0-windows-x86_64.msi"
$installerPath = "$env:TEMP\cmake_installer.msi"
Invoke-WebRequest -Uri $cmakeInstaller -OutFile $installerPath
Start-Process msiexec.exe -Wait -ArgumentList "/i $installerPath /quiet /norestart"

# Build llama.cpp with CMake
if (Test-Path -Path ".\llama.cpp") {
    New-Item -Path ".\llama.cpp\build" -ItemType "directory" -Force
    Set-Location -Path ".\llama.cpp\build"
    cmake .. -DLLAMA_CUBLAS=ON
    cmake --build . --config Release
    Set-Location -Path "..\.."
}

# Install aria2
winget install --id=aria2.aria2 -e


# Remove .exe extension from all files in the llama.cpp directory
Get-ChildItem -Path ".\llama.cpp" -Recurse -Filter *.exe | ForEach-Object {
    $newName = $_.FullName -replace '\.exe$', ''
    Rename-Item $_.FullName -NewName $newName
}


# Final message
Write-Host "Unfortunately, you chose to use Windows. This OS is not supported with Ollama but you can still use this program to interface with an Ollama endpoint or use the quantizing features."
