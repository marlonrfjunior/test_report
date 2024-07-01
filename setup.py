from setuptools import setup, find_packages

setup(
    name='test_report',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',  # inclua suas dependências aqui
        'pandas',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'test-report=test_report.__main__:main',
        ],
    },
    author='Seu Nome',
    author_email='seu.email@example.com',
    description='Uma biblioteca para gerar relatórios de testes automatizados.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seu_usuario/test_report',  # atualize com a URL do seu repositório
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
