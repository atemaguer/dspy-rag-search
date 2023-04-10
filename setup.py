from setuptools import setup, find_packages

setup(
    name="dsp-senior-project",
    version="0.1.1",
    description="Academic",
    author="Atem Aguer",
    author_email="atemjohn@stanford.edu",
    license="MIT License",
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        "dsp-ml"
    ],
)
