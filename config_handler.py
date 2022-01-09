# config handler


class ConfigHandler():

    def init_config(self,filename):

        params_dict = {}
        with open(filename) as f:
            lines = f.readlines()
        
            for line in lines:
                
                line2 = line.strip()
                temparray = line2.split()    
                if( temparray[0] == 'MOVEBLOCKLENGTH'):
                    self.moveblocklength = int(temparray[1])
                if( temparray[0] == 'MOVEBLOCKTRIES'):
                    self.moveblocktries = int(temparray[1])
                if( temparray[0] == 'POLLUTIONWEIGHT'):
                    self.pollutionweight = float(temparray[1])
                if( temparray[0] == 'EMPTYCOLUMNSWEIGHT'):
                    self.emptycolumnsweight = float(temparray[1])
                if( temparray[0] == 'NUMSUITS'):
                    self.numsuits = int(temparray[1])
                    if( self.numsuits not in [1,2,4]):
                        raise ValueError('Incorrect Number Of Suits!!!')
                if( temparray[0] == 'MAXRUNLENGTH'):
                    self.maxrunlengthweight = float(temparray[1])    
                    
                