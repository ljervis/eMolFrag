import traceback
import time

outputDir = '/home/luke/Projects/MolecularFragmentation/chembl_25/chembl_25_neo4j/output_mongo/'
outputFolderPath_log = '/home/luke/Projects/MolecularFragmentation/chembl_25/chembl_25_neo4j/output_mongo/output-log/'

def PrintLog(path, msg):
    # write log
    with open(path, 'at') as outLog:
        outLog.write(time.asctime( time.localtime(time.time()) ))
        outLog.write(msg)
        outLog.write('\n')

def RmBrickRedundancy(tcBorder, pool):
    try:
        from rmRedBrick01 import RmBrickRed
    except:
        print('Error Code: 1100-01')
        return

    # Brick Part
    #Step 3: Form and group lists by atom numbers
    fileNameAndAtomNumList_R=[]
    try:
        with open(outputFolderPath_log+'BrickListAll.txt','r') as inList:
            fileNameAndAtomNumList_R=inList.readlines()
    except Exception as e:
        print(e)
        print('Error Code: 1100.')
        return

    FNAANLList_R=[] #file name and atom number list list
    try:
        for FNAAN in fileNameAndAtomNumList_R: #FNAAN: file name and atom number
            FNAANList=FNAAN.split() #FNAANList: file name and atom number list
            FNAANLList_R.append([FNAANList[0],FNAANList[1:]])
    except:
        print('Error Code: 1101.')
        return

    atomNumPro_R=[]
    try:
        for tempValue in FNAANLList_R: #tempValue: [[filename],['T','','C','','N','','O','']]
            if tempValue[1] not in atomNumPro_R: #tempValue[1]: ['T','','C','','N','','O',''],Group Property
                atomNumPro_R.append(tempValue[1])
    except:
        print('Error Code: 1102.')
        return

    try:
        fileNameGroup_R=[[y[0] for y in FNAANLList_R if y[1]==x] for x in atomNumPro_R]
    except:
        print('Error Code: 1103.')
        return

    try:
        with open(outputFolderPath_log+'BrickGroupList.txt','w') as groupOut:
            for i in range(len(atomNumPro_R)):
                groupOut.write(' '.join(atomNumPro_R[i])+' - ')
                groupOut.write('File Num: ')
                groupOut.write(str(len(fileNameGroup_R[i])))
                groupOut.write('\n')
    except:
        print('Error Code: 1104.')
        return

    try:
        # Log
        path = outputFolderPath_log+'Process.log'
        msg = ' Start Remove Brick Redundancy '
        PrintLog(path, msg)
    except Exception as e:
        print(e)
        print('Error Code: 1105.')
        return

    #Step 4: Generate similarity data and etc.
    try:
        fileNameGroup_Rs=sorted(fileNameGroup_R,key=lambda x:len(x),reverse=True) #process long list first
    except:
        print('Error Code: 1106.')
        return

    try:
        # partial_RmBrick=partial(RmBrickRed, outputDir, tcBorder)
        # pool.map(partial_RmBrick,fileNameGroup_Rs)
        for i in range(len(fileNameGroup_Rs)):
            RmBrickRed(outputDir,tcBorder,fileNameGroup_Rs[i])
    except Exception as e:
        print(e)
        traceback.print_exc()
        print('Error Code: 1107.')
        return

    try:
        # Log
        path = outputFolderPath_log+'Process.log'
        msg = ' End Remove Brick Redundancy '
        PrintLog(path, msg)
    except:
        print('Error Code: 1108.')
        return


def RmLinkerRedundancy(pool):
    try:
        from rmRedLinker04 import RmLinkerRed
    except:
        print('Error Code: 1110-01')
        return

    # Linker Part
    #Step 3: Form and group lists by atom numbers
    fileNameAndAtomNumList_L=[]
    try:
        with open(outputFolderPath_log+'LinkerListAll.txt','r') as inList:
            fileNameAndAtomNumList_L=inList.readlines()
    except:
        print('Error Code: 1110. Read LinkerListAll.txt failed. This may be caused from no linker generated for some reason.')
        return

    FNAANLList_L=[] #file name and atom number list list
    try:
        for FNAAN in fileNameAndAtomNumList_L: #FNAAN: file name and atom number
            FNAANList=FNAAN.split() #FNAANList: file name and atom number list
            FNAANLList_L.append([FNAANList[0],FNAANList[1:]])
    except:
        print('Error Code: 1111.')
        return

    atomNumPro_L=[]
    try:
        for tempValue in FNAANLList_L:
            if tempValue[1] not in atomNumPro_L:
                atomNumPro_L.append(tempValue[1])
    except:
        print('Error Code: 1112.')
        return

    try:
        fileNameGroup_L=[[y[0] for y in FNAANLList_L if y[1]==x] for x in atomNumPro_L]
    except:
        print('Error Code: 1113.')
        return

    try:
        with open(outputFolderPath_log+'LinkerGroupList.txt','w') as groupOut:
            for i in range(len(atomNumPro_L)):
                groupOut.write(' '.join(atomNumPro_L[i])+' - ')
                groupOut.write('File Num: ')
                groupOut.write(str(len(fileNameGroup_L[i])))
                groupOut.write('\n')
    except:
        print('Error Code: 1114.')
        return

    try:
        # Log
        path = outputFolderPath_log+'Process.log'
        msg = ' Start Remove Linker Redundancy '
        PrintLog(path, msg)
    except:
        print('Error Code: 1115.')
        return

    #Step 4: Generate similarity data and etc.
    # try:
        # partial_RmLinker=partial(RmLinkerRed, outputDir)
    # except:
    #     print('Error Code: 1116.')
    #     return

    inputL=[]

    try:
        for i in range(len(fileNameGroup_L)):
            inputL.append([fileNameGroup_L[i],atomNumPro_L[i]])
    except:
        print('Error Code: 1117.')
        return

    try:
        inputLs=sorted(inputL,key=lambda x:len(x[0]),reverse=True)
    except:
        print('1118.')
        return

    try:
        # pool.map(partial_RmLinker,inputLs)
        for i in inputLs:
            RmLinkerRed(outputDir,i)
    except:
        print('1119.')
        return

    try:
        # Log
        path = outputFolderPath_log+'Process.log'
        msg = ' End Remove Linker Redundancy '
        PrintLog(path, msg)
    except:
        print('Error Code: 1120.')
        return
