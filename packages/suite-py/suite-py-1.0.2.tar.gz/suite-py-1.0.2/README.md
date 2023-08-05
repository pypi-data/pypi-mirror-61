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
(**ATTENZIONE:** `config.yml` _senza_ il punto iniziale nella cartella di destinazione)

**NB:** `projects_home` deve contenere il path assoluto (es: `projects_home: /home/larrywax/github/primait`)

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

Opzionalmente, è possibile configurare:
 - il canale in cui notificare le richieste di review usando la chiave `user.notify_channel` nel file di configurazione.
   Ad esempio:

    ```yml
    user:
      notify_channel: '#void'
    ```
 - lo slug da usare come default quando si crea un branch con `create-branch` (che va come default a `PRIMA-XXX`).
   Ad esempio:

    ```yml
    user:
      default_slug: 'OTHER-'
    ```
 - il timeout per le operazioni che coinvolgono CaptainHook (`ask-review`, `merge-pr` e `lock-project`).
   Ad esempio:

    ```yml
    user:
      captainhook_timeout: 2
    ```


## Usage

```
Usage: suite-py [OPTIONS] COMMAND [ARGS]...

Options:
  --project PATH     Nome del progetto su cui eseguire il comando (default
                     directory corrente)
  --timeout INTEGER  Timeout in secondi per le operazioni di CaptainHook
  --help             Show this message and exit.

Commands:
  ask-review     Chiede la review di una PR
  create-branch  Crea branch locale e imposta la card di YouTrack in...
  create-qa      Crea un QA (integrazione con qainit)
  delete-qa      Cancella un QA (integrazione con qainit)
  deploy         Deploy in produzione del branch master
  lock-project   Lock/unlock dei merge sul branch master di un progetto
  merge-pr       Merge del branch selezionato con master se tutti i check...
  open-pr        Apre una PR su GitHub
  rollback       Rollback in produzione
```

Per gustare a pieno le gioie dell'uso del terminale, abilitate la completion.
Per bash, mettere nel vostro `.bashrc` (o `.bash_profile`):

```sh
if which suite-py > /dev/null; then
    eval "$(_SUITE_PY_COMPLETE=source suite-py)"
fi
```

Per zsh, mettere in `.zshrc`:

```sh
if which suite-py > /dev/null; then
    eval "$(_SUITE_PY_COMPLETE=source_zsh suite-py)"
fi
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
