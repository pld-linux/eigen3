#
# Conditional build:
%bcond_with	tests		# make check (takes very long time, few tests fail)
%bcond_without	gdb		# GDB pretty printers

Summary:	C++ template library for linear algebra
Summary(pl.UTF-8):	Biblioteka szablonów C++ do algebry liniowej
Name:		eigen3
Version:	3.3.7
Release:	1
License:	LGPL v3+ or GPL v2+
Group:		Development/Libraries
#Source0Download: http://eigen.tuxfamily.org/index.php?title=Main_Page
Source0:	https://bitbucket.org/eigen/eigen/get/%{version}.tar.bz2
# Source0-md5:	05b1f7511c93980c385ebe11bd3c93fa
Patch0:		%{name}-buildtype.patch
URL:		http://eigen.tuxfamily.org/
BuildRequires:	cmake >= 2.8.5
%{?with_gdb:BuildRequires:	python-modules}
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eigen is a C++ template library for linear algebra: vectors, matrices,
and related algorithms. It is versatile, fast, elegant and
compiler-friendly.

Eigen handles, without code duplication and in a completely integrated
way:
 - both fixed-size and dynamic-size matrices and vectors
 - both dense and sparse (the latter is still experimental) matrices
   and vectors
 - both plain matrices/vectors and abstract expressions
 - both column-major (the default) and row-major matrix storage
 - both basic matrix/vector manipulation and many more advanced,
   specialized modules providing algorithms for linear algebra,
   geometry, quaternions, or advanced array manipulation.

%description -l pl.UTF-8
Eigen to biblioteka szablonów C++ do algebry liniowej: wektorów,
macierzy i związanych z nimi algorytmów. Jest elastyczna, szybka,
elegancka i przyjazna dla kompilatorów.

Obsługuje bez powielania kodu i w całkowicie zintegrowany sposób:
 - macierze i wektory o stałym i dynamicznym rozmiarze
 - macierze i wektory gęste i rzadkie (te drugie jeszcze
   eksperymentalnie)
 - zwykłe macierze/wektory jak i abstrakcyjne wyrażenia
 - przechowywanie danych kolumnowe (domyślne) oraz wierszowe
 - podstawowe operacje na macierzach/wektorach, jak i wiele
   bardziej zaawansowanych, specjalizowanych modułów z algorytmami
   algebry liniowej, geometrii, kwaternionów i zaawansowanych operacji
   na tablicach.

%package gdb
Summary:	eigen3 pretty printers for GDB
Summary(pl.UTF-8):	Funkcje wypisujące dane eigen3 dla GDB
Group:		Development/Debuggers

%description gdb
This package contains Python scripts for GDB pretty printing of the
eigen3 types/containers.
To use it add:

python
from eigen3.printers import register_eigen_printers
register_eigen_printers (None)
end

to a ~/.gdbinit file.

%description gdb -l pl.UTF-8
Ten pakiet zawiera skrypty Pythona dla GDB służące do ładnego
wypisywania typów i kontenerów eigen3.
Aby użyć skryptów trzeba dodać:

python
from eigen3.printers import register_eigen_printers
register_eigen_printers (None)
end

do pliku ~/.gdbinit .

%prep
%setup -q -n eigen-eigen-323c052e1731
%patch0 -p1

%build
install -d build
cd build
# CMakeLists.txt requires CMAKE_INSTALL_INCLUDEDIR to be relative (for proper .pc file generation)
%cmake .. \
	-DCMAKE_CXX_COMPILER_WORKS=1 \
	-DCMAKE_CXX_COMPILER="%{__cxx}" \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with gdb}
install -D debug/gdb/printers.py $RPM_BUILD_ROOT%{_datadir}/gdb/python/%{name}/printers.py
touch $RPM_BUILD_ROOT%{_datadir}/gdb/python/%{name}/__init__.py
%py_comp $RPM_BUILD_ROOT%{_datadir}/gdb/python/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/gdb/python/%{name}
%py_postclean %{_datadir}/gdb/python/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_includedir}/eigen3
%{_npkgconfigdir}/eigen3.pc
%dir %{_datadir}/eigen3
%{_datadir}/eigen3/cmake

%if %{with gdb}
%files gdb
%defattr(644,root,root,755)
%{_datadir}/gdb/python/%{name}
%endif
