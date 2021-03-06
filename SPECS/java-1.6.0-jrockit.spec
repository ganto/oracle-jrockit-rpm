# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
################################################################################
#
# RPM spec file for creating an Oracle JRockit package from the binary
# installer. It will completely rearrange the SDK to correspond to the
# Red Hat/Fedora JVM setup.
#

%define origin          jrockit
%define javaver         1.6.0
%define buildver        37
%define jrockitver      28.2.5
%define mcver           4.1.0

%define priority        %(%{__sed} 's+\\.++g' <<< "%{javaver}%{buildver}")

%define sdklnk          java-%{javaver}-%{origin}.%{_arch}
%define jrelnk          jre-%{javaver}-%{origin}.%{_arch}
%define sdkdir          %{name}-%{version}.%{_arch}
%define jredir          %{sdkdir}/jre
%define sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%define jrebindir       %{_jvmdir}/%{jrelnk}/bin
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}.%{_arch}

%define archdir          %{name}.%{_arch}

%ifarch %ix86
%define target_cpu      ia32
%else
%define target_cpu      x64
%endif

# Don't fail if there are unpackaged files
%define _unpackaged_files_terminate_build no

# This prevents aggressive stripping.
%define debug_package %{nil}

# Fix dependency generator:
# - Red Hat/Fedora only provides libodbc(inst).so.2 but no libodbc(inst).so
%define _use_internal_dependency_generator 0
%global requires_replace \
  /bin/sh -c "%{__find_requires} | %{__sed} -e 's/libodbc.so/libodbc.so.2/;s/libodbcinst.so/libodbcinst.so.2/'"
%global __find_requires %{requires_replace}


Name:           java-%{javaver}-%{origin}
Version:        %{javaver}.%{buildver}_R%{jrockitver}_%{mcver}
Release:        1%{?dist}
Epoch:          1
Summary:        Oracle JRockit Java Runtime Environment
License:        BCL, ASL 1.1, ASL 2.0, Microsoft EULA, Public Domain, W3C, XFree86copyright
Group:          Development/Languages
URL:            http://www.oracle.com/technetwork/middleware/jrockit
Source0:        %{origin}-jdk%{javaver}_%{buildver}-R%{jrockitver}-%{mcver}-linux-%{target_cpu}.bin
Source1:        jrockit-silent.xml
Provides:       jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{javaver}, java-%{javaver}, jre = %{epoch}:%{version}-%{release}
Provides:       java-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java = %{epoch}:%{javaver}
Requires(post):   /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
Requires:       jpackage-utils >= 0:1.5.38
Conflicts:      kaffe
ExclusiveArch:  i686 x86_64
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  findutils, jpackage-utils >= 0:1.5.38, sed
Provides:       jndi = %{epoch}:%{version}, jndi-ldap = %{epoch}:%{version}
Provides:       jndi-cos = %{epoch}:%{version}, jndi-rmi = %{epoch}:%{version}
Provides:       jndi-dns = %{epoch}:%{version}
Provides:       jaas = %{epoch}:%{version}
Provides:       jsse = %{epoch}:%{version}
Provides:       jce = %{epoch}:%{version}
Provides:       jdbc-stdext = %{epoch}:3.0, jdbc-stdext = %{epoch}:%{version}
Provides:       java-fonts = %{epoch}:%{version}, java-%{javaver}-fonts
Provides:       java-sasl = %{epoch}:%{version}

%description
JRockit JVM is the industry's highest performing Java Virtual Machine now built
into Oracle Fusion Middleware. It brings industry leading real time infrastructure
capabilities with JRockit Real Time and unparallelled JVM diagnostics with JRockit
Mission Control.

%package        devel
Summary:        Oracle JRockit Java Software Development Kit
Group:          Development/Tools
Requires(post):   /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
Provides:       java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{javaver}, java-sdk = %{epoch}:%{javaver}
Provides:       java-devel-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-%{javaver}-devel, java-devel = %{epoch}:%{javaver}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    devel
The Oracle JRockit Software Development Kit (SDK) contains the software and
tools that developers need to compile, debug, and run applets and applications
written using the Java programming language.

