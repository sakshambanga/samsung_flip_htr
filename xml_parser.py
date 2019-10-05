import xml.etree.ElementTree as ET
from Parser import InkML
tree = ET.parse("001.inkml")
root = tree.getroot()

class Parser:
    def __init__(self,file):
        tree = ET.parse(file)
        self.root = tree.getroot()
    
    def get_lookup(self):
        arr_final = []
        for item in root.findall('traceView/traceView/traceView'):
            #item --> Textline element
            arr = []
            children = item.findall('annotation')
            #children --> array of all annotations in a Textline
            for a in children:
                if a.attrib['type'] == 'transcription':
                    #filter for only transcriptions
                    for word_element in item.findall('traceView'):
                        for annot in  word_element.findall('annotation'):
                            if annot.attrib['type'] == 'transcription' and annot.text:
                                tmp = annot.text
                                arr_tmp = []
                                for c in word_element.findall('traceView'):
                                    #print(c.attrib)
                                    if 'traceDataRef' in c.attrib:
                                        arr_tmp.append(c.attrib['traceDataRef'][1:])
                                arr.append({tmp:arr_tmp})
                    arr_final.append({a.text:arr})
        return arr_final


def main():
    import argparse
    parser = argparse.ArgumentParser(description='InkML Reader')
    parser.add_argument('file', default="001.inkml", type=str, nargs='?')
    args = parser.parse_args()
    inkml = Parser(args.file)
    inkml = inkml.get_lookup()
    #print(inkml)
    inkml2 = InkML(args.file)
    inkml2 = inkml2.plot()

if __name__ == "__main__":
    main()



