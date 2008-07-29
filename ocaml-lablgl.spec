%define base_name	lablgl
%define name		ocaml-%{base_name}
%define version		1.02
%define release		%mkrel 19

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:    OpenGL interface for Objective Caml
License:    BSD
Group:      System/Libraries
URL:        http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
Source:     http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgl-%{version}.tar.bz2
Patch:      %{name}-1.02-tk8.5.patch
BuildRequires:  ocaml
BuildRequires:  camlp4
BuildRequires:  ocaml-labltk
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  X11-devel
BuildRequires:  Mesa-common-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

%package devel
Summary:    OpenGL interface for Objective Caml
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}

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
%patch0 -p 1

%build
cat > Makefile.config << EOF
CAMLC = ocamlc.opt
CAMLOPT = ocamlopt.opt
BINDIR = %{_bindir}
XINCLUDES = -I%{_includedir}
XLIBS = -L%{_libdir} -lXext -lXmu -lX11 -lXi
TKINCLUDES = -I%{_includedir}
GLLIBS = -lGL -lGLU
GLUTLIBS = -lglut
GLINCLUDES =
RANLIB = ranlib
COPTS = $RPM_OPT_FLAGS
EOF

make all opt

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{ocaml_sitelib}/stublibs
make \
   BINDIR=%{buildroot}/%{_bindir}\
   INSTALLDIR=%{buildroot}/%{ocaml_sitelib}/lablgl\
   DLLDIR=%{buildroot}/%{ocaml_sitelib}/stublibs\
   install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT CHANGES README
%dir %{ocaml_sitelib}/lablgl
%{ocaml_sitelib}/lablgl/*.cmi
%{ocaml_sitelib}/stublibs/*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{ocaml_sitelib}/lablgl/*
%exclude %{ocaml_sitelib}/lablgl/*.cmi