%package        src
Summary:        Source files for Oracle JRockit
Group:          Development/Languages
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    src
This package contains the source code for the Oracle JRockit class libraries.

%package        demo
Summary:        Java demo applications and sample code
Group:          Development/Languages
BuildArch:      noarch
Requires:       %{name}-devel = %{epoch}:%{version}-%{release}

%description    demo
This package contains the Oracle JRockit demo applications and sample code.

%package        jdbc
Summary:        JDBC/ODBC driver for Oracle JRockit
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    jdbc
This package contains the JDBC/ODBC driver for Oracle JRockit.

%package        missioncontrol
Summary:        Oracle JRockit Mission Control tools and Eclipse plugin
Group:          Development/Debuggers
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    missioncontrol
The JRockit Mission Control tools suite includes utilities to monitor,
manage, profile, and eliminate memory leaks in your Java application
without introducing the performance overhead normally associated with
tools of this type.


%prep
%setup -T -c
%{__chmod} +x %{SOURCE0}

# Set install location to the default build directory
%{__sed} -i -e "s+@@USER_INSTALL_DIR@@+$RPM_BUILD_DIR/%{name}-%{version}+" %{SOURCE1}

# Run the installer
%{SOURCE0} -mode=silent -silent_xml=%{SOURCE1} 2>/dev/null

%build
# Nope.


%install
%{__rm} -rf $RPM_BUILD_ROOT

# fix javac path
%{__sed} -i -e "s|^nbjdk.home=.*$|nbjdk.home=%{_jvmdir}/%{sdkdir}|g" sample/jmx/jmx-scandir/build.properties
%{__sed} -i -e "s|^nbjdk.home=.*$|nbjdk.home=%{_jvmdir}/%{sdkdir}|g" sample/webservices/EbayClient/build.properties
%{__sed} -i -e "s|^nbjdk.home=.*$|nbjdk.home=%{_jvmdir}/%{sdkdir}|g" sample/webservices/EbayServer/build.properties

# multilib-capable docs
%{__install} -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}.%{_arch}
%{__mv} THIRDPARTYLICENSEREADME.txt \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}.%{_arch}
%{__install} -d -m 755 \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-missioncontrol-%{version}.%{_arch}
%{__mv} missioncontrol/THIRDPARTYLICENSEREADME.txt \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-missioncontrol-%{version}.%{_arch}

# main files
%{__install} -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
%{__cp} -a bin include lib missioncontrol src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
%{__install} -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

# extensions handling
%{__install} -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
pushd $RPM_BUILD_ROOT%{jvmjardir}
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/jsse.jar jsse-%{version}.jar
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/jce.jar jce-%{version}.jar
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/rt.jar jndi-%{version}.jar
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/rt.jar jndi-ldap-%{version}.jar
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/rt.jar jndi-cos-%{version}.jar
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/rt.jar jndi-rmi-%{version}.jar
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/rt.jar jaas-%{version}.jar
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/rt.jar jdbc-stdext-%{version}.jar
  %{__ln_s} jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
  %{__ln_s} %{_jvmdir}/%{jredir}/lib/rt.jar sasl-%{version}.jar
  for jar in *-%{version}.jar ; do
    if [ x%{version} != x%{javaver} ]; then
      ln -fs ${jar} $(echo $jar | %{__sed} "s|-%{version}.jar|-%{javaver}.jar|g")
    fi
    ln -fs ${jar} $(echo $jar | %{__sed} "s|-%{version}.jar|.jar|g")
  done
popd

# rest of the jre
%{__cp} -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

# jce policy file handling
%{__install} -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{name}.%{_arch}/jce/vanilla
for file in local_policy.jar US_export_policy.jar; do
  %{__mv} $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/$file \
    $RPM_BUILD_ROOT%{_jvmprivdir}/%{archdir}/jce/vanilla
  # for ghosts
  touch $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/$file
