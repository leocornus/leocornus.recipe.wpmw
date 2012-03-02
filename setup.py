from setuptools import setup, find_packages
import os

version = '1.0.0'
name = 'leocornus.recipe.wpmw'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name=name,
      version=version,
      description="zc.buildout recipe for managing WordPress plugins/themes and MediaWiki extensions",
      long_description= (
        read('README')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('leocornus','recipe','wpmw','README.txt')
        + '\n' +
        'Download\n'
        '***********************\n'
        ),
      classifiers=[
       'Framework :: Buildout',
       'Intended Audience :: Developers',
       'License :: OSI Approved :: Zope Public License',
       'Topic :: Software Development :: Build Tools',
       'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='development buildout recipe',
      author='Sean Chen',
      author_email='sean.chen@leocorn.com',
      url='http://github.com/leocornus/%s' % name,
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['leocornus', 'leocornus.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires = [
        'zc.buildout >= 1.4.0',
        'setuptools',],
      extras_require={
        'test' : ['zope.testing'],
      },
      tests_require = ['zope.testing'],
      test_suite = '%s.tests.test_suite' % name,
      entry_points = { 'zc.buildout' : ['default = leocornus.recipe.wpmw:Plugins',
                                        'plugins = leocornus.recipe.wpmw:Plugins'] },
      )