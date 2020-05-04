'''
Created on 22 janv. 2020

@author: S047432
'''
from xml.dom import minidom
import argparse
import os
import logging
import collections

classes = []
ObjectBox = collections.namedtuple('ObjectBox', ['class_id', 'x_center', 'y_center', 'width', 'height'])

def convert(xml_file_path, output_dir):
    """
    convert XML file to yolo format file
    """
    boxes = []
    
    with open(xml_file_path, 'r') as xml_file:
        document = minidom.parse(xml_file)
        
        size = document.getElementsByTagName('size')[0]
        image_width = int(size.getElementsByTagName('width')[0].firstChild.nodeValue)
        image_height = int(size.getElementsByTagName('height')[0].firstChild.nodeValue)
        
        for detect_object in document.getElementsByTagName('object'):
            class_name = detect_object.getElementsByTagName('name')[0].firstChild.nodeValue
            if class_name not in classes:
                classes.append(class_name)
                
            box = detect_object.getElementsByTagName('bndbox')[0]
            xmin = int(box.getElementsByTagName('xmin')[0].firstChild.nodeValue)
            ymin = int(box.getElementsByTagName('ymin')[0].firstChild.nodeValue)
            xmax = int(box.getElementsByTagName('xmax')[0].firstChild.nodeValue)
            ymax = int(box.getElementsByTagName('ymax')[0].firstChild.nodeValue)
            
            boxes.append(ObjectBox(classes.index(class_name),
                                   (xmax + xmin) / (2 * image_width),
                                   (ymax + ymin) / (2 * image_height),
                                   (xmax - xmin) / image_width,
                                   (ymax - ymin) / image_height
                                    ))
            
        with open(os.path.join(output_dir, os.path.basename(xml_file_path).replace('.xml', '.txt')), 'w') as yolo_file:
            for box in boxes:
                yolo_file.write("{} {:6f} {:6f} {:6f} {:6f}\n".format(*box))
            

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Tool for converting PascalVOC format to yolo format')
    parser.add_argument('input', help='Input directory where PascalVOC (XML) formatted files are')
    parser.add_argument('output', help='Output directory where yolo files will be written')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.input):
        logging.error("{} does not exist".format(args.input))
        
    os.makedirs(args.output, exist_ok=True)
        
    for file in os.listdir(args.input):
        file_path = os.path.join(args.input, file)
        if os.path.splitext(file_path)[1] == '.xml':
            convert(file_path, args.output)
            
    with open(os.path.join(args.output, 'all_classes.txt'), 'w') as classes_file:
        for class_name in classes:
            classes_file.write(class_name + "\n")

