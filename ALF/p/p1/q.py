import argparse

def qa(n:int) -> list:
    Result=""
    i=0
    j=0
    prints=0
    while prints<n:
        Result+=f"{i}/{j} "
           
    print(Result)        
    return True



def qu(x:int) -> list:#Apartado Opcional
    return True

if __name__ == "__main__":#Just for testing purposes
    qa(15)
if __name__ == "__notmain__":
    #$ python q.py -a int or $ python q.py -u int
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-a', type=int, help='Call function qa with an integer argument')
    parser.add_argument('-u', type=int, help='Call function qu with an integer argument')
    args = parser.parse_args()
    if args.a is not None:
        qa(args.a)
    if args.u is not None:
        qu(args.u)
    