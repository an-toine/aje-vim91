%global scl_vendor aje
%global _scl_prefix /opt/%{scl_vendor}
%global scl_name_prefix aje-
%global scl_name_base vim
%global scl_name_version 90
%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}
%{?scl:%scl_package vim}
%{!?scl:%global pkg_name %{name}}
%scl_package %scl

%global sourcebasename %{pkg_name}-%{version}

Summary: A greatly improved version of the good old UNIX editor Vi
Name: %{?scl_prefix}%{pkg_name}
Version: 9.1.0095
Release: 1%{?dist}
License: GPLv2
Group: Applications/Text
URL: https://github.com/vim/vim

Source: https://github.com/%{pkg_name}/%{pkg_name}/archive/v%{version}.tar.gz
Source1: changelog-%{scl_prefix}%{pkg_name}

BuildRequires: gcc gettext make ruby ruby-devel ctags git python python-devel python3 python3-devel tcl-devel ncurses-devel lua-devel perl perl-devel perl-ExtUtils-Embed

Requires: %{?scl_prefix}%{pkg_name}-common
%{?scl:Requires: %scl_runtime}

%description
Vim is a greatly improved version of the good old UNIX editor Vi. Many new
features have been added: multi-level undo, syntax highlighting, command
line history, on-line help, spell checking, filename completion, block
operations, script language, etc. There is also a Graphical User
Interface (GUI) available. Still, Vi compatibility is maintained, those
who have Vi "in the fingers" will feel at home.

%package gtk
Summary: A GTK version of Vim editor
Group: Applications/Text

BuildRequires: gcc gettext make ruby ruby-devel ctags git python python-devel python3 python3-devel tcl-devel ncurses-devel lua-devel perl perl-devel perl-ExtUtils-Embed gtk3-devel libX11-devel libSM-devel libXt-devel libXpm-devel libICE-devel
Requires: %{?scl_prefix}%{pkg_name}-common

%description gtk
Vim is a greatly improved version of the good old UNIX editor Vi. Many new
features have been added: multi-level undo, syntax highlighting, command
line history, on-line help, spell checking, filename completion, block
operations, script language, etc. This package contains the Graphical User
Interface (GUI) version of the program.

%package common
Summary: Common runtimes and manpages for the Vim editor
Group: Applications/Text

%description common
This package contains common runtimes and manpages files for used by
both GUI and non GUI Vim packages.

%prep
%setup -c -n %{scl}
cd %{sourcebasename}

%build
cd %{sourcebasename}
%configure --with-features=huge \
            --enable-largefile \
            --disable-darwin \
            --enable-multibyte \
            --with-x=no \
            --disable-gui \
            --enable-rubyinterp=yes \
            --enable-python3interp=yes \
            --with-python3-config-dir=$(python3-config --configdir) \
            --enable-perlinterp=yes \
            --enable-luainterp=yes \
            --enable-cscope \
            --with-compiledby='Antoine Jouve'

make %{?_smp_mflags} VIMRUNTIMEDIR=%{_datadir}/%{pkg_name}/vim%{scl_name_version}
%{__cp} src/vim vim
make distclean

%configure --with-features=huge \
            --enable-largefile \
            --disable-darwin \
            --enable-multibyte \
            --enable-rubyinterp=yes \
            --with-x=yes \
            --enable-gtk3-check \
            --enable-gui=gtk3 \
            --enable-python3interp=yes \
            --with-python3-config-dir=$(python3-config --configdir) \
            --enable-perlinterp=yes \
            --enable-luainterp=yes \
            --enable-cscope \
            --with-compiledby='Antoine Jouve'

make %{?_smp_mflags} VIMRUNTIMEDIR=%{_datadir}/%{pkg_name}/vim%{scl_name_version}

%install
cd %{sourcebasename}
make install DESTDIR=$RPM_BUILD_ROOT VIMRCLOC=%{_root_sysconfdir}/%{_scl_prefix}/%{scl}/etc/ VIMRUNTIMEDIR=%{_datadir}/%{pkg_name}/vim%{scl_name_version}

# Move the last vim build result which is gvim to a correct name
mv %{buildroot}%{_bindir}/vim %{buildroot}%{_bindir}/gvim

# Fix gvim* links to gvim and not vim
for link in gview gvimdiff gvimtutor rgview rgvim
do
    ln -sf gvim %{buildroot}%{_bindir}/${link}
done

# Copy the previous minimal version of vim
install -D -m 0755 vim %{buildroot}%{_bindir}/vim

# Remove unused C files
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/macros/maze/mazeansi.c
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/macros/maze/mazeclean.c
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/macros/maze/maze.c
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/macros/tools/ccfilter.c
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/macros/tools/blink.c
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/tools/blink.c
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/tools/ccfilter.c
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/tools/xcmdsrv_client.c

# Copy example vimrc file to VIMRCLOC directory
mkdir -p $RPM_BUILD_ROOT/%{_root_sysconfdir}/%{_scl_prefix}/%{scl}/etc
%{__cp} $RPM_BUILD_ROOT/%{_datadir}/%{pkg_name}/vim%{scl_name_version}/vimrc_example.vim $RPM_BUILD_ROOT/%{_root_sysconfdir}/%{_scl_prefix}/%{scl}/etc/vimrc

# Chmod editorconfig mkzip script
chmod 755 $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/vim%{scl_name_version}/pack/dist/opt/editorconfig/mkzip.sh

