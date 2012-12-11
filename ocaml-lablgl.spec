%define base_name	lablgl
%define srcname		lablGL

%define rel		10
#define cvs		20081204
%define	cvs		0
# CVSROOT=:pserver:anoncvs@camlcvs.inria.fr:/caml cvs login
# (empty password)
# cvs co bazar-ocaml/lablGL
%if %{cvs}
%define distname	%{base_name}-%{cvs}.tar.lzma
%define srcdir		lablGL
%define release		0.%{cvs}.%{rel}
%else
%define distname	%{base_name}-%{version}.tar.gz
%define srcdir		%{srcname}-%{version}
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
BuildRequires:	mesa-common-devel

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
%setup -q -n %{srcdir}
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


%changelog
* Sat Sep 17 2011 Alexandre Lissy <alissy@mandriva.com> 1.04-9
+ Revision: 700145
- Using official 1.04 sources instead of "CVS"

* Fri Sep 16 2011 Alexandre Lissy <alissy@mandriva.com> 1.04-0.20081204.8
+ Revision: 700049
- Forcing release sicne package does not appear ...

* Fri Sep 16 2011 Alexandre Lissy <alissy@mandriva.com> 1.04-0.20081204.7
+ Revision: 700043
- Release bump, rebuilding for latest ocaml

* Mon Aug 16 2010 Florent Monnier <blue_prawn@mandriva.org> 1.04-0.20081204.6mdv2011.0
+ Revision: 570543
- corrected group

* Mon Jan 25 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.04-0.20081204.6mdv2010.1
+ Revision: 496366
- rebuild

* Sat Jun 27 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.04-0.20081204.5mdv2010.0
+ Revision: 389928
- rebuild

  + Florent Monnier <blue_prawn@mandriva.org>
    - remove doubles

* Mon Dec 29 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.04-0.20081204.4mdv2009.1
+ Revision: 321213
- install in %%{_libdir}/ocaml/lablGL instead of %%{_libdir}/ocaml/lablgl
- ship META file
- ship missing binaries

* Mon Dec 29 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.04-0.20081204.3mdv2009.1
+ Revision: 320757
- move non-devel files in main package
- don't ship ml sources
- site-lib hierarch doesn't exist anymore

* Tue Dec 09 2008 Pixel <pixel@mandriva.com> 1.04-0.20081204.2mdv2009.1
+ Revision: 312227
- rebuild

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 1.04-0.20081204.1mdv2009.1
+ Revision: 311040
- rebuild for new tcl
- add the necessary headers from Tk on-the-fly at build time
- add tcl86.patch to detect tcl 8.6, supersedes tk8.5.patch
- update to current CVS (needed for some build fixes)

* Sun Aug 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.03-1mdv2009.0
+ Revision: 273094
- new version

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.02-19mdv2009.0
+ Revision: 254264
- rebuild

* Fri Mar 07 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.02-17mdv2008.1
+ Revision: 181375
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.02-16mdv2008.1
+ Revision: 171005
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Sep 02 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.02-15mdv2008.0
+ Revision: 78223
- use lowercase installation directory

* Sat Sep 01 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.02-14mdv2008.0
+ Revision: 77696
- fix build with tk8.5
  ocaml policy compliance

  + Pixel <pixel@mandriva.com>
    - rebuild for ocaml 3.10.0


* Thu Jan 25 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.02-12mdv2007.0
+ Revision: 113167
- rebuild for new ocaml
- Import ocaml-lablgl

* Tue Aug 29 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.02-11mdv2007.0
- spec cleanup
- %%mkrel

* Thu Apr 27 2006 Pixel <pixel@mandriva.com> 1.02-10mdk
- rebuild for new ocaml

* Tue Jan 31 2006 Pixel <pixel@mandriva.com> 1.02-9mdk
- add BuildRequires tk-devel, tcl-devel

* Mon Jan 30 2006 Pixel <pixel@mandriva.com> 1.02-8mdk
- add BuildRequires Mesa-common-devel

* Fri Jan 27 2006 Pixel <pixel@mandriva.com> 1.02-7mdk
- add BuildRequires X11-devel

* Thu Jan 26 2006 Pixel <pixel@mandriva.com> 1.02-6mdk
- add BuildRequires camlp4

* Thu Jan 26 2006 Pixel <pixel@mandriva.com> 1.02-5mdk
- simplify BuildRequires (don't build require a file)
- only the stublibs are non-devel stuff (common mistake done in most our packages)

* Thu Jan 19 2006 Guillaume Bedot <littletux@mandriva.org> 1.02-4mdk
- Builds on x86_64

* Wed Nov 09 2005 Guillaume Bedot <littletux@mandriva.org> 1.02-3mdk
- really exclude devel files from ocaml-lablgl package

* Wed Nov 09 2005 Guillaume Bedot <littletux@mandriva.org> 1.02-2mdk
- fixed group
- source in devel package

* Wed Nov 09 2005 Guillaume Bedot <littletux@mandriva.org> 1.02-1mdk
- new release
- use bz2

* Fri Nov 04 2005 Pixel <pixel@mandriva.com> 1.01-2mdk
- rebuild for new ocaml

* Tue Nov 01 2005 Frederic Lepied <flepied@mandriva.com> 1.01-1mdk
- initial Mandriva Linux package

* Thu Jan 27 2005 Aleksey Nogin <rpm@nogin.org>
- Updated to 1.01
- Various minor spec file improvements.

