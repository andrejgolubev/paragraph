from jinja2 import Template

name='Andr' 

tm = Template('Привет {{name}}')
msg = tm.render(name=name)

print(msg)