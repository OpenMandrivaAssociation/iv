%define name    iv
%define version 2.6.1
%define release %mkrel 2

%define title       IV
%define longtitle   Image browser

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Image Viewer
Group:          Graphics
License:        GPL
Source:         http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2
Patch0:         iv-2.6.1-fix-build-errors.patch
Patch1:         iv-2.5.1-fix-lib64-build.patch
BuildRequires:  X11-devel
BuildRequires:  gtk+-devel
BuildRequires:  imlib-devel
BuildRequires:  imagemagick
BuildRequires:  ungif-devel
BuildRequires:  jpeg-devel
BuildRequires:  png-devel
BuildRequires:  mng-devel
BuildRequires:  libxxf86vm-static-devel
BuildRequires:  endeavour-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Sometimes reffered to as ImgView or IV, this is a basic image viewer
with pan and zoom capabilities, depends on GTK+ and Imlib. Can also
save to many different formats, display transparency, crop, print, and
do window grabs.

%prep
%setup -q
%patch0 -p 1
%patch1 -p 1

%build
export CFLAGS="%{optflags} -I%{_includedir}/endeavour2" 
%ifarch x86_64
%define platform Linux64
%else
%define platform Linux
%endif
./configure %{platform} \
    -v --disable=arch-i686 --libdir=-L%{_libdir} --enable=debug
%make all

%install
rm -rf %{buildroot}
%make PREFIX=%{buildroot}%_prefix MAN_DIR=%{buildroot}%{_mandir}/man1 install

# icons
convert %{name}/%{name}.xpm -resize 16x16 %{name}-16.png
convert %{name}/%{name}.xpm -resize 32x32 %{name}-32.png
convert %{name}/%{name}.xpm %{name}-48.png
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png 

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Viewer
EOF

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_iconsdir}/%{name}.xpm
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

