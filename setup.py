from setuptools import setup, find_packages

setup(
    name="pheno_sim",
    version="0.1.0",
    description="<Your package description>",
    author="Ross DeVito",
    author_email="rdevito@ucsd.edu",
    packages=find_packages(),
    install_requires=[
        "numpy",
        # Add any other dependencies here
    ],
    # python_requires=">=3.6",
)
