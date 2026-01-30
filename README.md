# 2do año - 2do cuatrimestre - prácticas

## Start working

### If you already have a remote repository that has content
If the repo already exists remotely and have content, 
you **don't have to initialize anything locally**.  
Just clone it inside an empty folder:  
`git clone https://github.com/MidSix/2do_2cuatri_p`  
Cloning:
- creates the local repo
- sets the remote automatically
- pulls all history

### about the file tree
This repository follows a very helpful approach to have everything about a subject inside
in just one folder. The `.gitignore` basically tells git to ignore
EVERYTHING inside the folder except for what's inside the p (practice) directory
and "notas" directory of
each subject. So you can have whatever you want inside the subject
folder and as long as is not inside p or "notas "folder git will goona ignored it 
and won't be eligible for versioninig. With this you can have for
example inside folder FAA a folder for the theory pdf's, another folder for
test code, whatever. And those folders won't be tracked, I really
found this usefull, so it's not an error to not
ignore this .gitignore.

So because of this configuration, anything added outside
of p or "notas" folder in each subject will be ignored for versioning.
That includes changing the name of the folder from p -> whatever.
So please don't change the name of p folder and "notas" folder.

Same goes for the names of each subject folder. If the names are
changed then the filter won't work and everything will be ignored
for versioning.

#### examples / summary:
you can have a subject folder like this.  
FAA/   
├── p/  
├── notas/  
├── pdfs_theory/  
├── code_examples/  
├── TGR's/  
├── past_tests/  
└── whatever/  

- and **ONLY**: `p/` and `notas/` are being tracked.  
- As long as you don't change the names of the **subjects**, 
- the names of `p/` and `notas/`  
- And the file structure (putting `notas/` or `p/` inside other folders or something like that)  
    Everything will work alright
