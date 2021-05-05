import sys
import io, os, json
import shutil
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))
from pydofus.d2o import D2OReader, InvalidD2OFile
from pydofus.d2i import D2I, InvalidD2IFile
from pydofus.d2p import D2PReader, InvalidD2PFile
from pydofus.swl import SWLReader, InvalidSWLFile
from pydofus.ele import ELE, InvalidELEFile
from pydofus.dlm import DLM, InvalidDLMFile
dofus_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus"
output_base_path = f'{path.parents[1]}{os.sep}jsons'


class Unpacker:

    @staticmethod
    def d2o_unpack(file_path):
        with open(file_path, 'rb') as d2o_file:
            try:
                d2o_reader = D2OReader(d2o_file)
                d2o_data = d2o_reader.get_objects()
                return d2o_data
            except InvalidD2OFile:
                pass

    @staticmethod
    def d2o_dump(file_path, output_path):
        file_name = os.path.basename(file_path)
        d2o_data = Unpacker.d2o_unpack(file_path)
        with open(f'{output_path}{os.sep}{file_name.replace("d2o", "json")}', "w") as json_output:
            json.dump(d2o_data, json_output, indent=4)

    @staticmethod
    def d2i_unpack(file_path):
        with open(file_path, "rb") as d2i_input:
            d2i = D2I(d2i_input)
            d2i_data = d2i.read()
        return d2i_data

    @staticmethod
    def d2i_dump(file_path, output_path):
        d2i_data = Unpacker.d2i_unpack(file_path)
        file_name = os.path.basename(file_path)
        with open(f'{output_path}{os.sep}{file_name.replace("d2i", "json")}', "w", encoding="utf-8") as json_output:
            json.dump(d2i_data, json_output, indent=2, ensure_ascii=False)

    @staticmethod
    def ele_unpack(file_path):
        with open(file_path, "rb") as ele_input:
            ele = ELE(ele_input)
            data = ele.read()
        return data

    @staticmethod
    def ele_dump(file_path, output_path):
        file_name = os.path.basename(file_path)
        data = Unpacker.ele_unpack(file_path)
        with open(f'{output_path}{os.sep}{file_name.replace(".ele", ".json")}', "w") as json_output:
            json.dump(data, json_output, indent=2)

    @staticmethod
    def dlm_unpack(file_path):
        with open(file_path, "rb") as dlm_input:
            dlm = DLM(dlm_input, "649ae451ca33ec53bbcbcc33becf15f4")
            data = dlm.read()
        return data

    @staticmethod
    def dlm_dump(file_path, output_path):
        file_name = os.path.basename(file_path)
        data = Unpacker.dlm_unpack(file_path)
        with open(f'{output_path}{os.sep}{file_name.replace("dlm", "json")}', "w") as json_output:
            json.dump(data, json_output, indent=2)

    @staticmethod
    def d2p_dump(file_path, output_path):
        file_name = os.path.basename(file_path)
        d2p_file = open(file_path, "rb")
        output_path = f'{output_path}{os.sep}{file_name.replace(".d2p","")}'
        try:
            os.stat(output_path)
        except:
            os.mkdir(output_path)
        try:
            d2p_reader = D2PReader(d2p_file, False)
            d2p_reader.load()
            total = len(d2p_reader.files.items())
            count = 0
            print(f'Dumping file {file_name}:')
            for name, specs in d2p_reader.files.items():
                count += 1
                try:
                    try:
                        os.stat(f'{output_path}{os.sep}{os.path.dirname(name)}')
                    except:
                        os.makedirs(f'{output_path}{os.sep}{os.path.dirname(name)}')
                    if "swl" in name:
                        swl = io.BytesIO(specs["binary"])
                        swl_reader = SWLReader(swl)
                        swl_data = {'version': swl_reader.version, 'frame_rate': swl_reader.frame_rate, 'classes': swl_reader.classes}
                        with open(f'{output_path}{os.sep}{name.replace("swl", "json")}', "w") as json_output:
                            json.dump(swl_data, json_output, indent=4)
                        with open(f'{output_path}{os.sep}{name.replace("swl", "swf")}', "wb") as swf_output:
                            swf_output.write(swl_reader.SWF)
                    elif "dlm" in name:
                        dlm_input = io.BytesIO(specs["binary"])
                        dlm = DLM(dlm_input, "649ae451ca33ec53bbcbcc33becf15f4")
                        data = dlm.read()
                        with open(f'{output_path}{os.sep}{name.replace("dlm", "json")}', "w") as json_output:
                            json.dump(data, json_output, indent=2)
                    else:
                        with open(f'{output_path}{os.sep}{name}', "wb") as file_output:
                            file_output.write(specs["binary"])
                    pass
                except:
                    continue
                print(f'[{"#"*(int((count/total)*50))+ " "*(50 - int((count/total)*50))}] {round((count/total)*100,2)}%', end='\r')
        except InvalidD2PFile:
            pass
        print('')

    @staticmethod
    def dofus_open(file_name):
        for root, dirs, files in os.walk(dofus_path):
            for file in files:
                if file == file_name:
                    file_path = os.path.join(root, file)
                    if file_name.endswith("d2o"):
                        return Unpacker.d2o_unpack(file_path)
                    if file_name.endswith("d2i"):
                        return Unpacker.d2i_unpack(file_path)
                    if file_name.endswith("ele"):
                        return Unpacker.ele_unpack(file_path)

    @staticmethod
    def dofus_dump(file_name):
        for root, dirs, files in os.walk(dofus_path):
            for file in files:
                if file == file_name:
                    file_path = os.path.join(root, file)
                    if file_name.endswith("ele"):
                        Unpacker.ele_dump(file_path, output_base_path)
                    if file_name.endswith("d2i"):
                        Unpacker.d2i_dump(file_path, output_base_path)
                    if file_name.endswith("d2o"):
                        Unpacker.d2o_dump(file_path, output_base_path)
                    if file_name.endswith("d2p"):
                        output_path = f'{output_base_path}{os.sep}maps'
                        try:
                            os.stat(output_path)
                        except:
                            os.mkdir(output_path)
                        Unpacker.d2p_dump(file_path, output_path)

    @staticmethod
    def dump_dofus_maps():
        maps_path = f'{dofus_path}{os.sep}content{os.sep}maps'
        for file_name in os.listdir(maps_path):
            if Unpacker.is_map_decompiled(file_name):
                continue
            if file_name.endswith(".d2p"):
                Unpacker.d2p_dump(f'{maps_path}{os.sep}{file_name}', f'{output_base_path}{os.sep}maps')

    @staticmethod
    def is_map_decompiled(file_name):
        for folder_name in os.listdir(f'{output_base_path}{os.sep}maps'):
            if folder_name + '.d2p' == file_name:
                return True
        return False

    @staticmethod
    def clear_output():
        shutil.rmtree(output_base_path)
        os.makedirs(output_base_path)
        os.makedirs(f'{output_base_path}{os.sep}maps')

if __name__ == '__main__':
    print(os.path.dirname(os.path.realpath(__file__)))
    a = Unpacker
    # a.d2p_dump(r"C:\Users\Lucas\AppData\Local\Ankama\zaap\dofus\content\maps\maps0.d2p",r"C:\Users\Lucas\Desktop\Dofus Decompiler\PyDofus-master\output")
    # a.dlm_dump(r"C:\Users\Lucas\Desktop\Dofus Decompiler\PyDofus-master\input\188746758.dlm",r"C:\Users\Lucas\Desktop\Dofus Decompiler\PyDofus-master\input")
    b = a.dofus_open('MapPositions.d2o')
    for i in b:
        print(i.get("id"))