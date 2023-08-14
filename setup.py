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
        "scikit-learn",
        "scipy",
        "seaborn",
        "shap",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "citrus = cl_tool.cli:citrus"
        ],
    },
)
