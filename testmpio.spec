%global testmpio_home %{_libdir}/testmpio
%global cart_major 4
%global daos_major 0

Name:		testmpio
Version:	1.2
Release:	2%{?dist}
Summary:	LLNL test suite

License:	Unknown
URL:		http://ftp.mcs.anl.gov/
Source0:	http://ftp.mcs.anl.gov/pub/mpi/mpi-test/%{name}-%{version}.tar.gz
Patch0:		daos.patch

BuildRequires:	mpich-devel
BuildRequires:	ed
Requires:	mpich
Provides:   %{name}-cart-%{cart_major}-daos-%{daos_major}

%description
LLNL test suite

%prep
%autosetup -n Testmpio
cat Makefile
%if (0%{?suse_version} >= 1500)
MPIHOME=/usr/lib64/mpi/gcc/mpich/
%else
MPIHOME=/usr/lib64/mpich/
%endif
ed Makefile <<EOF
/MPIHOME = /c
MPIHOME = ${MPIHOME//\//\\/}
.
wq
EOF

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/%{testmpio_home}/
install -m 755 testmpio %{buildroot}/%{testmpio_home}/
install -m 755 testmpio_daos %{buildroot}/%{testmpio_home}/

%files
%{testmpio_home}
%doc
%license

%changelog
* Sun Dec 29 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.2-2
- Add Provides: %{name}-cart-%{cart_major}-daos-%{daos_major}

* Wed Sep 04 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.2-1
- Initial package
