# DCSE AGY one-shot certification runner
# Task: DCSE-ORCH-20260908-007
# Purpose: host-local credential rotation + one governed worker claim/execution/result cycle.
# No credential value is written to disk or intentionally printed.

[CmdletBinding()]
param(
    [string]$ProjectRef = 'nevgdyfpxdaloacuutal',
    [string]$TaskId = 'DCSE-ORCH-20260908-007'
)

$ErrorActionPreference = 'Stop'
$SupabaseUrl = "https://$ProjectRef.supabase.co"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$WorkerPath = Join-Path $ProjectRoot 'workers\agy-cli-operational.js'
$StdoutLog = Join-Path $ProjectRoot 'agy-certification-worker.log'
$StderrLog = Join-Path $ProjectRoot 'agy-certification-worker-error.log'

$workerSecret = $null
$projectApiKey = $null
$rotationRaw = $null
$keysRaw = $null
$worker = $null

function Get-FirstRow {
    param($Object)
    if ($null -eq $Object) { return $null }
    if ($Object -is [System.Array]) { return $Object | Select-Object -First 1 }
    if ($Object.rows) { return $Object.rows | Select-Object -First 1 }
    if ($Object.data) { return $Object.data | Select-Object -First 1 }
    return $Object
}

try {
    Set-Location $ProjectRoot

    if (-not (Test-Path $WorkerPath)) {
        throw "Worker not found: $WorkerPath"
    }

    $workerText = Get-Content $WorkerPath -Raw
    if ($workerText -notmatch "WORKER_ONCE" -or $workerText -notmatch "WORKER_EXPECT_TASK_ID") {
        throw 'Current worker does not contain bounded one-shot certification support. Pull latest main first.'
    }

    Write-Output 'PREFLIGHT_WORKER_ONESHOT=PASS'

    supabase link --project-ref $ProjectRef | Out-Null
    Write-Output 'PROJECT_LINK=PASS'

    $rotationSql = @'
create or replace function v7_worker.rotate_antigravity_enrollment()
returns table(success boolean, message text, enrollment_secret text)
language plpgsql
security definer
set search_path = ''
as $function$
declare
    v_secret text;
    v_row v7_worker.agent_identity%rowtype;
    v_res record;
begin
    select * into v_row
      from v7_worker.agent_identity
     where agent_id = 'antigravity'
     for update;

    if not found then
        raise exception 'antigravity worker identity is not registered' using errcode = '42501';
    end if;
    if v_row.status <> 'approved' then
        raise exception 'antigravity worker is not approved' using errcode = '42501';
    end if;
    if v_row.auth_user_id is null then
        raise exception 'antigravity worker has no bound auth user' using errcode = '55000';
    end if;
    if not exists (select 1 from auth.users where id = v_row.auth_user_id) then
        raise exception 'bound auth user does not exist' using errcode = '55000';
    end if;

    v_secret := encode(extensions.gen_random_bytes(32), 'base64');

    update auth.users
       set encrypted_password = extensions.crypt(v_secret, extensions.gen_salt('bf', 10)),
           updated_at = now()
     where id = v_row.auth_user_id;

    select * into v_res
      from v7_worker.provision_worker_credential('antigravity', v_row.auth_user_id, v_secret);

    if not coalesce(v_res.success, false) then
        raise exception 'credential rotation failed: %', coalesce(v_res.message, 'unknown error');
    end if;

    return query select true, 'rotated antigravity enrollment credential', v_secret;
end;
$function$;

revoke all on function v7_worker.rotate_antigravity_enrollment() from public, anon, authenticated;
grant execute on function v7_worker.rotate_antigravity_enrollment() to service_role;
'@

    supabase db query $rotationSql --linked | Out-Null
    Write-Output 'ROTATION_FUNCTION=INSTALLED'

    $rotationRaw = supabase db query `
        'select * from v7_worker.rotate_antigravity_enrollment();' `
        --linked --output json

    $rotationObj = $rotationRaw | ConvertFrom-Json
    $rotationRow = Get-FirstRow $rotationObj
    $workerSecret = [string]$rotationRow.enrollment_secret

    if ([string]::IsNullOrWhiteSpace($workerSecret)) {
        throw 'Credential rotation returned no usable in-memory credential.'
    }
    Write-Output 'CREDENTIAL_ROTATION=PASS'

    supabase db query `
        'drop function if exists v7_worker.rotate_antigravity_enrollment();' `
        --linked | Out-Null
    Write-Output 'ROTATION_FUNCTION=REMOVED'

    $keysRaw = supabase projects api-keys --project-ref $ProjectRef --output json
    $keysObj = $keysRaw | ConvertFrom-Json

    if ($keysObj -is [System.Array]) { $keyRows = $keysObj }
    elseif ($keysObj.api_keys) { $keyRows = $keysObj.api_keys }
    elseif ($keysObj.data) { $keyRows = $keysObj.data }
    else { $keyRows = @($keysObj) }

    $pub = $keyRows |
        Where-Object {
            (-not $_.disabled) -and
            ($_.type -eq 'publishable' -or $_.type -eq 'anon' -or $_.name -eq 'anon')
        } |
        Select-Object -First 1

    if (-not $pub) { throw 'No enabled publishable/anon project API key was found.' }
    if ($pub.api_key) { $projectApiKey = [string]$pub.api_key }
    elseif ($pub.key) { $projectApiKey = [string]$pub.key }
    else { throw 'Project API key field could not be resolved.' }
    Write-Output 'PROJECT_API_KEY=RESOLVED'

    $env:SUPABASE_URL = $SupabaseUrl
    $env:SUPABASE_ANON_KEY = $projectApiKey
    $env:WORKER_AGENT_ID = 'antigravity'
    $env:WORKER_ENROLLMENT_SECRET = $workerSecret
    $env:AGY_EXECUTABLE = 'agy.exe'
    $env:AGY_PRINT_TIMEOUT = '120s'
    $env:AGY_PROCESS_TIMEOUT_MS = '150000'
    $env:WORKER_ONCE = '1'
    $env:WORKER_EXPECT_TASK_ID = $TaskId

    Remove-Item $StdoutLog,$StderrLog -ErrorAction SilentlyContinue

    $worker = Start-Process `
        -FilePath 'node' `
        -ArgumentList $WorkerPath `
        -WorkingDirectory $ProjectRoot `
        -RedirectStandardOutput $StdoutLog `
        -RedirectStandardError $StderrLog `
        -PassThru `
        -NoNewWindow `
        -Wait

    Write-Output "WORKER_EXIT_CODE=$($worker.ExitCode)"

    if ($worker.ExitCode -ne 0) {
        throw "STOP_GATE: one-shot worker exited with code $($worker.ExitCode)."
    }

    $resultRaw = supabase db query `
        "select submission_id, task_id, claim_id, agent_id, submission_status, result_event_type, submission_attempted_at from v7_worker.result_submission where task_id = '$TaskId' and agent_id = 'antigravity' order by submission_id desc limit 1;" `
        --linked --output json

    $resultObj = $resultRaw | ConvertFrom-Json
    $resultRow = Get-FirstRow $resultObj

    if (-not $resultRow -or $resultRow.task_id -ne $TaskId) {
        throw 'STOP_GATE: worker exited without a persisted governed result.'
    }

    Write-Output 'RESULT_PERSISTED=PASS'
    Write-Output "TASK=$($resultRow.task_id)"
    Write-Output "CLAIM_ID=$($resultRow.claim_id)"
    Write-Output "RESULT_EVENT=$($resultRow.result_event_type)"
    Write-Output "RESULT_STATUS=$($resultRow.submission_status)"
    Write-Output 'AGY_ONESHOT_CERTIFICATION_EXECUTION=PASS'
}
finally {
    try {
        supabase db query `
            'drop function if exists v7_worker.rotate_antigravity_enrollment();' `
            --linked 2>$null | Out-Null
    } catch {}

    $env:WORKER_ENROLLMENT_SECRET = $null
    $env:SUPABASE_ANON_KEY = $null
    $env:WORKER_ONCE = $null
    $env:WORKER_EXPECT_TASK_ID = $null

    $workerSecret = $null
    $projectApiKey = $null
    $rotationRaw = $null
    $keysRaw = $null

    Write-Output 'PROCESS_CREDENTIALS_CLEARED=PASS'
    Write-Output 'TEMP_ROTATION_SURFACE_REMOVED=PASS'
}
