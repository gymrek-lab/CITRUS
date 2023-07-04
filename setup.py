from setuptools import setup, find_packages

setup(
    name="CITRUS",
    version="0.1.0",
    description="<Your package description>",
    author="Ross DeVito",
    author_email="rdevito@ucsd.edu",
    packages=find_packages(),
    install_requires=[
        "numpy",
        # Add any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "CITRUS_sim=CITRUS.cl_tools.run_simulation:main",
        ],
    },
)
