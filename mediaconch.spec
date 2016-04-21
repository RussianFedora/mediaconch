%global libmediainfo_version    0.7.83
%global libzen_version          0.4.33

Name:           mediaconch
Version:        16.03
Release:        1%{?dist}
Summary:        Most relevant technical and tag data for video and audio files (CLI)

License:        GPLv3+ and MPLv2.0
URL:            http://MediaArea.net/MediaConch
Source0:        https://mediaarea.net/download/source/%{name}/%{version}/%{name}_%{version}.tar.xz

Group:          Applications/Multimedia

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  libmediainfo-devel >= %{libmediainfo_version}
BuildRequires:  libzen-devel >= %{libzen_version}
BuildRequires:  zlib-devel
BuildRequires:  libtool
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  zlib-devel
# BuildRequires:  libqt4-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  libcurl-devel
BuildRequires:  sqlite-devel
BuildRequires:  libevent-devel
# BuildRequires:  qt-devel
BuildRequires:  qt5-qtbase-devel

%if 0%{?fedora} >= 24 || 0%{?rhel} > 7
BuildRequires:  qt5-qtwebengine-devel
%else
BuildRequires:  qt5-qtwebkit-devel
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  jansson-devel


%description
MediaConch is an implementation checker, policy checker, reporter,
and fixer that targets preservation-level audiovisual files
(specifically Matroska, Linear Pulse Code Modulation (LPCM)
and FF Video Codec 1 (FFV1)).

This project is maintained by MediaArea and funded by PREFORMA.

This package includes the command line interface.

%package gui
Summary:    Supplies technical and tag information about a video or audio file (GUI)
Group:      Applications/Multimedia
Requires:   libzen%{?_isa} >= %{libzen_version}
Requires:   libmediainfo%{?_isa} >= %{libmediainfo_version}

%description gui
MediaConch is an implementation checker, policy checker, reporter,
and fixer that targets preservation-level audiovisual files
(specifically Matroska, Linear Pulse Code Modulation (LPCM)
and FF Video Codec 1 (FFV1)).

This project is maintained by MediaArea and funded by PREFORMA.

This package includes the graphical user interface.

%package server
Summary:    Supplies technical and tag information about a video or audio file (Server)
Group:      Applications/Multimedia
Requires:   libzen%{?_isa} >= %{libzen_version}
Requires:   libmediainfo%{?_isa} >= %{libmediainfo_version}

%description server
MediaConch is an implementation checker, policy checker, reporter,
and fixer that targets preservation-level audiovisual files
(specifically Matroska, Linear Pulse Code Modulation (LPCM)
and FF Video Codec 1 (FFV1)).

This project is maintained by MediaArea and funded by PREFORMA.

This package includes the server.

%prep
%setup -q -n MediaConch
rm -rf Source/ThirdParty

sed -i 's/.$//' *.txt *.html Release/*.txt

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
%if 0%{?fedora} >= 22 || 0%{?rhel} > 7
    %{qmake_qt5}
%else
    %{qmake_qt5} USE_WEBKIT=1
%endif
    %make_build
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd Project/GNU/CLI
    make install-strip DESTDIR=%{buildroot}
popd

pushd Project/GNU/Server
    make install-strip DESTDIR=%{buildroot}
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
install -dm 755 %{buildroot}/%{_datadir}/applications
install -m 644 -p Project/GNU/GUI/mediaconch-gui.desktop %{buildroot}/%{_datadir}/applications

desktop-file-install --dir="%{buildroot}%{_datadir}/applications" -m 644 Project/GNU/GUI/mediaconch-gui.desktop

install -dm 755 %{buildroot}/%{_datadir}/apps/konqueror/servicemenus
install -m 644 -p Project/GNU/GUI/mediaconch-gui.kde3.desktop %{buildroot}/%{_datadir}/apps/konqueror/servicemenus/mediaconch-gui.desktop

install -dm 755 %{buildroot}/%{_datadir}/kde4/services/ServiceMenus/
install -m 644 -p Project/GNU/GUI/mediaconch-gui.kde4.desktop %{buildroot}/%{_datadir}/kde4/services/ServiceMenus/mediaconch-gui.desktop

%post gui
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans gui
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc Release/ReadMe_CLI_Linux.txt History_CLI.txt
%license License.html License.GPLv3.html License.MPLv2.html
%{_bindir}/mediaconch

%files server
%doc Documentation/Daemon.md Documentation/Config.md
%{_bindir}/mediaconchd

%files gui
%doc Release/ReadMe_GUI_Linux.txt History_GUI.txt
%license License.html License.GPLv3.html License.MPLv2.html
%{_bindir}/mediaconch-gui
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/icons/hicolor/256x256/apps/*.png
%{_datadir}/apps/konqueror/servicemenus/*.desktop
%{_datadir}/kde4/services/ServiceMenus/*.desktop


%changelog
* Tue Apr 12 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.03-1
- Update to 16.03

* Wed Mar 02 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 16.02-1
- Update to 16.02
- add %%license macro

* Wed Feb 10 2016 Vasiliy N. Glazov <vascom2@gmail.com> 16.01-1
- Initial release
