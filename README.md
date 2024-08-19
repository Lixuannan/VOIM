# VOIM - Vim OI Improve

这是一个 VIM 插件。

这个插件用于为 OIer 提供更方便的 VIM 使用体验，其功能如下：

- 一键编译运行（已实现，现支持 C/C++ 以及 Python）
- 一键评测样例（基于 Competitive Companion，已完成）

使用这个插件是极其简单的，在插件列表中加入该插件即可。

如果你使用的是 vim-plug，你可以在 `.vimrc` 键入以下内容：

```vimrc
call plug#begin('~/.vim/plugged')
  Plug 'lixuannan/VOIM'
call plug#end()
```

然后在 vim 中输入命令 `:PlugInstall`。要更新插件，请在 vim 中输入命令 `:PlugUpdate`。

我们定义了一个一键编译运行的命令 `RunCode`，以及一键评测样例的命令 `:JudgeCode` 如果你要自定义快捷键，可以在 `.vimrc` 中这样写：

```vimrc
"设置全局的快捷键，其中 % 为当前文件的文件名
map <F5> :RunCode %<CR>
"设置插入模式的快捷键
imap <F5> <esc> :RunCode %<CR>
"设置选择模式的快捷键
vmap <F5> <esc> :RunCode %<CR>

map <F6> :JudgeCode %<CR>
imap <F6> <esc> :JudgeCode %<CR>
vmap <F6> <esc> :JudgeCode %<CR>

```

如果你得到报错 `Unsupport filetype detected, run failed` 但是你的代码后缀名没有问题，请你检查你的光标是否在你需要的文件上。

在最新版本的插件中，我们支持自定义编译器以及编译参数，你可以在用户的 `HOME` 目录中创建文件 `.VOIM.conf` 并写下配置。下面展示的文件为默认配置：

```cpp
# C 语言编译器
C_COMPILER = "gcc"
# C++ 编译器
CPP_COMPILER = "g++"
# Python 解释器
PYTHON_INTERPRETER = "python"
# C 编译选项
C_ARGV = "-Wextra -g"
# C++ 编译选项
CPP_ARGV = "-Wextra -g"
```

