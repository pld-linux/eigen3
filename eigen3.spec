Summary:	C++ template library for linear algebra
Summary(pl.UTF-8):	Biblioteka szablonów C++ do algebry liniowej
Name:		eigen3
Version:	3.2.4
Release:	0.1
License:	LGPL v3+ or GPL v2+
Group:		Development/Libraries
#Source0Download: http://eigen.tuxfamily.org/index.php?title=Main_Page
Source0:	https://bitbucket.org/eigen/eigen/get/%{version}.tar.bz2
# Source0-md5:	4c4b5ed9a388a1e475166d575af25477
Patch0:		%{name}-buildtype.patch
URL:		http://eigen.tuxfamily.org/
BuildRequires:	cmake >= 2.8.2
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

%prep
%setup -q -n eigen-eigen-10219c95fe65
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_CXX_COMPILER_WORKS=1 \
	-DCMAKE_CXX_COMPILER="%{__cxx}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_includedir}/eigen3
%{_npkgconfigdir}/eigen3.pc
