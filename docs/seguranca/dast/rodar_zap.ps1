# Executa a varredura DAST do TrackVault com o OWASP ZAP (Windows PowerShell).
#
# Uso, na raiz do repositório:
#   powershell -ExecutionPolicy Bypass -File docs\seguranca\dast\rodar_zap.ps1 -Rodada 1-inicial
#   powershell -ExecutionPolicy Bypass -File docs\seguranca\dast\rodar_zap.ps1 -Rodada 2-final
#
# Gera em docs\seguranca\dast\<Rodada>\: relatórios HTML/JSON/MD do ZAP,
# o log completo da execução e execucao.txt (data, duração, commit, versões).

param(
    [Parameter(Mandatory = $true)][ValidateSet('1-inicial', '2-final')][string]$Rodada,
    [string]$Zap = 'C:\Program Files\ZAP\Zed Attack Proxy\zap.bat'
)

$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$saida = Join-Path $base $Rodada
$plano = Join-Path $base 'zap-plano.yaml'
$homeZap = Join-Path $env:TEMP "zap-trackvault-$Rodada"

if (-not (Test-Path $Zap)) { throw "ZAP não encontrado em $Zap" }
New-Item -ItemType Directory -Force $saida | Out-Null
if (Test-Path $homeZap) { Remove-Item -Recurse -Force $homeZap }

$env:RELATORIO_DIR = $saida
$versaoZap = (Get-ChildItem (Split-Path $Zap) -Filter 'zap-*.jar' | Select-Object -First 1).BaseName
$commit = (git rev-parse --short HEAD).Trim()
$inicio = Get-Date

Write-Host "Alvo: https://trackvault-3hpa.onrender.com | Rodada: $Rodada | Commit: $commit | $versaoZap"
Write-Host 'A varredura leva de 30 a 60 minutos. Não feche esta janela.'

# O zap.bat procura o .jar na pasta atual: executa a partir da pasta do ZAP.
# -cmd: sem interface gráfica | -port/-dir: não conflita com um ZAP aberto
# Mensagens do Java no stderr não devem interromper o script.
$ErrorActionPreference = 'Continue'
Push-Location (Split-Path $Zap)
try {
    & $Zap -cmd -port 8095 -dir $homeZap -autorun $plano 2>&1 |
        ForEach-Object { "$_" } |
        Tee-Object -FilePath (Join-Path $saida 'zap-execucao.log')
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}
$fim = Get-Date

@"
Ferramenta: OWASP ZAP ($versaoZap), Automation Framework, modo -cmd
Plano: docs/seguranca/dast/zap-plano.yaml
Alvo: https://trackvault-3hpa.onrender.com (aplicação do próprio grupo)
Commit implantado no momento da varredura: $commit (branch main)
Início: $($inicio.ToString('dd/MM/yyyy HH:mm:ss'))
Fim: $($fim.ToString('dd/MM/yyyy HH:mm:ss'))
Duração: $([math]::Round(($fim - $inicio).TotalMinutes, 1)) min
Código de saída do ZAP: $codigo
Executado por: $(git config user.name)
"@ | Set-Content -Encoding utf8 (Join-Path $saida 'execucao.txt')

Write-Host "Concluído em $([math]::Round(($fim - $inicio).TotalMinutes, 1)) min. Relatórios em $saida"
