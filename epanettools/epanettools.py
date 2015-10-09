from epanettools import epanet2 as et
import tempfile, shutil, os


class EPANetSimulation():
    
    
    def __init__(self,inputFileName):
        if(et.ENopen(inputFileName,"tmp.rpt","tmp.dat")):
            raise FileNotFoundError("File %s not found" % inputFileName)
        self.OriginalInputFileName=inputFileName
        self.inputfile=self.create_temporary_copy(inputFileName)
        
    def create_temporary_copy(path):
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, 'temp_file_name')
        shutil.copy2(path, temp_path)
        return temp_path
        
