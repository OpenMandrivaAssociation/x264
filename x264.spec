Summary: 	H264/AVC encoder
Name: 		x264
Version: 	0.%{major}
%define	date	20111212
Release: 	0.%{data}.1
%define	rev	2245
%define	fname	%{name}-snapshot-%{date}-%{rev}
Source0: 	ftp://ftp.videolan.org/pub/videolan/x264/snapshots/%fname.tar.bz2

License: 	GPLv2+
Group: 		Video
Url: 		http://x264.nl/

BuildRequires:	yasm
BuildRequires:	git-core
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(libavfilter)

%description
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

This package is in tainted repository as the video encoder may be covered
by software patents.

%define	major	120
%define	libname	%mklibname %{name}_ %{major}
%define	devname	%mklibname -d %{name}

%package -n	%{libname}
Summary:	Shared library of x264
Group:		System/Libraries

%description -n	%{libname}
x264 dynamic libraries

%package -n	%{devname}
Summary:	H264/AVC encoding library headers
Group:		Development/C
Requires:	%{libname} = %{version}-%release
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
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
%makeinstall
ln -sf libx264.so.%{major} %{buildroot}%{_libdir}/libx264.so

%files
%doc AUTHORS doc/*
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libx264.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/libx264.a
%{_libdir}/libx264.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
