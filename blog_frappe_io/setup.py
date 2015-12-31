from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='blog_frappe_io',
    version=version,
    description='blog.frappe.io',
    author='Frappe',
    author_email='info@frappe.io',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
