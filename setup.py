from setuptools import setup, find_packages

setup(
    name="citrus",
    version="0.1.0",
    description="<Your package description>",
    author="Ross DeVito",
    author_email="rdevito@ucsd.edu",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "hail",
        "matplotlib",
        "numpy",
        "pandas",
        "pydot",
        "seaborn",
        "shap",
        # Add any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "citrus = cl_tool.run_simulation:citrus"
        ],
    },
)
