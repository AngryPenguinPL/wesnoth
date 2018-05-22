# TODO add a init file for server, if it is worth
# split data if we can force a rpm to be noarch

Summary:	Fantasy turn-based strategy game
Name:		wesnoth
Version:	1.14.1
Release:	1
License:	GPLv2+
Group:		Games/Strategy
Url:		http://www.wesnoth.org/
Source0:	http://downloads.sourceforge.net/project/wesnoth/wesnoth-%(echo %{version} |cut -d. -f1-2)/wesnoth-%{version}/wesnoth-%{version}.tar.bz2
Source1:	%{name}-icon.png
#Patch0:		wesnoth-sdl-fixed.patch
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(SDL2_net)
BuildRequires:	pkgconfig(SDL2_ttf)
BuildRequires:	pkgconfig(vorbis)
Obsoletes:	wesnoth-unstable < %{version}

%description
Battle for Wesnoth is a fantasy turn-based strategy game.
Battle for control of villages, using variety of units which
have advantages and disadvantages in different types of terrains and
against different types of attacks. Units gain experience and advance
levels, and are carried over from one scenario to the next campaign.

%package -n	%{name}-server
Summary:	Server for "Battle fo Wesnoth" game
Group:		Games/Strategy
Obsoletes:	wesnoth-unstable-server < %{version}

%description -n	%{name}-server
This package contains "Battle for wesnoth" server, used to play multiplayer
game without needing to install the full client.

%prep
%setup -qn %{name}-%{version}%([ -z $(echo %{version} |cut -d. -f3) ] && echo -n .0)
#patch0 -p0

%build
export LDFLAGS="$LDFLAGS -lpthread"
%cmake -DENABLE_STRICT_COMPILATION=OFF \
	-DBINDIR=%{_gamesbindir} \
	-DDATAROOTDIR=%{_gamesdatadir} \
	-DDESKTOPDIR=%{_datadir}/applications \
	-DDOCDIR=%{_datadir}/doc/%{name} \
	-DMANDIR=%{_mandir} -DICONDIR=%{_iconsdir}
%make

%install
%makeinstall_std -C build
find %{buildroot} -name .gitignore |xargs rm -f

%find_lang %{name} --with-man
%find_lang %{name}d --with-man

%files -f %{name}.lang
%doc README.md changelog.md players_changelog.md
%doc %{_docdir}/%{name}/html/
%license COPYING copyright
%{_gamesbindir}/%{name}
%{_mandir}/man6/%{name}.6*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_iconsdir}/hicolor/*/apps/%{name}-icon.png
%{_gamesdatadir}/%{name}/

%files server -f %{name}d.lang
%{_gamesbindir}/%{name}d
%{_mandir}/man6/%{name}d.6*
%ghost %{_localstatedir}/run/%{name}d/socket

