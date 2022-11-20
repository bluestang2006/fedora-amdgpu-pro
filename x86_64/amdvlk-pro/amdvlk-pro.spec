%define _build_id_links none

# global info
%global repo   22.20.4
%global major  22.20
%global minor  1498766
# Distro info
%global ubuntu 22.04

Name:          amdvlk-pro
Version:       %{repo}
Release:       4%{?dist}
License:       AMDGPU PRO  EULA NON-REDISTRIBUTABLE
Group:         System Environment/Libraries
Summary:       AMD Vulkan
URL:           http://repo.radeon.com/amdgpu

%undefine _disable_source_fetch
Source0:       http://repo.radeon.com/amdgpu/%{repo}/ubuntu/pool/proprietary/v/vulkan-amdgpu-pro/vulkan-amdgpu-pro_%{major}-%{minor}~%{ubuntu}_amd64.deb

Provides:      amdvlk-pro = %{major}-%{release}
Provides:      amdvlk-pro(x86_64) = %{major}-%{release}

BuildRequires: wget 
BuildRequires: cpio

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig 

Requires:      vulkan-loader
Requires:      openssl-libs

Recommends:    amdgpu-vulkan-switcher

%description
Amdgpu Pro Vulkan driver

%prep
mkdir -p files

ar x --output . %{SOURCE0}
tar -xJC files -f data.tar.xz || tar -xC files -f data.tar.gz

%install
mkdir -p %{buildroot}/opt/amdgpu-pro/vulkan/%{_lib}
mkdir -p %{buildroot}/opt/amdgpu-pro/etc/vulkan/implicit_layer.d/
mkdir -p %{buildroot}/opt/amdgpu-pro/etc/vulkan/icd.d/
mkdir -p %{buildroot}/opt/amdgpu-pro/share/licenses/
#
cp -r files/opt/amdgpu-pro/lib/x86_64-linux-gnu/* %{buildroot}/opt/amdgpu-pro/vulkan/%{_lib}/
rm -r files/etc
cp -r files/opt/amdgpu-pro/etc/vulkan/icd.d/* %{buildroot}/opt/amdgpu-pro/etc/vulkan/implicit_layer.d/
cp -r files/opt/amdgpu-pro/etc/vulkan/icd.d/* %{buildroot}/opt/amdgpu-pro/etc/vulkan/icd.d/
rm -v files/usr/share/doc/vulkan-amdgpu-pro/changelog.Debian.gz
mv -v files/usr/share/doc/vulkan-amdgpu-pro/copyright %{buildroot}/opt/amdgpu-pro/share/licenses/LICENSE-%{name}_%{_arch}-%{repo}-%{minor}.txt
#
echo "Fixing ICDs"
sed -i "s#/opt/amdgpu-pro/lib/x86_64-linux-gnu/amdvlk64.so#/opt/amdgpu-pro/vulkan/%{_lib}/amdvlk64.so#" "%{buildroot}/opt/amdgpu-pro/etc/vulkan/implicit_layer.d/amd_icd64.json"
sed -i "s#/opt/amdgpu-pro/lib/x86_64-linux-gnu/amdvlk64.so#/opt/amdgpu-pro/vulkan/%{_lib}/amdvlk64.so#" "%{buildroot}/opt/amdgpu-pro/etc/vulkan/icd.d/amd_icd64.json"
#
echo "adding *Disabled* library path"
mkdir -p %{buildroot}/etc/ld.so.conf.d
touch %{buildroot}/etc/ld.so.conf.d/amdvlk-pro-%{_arch}.conf
echo "#/opt/amdgpu-pro/vulkan/%{_lib}" > %{buildroot}/etc/ld.so.conf.d/amdvlk-pro-%{_arch}.conf

%files
"/etc/ld.so.conf.d/amdvlk-pro-%{_arch}.conf"
"/opt/amdgpu-pro/vulkan/%{_lib}/amdvlk64*"
"/opt/amdgpu-pro/etc/vulkan/implicit_layer.d/amd_icd64.json"
"/opt/amdgpu-pro/etc/vulkan/icd.d/amd_icd64.json"
"/opt/amdgpu-pro/share/licenses/LICENSE-%{name}_%{_arch}-%{repo}-%{minor}.txt"

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
