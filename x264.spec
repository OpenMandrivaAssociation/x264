%define major   115
%define name 	x264
%define version 0.%{major}
%define date 20110623
%define rev 2245
%define release %mkrel -c %{date} 1

%define libname %mklibname %{name}_ %{major}
%define develname %mklibname -d %{name}
%define fname %{name}-snapshot-%{date}-%{rev}

Summary: 	H264/AVC encoder
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	ftp://ftp.videolan.org/pub/videolan/x264/snapshots/%fname.tar.bz2

License: 	GPLv2+
Group: 		Video
Url: 		http://x264.nl/

BuildRequires:	yasm
BuildRequires: git-core
BuildRequires:	libx11-devel
BuildRequires:	ffmpeg-devel

BuildRoot:	%{_tmppath}/%{name}-%{versio}-%{release}

%description
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

This package is in tainted repository as the video encoder may be covered
by software patents.

%package -n %{libname}
Summary: Shared library of x264
Group: System/Libraries

%description -n %{libname}
x264 dynamic libraries

%package -n %develname
Summary: H264/AVC encoding library headers
Group: Development/C
Requires: %{libname} = %{version}-%release
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %develname
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

%prep
%setup -q -n %{fname}

%build
./configure --enable-shared --enable-pic --enable-visualize --enable-static \
	--extra-cflags="%{optflags}" --extra-ldflags="%{ldflags}" --prefix=/usr
%make

%install
rm -rf %{buildroot}
%makeinstall
ln -sf libx264.so.%{major} %{buildroot}%{_libdir}/libx264.so


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS doc/*
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libx264.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%{_libdir}/libx264.a
%{_libdir}/libx264.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc


