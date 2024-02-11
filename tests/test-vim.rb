control "vim-is-installed-1.0" do
    impact "critical"
    title "SCL Vim is installed"
    desc "Both the minimal and common packages are installed"

    describe package("aje-vim91-vim") do
        it { should be_installed }
        its("version") { should match %r{9\.1.*} }
    end

    describe package("aje-vim91-vim-common") do
        it { should be_installed }
        its("version") { should match %r{9\.1.*} }
    end
end

control "gvim-is-installed-1.0" do
    impact "medium"
    title "SCL gVim is installed"
    desc "The GTK version of Vim must be installed"

    describe package("aje-vim91-vim-gtk") do
        it { should be_installed }
        its("version") { should match %r{9\.1.*} }
    end
end

control "vim-binary-links-1.0" do
    impact "critical"
    title "SCL Vim tools are linked on Vim binary"
    desc "All Vim tools must be linked on the minimal Vim binary"

    for tool in ["vimdiff", "view", "rvim", "rview", "ex", "evim", "eview"]
        describe file("/opt/aje/aje-vim91/root/usr/bin/#{tool}") do
            its("type") { should eq :symlink }
            its("link_path") { should eq "/opt/aje/aje-vim91/root/usr/bin/vim" }
        end
    end

    describe file("/opt/aje/aje-vim91/root/usr/bin/vim") do
        its("type") { should eq :file }
        its("mode") { should cmp "0755" }
    end
end

control "gvim-binary-links-1.0" do
    impact "critical"
    title "SCL gVim tools are linked on gVim binary"
    desc "All gVim tools must be linked on the gVim binary"

    for tool in ["gvimdiff", "gview", "rgvim", "rgview"]
        describe file("/opt/aje/aje-vim91/root/usr/bin/#{tool}") do
            its("type") { should eq :symlink }
            its("link_path") { should eq "/opt/aje/aje-vim91/root/usr/bin/gvim" }
        end
    end

    describe file("/opt/aje/aje-vim91/root/usr/bin/gvim") do
        its("type") { should eq :file }
        its("mode") { should cmp "0755" }
    end
end

control "minimal-vim-is-working-1.0" do
    impact "critical"
    title "SCL vim version is working"
    desc "The Vim binary must be working and its version has to contain a few keywords"

    describe bash("scl enable aje-vim91 'vim --version'") do
        its("stdout") { should match %r{.*VIM - Vi IMproved 9\.1.*} }
        its("stdout") { should match %r{.*Huge version without GUI.*} }
        its("stdout") { should match %r{.*\+ruby.*} }
        its("stdout") { should match %r{.*\+python3.*} }
        its("stdout") { should match %r{.*\+lua.*} }
        its("exit_status") { should eq 0 }
    end

end

control "gvim-is-working-1.0" do
    impact "medium"
    title "SCL gVim version is working"
    desc "The gVim binary must be working and its version has to contain a few keywords"

    describe bash("scl enable aje-vim91 'gvim --version'") do
        its("exit_status") { should eq 0 }
    end

    describe bash("scl enable aje-vim91 'gvim --version'") do
        its("exit_status") { should eq 0 }
    end
end
