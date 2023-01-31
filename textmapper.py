def hr(start, stop, base):
    uselist = []
    r = stop - start + 1
    if len(str(base)) == 1:
        base = "0" + str(base)    

    for idx in range(r):
        if len(str(idx+start)) == 1:
            idxstr = "0" + str(idx+start)            
        else: 
            idxstr = str(idx+start)

        usestr = str(idxstr) + str(base)
        uselist.append(usestr)
        #print(usestr)
    return(uselist)

terrain = {}
terrain['sand'] = ["0710","0711","0712","0713","0714","0716","0810","0817","0818","0819","0820","0909","0920",'1008','1009','0809']
terrain['sand'] = terrain['sand']+['1107','1207','1306','1307','1404','1405','1504','1604','1702','1703','1802','1902']
terrain['sand'] = terrain['sand']+['2002','2003','2105','1920','2121','2221','2222','2120','2119','2020','2019','1108','1206'] 
terrain['sand'] = terrain['sand']+['2003','2105','1920','2121','2221','2222','2120','2119','2020','2019','1902','1818','1919'] 
terrain['sand'] = terrain['sand']+['2920','2921','2822','3018','3019','3016','3014','2912','3012','3113','3114','3011','3112'] 
terrain['sand'] = terrain['sand']+['2809','2810','2910','2607','2911','3115','3117','2605','2504','2304','2004','2405','1803'] 
terrain['sand'] = terrain['sand']+hr(21,23,6)+hr(26,27,6)+hr(23,27,23)+hr(23,15,18)+hr(11,13,19)+hr(8,10,20)+hr(14,16,4)+hr(13,16,18)+hr(26,27,8)
terrain['sand'] = terrain['sand']+hr(24,25,3)
terrain['desert'] = ['0716','0813','1113','1412','1505','1406','1806','1807','1912','0918','1019','0911','0911','1017','0815','1210']
terrain['desert'] = terrain['desert']+hr(8,9,12)+hr(9,10,10)+hr(11,12,11)+hr(10,11,15)+hr(17,18,9)+hr(18,19,10)+hr(19,20,11)+hr(17,18,5)
terrain['swamp'] = ['1910','2011']
terrain['mountain'] = ['1011','1812','0919','0917','0916','0915','1513','1609','1605','0816']
terrain['mountain'] = terrain['mountain']+hr(8,12,14)+hr(9,10,13)+hr(12,13,13)+hr(10,13,12)+hr(13,15,11)+hr(13,14,10)+hr(16,17,10)+hr(17,18,11)
terrain['mountain'] = terrain['mountain']+hr(15,16,12)+hr(17,18,11)+hr(16,17,10)+hr(16,17,7)+hr(15,17,6)
terrain['marsh'] = ['1306','1307','2119','1413','1611','1712','1409','1510','1914','2014','2216','2217','2818','2718','2313','2314','2407','2107','2006']
terrain['marsh'] = terrain['marsh']+hr(12,21,15)+hr(13,17,14)+hr(16,19,13)+hr(19,20,16)+hr(15,15,9)+hr(14,21,8)+hr(20,20,5)+hr(20,21,20)
terrain['marsh'] = terrain['marsh']+hr(13,15,7)+hr(19,25,9)+hr(22,26,10)+hr(23,26,11)+hr(20,22,12)+hr(25,26,12)+hr(26,28,13)+hr(27,28,14)+hr(27,28,17)
terrain['marsh'] = terrain['marsh']+hr(13,15,7)+hr(26,28,19)+hr(24,28,16)+hr(23,25,15)+hr(24,25,18)+hr(23,24,8)
terrain['water'] = ['2010','2110','2111','2211'] #inlandsea
terrain['bush'] = ['0811','1110','2915','2617','2618','2219','2220','2404','2505','2506','2709','2710','2811','3015','2916','3017','2918','2821','1918','1309']
terrain['bush'] = terrain['bush'] + ['1016','1117','2915','2617','2618','2219','2220','2404','2505','2506','2709','2710','2811','3015','2916','3015','2918','2821']
terrain['bush'] = terrain['bush'] + ['1109','1209','2915','3013','1907','1903']
terrain['bush'] = terrain['bush']+hr(11,12,0)+hr(12,13,8)+hr(10,12,18)+hr(13,18,17)+hr(23,27,22)+hr(17,18,4)
terrain['trees'] = ['1217','2018']
terrain['trees'] = terrain['trees']+hr(25,28,21)+hr(23,24,19)+hr(23,24,20)
terrain['forest'] = ["1904","1905","1906","2007","2208","2406","2507","2508","2609","2610","2611","2711","2913","2914","1814","2116","2316","2215","2818","2918"]
terrain['forest'] = terrain['forest'] + ["2318","2917","2919","2007"]
terrain['forest'] = terrain['forest'] + hr(11,18,16)+hr(19,21,17)+hr(23,24,17)+hr(25,25,17)+hr(21,22,18)+hr(25,25,19)+hr(26,20,20)+hr(22,23,7)+hr(23,24,21)+hr(25,28,20)
terrain['forest'] = terrain['forest']+hr(23,24,12)+ hr(24,25,13)+ hr(24,26,14)+ hr(26,28,13)+hr(27,28,12)+hr(22,23,7)+hr(20,22,13)+hr(20,22,14)+hr(26,28,15)
terrain['forest-mountain tower'] = ['3417'] #lord howe
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
