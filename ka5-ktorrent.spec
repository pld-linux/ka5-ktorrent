#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	webengine	# build without webengine
%define		kdeappsver	23.08.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		ktorrent
%ifarch x32
%undefine	with_webengine
%endif
Summary:	Native KDE BitTorrent client
Summary(de.UTF-8):	Ein nativer KDE BitTorrent Klient
Summary(pl.UTF-8):	Natywny klient BitTorrenta dla KDE
Name:		ka5-%{kaname}
Version:	23.08.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	c45343ba308d79e6ac539bc8170376cc
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network >= %{qtver}
BuildRequires:	Qt5Positioning-devel >= %{qtver}
BuildRequires:	Qt5PrintSupport-devel >= %{qtver}
BuildRequires:	Qt5Qml-devel >= %{qtver}
BuildRequires:	Qt5Quick-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
%{?with_webengine:BuildRequires:	Qt5WebChannel-devel >= %{qtver}}
%{?with_webengine:BuildRequires:	Qt5WebEngine-devel >= %{qtver}}
BuildRequires:	Qt5Widgets-devel
BuildRequires:	boost-devel
BuildRequires:	gettext-devel
BuildRequires:	ka5-libktorrent-devel >= 21.04.1
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-karchive-devel >= %{kframever}
BuildRequires:	kf5-kauth-devel >= %{kframever}
BuildRequires:	kf5-kcmutils-devel >= %{kframever}
BuildRequires:	kf5-kcodecs-devel >= %{kframever}
BuildRequires:	kf5-kcompletion-devel >= %{kframever}
BuildRequires:	kf5-kconfig-devel >= %{kframever}
BuildRequires:	kf5-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf5-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf5-kcrash-devel >= %{kframever}
BuildRequires:	kf5-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf5-kdnssd-devel >= %{kframever}
BuildRequires:	kf5-kdoctools-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	kf5-kiconthemes-devel >= %{kframever}
BuildRequires:	kf5-kio-devel >= %{kframever}
BuildRequires:	kf5-kitemviews-devel >= %{kframever}
BuildRequires:	kf5-kjobwidgets-devel >= %{kframever}
BuildRequires:	kf5-knotifications-devel >= %{kframever}
BuildRequires:	kf5-knotifyconfig-devel >= %{kframever}
BuildRequires:	kf5-kparts-devel >= %{kframever}
BuildRequires:	kf5-kplotting-devel >= %{kframever}
BuildRequires:	kf5-kross-devel >= %{kframever}
BuildRequires:	kf5-kservice-devel >= %{kframever}
BuildRequires:	kf5-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf5-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf5-kxmlgui-devel >= %{kframever}
BuildRequires:	kf5-solid-devel >= %{kframever}
BuildRequires:	kf5-sonnet-devel >= %{kframever}
BuildRequires:	kf5-syndication-devel >= %{kframever}
BuildRequires:	kp5-plasma-workspace-devel
BuildRequires:	phonon-qt5-devel
BuildRequires:	pkgconfig
BuildRequires:	taglib-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KTorrent is a BitTorrent program for KDE.

Its main features are:
- Downloads torrent files
- Upload speed capping, seeing that most people can't upload infinite
  amounts of data.
- Internet searching using various search engines, you can even add
  your own.
- UDP Trackers

%description -l de.UTF-8
KTorrent ist ein BitTorrent Klient für KDE.

Hauptfunktionen sind:
- Torrent-Dateien Download
- Begränzung des Uploades, so dass Mehrheit der Leute nicht unerlaubt
  unbegränzte Datenflüsse sendet
- Durchsuchung des Internets mit hilfe diverser Browser, man kann
  sogar den eigenen Browser dazu schreiben
- UDP Trackers

%description -l pl.UTF-8
KTorrent to klient BitTorrenta dla KDE.

Główne cechy to:
- ściąganie plików torrent
- ograniczanie szybkości uploadu, baczące żeby większość ludzi
  nie przesyłała nieograniczonej ilości danych
- przeszukiwanie Internetu przy użyciu różnych wyszukiwarek, można
  nawet dodać własną
