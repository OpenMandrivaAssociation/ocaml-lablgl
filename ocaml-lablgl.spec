%define modname lablgl
%define srcname lablGL

Summary:	OpenGL interface for OCaml
Name:		ocaml-%{modname}
Version:	1.05
Release:	1
License:	BSD
Group:		Development/Other
Url:		http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
Source0:	http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/%{modname}-%{version}.tar.gz
BuildRequires:	camlp4
BuildRequires:	ocaml
BuildRequires:	ocaml-labltk
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(xmu)
Requires:	ocaml-labltk

%description
LablGL is is an OCaml interface to OpenGL. Support is included for
use with both Glut (standalone) and LablTk.

%files
%doc COPYRIGHT CHANGES README
%dir %{_libdir}/ocaml/lablGL
%{_libdir}/ocaml/lablGL/*.cmi
%{_libdir}/ocaml/lablGL/*.cma
%{_libdir}/ocaml/lablGL/META
%{_libdir}/ocaml/stublibs/*.so
%{_bindir}/lablgl
%{_bindir}/lablglut

#----------------------------------------------------------------------------

%package devel
Summary:	OpenGL interface for OCaml
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glu)
Requires:	pkgconfig(glut)
Requires:	pkgconfig(xmu)

%description devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%files devel
%{_libdir}/ocaml/lablGL/*.a
%{_libdir}/ocaml/lablGL/*.cmx
%{_libdir}/ocaml/lablGL/*.cmxa
%{_libdir}/ocaml/lablGL/*.mli

#----------------------------------------------------------------------------

%prep
%setup -q -n %{modname}-%{version}

cp -f %{_includedir}/tk8.6/generic/tkInt.h Togl/src/Togl/tkInt%{tcl_version}.h
cp -f %{_includedir}/tk8.6/generic/tkIntDecls.h Togl/src/Togl/tkIntDecls%{tcl_version}.h
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
directory="+lablGL"
archive(byte) = "lablgl.cma"
archive(native) = "lablgl.cmxa"

package "togl" (
  requires = "labltk lablGL"
  archive(byte) = "togl.cma"
  archive(native) = "togl.cmxa"
)

package "glut" (
  requires = "lablGL"
  archive(byte) = "lablglut.cma"
  archive(native) = "lablglut.cmxa"
)
EOF

