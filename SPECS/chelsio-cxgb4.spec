%global package_speccommit 45370bba0e1029cea51b427f8302a3683091dfb5
%global usver 1.0.1
%global xsver 4
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 1.0.1
%define vendor_name Chelsio
%define vendor_label chelsio
%define driver_name cxgb4

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 1.0.1
Release: %{?xsrel}%{?dist}
License: GPL
Source0: chelsio-cxgb4-1.0.1.tar.gz

Provides: cheliso-cxgb4 = %{version}-%{release}
Obsoletes: cheliso-cxgb4 < 1.0.1-2

BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} KVER=%{kernel_version}

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} KVER=%{kernel_version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%{?_cov_results_package}

%changelog
* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.1-4
- CP-38416: Enable static analysis

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.1-3
- CP-35517: Fix build

* Wed May 22 2019 Deli Zhang <deli.zhang@citrix.com> - 1.0.1-2
- CA-315989: Correct the package name to chelsio-cxgb4

* Thu Jan 10 2019 Deli Zhang <deli.zhang@citrix.com> - 1.0.1-1
- CP-30263: Upgrade chelsio-cxgb4 driver to version 1.0.1
