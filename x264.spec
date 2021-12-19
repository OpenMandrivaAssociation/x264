%define	major	163
%define	date	20210901
%define	git	5db6aa6cab1b146e07b60cc1736a01f21da01154
%define	fname	%{name}-stable-%{git}
%define	libname	%mklibname %{name}_ %{major}
%define	devname	%mklibname -d %{name}
%define	static	%mklibname -d -s %{name}

%define _disable_lto 1
%global optflags %{optflags} -O3

# x264 is used by ffmpeg, ffmpeg is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%define lib32name lib%{name}_%{major}
%define dev32name lib%{name}-devel

Summary:	H264/AVC encoder
Name:		x264
Version:	0.%{major}
Release:	0.%{date}.2
Source0:	https://code.videolan.org/videolan/x264/-/archive/stable/x264-stable-%{date}.tar.bz2
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
%if %{with compat32}
BuildRequires:	devel(libX11)
%endif
BuildRequires:	pkgconfig(bash-completion)
Requires:	%{libname} = %{EVRD}

%description
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

This package is in restricted repository as the video encoder may be covered
by software patents.

%package -n %{libname}
Summary:	Shared library of x264
Group:		System/Libraries
Obsoletes:	%{mklibname x264_ 120} <= 0.120
Obsoletes:	%{mklibname x264_ 124} <= 0.124

%description -n %{libname}
x264 dynamic libraries.

%package -n %{devname}
Summary:	H264/AVC encoding library headers
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.

%package -n %{static}
Summary:	Static library for the x264 H264/AVC encoding library
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n %{static}
Static library for the x264 H264/AVC encoding library.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared library of x264 (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
x264 dynamic libraries.

%package -n %{dev32name}
Summary:	H264/AVC encoding library headers (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n %{dev32name}
x264 is a free library for encoding H264/AVC video streams. The code
is written by Laurent Aimar, Eric Petit(OS X), Min Chen (vfw/nasm),
Justin Clay(vfw), Måns Rullgård and Loren Merritt from scratch. It is
released under the terms of the GPL license.
%endif

%prep
%autosetup -n %{fname} -p1
sed -i -e 's|-O3 -ffast-math|%{optflags}|g' configure

# Looks like autoconf, but isn't -- out-of-tree builds aren't supported,
# so we have to get a little ugly
%if %{with compat32}
mkdir build32
cp -a $(ls |grep -v build32) build32/
cd build32
export CFLAGS="$(echo %{optflags} |sed -e 's,-m64,,g') -m32"
export LDFLAGS="$(echo %{ldflags} |sed -e 's,-m64,,g') -m32"
export CC=gcc
./configure --host=i686-openmandriva-linux-gnu \
	--prefix=%{_prefix} \
	--libdir=%{_prefix}/lib \
	--enable-pic \
	--enable-shared
unset CFLAGS
unset LDFLAGS
unset CC
cd ..
%endif
%configure	--enable-shared \
		--enable-static \
		--enable-pic \

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install

%files
%doc AUTHORS doc/*
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/*

%files -n %{libname}
%{_libdir}/libx264.so.%{major}*

%files -n %{devname}
%{_libdir}/libx264.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc

%files -n %{static}
%{_libdir}/libx264.a

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libx264.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libx264.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
