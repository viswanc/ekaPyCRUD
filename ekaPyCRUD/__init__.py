r"""
A crud app builder for python.
"""

# Meta
__plugin_name__ = 'python.crud.app'
__keywords__ = 'Python CRUD app'
__author__ = 'Viswanath Chidambaram'
__email__ = 'viswanc@thoughtworks.com'
__version__ = '0.0.1'

# Imports
from eka.classes.node import node
from eka.classes.ymlParser import parseYML
from eka.plugins import define, getPluginClass

# Data
Definitions = parseYML(r"""
python.crud.app:
  properties:
    builder:
      allOf:
        - $ref: '#/definitions/config'
        - type: object
          properties:
            builder:
              allOf:
                - $ref: '#/definitions/config'
                - properties:
                    store:
                      required: true
""")

# Helpers
def getSchemaExtension(className):
  Schema = {'definitions': Definitions}
  Schema.update(Definitions[className])

  return Schema

@define(__plugin_name__)
class PythonCrud(node):
  def __init__(self, Structure, Scopes):
    node.__init__(self, Structure, Scopes, getSchemaExtension(__plugin_name__))

  def build(self):
    from os.path import dirname
    from eka.classes.builders.jinja import jinjaBuilder

    Structure = self.Structure

    buildTgt = Structure['buildBase']
    buildSrc = '%s/res' % dirname(__file__)

    getPluginClass(Structure['builder']['store']['class'])(self.Structure, self.Scopes).build()

    return jinjaBuilder().build(buildSrc, buildTgt, Structure)
