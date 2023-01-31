terrain = {}
terrain['sand'] = ["0710","0711","0712","0713","0714","0716"]+ ["0810","0817","0818","0819","0820"]+ ["0909","0920"]
terrain['sand'] = terrain['sand'] 
terrain['sand'] = terrain['sand'] #coast
terrain['desert'] = ['3513']
terrain['mountain'] = ['3513']
terrain['alluvial'] = ['3513']
terrain['lake'] = ['2010','2110','2111','2211'] #inlandsea
terrain['bush'] = ['3513'] #bush1
terrain['bush2'] = ['3513']
terrain['bush3'] = ['3513']
terrain['volcano'] = ['3417'] #lord howe
terrain['fir'] = ['3513'] #norfolk


with open('ausmap.txt','w') as f:
    
    for j in range(36):
        jstr = str(j+1)
        for i in range(24):
            istr = str(i+1)
            if len(str(j+1)) == 1:
                jstr = "0" + str(j+1)
            if len(str(i+1)) == 1:
                istr = "0" + str(i+1)
                
            usestr = jstr  + istr
            defstr = "ocean"
            for key in terrain:
                if usestr in terrain[key]:
                    defstr = key
            printstr = usestr  + " " + defstr
            print(printstr)

            f.write(printstr)