done

# versionless symlinks
pushd $RPM_BUILD_ROOT%{_jvmdir}
  %{__ln_s} %{jredir} %{jrelnk}
  %{__ln_s} %{sdkdir} %{sdklnk}
popd

pushd $RPM_BUILD_ROOT%{_jvmjardir}
  %{__ln_s} %{sdkdir} %{jrelnk}
  %{__ln_s} %{sdkdir} %{sdklnk}
popd

# demo/sample
%{__install} -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__cp} -a demo sample $RPM_BUILD_ROOT%{_datadir}/%{name}

# generate file lists
%{_bindir}/find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | %{__sed} 's|'$RPM_BUILD_ROOT'|%dir |' >  %{name}-%{version}-all.files
%{_bindir}/find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | %{__sed} 's|'$RPM_BUILD_ROOT'||'      >> %{name}-%{version}-all.files

%{__grep} Jdbc    %{name}-%{version}-all.files | sort \
  > %{name}-%{version}-jdbc.files
%{__cat} %{name}-%{version}-all.files \
  | %{__grep} -v missioncontrol \
  | %{__grep} -v Jdbc \
  | %{__grep} -v jre/lib/security \
  > %{name}-%{version}.files


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%post
update-alternatives \
  --install %{_bindir}/java       java         %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre          jre          %{_jvmdir}/%{jrelnk} \
  --slave %{_jvmjardir}/jre       jre_exports  %{_jvmjardir}/%{jrelnk} \
  --slave %{_bindir}/keytool      keytool      %{jrebindir}/keytool \
  --slave %{_bindir}/policytool   policytool   %{jrebindir}/policytool \
  --slave %{_bindir}/rmid         rmid         %{jrebindir}/rmid \
  --slave %{_bindir}/rmiregistry  rmiregistry  %{jrebindir}/rmiregistry \
  --slave %{_bindir}/servertool   servertool   %{jrebindir}/servertool \
  --slave %{_bindir}/tnameserv    tnameserv    %{jrebindir}/tnameserv

update-alternatives \
  --install %{_jvmdir}/jre-%{origin} jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{origin} jre_%{origin}_exports %{_jvmjardir}/%{jrelnk}

update-alternatives \
  --install %{_jvmdir}/jre-%{javaver} jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{javaver} jre_%{javaver}_exports %{_jvmjardir}/%{jrelnk}

if [ -d %{_jvmdir}/%{jrelnk}/lib/security ]; then
  # Need to remove the old jars in order to support upgrading, ugly :(
  # update-alternatives fails silently if the link targets exist as files.
  %{__rm} -f %{_jvmdir}/%{jrelnk}/lib/security/{local,US_export}_policy.jar
fi

update-alternatives \
  --install \
    %{_jvmdir}/%{jrelnk}/lib/security/local_policy.jar \
    jce_%{javaver}_%{origin}_local_policy \
    %{_jvmprivdir}/%{archdir}/jce/vanilla/local_policy.jar \
    %{priority} \
  --slave \
    %{_jvmdir}/%{jrelnk}/lib/security/US_export_policy.jar \
    jce_%{javaver}_%{origin}_us_export_policy \
    %{_jvmprivdir}/%{archdir}/jce/vanilla/US_export_policy.jar

