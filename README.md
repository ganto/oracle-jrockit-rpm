# RPM Spec for Oracle JRockit JDK

## What is it?

* A Spec file to build a Red Hat/Fedora-compatible [Oracle JRockit](http://www.oracle.com/technetwork/middleware/jrockit/overview/index.html) Java 6 RPM package
* It is using the binary installer from Oracle as origin for the RPM
* RPMs can be generated for either x86\_64 or i386 (different installers required)

## What will you get?

* The *java-1.6.0-jrockit.spec* file will repackage the JDK in the Red Hat manner which fully integrates with the 'alternatives' system. The following RPMs will be generated:
 * java-1.6.0-jrockit : Oracle JRockit Java Runtime Environment (JRE)
 * java-1.6.0-jrockit-devel : Oracle JRockit Java Development Kit (JDK)
 * java-1.6.0-jrockit-jdbc : Oracle JRockit ODBC/JDBC Drivers
 * java-1.6.0-jrockit-demo : Java Demo Applications and Sample Code
 * java-1.6.0-jrockit-src : Java Source Code of Oracle JRockit
 * java-1.6.0-jrockit-missioncontrol : Oracle [Mission Control](http://www.oracle.com/technetwork/middleware/jrockit/mission-control/index.html) application and Eclipse Plugin

## Why do you need this?

 * If you don't know why you need this, you probably don't need it.
 * If you already use Oracle JRockit, it will help you to distribute, install, update and uninstall it, while keeping the footprint of the installation as minimal as desired.
 * The generated RPM packages are multilib-capable. So you can easily install the 32bit and 64bit version of Oracle JRockit on the same machine and easily switch between them using the 'update-alternatives' utility.

## How-To build the RPMs?

* [Download](http://www.oracle.com/technetwork/middleware/jrockit/downloads/index.html) the JRockit Linux binary installer from Oracle (x64 or ia32) and place it into the SOURCES folder of your RPM build environment, together with the *jrockit-silent.xml* available from this repository.
* Use your favorite RPM builder (e.g. rpmbuild, mock) to build the packages.
* If you still don't understand how to build the RPMs, check out [this](https://fedoraproject.org/wiki/How_to_create_a_GNU_Hello_RPM_package) guide.
