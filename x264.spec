%define distsuffix plf

%define major 142
%define date 20140615
%define rev 2245
%define fname %{name}-snapshot-%{date}-%{rev}-stable

%define libname %mklibname %{name}_ %{major}
%define devname %mklibname %{name} -d
%define static %mklibname %{name} -d -s

Summary:	H264/AVC encoder
Name:		x264
Version:	0.%{major}
Release:	0.%{date}.2
License:	GPLv2+
Group:		Video
Url:		http://x264.nl/
Source0:	ftp://ftp.videolan.org/pub/videolan/x264/snapshots/%{fname}.tar.bz2
BuildRequires:	git-core
BuildRequires:	yasm
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(x11)

%description
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

This package is in Restricted repository as the video encoder may be covered
by software patents.

%files
%doc AUTHORS doc/*
%{_bindir}/%{name}

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library of x264
Group:		System/Libraries

%description -n %{libname}
x264 dynamic libraries.

%files -n %{libname}
%{_libdir}/libx264.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	H264/AVC encoding library headers
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

%files -n %{devname}
%{_libdir}/libx264.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%package -n %{static}
Summary:	Static library for the x264 H264/AVC encoding library
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}
Conflicts:	%{_lib}x264-devel < 0.142

%description -n %{static}
Static library for the x264 H264/AVC encoding library.

%files -n %{static}
%{_libdir}/libx264.a

#----------------------------------------------------------------------------

%prep
%setup -q -n %{fname}

%build
CFLAGS="%{optflags} -Ofast" \
%configure2_5x \
	--enable-shared \
	--enable-static \
	--enable-pic \
	--enable-visualize \
	--disable-gpac
%make

%install
%makeinstall

