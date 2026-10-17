import pandas as pd

def read_wells(path):
    data_frame = pd.read_csv(path)
    return data_frame

def read_layers(path):
    data_frame = pd.read_excel(path)
    return data_frame
    
def read_pumping_test(path):
    data_frame = pd.read_csv(path, sep="\t")
    return data_frame

def print_info(table):
    print(table.shape)
    print(table.columns)
    print(table.dtypes)
    print(table.head(), "\t")
    
def save_csv(path, table, output_file):
    path.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_file, index=False)
    
def save_txt(path, table, output_file):
    path.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(table.to_string())
    
def save_xlsx(path, table, output_file):
    path.mkdir(parents=True, exist_ok=True)
    table.to_excel(output_file, index=True)
    
def print_matrix_info(matrix):
    print(matrix.ndim)
    print(matrix.shape)
    print(matrix.size)
    print(matrix.dtype)
    
class DatasetInfo:
    def __init__(self, name, table):
        self.name = name
        self.rows, self.columns = table.shape

    def describe(self):
        return f"{self.name}: {self.rows} строк, {self.columns} столбцов"