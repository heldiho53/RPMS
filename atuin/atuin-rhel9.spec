Name:           atuin
Version:        12.0.0
Release:        el9.1.7
Summary:        Magical shell history
License:        MIT
Group:          System/Console
URL:            https://github.com/ellie/atuin
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        vendor.tar.gz
Source2:        cargo_config
BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  cargo-rpm-macros
BuildRequires:  rust-toolset

%description
Atuin replaces your existing shell history with a SQLite database, and records additional context for your commands.
Additionally, it provides optional and fully encrypted synchronisation of your history between machines, via an Atuin server.

%package bash-completion
Summary:        Bash completion for %{name}
Requires:       %{name} = %{version}
Supplements:    (%{name} and bash-completion)
BuildArch:      noarch

%description bash-completion
Bash command line completion support for %{name}.

%package fish-completion
Summary:        Fish completion for %{name}
Requires:       %{name} = %{version}
Supplements:    (%{name} and fish)
BuildArch:      noarch

%description fish-completion
Fish command line completion support for %{name}.

%package zsh-completion
Summary:        Zsh completion for %{name}
Requires:       %{name} = %{version}
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description zsh-completion
Zsh command line completion support for %{name}.

%prep
%autosetup -a1
mkdir .cargo
cp %{SOURCE2} .cargo/config

%build
%{cargo_build} --all-features

for shell in "zsh" "bash" "fish"
do
  ./target/release/%{name} gen-completions --shell "$shell" > target/%{name}."$shell"
done

%install
%{?cargo_install}
export CARGO_INSTALL_ROOT=%{buildroot}/usr
%{cargo_install}
install -D -m 0644 "target/%{name}.bash" "%{buildroot}/%{_datadir}/bash-completion/completions/%{name}"
install -D -m 0644 "target/%{name}.fish" "%{buildroot}/%{_datadir}/fish/vendor_completions.d/%{name}.fish"
install -D -m 0644 "target/%{name}.zsh" "%{buildroot}/%{_datadir}/zsh/site-functions/_%{name}"

%files
%license LICENSE
%doc README.md CHANGELOG.md src/shell
%{_bindir}/atuin

%files bash-completion
%{_datadir}/bash-completion/completions/%{name}

%files fish-completion
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}.fish

%files zsh-completion
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
