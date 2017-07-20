%global libmediainfo_version    0.7.94
%global libzen_version          0.4.35

Name:           mediaconch
Version:        17.06
Release:        3%{?dist}
Summary:        Most relevant technical and tag data for video and audio files (CLI)

License:        GPLv3+ and MPLv2.0
URL:            https://mediaarea.net/MediaConch/
Source0:        https://mediaarea.net/download/source/%{name}/%{version}/%{name}_%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libmediainfo) >= %{libmediainfo_version}
BuildRequires:  pkgconfig(libzen) >= %{libzen_version}
BuildRequires:  pkgconfig(zlib)
BuildRequires:  libtool
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libevent)
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebengine-devel
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(jansson)
BuildRequires:  systemd
BuildRequires:  libappstream-glib


%description
MediaConch is an implementation checker, policy checker, reporter,
and fixer that targets preservation-level audiovisual files
(specifically Matroska, Linear Pulse Code Modulation (LPCM)
and FF Video Codec 1 (FFV1)).

This project is maintained by MediaArea and funded by PREFORMA.

This package includes the command line interface.

%package gui
Summary:    Supplies technical and tag information about a video or audio file (GUI)
Requires:   hicolor-icon-theme

%description gui
MediaConch is an implementation checker, policy checker, reporter,
and fixer that targets preservation-level audiovisual files
(specifically Matroska, Linear Pulse Code Modulation (LPCM)
and FF Video Codec 1 (FFV1)).

This project is maintained by MediaArea and funded by PREFORMA.

This package includes the graphical user interface.

%package server
Summary:    Supplies technical and tag information about a video or audio file (Server)
%{?systemd_requires}

%description server
MediaConch is an implementation checker, policy checker, reporter,
and fixer that targets preservation-level audiovisual files
(specifically Matroska, Linear Pulse Code Modulation (LPCM)
and FF Video Codec 1 (FFV1)).

This project is maintained by MediaArea and funded by PREFORMA.

This package includes the server.

%prep
%autosetup -n MediaConch
rm -rf Source/ThirdParty
sed -i 's/.$//' *.txt *.html Release/*.txt

sed -i 's/AC_PROG_LIBTOOL/LT_INIT([disable-static])/' Project/GNU/CLI/configure.ac
sed -i 's/AC_PROG_LIBTOOL/LT_INIT([disable-static])/' Project/GNU/Server/configure.ac
# sed -i 's/INCLUDES/AM_CPPFLAGS/' Project/GNU/CLI/Makefile.am
# sed -i 's/INCLUDES/AM_CPPFLAGS/' Project/GNU/Server/Makefile.am

pushd Project/GNU/CLI
    autoreconf -fiv
popd

pushd Project/GNU/Server
    autoreconf -fiv
popd


%build
# build CLI
pushd Project/GNU/CLI
    %configure --enable-static=no
    %make_build
popd

# build server
pushd Project/GNU/Server
    %configure --enable-static=no
    %make_build
popd

# now build GUI
pushd Project/Qt
    %{qmake_qt5}
    %make_build
popd


%install
pushd Project/GNU/CLI
    %make_install
popd

pushd Project/GNU/Server
    %make_install
popd

pushd Project/Qt
    install -dm 755 %{buildroot}%{_bindir}
    install -m 755 -p mediaconch-gui %{buildroot}%{_bindir}
popd

# icon
install -dm 755 %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -m 644 -p Source/Resource/Image/MediaConch.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -dm 755 %{buildroot}%{_datadir}/pixmaps
install -m 644 -p Source/Resource/Image/MediaConch.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# menu-entry
install -dm 755 %{buildroot}%{_datadir}/applications
install -m 644 -p Project/GNU/GUI/mediaconch-gui.desktop %{buildroot}%{_datadir}/applications

desktop-file-install --dir="%{buildroot}%{_datadir}/applications" -m 644 Project/GNU/GUI/mediaconch-gui.desktop

install -dm 755 %{buildroot}%{_datadir}/appdata/
install -m 644 -p Project/GNU/GUI/mediaconch-gui.appdata.xml %{buildroot}%{_datadir}/appdata/mediaconch-gui.appdata.xml

install -dm 755 %{buildroot}%{_unitdir}
install -m 644 -p Project/GNU/Server/mediaconchd.service  %{buildroot}%{_unitdir}/mediaconchd.service

install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -p Project/GNU/Server/MediaConch.rc  %{buildroot}%{_sysconfdir}/%{name}/MediaConch.rc

%check
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

%post gui
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gui
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post server
%systemd_post mediaconchd.service

%preun server
%systemd_preun mediaconchd.service

%postun server
%systemd_postun_with_restart mediaconchd.service

%files
%doc Release/ReadMe_CLI_Linux.txt History_CLI.txt
%license License.html License.GPLv3.html License.MPLv2.html
%{_bindir}/mediaconch

%files server
%doc Documentation/Daemon.md Documentation/Config.md
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/mediaconchd
%{_unitdir}/mediaconchd.service


%files gui
%doc Release/ReadMe_GUI_Linux.txt History_GUI.txt
%license License.html License.GPLv3.html License.MPLv2.html
%{_bindir}/mediaconch-gui
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/icons/hicolor/256x256/apps/*.png
%{_datadir}/appdata/mediaconch-gui.appdata.xml


%changelog
* Thu Jul 20 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 17.06-3
- AC_PROG_LIBTOOL -> LT_INIT

* Wed Jul 19 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 17.06-2
- Clean spec

* Fri Jul 14 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 17.06-1
- Update to 17.06

* Thu Jun 29 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 17.05-1
- Update to 17.05

* Thu Apr 13 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 17.03-1
- Update to 17.03

* Thu Apr 06 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 17.02-1
- Update to 17.02

* Thu Feb 09 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 17.01-1
- Update to 17.01

* Mon Jan 09 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 16.12-1
- Update to 16.12

* Fri Dec 09 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.11-1
- Update to 16.11

* Thu Nov 24 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.10-1
- Update to 16.10

* Fri Oct 28 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.09-1
- Update to 16.09

* Wed Sep 21 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.08-1
- Update to 16.08

* Mon Aug 01 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.07-1
- Update to 16.07

* Wed Jul 06 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.06-1
- Update to 16.06

* Wed Jun 01 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.05-1
- Update to 16.05

* Thu May 05 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.04-1
- Update to 16.04

* Tue Apr 26 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.03-3
- Add validate appdata XML

* Tue Apr 26 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.03-2
- Add appdata XML
- Switch BRs to use pkgconfig
- Add systemd unit for mediaconchd

* Tue Apr 12 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.03-1
- Update to 16.03

* Wed Mar 02 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.02-1
- Update to 16.02
- add %%license macro

* Wed Feb 10 2016 Vasiliy N. Glazov <vascom2@gmail.com> 16.01-1
- Initial release
