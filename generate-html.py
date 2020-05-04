'''
Created on 31 mars 2020

@author: S047432
'''
import PIL
from PIL import Image, ImageDraw, ImageFont
import random
import sys
import os
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

 
class TextField:
    
    class_id = 0
    
    def __init__(self, width, height, arc_radius, border_color, label_outside, label_outside_color, label_inside, font, form_background_color, label_outside_width=None):
        """
        :param font_size: between 0 and 1. percentage of the field height
        :param label_outside_width: width of the label zone in pixels. If not given, label_size will be the size of the label
        """
        
        self.width = width
        self.height = height
        self.arc_radius = arc_radius
        self.label_outside = label_outside
        self.label_outside_color = label_outside_color
        self.label_inside = label_inside
        self.border_color = border_color
        self.background_color = form_background_color
        self.label_outside_width = label_outside_width
        self.font = font
        
    def draw(self, x, y, img, image_draw):
        """
        :param x: the x position of the element
        :param y: the y position of the element
        :param img: The image element we are drawing on
        :param image_draw: the PIL ImageDraw object
        """
        field_x = x
        
        # box containing arc must be twice the size of the radius
        arc_size_for_corner = self.arc_radius * 2 
        
        label_outside_width, label_outside_height = image_draw.textsize(self.label_outside, self.font)

        field_x = x + self.label_outside_width + 20

        if self.arc_radius > 0:
            image_draw.arc((field_x, y, field_x + arc_size_for_corner, y + arc_size_for_corner), 180, 270, fill=self.border_color)  # top-left
            image_draw.arc((field_x, y + self.height - arc_size_for_corner, field_x + arc_size_for_corner, y + self.height), 90, 180, fill=self.border_color) # bottom-left
            image_draw.arc((field_x + self.width - arc_size_for_corner, y, field_x + self.width, y + arc_size_for_corner), -90, 0, fill=self.border_color) # top-right
            image_draw.arc((field_x + self.width - arc_size_for_corner, y + self.height - arc_size_for_corner, field_x + self.width, y + self.height), 0, 90, fill=self.border_color) # bottom -right
            
        image_draw.line([(field_x + self.arc_radius, y), (field_x + self.width - self.arc_radius, y)], fill=self.border_color) # top line
        image_draw.line([(field_x + self.width, y + self.arc_radius), (field_x + self.width, y + self.height - self.arc_radius)], fill=self.border_color) # right line
        image_draw.line([(field_x + self.arc_radius, y + self.height), (field_x + self.width - self.arc_radius, y + self.height)], fill=self.border_color) # bottom line
        image_draw.line([(field_x, y + self.arc_radius), (field_x, y + self.height - self.arc_radius)], fill=self.border_color) # left line
        
        
        ImageDraw.floodfill(img, ((2 * field_x + self.width) / 2, (2 * y + self.height) / 2), value=self.background_color)
        image_draw = ImageDraw.Draw(img)
        
        
        if self.label_outside:
            image_draw.text((x, y + (self.height - label_outside_height) / 2), self.label_outside, font=self.font, fill=self.label_outside_color)
            
        if self.label_inside:
            image_draw.text((field_x + 5, y + (self.height - label_outside_height) / 2), self.label_inside, font=self.font, fill=(150, 150, 150))
            
        return (self.class_id, field_x, y, self.width, self.height)
        
