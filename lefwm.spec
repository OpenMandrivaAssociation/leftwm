%global debug_package %{nil}
Name:		leftwm
Version:	0.5.4
Release:	1
Source0:	https://github.com/leftwm/leftwm/archive/%{version}/%{name}-%{version}.tar.gz
Source1:leftwm-0.5.4-vendor.tgz
Summary:	A tiling window manager for adventurers
URL:		https://github.com/leftwm/leftwm
License:	MIT
Group:		Window Manager/Other

BuildRequires:	cargo

%description
%summary

%prep
%autosetup -p1

tar -zxf %{SOURCE1}

mkdir -p .cargo

cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
cargo build --release --frozen

%install
install -D -p -m 0644 %{name}.desktop -t %{buildroot}%{_datadir}/xsessions/
install -D -p -m 0644 %{name}/doc/%{name}.1 -t %{buildroot}%{_mandir}/man1/

install -D -p -m 0755 \
    target/release/%{name} \
    target/release/%{name}-check \
    target/release/%{name}-command \
    target/release/%{name}-state \
    target/release/%{name}-worker \
    -t %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a themes %{buildroot}%{_datadir}/%{name}/

strip --strip-all %{buildroot}%{_bindir}/*

%files
%license LICENSE.md
%doc README.md CHANGELOG.md
%{_bindir}/%{name}
%{_bindir}/%{name}-*
%{_datadir}/%{name}/
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man1/*.1*
