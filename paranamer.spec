%{?_javapackages_macros:%_javapackages_macros}

# FIXME: javapackages fails to find deps
%bcond_with paranamer-integration-tests

%global githash cb6709646eed97c271d73f50ad750cc43c8e052a
Name:             paranamer
Version:          2.8
Release:          4%{?dist}
Summary:          Library for accessing non-private method parameter names at run-time
Group:            Development/Java
License:          BSD
URL:              https://github.com/paul-hammant/paranamer
Source0:          https://github.com/paul-hammant/paranamer/archive/%{githash}/%{name}-%{githash}.tar.gz

Patch0:           0001-Port-to-current-qdox.patch

BuildRequires:    maven-local
BuildRequires:    mvn(com.thoughtworks.qdox:qdox)
BuildRequires:    mvn(javax.inject:javax.inject)
BuildRequires:    mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:    mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:    mvn(org.codehaus:codehaus-parent:pom:)
BuildRequires:    mvn(org.mockito:mockito-all)
BuildRequires:    mvn(org.ow2.asm:asm)
BuildRequires:    mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:        noarch

%description
It is a library that allows the parameter names of non-private methods
and constructors to be accessed at run-time.

%package ant
Summary:          ParaNamer Ant

%description ant
This package contains the ParaNamer Ant tasks.

%package generator
Summary:          ParaNamer Generator

%description generator
This package contains the ParaNamer Generator.

%if %{with paranamer-integration-tests}
%package integration-tests
Summary:          ParaNamer Integration Test Parent POM

%description integration-tests
ParaNamer Integration Test Parent POM.

%package it-011
Summary:          ParaNamer Integration Test 011

%description it-011
ParaNamer IT 011: can use maven plugin defaults.
%endif

%package maven-plugin
Summary:          ParaNamer Maven plugin

%description maven-plugin
This package contains the ParaNamer Maven plugin.

%package parent
Summary:          ParaNamer Parent POM

%description parent
This package contains the ParaNamer Parent POM.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{githash}

#patch0 -p1

# Cleanup
find -name "*.class" -print -delete
# Do not erase test resources
find -name "*.jar" -print ! -name "test.jar" -delete

chmod -x LICENSE.txt

# javapackages fails to find deps
%if %{without paranamer-integration-tests}
%pom_disable_module it-011 paranamer-integration-tests/
%pom_disable_module paranamer-integration-tests pom.xml
%endif

# Remove wagon extension
%pom_xpath_remove "pom:build/pom:extensions"

%pom_remove_plugin -r :maven-dependency-plugin
%pom_remove_plugin -r :maven-javadoc-plugin
%pom_remove_plugin -r :maven-source-plugin

# Disable distribution module
%pom_disable_module %{name}-distribution

# Unavailable test deps
%pom_remove_dep -r net.sourceforge.f2j:
%pom_xpath_remove -r "pom:dependency[pom:classifier = 'javadoc' ]"
# package org.netlib.blas does not exist
rm -r %{name}/src/test/com/thoughtworks/paranamer/JavadocParanamerTest.java
# testRetrievesParameterNamesFromBootstrapClassLoader java.lang.AssertionError:
#       Should not find names for classes loaded by the bootstrap class loader.
rm -r %{name}/src/test/com/thoughtworks/paranamer/BytecodeReadingParanamerTestCase.java

%build

%mvn_build -s

%install
%mvn_install

%files -f .mfiles-%{name}
%doc README.md
%doc LICENSE.txt

%files ant -f .mfiles-%{name}-ant

%files generator -f .mfiles-%{name}-generator
%doc LICENSE.txt

%if %{with paranamer-integration-tests}
%files integration-tests -f .mfiles-%{name}-integration-tests
%doc LICENSE.txt

%files it-011 -f .mfiles-%{name}-it-011
%doc LICENSE.txt
%endif

%files maven-plugin -f .mfiles-%{name}-maven-plugin

%files parent -f .mfiles-%{name}-parent
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Fri Feb 10 2017 Michael Simacek <msimacek@redhat.com> - 2.8-4
- Port to current qdox

* Tue Jun 21 2016 gil cattaneo <puntogil@libero.it> 2.8-3
- add missing build requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 25 2015 gil cattaneo <puntogil@libero.it> - 2.8-1
- Upstream release 2.8
- Fix FTBFS RHBZ#1239758
- Split maven plugin to sub package RHBZ#1119279
- Use Qdox 2.x RHBZ#1191694
- Run test suite
- Use BR mvn()-like
- Fix URL field
- Introduce license macro
- Minor changes for adapt to current guideline

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 17 2014 Marek Goldmann <mgoldman@redhat.com> - 2.4.1-9
- Switch to xmvn

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.4.1-7
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Marek Goldmann <mgoldman@redhat.com> - 2.4.1-5
- Using pom macros
- Fixed build by adding version to the plugin

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.4.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 12 2012 Marek Goldmann <mgoldman@redhat.com> 2.4.1-1
- Upstream release 2.4.1
- Cleanup in spec file

* Mon Mar 12 2012 Marek Goldmann <mgoldman@redhat.com> 2.2-2
- Updated summary and url

* Tue Feb 21 2012 Marek Goldmann <mgoldman@redhat.com> 2.2-1
- Initial packaging

