%global debug_package %{nil}
%global vertag v1.0.0-AU84

Name:           audioreach-pipewire-plugin
Version:        1.0.0
Release:        1%{?dist}
Summary:        PipeWire plugin for AudioReach audio framework
License:        BSD-3-Clause
URL:            https://github.com/Audioreach/audioreach-pipewire-plugin
Source0:        %{url}/archive/refs/tags/%{vertag}.tar.gz#/%{name}-%{version}.tar.gz

ExclusiveArch:  aarch64

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  expat-devel
BuildRequires:  pkgconfig(agm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(pal-headers)
BuildRequires:  pkgconfig(tinyalsa)

Requires:       pipewire
Requires:       wireplumber

%description
Provides a PipeWire module (libpipewire-module-pal) that integrates
AudioReach PAL devices with the PipeWire audio server, enabling audio
routing and processing through AudioReach DSP pipelines on Qualcomm
platforms.

%prep
%setup -n %{name}-1.0.0-AU84
# Fix hardcoded /usr/lib path — on aarch64 modules go to %%{_libdir}
sed -i 's|$(DESTDIR)/usr/lib/pipewire|$(DESTDIR)$(libdir)/pipewire|g' Makefile.am

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
# Remove .la file and unused pw-pal.pc (plugin only, no library consumers)
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name 'pw-pal.pc' -delete
# libtool installs a copy to %%{_libdir}; only the pipewire-0.3/ copy is needed
rm -f %{buildroot}%{_libdir}/libpipewire-module-pal.so

%files
%license LICENSE
%{_libdir}/pipewire-0.3/libpipewire-module-pal.so
%{_datadir}/pipewire/pipewire.conf.d/pw-pal-plugin.conf
%{_datadir}/wireplumber/wireplumber.conf.d/60-disable-alsa.conf
%{_datadir}/wireplumber/wireplumber.conf.d/90-device-detection.conf
%{_datadir}/wireplumber/scripts/90-device-detection.lua

%changelog
* Wed Aug 19 2026 Qualcomm Linux <quic_linux@quicinc.com> - 1.0.0-1
- Initial RPM packaging of audioreach-pipewire-plugin version 1.0.0
