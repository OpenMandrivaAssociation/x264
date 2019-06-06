%define	major	155
%define	date	20190209
%define	time	2245
%define	fname	%{name}-snapshot-%{date}-%{time}-stable
%define	libname	%mklibname %{name}_ %{major}
%define	devname	%mklibname -d %{name}
%define	static	%mklibname -d -s %{name}

%define _disable_lto 1

Summary:	H264/AVC encoder
Name:		x264
Version:	0.%{major}
Release:	0.%{date}.1
Source0:	ftp://ftp.videolan.org/pub/videolan/x264/snapshots/%fname.tar.bz2
Patch0:		x264-dynamically-link-against-gpac.patch
Patch1:		x264-arm.patch
License:	GPLv2+
Group:		Video
Url:		http://x264.nl/

BuildRequires:	yasm
%ifarch %{ix86} %{x86_64}
BuildRequires:	nasm >= 2.13
%endif
BuildRequires:	git-core
BuildRequires:	pkgconfig(gpac)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(x11)

%description
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

This package is in restricted repository as the video encoder may be covered
by software patents.

%package -n	%{libname}
Summary:	Shared library of x264
Group:		System/Libraries
Obsoletes:	%{mklibname x264_ 120} <= 0.120
Obsoletes:	%{mklibname x264_ 124} <= 0.124

%description -n	%{libname}
x264 dynamic libraries.

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

%package -n	%{static}
Summary:	Static library for the x264 H264/AVC encoding library
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n %{static}
Static library for the x264 H264/AVC encoding library.

%prep
%setup -q -n %{fname}
%apply_patches

%build
CFLAGS="%{optflags} -Ofast" \
%configure	--enable-shared \
		--enable-pic \
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

%files -n %{static}
%{_libdir}/libx264.a
