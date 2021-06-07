%global testmpio_home %{_libdir}/mpich/testmpio

Name:		testmpio
Version:	1.2
Release:	4%{?dist}
Summary:	LLNL test suite

License:	Unknown
URL:		http://ftp.mcs.anl.gov/
Source0:	http://ftp.mcs.anl.gov/pub/mpi/mpi-test/%{name}-%{version}.tar.gz
Patch0:		daos.patch

BuildRequires:	mpich-devel
BuildRequires:	ed

%description
LLNL test suite

%prep
%autosetup -n Testmpio
cat Makefile
%if (0%{?suse_version} >= 1500)
# hack because module load on Leap doesn't set MPIHOME
MPIHOME=/usr/lib64/mpi/gcc/mpich/
%else
module load mpi/mpich-x86_64
MPIHOME=$MPI_HOME
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
mkdir -p %{buildroot}/%{testmpio_home}/ %{buildroot}%{_libdir}/
# create compatibility link
ln -s ../mpich/testmpio %{buildroot}/%{_libdir}/

install -m 755 testmpio %{buildroot}/%{testmpio_home}/
install -m 755 testmpio_daos %{buildroot}/%{testmpio_home}/

%files
%{testmpio_home}
%{_libdir}/testmpio
%doc
%license

%changelog
* Mon May 31 2021 Brian J. Murrell <brian.murrell@intel.com> - 1.2-4
- Build on EL8
- Remove the virtual provides
- Install under mpich prefix
- Create compatibility link

* Thu Jun 18 2020 Brian J. Murrell <brian.murrell@intel.com> - 1.2-3
- Use the MPIHOME that module load returns except on Leap 15

* Sun Dec 29 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.2-2
- Add Provides: %{name}-cart-%{cart_major}-daos-%{daos_major}

* Wed Sep 04 2019 Brian J. Murrell <brian.murrell@intel.com> - 1.2-1
- Initial package
