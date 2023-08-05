from setuptools import setup
 
setup(
    name='open_excel',                      # The name of the PyPI-package (includes all Ansible Modules on the matter)
    version='0.101a',                         # Update the version number for new releases
    description='Ansible Modules to Search/Read an Excel file and register its content into an ansible list of dict',
    long_description='Two Ansible Modules, one to read excel files and the other to search for contents within the excel file. Check README documentation for more details',
    keywords='excel,search,spreadsheet',
    url='https://github.com/mohameosam/open_excel',
    author='Mohamed Abouahmed, Kovarus Inc., San Ramon, CA <mabouahmed@kovarus.com>',
    author_email='mohamedosam@gmail.com',
    license='GPL v3',
    packages=['open_excel'],
    python_requires='>=2.7',
    install_requires='openpyxl',
    scripts=['open_excel', 'search_excel']  # The Ansible Modules included in the package
)