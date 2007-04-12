%define base_name	lablgl
%define name		ocaml-%{base_name}
%define version		1.02
%define release		%mkrel 12

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:    LablGL is an OpenGL interface for Objective Caml
License:    BSD
Group:      System/Libraries
URL:        http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
Source:     http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgl-%{version}.tar.bz2
BuildRequires:  ocaml
BuildRequires:  camlp4
BuildRequires:  ocaml-labltk
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  X11-devel
BuildRequires:  Mesa-common-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

%package -n %{name}-devel
Summary:    LablGL is an OpenGL interface for Objective Caml
Group:      System/Libraries

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
%setup -q -n lablgl-%version

%build
cat > Makefile.config << EOF
CAMLC = ocamlc.opt
CAMLOPT = ocamlopt.opt
BINDIR = %{_bindir}
XINCLUDES = -I%{_prefix}/X11R6/include
XLIBS = -L%{_prefix}/X11R6/%{_lib} -lXext -lXmu -lX11 -lXi
TKINCLUDES = -I%{_includedir}
GLLIBS = -lGL -lGLU
GLUTLIBS = -lglut
GLINCLUDES =
RANLIB = ranlib
COPTS = $RPM_OPT_FLAGS
EOF

make -j1 all opt

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir} %{buildroot}/%{_libdir}/ocaml/stublibs
make\
   PREFIX=%{buildroot}/%{_prefix}\
   BINDIR=%{buildroot}/%{_bindir}\
   LIBDIR=%{buildroot}/%{_libdir}/ocaml\
   INSTALLDIR=%{buildroot}/%{_libdir}/ocaml/lablGL\
   DLLDIR=%{buildroot}/%{_libdir}/ocaml/stublibs\
   install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYRIGHT
%{_libdir}/ocaml/stublibs/*

%files -n %{name}-devel
%defattr(-,root,root)
%doc CHANGES README
%{_bindir}/*
%{_libdir}/ocaml/lablGL


