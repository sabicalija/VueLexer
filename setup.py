from setuptools import setup, find_packages

setup(
    name='vuelexer',
    version='0.0.1',
    description='Custom Vue.js Pygments Lexer',
    license='GPL-v3',
    keywords='pygments lexer vue',
    author='Alija Sabic',
    author_email='sabic.alija@gmail.com',
    packages=find_packages(),
    install_requires=['pygments >= 1.5'],
    entry_points="""
        [pygments.lexers]
        vuelexer = lexer.vuelexer:VueLexer
    """,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPL-v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