class Button:
    
    class_id = 1
    
    def __init__(self, width, height, arc_radius, form_background_color, label_inside, label_inside_color, font_size):
        self.width = width
        self.height = height
        self.arc_radius = arc_radius
        self.label_inside = label_inside
        self.label_inside_color = label_inside_color
        self.border_color = form_background_color
        self.background_color = form_background_color
        self.font_size = font_size
        
    def draw(self, x, y, img, image_draw):
        """
        :param x: the x position of the element
        :param y: the y position of the element
        :param img: The image element we are drawing on
        :param image_draw: the PIL ImageDraw object
        """
        font_size = int(self.height * self.font_size)
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # box containing arc must be twice the size of the radius
        arc_size_for_corner = self.arc_radius * 2 
        text_width, text_height = image_draw.textsize(self.label_inside, font)
        
        # change width if its too low
        self.width = max(text_width + 10, self.width)

        if self.arc_radius > 0:
            image_draw.arc((x, y, x + arc_size_for_corner, y + arc_size_for_corner), 180, 270, fill=self.border_color)  # top-left
            image_draw.arc((x, y + self.height - arc_size_for_corner, x + arc_size_for_corner, y + self.height), 90, 180, fill=self.border_color) # bottom-left
            image_draw.arc((x + self.width - arc_size_for_corner, y, x + self.width, y + arc_size_for_corner), -90, 0, fill=self.border_color) # top-right
            image_draw.arc((x + self.width - arc_size_for_corner, y + self.height - arc_size_for_corner, x + self.width, y + self.height), 0, 90, fill=self.border_color) # bottom -right
            
        image_draw.line([(x + self.arc_radius, y), (x + self.width - self.arc_radius, y)], fill=self.border_color) # top line
        image_draw.line([(x + self.width, y + self.arc_radius), (x + self.width, y + self.height - self.arc_radius)], fill=self.border_color) # right line
        image_draw.line([(x + self.arc_radius, y + self.height), (x + self.width - self.arc_radius, y + self.height)], fill=self.border_color) # bottom line
        image_draw.line([(x, y + self.arc_radius), (x, y + self.height - self.arc_radius)], fill=self.border_color) # left line
        
        ImageDraw.floodfill(img, ((2 * x + self.width) / 2, (2 * y + self.height) / 2), value=self.background_color)
        image_draw = ImageDraw.Draw(img)

        image_draw.text((x + (self.width - text_width) / 2, y + (self.height - text_height) / 2), self.label_inside, font=font, fill=self.label_inside_color)
        
        return (self.class_id, x, y, self.width, self.height)
    
class Form:
    
    def __init__(self, form_background_color, width, height, rows, row_height):
        """
        Draw a form with a color and size
        :param form_background_color: a RGB tuple or string
        :param width: background width
        :param height: background height
        :param rows: number of rows
        """
        
        supersample_factor = 1 # TODO: apply
        self.background_color = form_background_color
        self.width = width
        self.height = height
        self.rows = rows
        self.row_height = row_height
        self.margin_top = (self.height - self.rows * self.row_height) / 2
        
        self.img = Image.new('RGB', (width * supersample_factor, height * supersample_factor), form_background_color)
        self.img_draw = ImageDraw.Draw(self.img)
        
    def draw(self, x, element, row):
        y = self.margin_top + row * self.row_height
        class_id, el_x, el_y, el_w, el_h = element.draw(x, y, self.img, self.img_draw)
        
        # compute bounding box coordinates in yolo format (class_id, center_x, center_y, width, height). All coordinates are computed relative to picture size
        return (class_id,
                (2 * el_x + el_w) / (2 * self.width),
                (2 * el_y + el_h) / (2 * self.height),
                el_w / self.width,
                el_h / self.height
                )
        
    def create_image(self, path, yolo_coordinates, image_quality):
        """
        creates the image file
        """
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        
        with open(path, 'wb') as output:
            self.img.save(output, format="JPEG", quality=image_quality)
            
        with open(path.replace('.jpg', '.txt'), 'w') as yolo:
            for yolo_coordinate in yolo_coordinates:
                yolo.write("{} {:6f} {:6f} {:6f} {:6f}\n".format(*yolo_coordinate))
            
def generate_light_color():
    min_sum = 550
    first_channel = 255
    second_channel = random.randint(190, 255)
    thrid_channel = random.randint(min_sum - first_channel - second_channel, 255)
    color = [first_channel, second_channel, thrid_channel]
    random.shuffle(color)
    return tuple(color) 
            
def generate_very_light_color():
    first_channel = random.randint(245, 255)
    second_channel = random.randint(245, 255)
    thrid_channel = random.randint(245, 255)
    color = [first_channel, second_channel, thrid_channel]
    random.shuffle(color)
    return tuple(color) 


def generate_dark_color():
    max_sum = 450
    first_channel = random.randint(0, 255)
    second_channel = random.randint(0, min(255, max_sum - first_channel))
    thrid_channel = random.randint(0, min(255, max_sum - first_channel - second_channel))
    color = [first_channel, second_channel, thrid_channel]
    random.shuffle(color)
    return tuple(color) 


def luminance(color):
    
    def factor(channel_value):
        channel_factor = channel_value / 255.
        if channel_factor <= 0.03928:
            channel_factor = channel_factor / 12.92;
        else:
            channel_factor = ((channel_factor + 0.055) / 1.055) ** 2.4
        return channel_factor

    return (factor(color[0]) * 0.2126 + factor(color[1]) * 0.7152 + factor(color[2]) * 0.0722) + 0.05; 

def compute_color_diff(color1, color2):
    
    lum1 = luminance(color1);
    lum2 = luminance(color2);
    brightest = max(lum1, lum2);
    darkest = min(lum1, lum2);
    return brightest / darkest;
    
