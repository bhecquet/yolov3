# for i in range(2000):
#     print("dataset_generated_small/out-{}.jpg".format(i))


# ----------------------------------------------------
# code for creating a "_form_" object for each picture
# ----------------------------------------------------
#
# from xml.dom import minidom
# from xml import dom
# import os
# 
# def convert(xml_file_path):
#     """
#     convert XML file to yolo format file
#     """
#     boxes = []
#     
#     with open(xml_file_path, 'r') as xml_file:
#         document = minidom.parse(xml_file)
#         
#         size = document.getElementsByTagName('size')[0]
#         image_width = int(size.getElementsByTagName('width')[0].firstChild.nodeValue)
#         image_height = int(size.getElementsByTagName('height')[0].firstChild.nodeValue)
#         
#         form = minidom.parseString("""<object>
#         <name>_form_</name>
#         <pose>Unspecified</pose>
#         <truncated>0</truncated>
#         <difficult>0</difficult>
#         <bndbox>
#             <xmin>0</xmin>
#             <ymin>0</ymin>
#             <xmax>416</xmax>
#             <ymax>416</ymax>
#         </bndbox>
#     </object>""")
#         document.childNodes[0].appendChild(form.childNodes[0])
#         xml_content = document.toxml()
#         
#     with open(xml_file_path, 'w') as xml_file:
#         xml_file.write(xml_content)
#       
#       
# 
# if __name__ == '__main__':
#     for file in os.listdir(r'D:\Dev\yolo\yolov3\dataset'):
#         file_path = os.path.join(r'D:\Dev\yolo\yolov3\dataset', file)
#         if os.path.splitext(file_path)[1] == '.xml':
#             convert(file_path)
    
