defaultpath = __file__.replace("CLI\\resources.py", "")
def grabpath(id):
  return defaultpath+f"RESOURCES\\{id}.py"

class Resources:
  def getresource(id) -> str:
    return open(grabpath(id), 'r').read()
