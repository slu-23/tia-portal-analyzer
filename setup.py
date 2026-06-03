from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tia-portal-analyzer",
    version="0.1.0",
    author="slu-23",
    description="AI-powered TIA Portal program analyzer and detector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slu-23/tia-portal-analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0",
        "loguru>=0.7",
        "lxml>=4.9",
    ],
)
