from jinja2 import Environment, PackageLoader

env = Environment( loader = PackageLoader( 'bpc_serverless', 'templates' ) )
## @note Can send globals to env

print '# Using PackageLoader'
print '# Templates Available:'
print env.list_templates('mask')

def render(payload=None):
    if payload is None:
        payload = {'word': 'Template'}

    template = env.get_template( 'view/messytest.mask' )
    return template.render( payload ).encode('utf8')
