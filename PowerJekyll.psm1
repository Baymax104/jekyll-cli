
function blog {
    $Location = Get-Location
    Set-Location -Path "$PSScriptRoot\core"
    try {
        Invoke-Expression "python '$PSScriptRoot\core\main.py' $args"
    } finally {
        Set-Location -Path $Location
    }
}

Register-ArgumentCompleter -Native -CommandName blog -ScriptBlock {
    param($commandName, $wordToComplete, $cursorPosition)

    # set environment varaible for autocomplete()
    $completion_file = New-TemporaryFile
    $env:ARGCOMPLETE_USE_TEMPFILES = 1
    $env:_ARGCOMPLETE_STDOUT_FILENAME = $completion_file
    $env:COMP_LINE = $wordToComplete
    $env:COMP_POINT = $cursorPosition
    $env:_ARGCOMPLETE = 1
    $env:_ARGCOMPLETE_SUPPRESS_SPACE = 0
    $env:_ARGCOMPLETE_IFS = "`n"
    $env:_ARGCOMPLETE_SHELL = "powershell"

    # execute script
    blog 2>&1 | Out-Null

    # get completions from $completion_file and output the completion
    Get-Content $completion_file -Encoding GBK | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, "ParameterValue", $_)
    }
    Remove-Item $completion_file, Env:\_ARGCOMPLETE_STDOUT_FILENAME, Env:\ARGCOMPLETE_USE_TEMPFILES, Env:\COMP_LINE, Env:\COMP_POINT, Env:\_ARGCOMPLETE, Env:\_ARGCOMPLETE_SUPPRESS_SPACE, Env:\_ARGCOMPLETE_IFS, Env:\_ARGCOMPLETE_SHELL
}

Export-ModuleMember -Function blog