%define base_name	lablgl

%define rel		8
%define cvs		20081204
# CVSROOT=:pserver:anoncvs@camlcvs.inria.fr:/caml cvs login
# (empty password)
# cvs co bazar-ocaml/lablGL
%if %cvs
%define distname	%{base_name}-%{cvs}.tar.lzma
%define dirname		lablGL
%define release		0.%{cvs}.%{rel}
%else
%define distname	%{base_name}-%{version}.tar.gz
%define dirname		%{base_name}-%{version}
%define release		%{rel}
%endif

Name:		ocaml-%{base_name}
Version:	1.04
Release:	%{release}
Summary:	OpenGL interface for Objective Caml
License:	BSD
Group:		Development/Other
URL:		http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
Source0:	http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/%{distname}
Patch0:		lablgl-1.0.4-tcl86.patch
BuildRequires:	ocaml
BuildRequires:	camlp4
BuildRequires:	ocaml-labltk
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	X11-devel
BuildRequires:	Mesa-common-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%package devel
Summary:	OpenGL interface for Objective Caml
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description
LablGL is is an Objective Caml interface to OpenGL. Support is included for use
inside LablTk, and LablGTK also includes specific support for LablGL.

It can be used either with proprietary OpenGL implementations (SGI, Digital
Unix, Solaris...), with XFree86 GLX extension, or with open-source Mesa.

%description -n %{name}-devel
LablGL is is an Objective Caml interface to OpenGL. Support is included for use
inside LablTk, and LablGTK also includes specific support for LablGL.

It can be used either with proprietary OpenGL implementations (SGI, Digital
Unix, Solaris...), with XFree86 GLX extension, or with open-source Mesa.

%prep
%setup -q -n %{dirname}
%patch0 -p1 -b .tcl86

cp -f %{_includedir}/tk%{tcl_version}/generic/tkInt.h Togl/src/Togl/tkInt%{tcl_version}.h
cp -f %{_includedir}/tk%{tcl_version}/generic/tkIntDecls.h Togl/src/Togl/tkIntDecls%{tcl_version}.h
sed -i -e 's,tkIntDecls.h,tkIntDecls%{tcl_version}.h,g' Togl/src/Togl/tkInt%{tcl_version}.h

cat > Makefile.config << EOF
CAMLC = ocamlc.opt
CAMLOPT = ocamlopt.opt
BINDIR = %{_bindir}
XINCLUDES = -I%{_includedir}
XLIBS = -L%{_libdir} -lXext -lXmu -lX11
TKINCLUDES = -I%{_includedir}
GLINCLUDES =
GLLIBS = -lGL -lGLU
GLUTLIBS = -lglut
RANLIB = :
LIBDIR = %{_libdir}/ocaml
DLLDIR = %{_libdir}/ocaml/stublibs
INSTALLDIR = %{_libdir}/ocaml/lablGL
TOGLDIR=Togl
COPTS = %{optflags}
EOF

%build

make all opt

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_libdir}/ocaml/lablGL
install -d -m 755 %{buildroot}%{_libdir}/ocaml/stublibs
make \
   BINDIR=%{buildroot}%{_bindir}\
   INSTALLDIR=%{buildroot}%{_libdir}/ocaml/lablGL\
   DLLDIR=%{buildroot}%{_libdir}/ocaml/stublibs\
   install

rm -f %{buildroot}%{_libdir}/ocaml/lablGL/*.ml

# Make and install a META file.
cat > %{buildroot}%{_libdir}/ocaml/lablGL/META<<EOF
version="%{version}"
directory="+lablgl"
archive(byte) = "lablgl.cma"
archive(native) = "lablgl.cmxa"

package "togl" (
  requires = "labltk lablgl"
  archive(byte) = "togl.cma"
  archive(native) = "togl.cmxa"
)

package "glut" (
  requires = "lablgl"
  archive(byte) = "lablglut.cma"
  archive(native) = "lablglut.cmxa"
)
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT CHANGES README
%dir %{_libdir}/ocaml/lablGL
%{_libdir}/ocaml/lablGL/*.cmi
%{_libdir}/ocaml/lablGL/*.cma
%{_libdir}/ocaml/lablGL/META
%{_libdir}/ocaml/stublibs/*.so
%{_bindir}/lablgl
%{_bindir}/lablglut

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/ocaml/lablGL/*.a
%{_libdir}/ocaml/lablGL/*.cmx
%{_libdir}/ocaml/lablGL/*.cmxa
%{_libdir}/ocaml/lablGL/*.mli
%exclude %{_bindir}/lablgl
%exclude %{_bindir}/lablglut