- trackery UDP

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ktmagnetdownloader
%attr(755,root,root) %{_bindir}/ktorrent
%attr(755,root,root) %{_bindir}/ktupnptest
%ghost %{_libdir}/libktcore.so.16
%attr(755,root,root) %{_libdir}/libktcore.so.*.*.*
%if %{with webengine}
%{_iconsdir}/hicolor/16x16/actions/kt-add-feeds.png
%{_iconsdir}/hicolor/16x16/actions/kt-add-filters.png
%{_iconsdir}/hicolor/16x16/actions/kt-remove-feeds.png
%{_iconsdir}/hicolor/16x16/actions/kt-remove-filters.png
%{_iconsdir}/hicolor/22x22/actions/kt-add-feeds.png
%{_iconsdir}/hicolor/22x22/actions/kt-add-filters.png
%{_iconsdir}/hicolor/22x22/actions/kt-remove-feeds.png
%{_iconsdir}/hicolor/22x22/actions/kt-remove-filters.png
%{_iconsdir}/hicolor/32x32/actions/kt-add-feeds.png
%{_iconsdir}/hicolor/32x32/actions/kt-add-filters.png
%{_iconsdir}/hicolor/32x32/actions/kt-remove-feeds.png
%{_iconsdir}/hicolor/32x32/actions/kt-remove-filters.png
%endif
%{_desktopdir}/org.kde.ktorrent.desktop
%{_iconsdir}/hicolor/128x128/apps/ktorrent.png
%{_iconsdir}/hicolor/16x16/actions/kt-stop-all.png
%{_iconsdir}/hicolor/16x16/actions/kt-stop.png
%{_iconsdir}/hicolor/16x16/actions/kt-upnp.png
%{_iconsdir}/hicolor/16x16/apps/ktorrent.png
%{_iconsdir}/hicolor/22x22/actions/kt-magnet.png
%{_iconsdir}/hicolor/22x22/actions/kt-pause.png
%{_iconsdir}/hicolor/22x22/actions/kt-remove.png
%{_iconsdir}/hicolor/22x22/actions/kt-set-max-download-speed.png
%{_iconsdir}/hicolor/22x22/actions/kt-set-max-upload-speed.png
%{_iconsdir}/hicolor/22x22/actions/kt-speed-limits.png
%{_iconsdir}/hicolor/22x22/actions/kt-start-all.png
%{_iconsdir}/hicolor/22x22/actions/kt-start.png
%{_iconsdir}/hicolor/22x22/actions/kt-stop-all.png
%{_iconsdir}/hicolor/22x22/actions/kt-stop.png
%{_iconsdir}/hicolor/22x22/apps/ktorrent.png
%{_iconsdir}/hicolor/32x32/actions/kt-info-widget.png
%{_iconsdir}/hicolor/32x32/actions/kt-magnet.png
%{_iconsdir}/hicolor/32x32/actions/kt-pause.png
%{_iconsdir}/hicolor/32x32/actions/kt-queue-manager.png
%{_iconsdir}/hicolor/32x32/actions/kt-remove.png
%{_iconsdir}/hicolor/32x32/actions/kt-set-max-download-speed.png
%{_iconsdir}/hicolor/32x32/actions/kt-set-max-upload-speed.png
%{_iconsdir}/hicolor/32x32/actions/kt-speed-limits.png
%{_iconsdir}/hicolor/32x32/actions/kt-start-all.png
%{_iconsdir}/hicolor/32x32/actions/kt-start.png
%{_iconsdir}/hicolor/32x32/actions/kt-stop-all.png
%{_iconsdir}/hicolor/32x32/actions/kt-stop.png
%{_iconsdir}/hicolor/32x32/actions/kt-upnp.png
%{_iconsdir}/hicolor/32x32/apps/ktorrent.png
%{_iconsdir}/hicolor/48x48/actions/kt-bandwidth-scheduler.png
%{_iconsdir}/hicolor/48x48/actions/kt-change-tracker.png
%{_iconsdir}/hicolor/48x48/actions/kt-check-data.png
%{_iconsdir}/hicolor/48x48/actions/kt-chunks.png
%{_iconsdir}/hicolor/48x48/actions/kt-info-widget.png
%{_iconsdir}/hicolor/48x48/actions/kt-magnet.png
%{_iconsdir}/hicolor/48x48/actions/kt-pause.png
%{_iconsdir}/hicolor/48x48/actions/kt-plugins.png
%{_iconsdir}/hicolor/48x48/actions/kt-queue-manager.png
%{_iconsdir}/hicolor/48x48/actions/kt-remove.png
%{_iconsdir}/hicolor/48x48/actions/kt-restore-defaults.png
%{_iconsdir}/hicolor/48x48/actions/kt-set-max-download-speed.png
%{_iconsdir}/hicolor/48x48/actions/kt-set-max-upload-speed.png
%{_iconsdir}/hicolor/48x48/actions/kt-show-hide.png
%{_iconsdir}/hicolor/48x48/actions/kt-show-statusbar.png
%{_iconsdir}/hicolor/48x48/actions/kt-speed-limits.png
%{_iconsdir}/hicolor/48x48/actions/kt-start-all.png
%{_iconsdir}/hicolor/48x48/actions/kt-start.png
%{_iconsdir}/hicolor/48x48/actions/kt-stop-all.png
%{_iconsdir}/hicolor/48x48/actions/kt-stop.png
%{_iconsdir}/hicolor/48x48/actions/kt-upnp.png
%{_iconsdir}/hicolor/48x48/apps/ktorrent.png
%{_iconsdir}/hicolor/64x64/actions/kt-magnet.png
%{_iconsdir}/hicolor/64x64/apps/ktorrent.png
%{_iconsdir}/hicolor/scalable/actions/kt-magnet.svgz
%{_iconsdir}/hicolor/scalable/actions/kt-set-max-download-speed.svgz
%{_iconsdir}/hicolor/scalable/actions/kt-set-max-upload-speed.svgz
%{_iconsdir}/hicolor/scalable/actions/kt-speed-limits.svgz
%{_datadir}/knotifications5/ktorrent.notifyrc
%{?with_webengine:%{_datadir}/ktorrent}
%{_datadir}/kxmlgui5/ktorrent
%{_datadir}/metainfo/org.kde.ktorrent.appdata.xml
%dir %{_libdir}/qt5/plugins/ktorrent_plugins
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_bwscheduler.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_downloadorder.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_infowidget.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_ipfilter.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_logviewer.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_magnetgenerator.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_mediaplayer.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_scanfolder.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_scanforlostfiles.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_shutdown.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_stats.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_upnp.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_zeroconf.so

%if %{with webengine}
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_search.so
%attr(755,root,root) %{_libdir}/qt5/plugins/ktorrent_plugins/ktorrent_syndication.so
%endif
