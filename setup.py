"""
Distribution Configuration for DCF Valuation Tool

Professional package setup configuration for cross-platform distribution
of the DCF Valuation Tool with comprehensive dependency management.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dcf-valuation-tool",
    version="1.0.0",
    author="DCF Development Team",
    author_email="support@dcftool.com",
    description="Professional-grade Discounted Cash Flow analysis application for financial valuation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mangekyo-Sharingan/DCFTool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    keywords="dcf valuation finance investment analysis cash-flow modeling",
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dcftool=main:main",
        ],
        "gui_scripts": [
            "dcftool-gui=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/Mangekyo-Sharingan/DCFTool/issues",
        "Source": "https://github.com/Mangekyo-Sharingan/DCFTool",
        "Documentation": "https://github.com/Mangekyo-Sharingan/DCFTool/wiki",
    },
)
