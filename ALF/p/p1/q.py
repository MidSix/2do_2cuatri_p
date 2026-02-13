import argparse

def qa(n:int) -> bool:
    Result=""
    i=0
    j=0
    last_j=0
    prints=0
    while prints<n:
        Result+=f"{i}/{j} "
        prints+=1
        if j==0:
            j=last_j+1
            i=0
            last_j+=1
        else:
            i+=1
            j-=1       
    print(Result)        
    return True


def qu(n:int) -> bool:#Apartado Opcional, podria implementarlo sobre qa, pero no se pide explicitamente
    Result=""
    i=0
    j=0
    last_j=0
    prints=0
    while prints<n:
        if i==0 or j==0:
            Result+=f"{i}/{j} "
            prints+=1
        elif j%i==0 and j!=i:
            Result+=f"{i}/{j} "
            prints+=1
            
        if j==0:
            j=last_j+1
            i=0
            last_j+=1
        else:
            i+=1
            j-=1       
    print(Result)    
    return True

#El apartado opcional incluye una medición de tiempos y comparación entre ambos
#a valores altos de n, incluyendo conclusiones sobre resultados obtenidos
#Pero no me parece que haga falta ya que el qa parece bien hecho
if __name__ == "__main__":
    #$ python q.py -qa int or $ python q.py -qu int
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-qa', type=int, help='Call function qa with an integer argument')
    parser.add_argument('-qu', type=int, help='Call function qu with an integer argument')
    args = parser.parse_args()
    if args.qa is not None:
        qa(args.qa)
    elif args.qu is not None:
        qu(args.qu)
    