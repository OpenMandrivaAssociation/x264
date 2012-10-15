Summary:	H264/AVC encoder
Name:		x264
%define	major	125
Version:	0.%{major}
%define	date	20121015
Release:	0.%{date}.1
%define	rev	2245
%define	fname	%{name}-snapshot-%{date}-%{rev}-stable
Source0:	ftp://ftp.videolan.org/pub/videolan/x264/snapshots/%fname.tar.bz2

License:	GPLv2+
Group:		Video
Url:		http://x264.nl/

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

%define	libname	%mklibname %{name}_ %{major}
%define	devname	%mklibname -d %{name}
%define staticname %mklibname -d %{name}-static

%package -n	%{libname}
Summary:	Shared library of x264
Group:		System/Libraries

%description -n	%{libname}
x264 dynamic libraries

%package -n	%{devname}
Summary:	H264/AVC encoding library headers
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

%package -n	%{staticname}
Summary:	Static library for the x264 H264/AVC encoding library
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n %{staticname}
Static library for the x264 H264/AVC encoding library

%prep
%setup -q -n %{fname}

%build
CFLAGS="%{optflags} -Ofast" \
%configure2_5x	--enable-shared \
		--enable-pic \
		--enable-visualize \
		--enable-static
%make

%install
%makeinstall

%files
%doc AUTHORS doc/*
%{_bindir}/%{name}

%files -n %{libname}
%{_libdir}/libx264.so.%{major}*

%files -n %{devname}
%{_libdir}/libx264.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc

%files -n %{staticname}
%{_libdir}/libx264.a
