import os
import platform
import shutil
import subprocess
import sys
from distutils.command.build import build

from setuptools import setup

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:
    cmd_class = {}
else:
    class BdistWheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = _bdist_wheel.get_tag(self)
            python = 'py{}'.format(sys.version_info[0])
            return python, 'none', plat
    cmd_class = {'bdist_wheel': BdistWheel}


PACKAGE_PATH = 'rhvoice_wrapper_bin'
RHVOICE = 'RHVoice'
SOURCE_URL = 'https://github.com/Olga-Yakovleva/RHVoice.git'
CHECKOUT_COMMIT = 'dc36179'
LIB = 'lib'
EXT = 'dylib' if platform.system().lower() == 'darwin' else 'so'


def is_64bit():
    return sys.maxsize > 2**32


def is_win():
    return os.name == 'nt'


def library_selector(rhvoice_path):
    starts = os.path.join(rhvoice_path, 'build', platform.system().lower())
    if is_win():
        targets = [os.path.join(starts, 'x86_64' if is_64bit() else 'x86', 'lib', 'RHVoice.dll')]
    else:
        targets = [
            os.path.join(starts, 'core', 'libRHVoice_core.{}'.format(EXT)),
            os.path.join(starts, 'lib', 'libRHVoice.{}'.format(EXT))
        ]
    return targets


def scons_selector():
    cmd = ['scons']
    if is_win():
        cmd.append('enable_xp_compat=no')
        cmd.append('enable_x64={}'.format('yes' if is_64bit() else 'no'))
    return cmd


def check_build(libraries_path):
    for target in libraries_path:
        if not os.path.isfile(target):
            return 'File {} not found'.format(target)


def executor(cmd, cwd):
    err = None
    try:
        run = subprocess.call(cmd, cwd=cwd, shell=is_win())
    except Exception as e:
        err = e
    else:
        if run != 0:
            err = 'code: {}'.format(run)
    if err is not None:
        raise RuntimeError('Error executing {} in {}. {}'.format(cmd, str(cwd), err))


class RHVoiceBuild(build):
    def run(self):
        rhvoice_path = os.path.join(self.build_base, RHVOICE)
        build_lib_lib = os.path.join(self.build_lib, PACKAGE_PATH, LIB)

        self.mkpath(self.build_base)
        self.mkpath(self.build_lib)
        self.mkpath(build_lib_lib)

        libraries_path = library_selector(rhvoice_path)

        clone = [['git', 'clone', SOURCE_URL, rhvoice_path], None]
        checkout = [['git', 'checkout', CHECKOUT_COMMIT], rhvoice_path]
        scons = [scons_selector(), rhvoice_path]

        if not os.path.isdir(rhvoice_path):
            self.execute(executor, clone, 'Clone {}'.format(SOURCE_URL))
            self.execute(executor, checkout, 'Git checkout {}'.format(CHECKOUT_COMMIT))
        else:
            self.warn('Use existing source data from {}'.format(rhvoice_path))
        if check_build(libraries_path) is None:
            self.warn('Source already build? Use existing binary data from {}'.format(rhvoice_path))
        else:
            self.execute(executor, scons, 'Compiling RHVoice...')

        msg = check_build(libraries_path)
        if msg is not None:
            raise RuntimeError(msg)

        if not self.dry_run:  # copy files
            self.debug_print('Starting libraries copying..')
            for target in libraries_path:
                dst = os.path.join(build_lib_lib, os.path.basename(target))
                self.debug_print('copying {} to {}...'.format(target, dst))
                dst = shutil.copy(target, dst)
                self.debug_print('copy {} to {}'.format(target, dst))
        build.run(self)


cmd_class['build'] = RHVoiceBuild

with open('README.md') as fh:
    long_description = fh.read()

with open('version') as fh:
    version = fh.read().splitlines()[0]

setup(
    name='rhvoice-wrapper-bin',
    version=version,
    packages=[PACKAGE_PATH],
    package_data={PACKAGE_PATH: [os.path.join(LIB, '*')]},
    url='https://github.com/Aculeasis/rhvoice-wrapper-bin',
    license='GPLv3+',
    author='Aculeasis',
    author_email='amilpalimov2@ya.ru',
    description='Provides RHVoice libraries for rhvoice-wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.4',
    install_requires=['rhvoice-wrapper-data'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=False,
    cmdclass=cmd_class,
    include_package_data=True,
)
