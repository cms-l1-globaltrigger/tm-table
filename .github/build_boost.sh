: ${BOOST_VERSION:=1.84.0}
: ${BOOST_BASE:=$(pwd)/dist/boost}

mkdir -p build
cd build
curl -LO https://github.com/boostorg/boost/releases/download/boost-${BOOST_VERSION}/boost-${BOOST_VERSION}.tar.xz
tar xf boost-${BOOST_VERSION}.tar.xz
cd boost-${BOOST_VERSION}
./bootstrap.sh
./b2 -j4 --with-system --with-filesystem link=shared runtime-link=shared threading=multi variant=release install --prefix=${BOOST_BASE}
