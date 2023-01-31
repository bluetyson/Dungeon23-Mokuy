def hr(start, stop, base):
    uselist = []
    for i in range(stop-start):
        usestr = str(i+start) + str(base)
        uselist.append(usestr)
        #print(usestr)
        return(uselist)

terrain = {}
terrain['sand'] = ["0710","0711","0712","0713","0714","0716","0810","0817","0818","0819","0820","0909","0920",'1008','1009']
terrain['sand'] = terrain['sand']+['1107','1207','1306','1307','1404','1405','1504','1604','1702','1703','1802','1902']
terrain['sand'] = terrain['sand']+['2002','2003','1306','1307','1404','1405','1504','1604','1702','1703','1802','1902'] 
terrain['desert'] = ['0716','0813']
terrain['mountain'] = ['1011']
terrain['river'] = ['1306','1307']
terrain['water'] = ['2010','2110','2111','2211'] #inlandsea
terrain['bush'] = ['0811'] #bush1
terrain['trees'] = ['1217']
terrain['forest'] = hr(11,18,16)+hr(19,21,17)+hr(23,24,17)+hr(25,25,17)+hr(21,22,18)+hr(25,25,19)++hr(26,20,20)
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
