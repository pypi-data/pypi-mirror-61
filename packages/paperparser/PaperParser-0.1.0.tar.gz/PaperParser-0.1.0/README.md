# PaperParser

## Installing Python and Poetry

Install pyenv:

```bash
brew install pyenv
brew install pyenv-virtualenv
```

Add the following lines to your `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Install different python versions:

```bash
pyenv install 3.8.1
pyenv install 3.7.6
pyenv local 3.8.1 3.7.6
python3 --version
python3.7 --version
```

Install poetry:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

Add the following lines to your `~/.bashrc` or `~/.zshrc`:

```bash
source ~/.poetry/env
```

## Installing and Opening in VSCode

```bash
poetry install
poetry shell
code .
```

The select the python interpreter with the project name in.

## Updating Dependencies

```bash
poetry update
```

## Tests

```
nox -k "3.8"
```

## Credits

Heavily inspired by [hypermodern-python](https://github.com/cjolowicz/hypermodern-python) by [cjolowicz](https://github.com/cjolowicz)
