import os
import shutil
import subprocess
import sys
from distutils.command.build import build

from setuptools import setup

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = _bdist_wheel.get_tag(self)
            python, abi = 'py{}'.format(sys.version_info[0]), 'none'
            return python, abi, plat
except ImportError:
    bdist_wheel = None


PACKAGE_PATH = 'rhvoice_wrapper_bin'
RHVOICE = 'RHVoice'
SOURCE_URL = 'https://github.com/Olga-Yakovleva/RHVoice.git'
LIB = 'lib'


def _check_build(libraries_path):
    for target in libraries_path:
        if not os.path.isfile(target):
            return 'File {} not found'.format(target)


class RHVoiceBuild(build):
    def run(self):
        def exec_(params, path_cwd):
            run = subprocess.run(params, cwd=path_cwd)
            if run.returncode != 0:
                raise RuntimeError('Error executing {} in {}'.format(params, str(path_cwd)))

        rhvoice_path = os.path.join(self.build_base, RHVOICE)
        build_lib = os.path.join(self.build_lib, PACKAGE_PATH)
        build_lib_lib = os.path.join(build_lib, LIB)

        self.mkpath(self.build_base)
        self.mkpath(self.build_lib)
        self.mkpath(build_lib_lib)

        libraries_path = [
            os.path.join(rhvoice_path, 'build/linux/core/libRHVoice_core.so'),
            os.path.join(rhvoice_path, 'build/linux/lib/libRHVoice.so')
        ]

        clone = [['git', 'clone', SOURCE_URL, rhvoice_path], None]
        commit = 'dc36179'
        checkout = [['git', 'checkout', commit], rhvoice_path]
        scons = [['scons'], rhvoice_path]

        if not os.path.isdir(rhvoice_path):
            self.execute(exec_, clone, 'Clone {}'.format(SOURCE_URL))
            self.execute(exec_, checkout, 'Git checkout {}'.format(commit))
        else:
            self.warn('Use existing source data from {}'.format(rhvoice_path))
        if _check_build(libraries_path) is None:
            self.warn('Source already build? Use existing binary data from {}'.format(rhvoice_path))
        else:
            self.execute(exec_, scons, 'Compiling RHVoice...')

        msg = _check_build(libraries_path)
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


with open('README.md') as fh:
    long_description = fh.read()

with open('version') as fh:
    version = fh.read().splitlines()[0]

cmd_class = {'build': RHVoiceBuild}
if bdist_wheel:
    cmd_class['bdist_wheel'] = bdist_wheel

setup(
    name='rhvoice-wrapper-bin',
    version=version,
    packages=[PACKAGE_PATH],
    package_data={PACKAGE_PATH: ['{}/*'.format(LIB)]},
    url='https://github.com/Aculeasis/rhvoice-wrapper-bin',
    platforms='linux',
    license='GPLv3+',
    author='Aculeasis',
    author_email='amilpalimov2@ya.ru',
    description='Provides RHVoice libraries and data for rhvoice-wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    install_requires=['rhvoice-wrapper-data'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=False,
    cmdclass=cmd_class,
    include_package_data=True,
)
