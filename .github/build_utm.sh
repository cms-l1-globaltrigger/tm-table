: ${UTM_VERSION:=0.13.0}
: ${UTM_BASE:=$(pwd)/dist/utm}
: ${BOOST_BASE:=$(pwd)/dist/boost}
: ${XERCES_C_BASE:=$(pwd)/dist/xerces-c}

mkdir -p build
cd build
curl -OL https://gitlab.cern.ch/cms-l1t-utm/utm/-/archive/utm_${UTM_VERSION}/utm-utm_${UTM_VERSION}.tar.gz
tar xzf utm-utm_${UTM_VERSION}.tar.gz
cd utm-utm_${UTM_VERSION}
./configure
make all -j4 CPPFLAGS='-DNDEBUG -DSWIG' BOOST_BASE=${BOOST_BASE} XERCES_C_BASE=${XERCES_C_BASE}
make install PREFIX=${UTM_BASE}
