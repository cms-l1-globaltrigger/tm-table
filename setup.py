import glob
import re
import shutil
import subprocess
import os

from setuptools import setup, Extension
import setuptools.command.build_py

UTM_VERSION = '0.13.0'
PACKAGE_NAME = 'tmTable'
PACKAGE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), PACKAGE_NAME))

UTM_ROOT = os.environ.get('UTM_ROOT')
if not UTM_ROOT:
    raise RuntimeError("UTM_ROOT not defined")

UTM_XSD_DIR = os.environ.get('UTM_XSD_DIR')
if not UTM_XSD_DIR:
    raise RuntimeError("UTM_XSD_DIR not defined")

XERCES_LIB_DIR = os.environ.get('XERCES_LIB_DIR', os.path.dirname(__file__))


def load_version(f):
    """Load version from `version.h` file."""
    content = f.read()
    versions = []
    for name in ('MAJOR', 'MINOR', 'PATCH'):
        version = re.findall(r'#define\s+{}_VERSION_{}\s+(\d+)'.format(PACKAGE_NAME, name), content)[0]
        versions.append(version)
    return '.'.join(versions)


def copy_files(sources, dest):
    """Copy files to destination directory."""
    for src in sources:
        shutil.copy(src, os.path.join(dest, os.path.basename(src)))


with open(os.path.join(UTM_ROOT, PACKAGE_NAME, 'include', 'utm', PACKAGE_NAME, 'version.h')) as f:
    assert UTM_VERSION == load_version(f)


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def create_modules(self):
        cwd = os.getcwd()
        # inside package
        os.chdir(PACKAGE_DIR)
        # (re)create XSD directories
        xsd_dir = 'xsd'
        xsd_type_dir = os.path.join(xsd_dir, 'xsd-type')
        if os.path.exists(xsd_dir):
            shutil.rmtree(xsd_dir)
        os.makedirs(xsd_dir)
        os.makedirs(xsd_type_dir)
        # copy XSD files
        copy_files(glob.glob(os.path.join(UTM_XSD_DIR, '*.xsd')), xsd_dir)
        copy_files(glob.glob(os.path.join(UTM_XSD_DIR, 'xsd-type', '*.xsd')), xsd_type_dir)
        # run SWIG to (re)create bindings module
        subprocess.check_call(['swig', '-c++', '-python', '-outcurrentdir', '-I{}'.format(os.path.join(UTM_ROOT, PACKAGE_NAME, 'include', 'utm')), '{}.i'.format(PACKAGE_NAME)])
        # (re)create version module
        with open('version.py', 'w') as f:
            f.write("__version__ = '{}'".format(UTM_VERSION))
            f.write(os.linesep)
        os.chdir(cwd)

    def run(self):
        self.create_modules()
        # run actual build command
        setuptools.command.build_py.build_py.run(self)


tmTable_ext = Extension(
    name='_tmTable',
    define_macros=[('SWIG', '1'),],
    sources=[
        os.path.join(PACKAGE_DIR, 'tmTable_wrap.cxx'),
    ],
    include_dirs=[
        os.path.join(UTM_ROOT, 'tmUtil', 'include', 'utm'),
        os.path.join(UTM_ROOT, 'tmXsd', 'include', 'utm'),
        os.path.join(UTM_ROOT, PACKAGE_NAME, 'include', 'utm'),

    ],
    library_dirs=[
        PACKAGE_DIR,
        os.path.join(UTM_ROOT, XERCES_LIB_DIR),
        os.path.join(UTM_ROOT, 'tmUtil'),
        os.path.join(UTM_ROOT, 'tmXsd'),
        os.path.join(UTM_ROOT, PACKAGE_NAME),
    ],
    libraries=['xerces-c', 'tmutil', 'tmxsd', 'tmtable'],
    extra_compile_args=['-std=c++11'],
)

setup(
    version=UTM_VERSION,
    ext_modules=[tmTable_ext],
    cmdclass={
        'build_py': BuildPyCommand,
    },
    packages=[PACKAGE_NAME],
    package_data={
        PACKAGE_NAME: [
            os.path.join('xsd', '*.xsd'),
            os.path.join('xsd', 'xsd-type', '*.xsd'),
            '*.i',
        ]
    },
)
