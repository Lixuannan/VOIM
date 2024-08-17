# VOIM - Vim OI Improve

这是一个 VIM 插件。

这个插件用于为 OIer 提供更方便的 VIM 使用体验，其功能如下：

- 一键编译运行（已实现，现支持 C/C++ 以及 Python）
- 一键提交到 OJ （计划实现，或许很快完成）

使用这个插件是极其简单的，你可以到 Releases 下载编译好的二进制文件并把它放到 `bin` 目录里面。然后在你的 `.vimrc` 文件中加入简单的三行，已将 \<F5\> 设置为编译运行的快捷键：

```vimrc
map <F5> :!VOIM % <CR>
imap <F5> <esc> :!VOIM % <CR>
vmap <F5> <esc> :!VOIM % <CR>
```


