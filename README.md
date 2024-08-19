# VOIM - Vim OI Improve

这是一个 VIM 插件。

这个插件用于为 OIer 提供更方便的 VIM 使用体验，其功能如下：

- 一键编译运行（已实现，现支持 C/C++ 以及 Python）
- 一键评测样例（基于 Competitive Companion，就快要完成了）

使用这个插件是极其简单的，在插件列表中加入该插件即可。

如果你使用的是 vim-plug，你可以在 `.vimrc` 键入以下内容：

```vimrc
call plug#begin('~/.vim/plugged')
  Plug 'lixuannan/VOIM'
call plug#end()
```

然后在 vim 中输入命令 `:PlugInstall`。要更新插件，请在 vim 中输入命令 `:PlugUpdate`。

插件默认使用 \<F5\> 作为编译运行的快捷键，但是为了方便用户使用，我们还定义了一个一键编译运行的命令 `RunCode`。如果你要自定义快捷键，可以使用类似这样的语法：

```vimrc
"设置全局的快捷键，其中 % 为当前文件的文件名
map <F5> :RunCode %<CR>
"设置插入模式的快捷键
imap <F5> <esc> :RunCode % <CR>
"设置选择模式的快捷键
vmap <F5> <esc> :RunCode % <CR>
```

如果你得到报错 `Unsupport filetype detected, run failed` 但是你的代码后缀名没有问题，请你检查你的光标是否在你需要的文件上。