# Copy vimrc file when SCL is registered
mkdir -p %{buildroot}%{?_scl_scripts}/register.d/
cat <<EOF | tee %{buildroot}%{?_scl_scripts}/register.d/20.copy-vimrc
#!/bin/sh
mkdir -p %{_root_sysconfdir}/%{_scl_prefix}/%{scl}/etc
cp -a %{_datadir}/%{pkg_name}/vim%{scl_name_version}/vimrc_example.vim %{_root_sysconfdir}/%{_scl_prefix}/%{scl}/etc/vimrc
EOF
chmod +x %{buildroot}%{?_scl_scripts}/register.d/20.copy-vimrc

# Remove vimrc file when SCL is unregistered
mkdir -p %{buildroot}%{?_scl_scripts}/deregister.d/
cat <<EOF | tee %{buildroot}%{?_scl_scripts}/deregister.d/20.remove-vimrc
#!/bin/sh
rm %{_root_sysconfdir}/%{_scl_prefix}/%{scl}/etc/vimrc
EOF
chmod +x %{buildroot}%{?_scl_scripts}/deregister.d/20.remove-vimrc

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{sourcebasename}/README.txt
%license %{sourcebasename}/runtime/doc/uganda.txt
%{_bindir}/eview
%{_bindir}/evim
%{_bindir}/ex
%{_bindir}/rview
%{_bindir}/rvim
%{_bindir}/view
%{_bindir}/vim
%{_bindir}/vimdiff
%{_bindir}/xxd

%files gtk
%defattr(-, root, root, -)
%doc %{sourcebasename}/README.txt
%doc %{sourcebasename}/runtime/doc/gui_x11.txt
%license %{sourcebasename}/runtime/doc/uganda.txt
%{_bindir}/gview
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/rgview
%{_bindir}/rgvim
%{_bindir}/gvimtutor
%{_datadir}/applications/*
%{_datadir}/icons/*/*/apps/*

%files common
%defattr(-, root, root, -)
%doc %{sourcebasename}/README.txt
%license %{sourcebasename}/runtime/doc/uganda.txt
%config(noreplace) %{_root_sysconfdir}/%{_scl_prefix}/%{scl}/etc/vimrc
%{_bindir}/vimtutor
%{_mandir}/*
%lang(af) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/af/LC_MESSAGES/vim.mo
%lang(ca) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ca/LC_MESSAGES/vim.mo
%lang(cs.cp1250) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/cs.cp1250/LC_MESSAGES/vim.mo
%lang(cs) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/cs/LC_MESSAGES/vim.mo
%lang(da) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/da/LC_MESSAGES/vim.mo
%lang(de) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/de/LC_MESSAGES/vim.mo
%lang(en_GB) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/en_GB/LC_MESSAGES/vim.mo
%lang(eo) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/eo/LC_MESSAGES/vim.mo
%lang(es) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/es/LC_MESSAGES/vim.mo
%lang(fi) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/fi/LC_MESSAGES/vim.mo
%lang(fr) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/fr/LC_MESSAGES/vim.mo
%lang(ga) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ga/LC_MESSAGES/vim.mo
%lang(it) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/it/LC_MESSAGES/vim.mo
%lang(ja.euc-jp) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ja.euc-jp/LC_MESSAGES/vim.mo
%lang(ja.sjis) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ja.sjis/LC_MESSAGES/vim.mo
%lang(ja) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ja/LC_MESSAGES/vim.mo
%lang(ko.UTF-8) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ko.UTF-8/LC_MESSAGES/vim.mo
%lang(ko) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ko/LC_MESSAGES/vim.mo
%lang(lv) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/lv/LC_MESSAGES/vim.mo
%lang(nb) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/nb/LC_MESSAGES/vim.mo
%lang(nl) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/nl/LC_MESSAGES/vim.mo
%lang(no) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/no/LC_MESSAGES/vim.mo
%lang(pl.UTF-8) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/pl.UTF-8/LC_MESSAGES/vim.mo
%lang(pl.cp1250) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/pl.cp1250/LC_MESSAGES/vim.mo
%lang(pl) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/pl/LC_MESSAGES/vim.mo
%lang(pt_BR) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/pt_BR/LC_MESSAGES/vim.mo
%lang(ru.cp1251) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ru.cp1251/LC_MESSAGES/vim.mo
%lang(ru) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/ru/LC_MESSAGES/vim.mo
%lang(sk.cp1250) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/sk.cp1250/LC_MESSAGES/vim.mo
%lang(sk) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/sk/LC_MESSAGES/vim.mo
%lang(sr) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/sr/LC_MESSAGES/vim.mo
%lang(sv) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/sv/LC_MESSAGES/vim.mo
%lang(tr) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/tr/LC_MESSAGES/vim.mo
%lang(uk.cp1251) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/uk.cp1251/LC_MESSAGES/vim.mo
%lang(uk) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/uk/LC_MESSAGES/vim.mo
%lang(vi) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/vi/LC_MESSAGES/vim.mo
%lang(zh_CN.UTF-8) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/zh_CN.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_CN.cp936) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/zh_CN.cp936/LC_MESSAGES/vim.mo
%lang(zh_CN) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/zh_CN/LC_MESSAGES/vim.mo
%lang(zh_TW.UTF-8) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/zh_TW.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_TW) %{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/zh_TW/LC_MESSAGES/vim.mo
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/autoload/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/*.vim
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/colors/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/compiler/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/doc/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/ftplugin/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/indent/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/import/dist/*.vim
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/keymap/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/*.vim
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/lang/*.txt
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/macros/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/pack/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/plugin/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/print/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/spell/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/syntax/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/tools/*
%{_datadir}/%{pkg_name}/vim%{scl_name_version}/tutor/*

%{_scl_scripts}/register.d/*
%{_scl_scripts}/deregister.d/*

%changelog
%include %{_sourcedir}/changelog-%{scl_prefix}%{pkg_name}
