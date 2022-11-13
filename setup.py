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
)
