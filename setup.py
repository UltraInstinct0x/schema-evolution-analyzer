from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="schema-evolution-analyzer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for analyzing database schema evolution patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/schema-evolution-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
    install_requires=[
        "prometheus-client==0.16.0",
        "structlog==23.1.0",
        "elasticsearch==8.8.0",
        "sentry-sdk==1.25.1",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "locust==2.15.1",
        "psycopg2-binary==2.9.3",
        "pyyaml==6.0",
        "pytest==7.1.2",
        "sqlparse==0.4.2",
        "networkx==2.8.2",
        "typing-extensions==4.2.0",
    ],
    extras_require={
        "dev": [
            "flake8",
            "black",
            "mypy",
            "isort",
        ],
    },
    entry_points={
        "console_scripts": [
            "schema-evolution-analyzer=schema_analyzer.cli:main",
        ],
    },
)