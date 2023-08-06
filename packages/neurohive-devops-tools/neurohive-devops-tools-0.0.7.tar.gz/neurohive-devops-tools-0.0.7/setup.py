import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neurohive-devops-tools",
    version="0.0.7",
    author="Dmitriy Shelestovskiy",
    author_email="one@sonhador.ru",
    description="Neurohive devops tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'bb-trigger=neurohive.integration.bitbucket:main',
            'bb-check-prs-branch=neurohive.integraion.bitbucket:check_branch'
        ]
    },
    install_requires=[
        "requests"
    ]
)