%post devel
update-alternatives \
  --install %{_bindir}/javac      javac        %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java         java_sdk     %{_jvmdir}/%{sdklnk} \
  --slave %{_jvmjardir}/java      java_sdk_exports %{_jvmjardir}/%{sdklnk} \
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir}/appletviewer \
  --slave %{_bindir}/apt          apt          %{sdkbindir}/apt \
  --slave %{_bindir}/extcheck     extcheck     %{sdkbindir}/extcheck \
  --slave %{_bindir}/idlj         idlj         %{sdkbindir}/idlj \
  --slave %{_bindir}/jar          jar          %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner    jarsigner    %{sdkbindir}/jarsigner \
  --slave %{_bindir}/javadoc      javadoc      %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah        javah        %{sdkbindir}/javah \
  --slave %{_bindir}/javap        javap        %{sdkbindir}/javap \
  --slave %{_bindir}/jconsole     jconsole     %{sdkbindir}/jconsole \
  --slave %{_bindir}/jdb          jdb          %{sdkbindir}/jdb \
  --slave %{_bindir}/jhat         jhat         %{sdkbindir}/jhat \
  --slave %{_bindir}/jps          jps          %{sdkbindir}/jps \
  --slave %{_bindir}/jrunscript   jrunscript   %{sdkbindir}/jrunscript \
  --slave %{_bindir}/jstat        jstat        %{sdkbindir}/jstat \
  --slave %{_bindir}/jstatd       jstatd       %{sdkbindir}/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir}/native2ascii \
  --slave %{_bindir}/rmic         rmic         %{sdkbindir}/rmic \
  --slave %{_bindir}/schemagen    schemagen    %{sdkbindir}/schemagen \
  --slave %{_bindir}/serialver    serialver    %{sdkbindir}/serialver \
  --slave %{_bindir}/pack200      pack200      %{sdkbindir}/pack200 \
  --slave %{_bindir}/unpack200    unpack200    %{sdkbindir}/unpack200 \
  --slave %{_bindir}/wsgen        wsgen        %{sdkbindir}/wsgen \
  --slave %{_bindir}/wsimport     wsimport     %{sdkbindir}/wsimport \
  --slave %{_bindir}/xjc          xjc          %{sdkbindir}/xjc

update-alternatives \
  --install %{_jvmdir}/java-%{origin} java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{origin} java_sdk_%{origin}_exports %{_jvmjardir}/%{sdklnk}

update-alternatives \
  --install %{_jvmdir}/java-%{javaver} java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{javaver} java_sdk_%{javaver}_exports %{_jvmjardir}/%{sdklnk}

%postun
if [ $1 -eq 0 ]; then
  update-alternatives --remove java %{jrebindir}/java
  update-alternatives --remove \
    jce_%{javaver}_%{origin}_local_policy \
    %{_jvmprivdir}/%{archdir}/jce/vanilla/local_policy.jar
  update-alternatives --remove jre_%{origin}  %{_jvmdir}/%{jrelnk}
  update-alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi


%postun devel
if [ $1 -eq 0 ]; then
  update-alternatives --remove javac %{sdkbindir}/javac
  update-alternatives --remove java_sdk_%{origin}  %{_jvmdir}/%{sdklnk}
  update-alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi


%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}.%{_arch}/THIRDPARTYLICENSEREADME.txt
%dir %{_jvmdir}/%{sdkdir}
%{jvmjardir}
%dir %{_jvmdir}/%{jredir}/lib/security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/blacklist
%ghost %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%ghost %{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*

%files devel
%defattr(-,root,root,-)
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%{_jvmdir}/%{sdkdir}/bin/*
%exclude %{_jvmdir}/%{sdkdir}/bin/jrmc
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}

%files src
%defattr(-,root,root,-)
%{_jvmdir}/%{sdkdir}/src.zip

%files demo
%defattr(-,root,root,-)
%doc demo/DEMOS_LICENSE
%doc sample/SAMPLES_LICENSE
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/demo
%{_datadir}/%{name}/sample
%exclude %{_datadir}/%{name}/demo/DEMOS_LICENSE
%exclude %{_datadir}/%{name}/sample/SAMPLES_LICENSE

%files jdbc -f %{name}-%{version}-jdbc.files
%defattr(-,root,root,-)

%files missioncontrol
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-missioncontrol-%{version}.%{_arch}/THIRDPARTYLICENSEREADME.txt
%{_jvmdir}/%{sdkdir}/bin/jrmc
%{_jvmdir}/%{sdkdir}/missioncontrol


%changelog
* Tue Apr 30 2013 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1.6.0.37_R28.2.5_4.1.0-1
- Initial packaging, heavily based on the java-1.6.0-sun.spec file
