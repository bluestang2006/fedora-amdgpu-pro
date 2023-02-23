%define _build_id_links none

# global info
%global amdvlk 2023.Q1.2


Name:          amdvlk
Version:       %{amdvlk}
Release:       1%{dist}
License:       MIT 
Group:         System Environment/Libraries
Summary:       AMD Open Source Driver for Vulkan

URL:           https://github.com/GPUOpen-Drivers/AMDVLK
Vendor:        Advanced Micro Devices (AMD)

%undefine _disable_source_fetch
Source0 :      https://github.com/GPUOpen-Drivers/AMDVLK/releases/download/v-%{amdvlk}/amdvlk_%{amdvlk}_i386.deb

Provides:      amdvlk = %{amdvlk}-%{release}
Provides:      amdvlk(x86_64) = %{amdvlk}-%{release}

BuildRequires: wget 
BuildRequires: cpio

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig 

Requires:      vulkan-loader
Requires:      openssl-libs

Recommends:    amdgpu-vulkan-switcher(x86_64)

%description
AMD Open Source Driver for Vulkan

%prep
mkdir -p files

ar x --output . %{SOURCE0}
tar -xJC files -f data.tar.xz || tar -xC files -f data.tar.gz

%install
mkdir -p %{buildroot}/opt/amdvlk/vulkan/%{_lib}
mkdir -p %{buildroot}/opt/amdvlk/etc/vulkan/icd.d
mkdir -p %{buildroot}/opt/amdvlk/share/licenses/
#
cp -r files/usr/lib/i386-linux-gnu/* %{buildroot}/opt/amdvlk/vulkan/%{_lib}/
cp -r files/etc/vulkan/icd.d/* %{buildroot}/opt/amdvlk/etc/vulkan/icd.d/
rm -v files/usr/share/doc/amdvlk/changelog.Debian.gz
mv -v files/usr/share/doc/amdvlk/LICENSE.txt %{buildroot}/opt/amdvlk/share/licenses/LICENSE-%{name}_%{_arch}-%{amdvlk}.txt
#
echo "Fixing ICD"
sed -i "s#/usr/lib/i386-linux-gnu/amdvlk32.so#/opt/amdvlk/vulkan/%{_lib}/amdvlk32.so#" "%{buildroot}/opt/amdvlk/etc/vulkan/icd.d/amd_icd32.json"
#
echo "adding *Disabled* library path"
mkdir -p %{buildroot}/etc/ld.so.conf.d
touch %{buildroot}/etc/ld.so.conf.d/amdvlk-%{_arch}.conf
echo "#/opt/amdvlk/vulkan/%{_lib}" > %{buildroot}/etc/ld.so.conf.d/amdvlk-%{_arch}.conf

%files
"/etc/ld.so.conf.d/amdvlk-%{_arch}.conf"
"/opt/amdvlk/vulkan/%{_lib}/amdvlk32.so"
"/opt/amdvlk/etc/vulkan/icd.d/amd_icd32.json"
"/opt/amdvlk/share/licenses/LICENSE-%{name}_%{_arch}-%{amdvlk}.txt"

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
