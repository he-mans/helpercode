import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import sys
import argparse
import traceback

class ArgumentError(Exception):
    def __init__(self,file_name):
        error = f"missing details: input format = {file_name} -i <input file dir> -o <output file dir> -n <output file name>"
        Exception.__init__(self,error)

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i","--input_dir",type=str)
    parser.add_argument("-o","--output_dir",type=str)
    parser.add_argument("-n","--output_file_name",type=str)
    args = parser.parse_args()

    if args.input_dir is None:
        raise ArgumentError(sys.argv[0])
        return

    if args.output_dir is None:
        raise ArgumentError(sys.argv[0])
        return

    if args.output_file_name is None:
        raise ArgumentError(sys.argv[0])
        return

    image_path,output_path = args.input_dir,args.output_dir
    output = os.path.join(output_path,f"{args.output_file_name}")
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv(output, index=None)
    print('Successfully converted all xml to csv')


if __name__ == '__main__':
    main()
