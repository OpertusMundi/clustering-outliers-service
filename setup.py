import setuptools

setuptools.setup(
    name='clustering_outliers',
    version='0.0.1',
    description='kmeans Clustering',
    license='MIT',
    packages=setuptools.find_packages(exclude=('tests*',)),
    install_requires=[
        # moved to requirements.txt
    ],
    package_data={'clustering_outliers': [
        'logging.conf', 'schema.sql'
    ]},
    python_requires='>=3.7',
    zip_safe=False,
)
