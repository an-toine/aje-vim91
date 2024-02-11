# aje-vim91 software collection

[![rpmbuild](https://github.com/an-toine/aje-vim91/workflows/rpmbuild/badge.svg)](https://github.com/an-toine/aje-vim91/actions)

This Software Collection is providing Vim 9 rpm packages for CentOS 7.

## About this software collection

When using specific plugins, the latest Vim version may be required. However,
the version shipped with CentOS is a bit outdated and a rebuild from
sources is needed.

To ease the use and installation of the latest upstream Vim version on
CentOS 7, this Software Collection was created.

Using Github actions, sources are cloned from official Vim
[repo](https://github.com/vim/vim) every night, and a rebuild of the last
tagged version is performed if needed. Once the workflow execution is complete,
a new [release](https://github.com/an-toine/aje-vim91/releases) is created.

### Limitations

Even though minimal functionnal testing is performed before releasing a new
version, these packages are not production ready and may crash or introduce
bugs or regressions.

Therefore, this Software Collection should be used when new features outweighs
the need of stability.
As a general advice, the Vim package shipped with CentOS 7 should not be
removed from the system when using this collection.

## Usage

This software collection can be installed alongside the official Vim package.

To install the collection tree structure, install at least packages
`aje-vim91` and `aje-vim91-runtime`.

Vim binaries can then be installed using packages `aje-vim91-vim-common` and
`aje-vim91-vim`. Package `aje-vim91-vim-gtk` is optionnal and installs GUI
binaries such as `gVim`.

Once installation is complete, you can enable this SCL with :

    scl enable aje-vim91

and start using Vim as you are used to.
