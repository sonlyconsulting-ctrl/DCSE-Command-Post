[CmdletBinding()]
param(
    [int]$PreferredPort = 8080,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$appRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $appRoot

function Test-PortAvailable {
    param([int]$Port)
    $listener = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        return $true
    }
    catch {
        return $false
    }
    finally {
        if ($listener) {
            $listener.Stop()
        }
    }
}

function Find-ReviewPort {
    param([int]$StartPort)
    foreach ($candidate in $StartPort..($StartPort + 19)) {
        if (Test-PortAvailable -Port $candidate) {
            return $candidate
        }
    }
    throw "No available local port was found between $StartPort and $($StartPort + 19)."
}

function Get-PythonCommand {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        try {
            & $python.Source --version *> $null
            if ($LASTEXITCODE -eq 0) {
                return @($python.Source)
            }
        }
        catch {}
    }

    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        try {
            & $py.Source -3 --version *> $null
            if ($LASTEXITCODE -eq 0) {
                return @($py.Source, "-3")
            }
        }
        catch {}
    }

    return $null
}

try {
    $port = Find-ReviewPort -StartPort $PreferredPort
    $url = "http://127.0.0.1:$port/"
    $pythonCommand = @(Get-PythonCommand)

    Write-Host ""
    Write-Host "Vow & Go local review" -ForegroundColor Cyan
    Write-Host "Folder: $appRoot"
    Write-Host "URL:    $url"
    Write-Host "Stop:   Press Ctrl+C in this window."
    Write-Host ""

    if (-not $NoBrowser) {
        Start-Process $url
    }

    if ($pythonCommand) {
        $executable = $pythonCommand[0]
        $prefixArguments = @()
        if ($pythonCommand.Count -gt 1) {
            $prefixArguments = $pythonCommand[1..($pythonCommand.Count - 1)]
        }
        Write-Host "Starting the Python review server..." -ForegroundColor Green
        & $executable @prefixArguments -m http.server $port --bind 127.0.0.1 --directory $appRoot
        exit $LASTEXITCODE
    }

    Write-Warning "Python is unavailable. Trying the included Node.js static-server fallback."
    $node = Get-Command node -ErrorAction SilentlyContinue
    if (-not $node) {
        throw "Python and Node.js are unavailable. Install Python 3, then double-click START_VOW_AND_GO.cmd again."
    }

    & $node.Source (Join-Path $appRoot "tools\static-server.mjs") --port $port
    exit $LASTEXITCODE
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