#     color1_rgb = sRGBColor(color1[0] / 255., color1[1] / 255., color1[2] / 255.);
#     color2_rgb = sRGBColor(color2[0] / 255., color2[1] / 255., color2[2] / 255.); 
#     
#     color1_lab = convert_color(color1_rgb, LabColor);
#     color2_lab = convert_color(color2_rgb, LabColor);
#     
#     return delta_e_cie2000(color1_lab, color2_lab);  



if __name__ == '__main__':
    
    min_width = 300
    max_width = 416
    min_rows = 3
    max_rows = 4
    min_field_height = 16
    max_field_height = 30 # may be 40 when field width is greater, due to font size
    number_of_images = 2000
    
    
    os.makedirs('out', exist_ok=True)
    
    labels = ['Name', 'Nom', 'Prenom', 'Login', 'Age', 'password', 'Birthdate', 'location', 'information', 'vehicule', 'Chat', 
              'naissance', 'Address', 'adresse', 'Ville', 'City', 'Rue', 'Street', 'email', 'Username', 'Contact', 'Phone', 'number', 
              'Age', 'Message', 'zip code', 'Code postal', 'Country', 'Pays', 'State', 'Company', 'Entreprise', 'URL']
    button_labels = ['OK', 'Validate', 'Cancel', 'Save', 'Hello', 'Enregistrer', 'continue', 'Stop', 'Ajouter', 'Add', 'Remove', 'Supprimer']
    
    i = 0
    for i in range(number_of_images):
                
        rows = random.randint(min_rows, max_rows)
        row_spacing = random.randint(5, 30) # spacing between each row
        field_height = random.randint(min_field_height, max_field_height)
        button_height = random.randint(min_field_height, max_field_height)
        form_height = random.randint(15 + (rows - 1) * (row_spacing + field_height) + button_height + row_spacing, rows * 100)
        form_width = random.randint(min_width, max_width)
        form_background_color = generate_light_color()
        
        form = Form(form_background_color, form_width, form_height, rows, row_spacing + field_height)
        
        field_font_size = random.uniform(0.6, 0.8)
        field_font = ImageFont.truetype("arial.ttf", int(field_height * field_font_size))
        field_background_color = generate_very_light_color()
        button_font_size = random.uniform(0.6, 0.8)
        field_has_value = random.choices([True, False])[0]   # does the field has a value inside
        yolo_coordinates = []
        field_aligned = random.randint(0, 1)
        field_names = random.choices(labels, k=rows - 1)
        field_min_label_size = max([form.img_draw.textsize(n, field_font)[0] for n in field_names])
        field_fixed_size = random.randint(field_min_label_size + 10, field_min_label_size + 30)
        
        
        form_color_diff = 0
        while form_color_diff < 4:
            label_color = generate_dark_color()
            form_color_diff = compute_color_diff(label_color, form_background_color)
            
        button_color_diff = 0
        while button_color_diff < 2:
            button_color = generate_dark_color()
            button_label_color = generate_light_color()
            button_color_diff = compute_color_diff(button_color, button_label_color)
        
        for row_id, field_name in enumerate(field_names):
            
            if field_aligned: # field aligned
                field_label_size = field_fixed_size
            else:
                field_label_size = form.img_draw.textsize(field_name, field_font)[0]
            
            field_width = random.randint(form.img_draw.textsize(field_name, field_font)[0], form_width - field_label_size - 30) # (10 px of left margin + 20 px of space between text and field)
            
            if field_has_value:
                field_value = field_name
            else:
                field_value = ""
            
            text_field = TextField(field_width, # field width 
                                   field_height,              # field height
                                   random.randint(0, 3),                # corners
                                   (form_background_color[0] - 15, form_background_color[1] - 15, form_background_color[2] - 15) , # border color
                                   field_name,                          # name of the text field
                                   label_color, 
                                   field_value, 
                                   field_font,
                                   field_background_color,
                                   field_label_size)
            yolo_coordinates.append(form.draw(10, text_field, row_id))
    
        # buttons
        button_name = random.choice(button_labels)
        button_width = random.randint(len(button_name) * 15, len(button_name) * 25)
        button_position_x = random.randint(10, form_width - button_width - 20)
        button = Button(button_width, 
                        button_height,
                        random.randint(0, 3),                # corners
                        button_color, 
                        button_name, 
                        button_label_color,
                        button_font_size)
        yolo_coordinates.append(form.draw(button_position_x, button, rows - 1))
        image_quality = random.randint(70, 100)
        
        print("image " + str(i))
        form.create_image("out/out-{}.jpg".format(i), yolo_coordinates, image_quality)
    
  