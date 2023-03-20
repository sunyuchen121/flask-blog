a = __name__
print(a)
from flask import Flask

b = Flask(a)
print(b.root_path)
