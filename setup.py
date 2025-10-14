from setuptools import setup, find_packages

setup(
    name="plot_distribution",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # зависимости
        "matplotlib",
        "pandas",
        "seaborn"
    ],
)
