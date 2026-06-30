import os
BEGINNING_OF_COMMAND = '-- name:'

class QueryRegistry :
    def __init__(self, filepath:str) :
        self.load_from_file(filepath)
    
    def load_from_file(self, path) :
        if not os.path.exists(path) :
            raise FileNotFoundError("Couldn't locate queries path")
        
        current_command = None
        sql_query =  []

        with open(path, 'r', encoding = "utf-8") as f :
            for line in f :
                if line.startswith(BEGINNING_OF_COMMAND) :
                    if current_command :
                        setattr(self, current_command, "".join(sql_query).strip() )
                    command = line.replace(BEGINNING_OF_COMMAND, '').strip( )
                    current_command = command
                elif current_command :
                    sql_query.append(line)

                    
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError
        super().__setattr__(name,value)