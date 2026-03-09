import clingo
import sys

### Main program
if len(sys.argv)<2:
    print("decode.py file1 [file2 ... ]")
    sys.exit()

# Loading files and grounding
ctl = clingo.Control()
ctl.add("base", [], "")
for arg in sys.argv[1:]:
    ctl.load(arg)
ctl.ground([("base", [])])
ctl.configuration.solve.models="2" # This retrieves 2 models at most
nummodels=0

# Solving    
x=0
with ctl.solve(yield_=True) as handle:
  for model in handle:
      if nummodels>0: print("Warning: more than 1 model"); break
      for atom in model.symbols(atoms=True):
          if atom.name=="q" and len(atom.arguments)==1: # retrieving a predicate q(N) with N numerical
            x=atom.arguments[0].number
            print(f"number {x} holds for predicate q")
          elif atom.name=="p" and len(atom.arguments)==2: # retrieving a predicate p(X,N) with N numerical
              text=atom.arguments[0].name
              y=atom.arguments[1].number
              print(f"symbol {text} and number {y} hold for predicate p")
      nummodels=1 
if nummodels==0: print("UNSATISFIABLE")

