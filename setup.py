from setuptools import setup, find_packages

setup(
    name='vuelexer',
    packages=find_packages(),
    entry_points="""
    [pygments.lexers]
    vuelexer = vuelexer:VueLexer
    """,
)
