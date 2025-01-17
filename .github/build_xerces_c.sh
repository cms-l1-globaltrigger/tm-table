: ${XERCES_C_VERSION:=3.2.5}
: ${XERCES_C_BASE:=$(pwd)/dist/xerces-c}

mkdir -p build
cd build
curl -L https://github.com/apache/xerces-c/archive/v${XERCES_C_VERSION}.tar.gz --output xerces-c-${XERCES_C_VERSION}.tar.gz
tar xzf xerces-c-${XERCES_C_VERSION}.tar.gz
cd xerces-c-${XERCES_C_VERSION}
./configure --prefix=${XERCES_C_BASE}
make -j4
make install
