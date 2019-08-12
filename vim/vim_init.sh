#!/usr/bin/env bash
# ide install shell script based on vim by yyq
# @20190810

if [ "$(uname)" == "Darwin" ]; then
	# brew update; brew install vim
	echo "mac osx"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
	# sudo apt-get remove vim-tiny; sudo apt-get update; sudo apt-get install vim
	echo "GNU/Linux"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT"  ]; then
	# Do something under 32 bits Windows NT platform
	echo "win no install"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT"  ]; then
	# Do something under 64 bits Windows NT platform
	echo "win nt no install"
fi

vim --version
echo "****************************************************************************************"

mkdir ~/.vim; mkdir ~/.vim/bundle; mkdir ~/.vim/autoload;
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
git clone https://github.com/jiangmiao/auto-pairs.git ~/.vim/bundle/auto-pairs
git clone https://github.com/kien/ctrlp.vim.git ~/.vim/bundle/ctrlp.vim
git clone https://github.com/vim-syntastic/syntastic.git ~/.vim/bundle/syntastic
git clone https://github.com/vim-scripts/indentpython.vim.git ~/.vim/bundle/indentpython.vim
git clone https://github.com/ycm-core/YouCompleteMe.git ~/.vim/bundle/YouCompleteMe
git clone https://github.com/davidhalter/jedi-vim.git ~/.vim/bundle/jedi-vim
git clone https://github.com/scrooloose/nerdtree.git ~/.vim/bundle/nerdtree
git clone https://github.com/jistr/vim-nerdtree-tabs.git ~/.vim/bundle/vim-nerdtree-tabs
git clone https://github.com/lifepillar/vim-solarized8.git ~/.vim/bundle/vim-solarized8
git clone https://github.com/altercation/vim-colors-solarized.git ~/.vim/bundle/vim-colors-solarized
git clone https://github.com/jnurmine/Zenburn.git ~/.vim/bundle/Zenburn
git clone https://github.com/nvie/vim-flake8.git ~/.vim/bundle/vim-flake8
git clone https://github.com/tpope/vim-fugitive.git ~/.vim/bundle/vim-fugitive

echo "****************************************************************************************"

rm ~/.vim/autoload/pathogen.vim
cp $PWD/autoload/pathogen.vim ~/.vim/autoload/pathogen.vim

rm ~/.vimrc
cp $PWD/vimrc ~/.vimrc

<<'COMMENT'
solve CRLF in the file

For Ubuntu/Debian: sudo apt-get install tofrodos; sudo ln -s /usr/bin/fromdos /usr/bin/dos2unix
For CentOS, Fedora, ...: sudo yum install dos2unix
Then use it this way: dos2unix ~/.vimrc
COMMENT

sudo apt-get install tofrodos; sudo ln -s /usr/bin/fromdos /usr/bin/dos2unix
dos2unix ~/.vimrc

echo "****************************************************************************************"
