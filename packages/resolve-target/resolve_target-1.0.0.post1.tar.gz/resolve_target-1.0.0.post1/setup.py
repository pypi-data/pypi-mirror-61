from setuptools import setup

setup(
    name='resolve_target',
    version='1.0.0-1',
    license='MIT',
    description='Contacts URL(s) and resolves the redirection target(s).',
    long_description=open('README.rst').read(),
    author='Aleksey Vitebskiy',
    author_email='aleksey.vitebskiy@gmail.com',
    packages=['resolve_target'],
    url='https://github.com/avitebskiy/resolve_target',
    download_url='https://github.com/avitebskiy/resolve_target/archive/1.0.0.tar.gz',
    keywords=['http', 'www', 'developer', 'redirect', 'web', 'hostname'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
        'console_scripts': [
            'resolve_target=resolve_target.resolve_target:main'
        ],
    },
)
