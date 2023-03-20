b = __name__
print(b)

import sys
print(sys.modules.get("views.admin"))
print(sys.modules.get("admin"))
