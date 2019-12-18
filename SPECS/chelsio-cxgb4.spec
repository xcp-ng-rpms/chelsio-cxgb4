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
Release: 2%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-chelsio-cxgb4/archive?at=1.0.1&format=tgz&prefix=driver-chelsio-cxgb4-1.0.1#/chelsio-cxgb4-1.0.1.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-chelsio-cxgb4/archive?at=1.0.1&format=tgz&prefix=driver-chelsio-cxgb4-1.0.1#/chelsio-cxgb4-1.0.1.tar.gz) = f7797e0a44726a838e8cf64b383b454918c239eb


Provides: cheliso-cxgb4 = %{version}-%{release}
Obsoletes: cheliso-cxgb4 < 1.0.1-2

BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} KVER=%{kernel_version}

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} KVER=%{kernel_version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

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

%changelog
* Wed May 22 2019 Deli Zhang <deli.zhang@citrix.com> - 1.0.1-2
- CA-315989: Correct the package name to chelsio-cxgb4

* Thu Jan 10 2019 Deli Zhang <deli.zhang@citrix.com> - 1.0.1-1
- CP-30263: Upgrade chelsio-cxgb4 driver to version 1.0.1
