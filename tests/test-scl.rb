control "scl-runtime-package-is-installed-1.0" do
    impact "critical"
    title "SCL metapackage and runtime are installed"
    desc "These 2 package contain the basic tooling to use the software collection"

    describe package("aje-vim91") do
        it { should be_installed }
    end

    describe package("aje-vim91-runtime") do
        it { should be_installed }
    end
end

control "scl-dev-packages-are-installed-1.0" do
    impact "medium"
    title "SCL development packages are installed"
    desc "These packages are used when building other products using this SCL"

    describe package("aje-vim91-build") do
        it { should be_installed }
    end

    describe package("aje-vim91-scldevel") do
        it { should be_installed }
    end
end

control "scl-can-be-enabled-1.0" do
    impact "critical"
    title "SCL enable script can be used"
    desc "The enable script must be executable and alter PATH variables"

    describe file("/opt/aje/aje-vim91/enable") do
        its("mode") { should cmp "0755" }
        its("content") { should match %r{export PATH=".*"} }
    end

    describe bash("scl enable aje-vim91 'echo $PATH'") do
        its("stdout") { should match %r{/opt/aje/aje-vim91/root/usr/bin:/opt/aje/aje-vim91/root/usr/sbin:.*} }
        its("stderr") { should eq "" }
        its("exit_status") { should eq 0 }
    end
end
