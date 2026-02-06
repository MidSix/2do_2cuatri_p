import argparse
def mg_int(n:int)->bool:
    x=0
    y=1
    z=1
    prints=0
    while prints<n:
        print((x*"∼")+"m"+(y*"∼")+"g"+(z*"∼"))
        prints+=1
        if y==1:
            z+=1
            y=z
            x=0
        else:
            x+=1
            y-=1
    return True

def mg_str(chain:str)->bool: #Apartado opcional, este era chill
    indx_m=chain.index("m")
    indx_g=chain.index("g")
    
    if ((indx_m>indx_g) #Si m aparece después de g, la cadena es incorrecta
    or (chain.count("m")!=1 or chain.count("g")!=1)#Si hay más de una m o g, la cadena es incorrecta
    or (chain.replace("m","").replace("g","").replace("∼","")!="")#Si hay algún caracter que no sea m, g o ∼, la cadena es incorrecta :#
    ):
        return print("No")
    #Apartir de aquí, sabemos que la cadena es del tipo ∼^x m ∼^y g ∼^z, con x,y,z>=0, y que solo hay un m y un g
    if len(chain)==2:#Si la cadena es "mg", es correcta(Esto es para ahorrar cálculos posteriores, aunque no deberia ser necesario)
        return print("Yes")
    
    x=indx_m#Todo lo que hay antes de m son ∼
    y=indx_g-(indx_m+1)#Todo lo que hay entre m y g son ∼
    z=len(chain)-(indx_g+1)#Todo lo que hay después de g son ∼
    
    if ((z==0 or y==0)#Es imposible obtener cadenas de con y=0 o z=0 
    or (x>=z)#Si x es mayor o igual a z, es incorrecta
    ): 
        return print("No")
    
    return print("Yes")#Si se cumplen las condiciones anteriores, la cadena es correcta

    


if __name__ == "__main__":
    mg_str("mg")
if __name__ == "__notmain__":
    #$ python mg.py int or $ python mg.py string
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('n', type=int, help='An integer for the accumulator')
    parser.add_argument('s', type=str, help='A string for the accumulator, example: "mg" or "∼m∼g"')
    args = parser.parse_args()
    if args.n is not None:
        mg_int(args.n)
    elif args.s is not None:
        mg_str(args.s)