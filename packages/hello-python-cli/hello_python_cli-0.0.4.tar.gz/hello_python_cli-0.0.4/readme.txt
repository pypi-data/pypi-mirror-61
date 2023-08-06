Simple CLI python program using docopt with tests

virtualenv -p python3 venv
source venv/bin/activate
create .envrc
direnv allow

pip install docopt pytest flake8

# Configure git to use pre-commit hook
flake8 --install-hook git

# to install 'hello'
python setup.py install

# to test
pytest

Note: A push will publish to test.pypi.org


# want zsh completion?
# 1. add these lines to ~/.zshrc
# folder of all of your autocomplete functions
fpath=($HOME/.zsh-completions $fpath)
# enable autocomplete function
autoload -U compinit
compinit
# 2. copy script to something in fpath (echo $fpath)
cp _hello ~/.zsh-completions/
# 3. reload zsh
exec zsh
# 4. try it out...
hello --<tab>

# want bash completion?
brew install bash-completion
echo "[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion" >> ~/.bash_profile
# reload (only need to do this once)
source ~/.bash_profile
copy hello_completion.sh /usr/local/etc/bash_completion.d/hello
try it out
hello --<tab>
