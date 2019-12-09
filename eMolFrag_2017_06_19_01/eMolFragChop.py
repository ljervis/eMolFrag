import os
from multiprocessing import Pool
from functools import partial

inputFolderPath = '/home/luke/Projects/MolecularFragmentation/chembl_25/chembl_25_neo4j/mol2_files_2d/'
outputFolderPath = '/home/luke/Projects/MolecularFragmentation/chembl_25/chembl_25_neo4j/output_mongo/'
processNum = 8

def GetInputList():
    #Step 1: Get a list of original *.mol2 files
    try:
        fileNameList=[]
        infilePathList=[]
        try:
            for root, dirs, files in os.walk(inputFolderPath):
                for file in files:
                    fileNameList.append(file)
                    # infilePathList.append(inputFolderPath+file+'\n')
                    infilePathList.append(file + '\n')
        except Exception as e:
            print('Error Code: 1081.')
            print(e)
            return
        try:
            with open(outputFolderPath+'output-log/InputList','at') as outList:
                outList.writelines(infilePathList)
        except:
            print('Error Code: 1082.')
            return

    except:
        print('Error Code: 1080. Failed to get input file list.')
        return

def Chop():
    try:
        from chopRDKit03 import ChopWithRDKit
    except Exception as e:
        print(e)
        print('Error Code: 1090-01.')
        return

    try:
        inputList=[]
        with open(outputFolderPath+'output-log/InputList','r') as inList:
            for lines in inList:
                inputList.append(lines.replace('\n',''))
    except:
        print('Error Code: 1091.')
        return

    try:
        # pool=Pool(processes=processNum)
        # partial_Chop=partial(ChopWithRDKit, outputFolderPath)
        # pool.map(partial_Chop,inputList)
        for i in inputList:
            ChopWithRDKit(outputFolderPath, i)
    except Exception as e:
        print(e)
        print('Error Code: 1092.')
        return

def SetUp():
    for root, dirs, files in os.walk(outputFolderPath + 'output-chop'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    for root, dirs, files in os.walk(outputFolderPath + 'output-chop-comb'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    for root, dirs, files in os.walk(outputFolderPath + 'output-sdf'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    for root, dirs, files in os.walk(outputFolderPath + 'output-brick'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    for root, dirs, files in os.walk(outputFolderPath + 'output-linker'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    open(outputFolderPath + 'output-log/BrickListAll.txt', 'w').close()
    open(outputFolderPath + 'output-log/InputList', 'w').close()
    open(outputFolderPath + 'output-log/LinkerListAll.txt', 'w').close()
    open(outputFolderPath + 'output-log/ListAll', 'w').close()
    open(outputFolderPath + 'output-log/errors.txt', 'w').close()
    open(outputFolderPath + 'output-log/brick-log.txt', 'w').close()
    open(outputFolderPath + 'output-log/bricks-red-out.txt', 'w').close()
    open(outputFolderPath + 'output-log/BrickGroupList.txt', 'w').close()

def RemoveRedundancy():
    from eMolFragRemoveRedundancy import RmLinkerRedundancy, RmBrickRedundancy
    RmBrickRedundancy(1.0, None)
    # RmLinkerRedundancy(None)



def main():
    # SetUp()
    # GetInputList()
    # Chop()
    open(outputFolderPath + 'output-log/brick-log.txt', 'w').close()
    open(outputFolderPath + 'output-log/bricks-red-out.txt', 'w').close()
    open(outputFolderPath + 'output-log/BrickGroupList.txt', 'w').close()
    RemoveRedundancy()

if __name__ == "__main__":
    main()