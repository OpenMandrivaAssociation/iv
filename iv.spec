%define name    iv
%define version 2.2.4
%define release %mkrel 1

%define title       IV
%define longtitle   Image browser

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Image Viewer
Group:          Graphics
License:        GPL
URL:            http://wolfpack.twu.net/IV/
Source:         http://wolfpack.twu.net/users/wolfpack/%{name}-%{version}.tar.bz2
BuildRequires:  XFree86-devel
BuildRequires:  gtk+-devel
BuildRequires:  imlib2-devel
BuildRequires:  ImageMagick
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Sometimes reffered to as ImgView or IV, this is a basic image viewer
with pan and zoom capabilities, depends on GTK+ and Imlib. Can also
save to many different formats, display transparency, crop, print, and
do window grabs.

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
./configure Linux -v --disable=arch-i686 --libdir=-L%{_libdir}
#%make CFLAGS="%{optflags}" all
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

