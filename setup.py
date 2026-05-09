#!/usr/bin/env python3
"""
Setup script for Blog Publisher
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blog-publisher",
    version="1.0.0",
    author="OpenSeneca",
    author_email="openseneca@example.com",
    description="Formats blog post outlines for publication on Substack, Obsidian, and other platforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenSeneca/blog-publisher",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses Python stdlib only
    ],
    entry_points={
        "console_scripts": [
            "blog-publisher=blog_publisher:main",
        ],
    },
)
