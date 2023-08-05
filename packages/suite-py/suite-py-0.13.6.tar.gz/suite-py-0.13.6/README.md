# Suite-py

## Installation

Installare il package suite-py da pip
```
pip3 install suite-py
```

crea una directory nella tua home
```
mkdir $HOME/.suite_py
```

copia il contenuto di `.config.yml.dist` (si trova nella root di questo progetto) dentro `$HOME/.suite_py/config.yml` e sostituisci i placeholder con le tue info

NB: `projects_home` deve contenere il path assoluto (es: `projects_home: /home/larrywax/github/primait`)

Al primo avvio ti verranno chiesti i token di accesso di diversi tool, di seguito le guide per generarli:
- github: https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line (selezionare solo i permessi "repo")
- youtrack: https://www.jetbrains.com/help/youtrack/incloud/Manage-Permanent-Token.html (selezionare scope YouTrack)
- slack: https://api.slack.com/custom-integrations/legacy-tokens (loggarsi su Slack e poi visitare la pagina per vedere il token)
- drone:
  - andate su https://drone-1.prima.it
  - cliccate in alto a destra sul vostro profilo
  - selezionate l'opzione token
  - ???
  - profit

## Usage

```
usage: suite-py [-h] [--project PROJECT] {create-branch,lock-project,open-pr,ask-review,create-qa,delete-qa,merge-pr,deploy} ...

positional arguments:
  {create-branch,lock-project,open-pr,ask-review,create-qa,delete-qa,merge-pr,deploy}
                        sub-command help
    create-branch       Crea branch locale e imposta la card di YouTrack in progress
    lock-project        Lock/unlock dei merge sul branch master di un progetto
    open-pr             Apre una PR su GitHub
    ask-review          Chiede la review di una PR
    create-qa           Crea un QA (integrazione con qainit)
    delete-qa           Cancella un QA (integrazione con qainit)
    merge-pr            Merge del branch selezionato con master se tutti i check sono ok
    deploy              Deploy in produzione del branch master

optional arguments:
  -h, --help            show this help message and exit
  --project PROJECT     Nome del progetto su cui eseguire il comando (default directory corrente)
```

## Development

bump up version
```
hatch grow [fix|minor|major]
```

build python package
```
hatch build
```

publish package on pypi
```
hatch release --username your_pypi_username
```

publish on pypi test
```
hatch release --test --username your_pypi_username
```
