'''
Created on 31 mars 2020

@author: S047432
'''
import PIL
from PIL import Image, ImageDraw, ImageFont
import random
import sys
import os

 
class TextField:
    
    class_id = 0
    
    def __init__(self, width, height, arc_radius, border_color, label_outside=None, label_outside_color=None, label_inside=None):
        self.width = width
        self.height = height
        self.arc_radius = arc_radius
        self.label_outside = label_outside
        self.label_outside_color = label_outside_color
        self.label_inside = label_inside
        self.border_color = border_color
        
    def draw(self, x, y, img, image_draw):
        """
        :param x: the x position of the element
        :param y: the y position of the element
        :param img: The image element we are drawing on
        :param image_draw: the PIL ImageDraw object
        """
        font_size = int(self.height * 0.8)
        font = ImageFont.truetype("arial.ttf", font_size)
        
        field_x = x
        
        # box containing arc must be twice the size of the radius
        arc_size_for_corner = self.arc_radius * 2 
        
        if self.label_outside:
            self.label_outside_size = image_draw.textsize(self.label_outside, font)
            field_x = x + self.label_outside_size[0] + 20

        if self.arc_radius > 0:
            image_draw.arc((field_x, y, field_x + arc_size_for_corner, y + arc_size_for_corner), 180, 270, fill=self.border_color)  # top-left
            image_draw.arc((field_x, y + self.height - arc_size_for_corner, field_x + arc_size_for_corner, y + self.height), 90, 180, fill=self.border_color) # bottom-left
            image_draw.arc((field_x + self.width - arc_size_for_corner, y, field_x + self.width, y + arc_size_for_corner), -90, 0, fill=self.border_color) # top-right
            image_draw.arc((field_x + self.width - arc_size_for_corner, y + self.height - arc_size_for_corner, field_x + self.width, y + self.height), 0, 90, fill=self.border_color) # bottom -right
            
        image_draw.line([(field_x + self.arc_radius, y), (field_x + self.width - self.arc_radius, y)], fill=self.border_color) # top line
        image_draw.line([(field_x + self.width, y + self.arc_radius), (field_x + self.width, y + self.height - self.arc_radius)], fill=self.border_color) # right line
        image_draw.line([(field_x + self.arc_radius, y + self.height), (field_x + self.width - self.arc_radius, y + self.height)], fill=self.border_color) # bottom line
        image_draw.line([(field_x, y + self.arc_radius), (field_x, y + self.height - self.arc_radius)], fill=self.border_color) # left line
        
        
        ImageDraw.floodfill(img, ((2 * field_x + self.width) / 2, (2 * y + self.height) / 2), value=(255, 255, 255))
        image_draw = ImageDraw.Draw(img)
        
        
        if self.label_outside:
            image_draw.text((x, y + self.height - font_size - 2), self.label_outside, font=font, fill=self.label_outside_color)
            
        if self.label_inside:
            image_draw.text((field_x + 5, y + self.height - font_size - 2), self.label_inside, font=font, fill=(150, 150, 150))
            
        return (self.class_id, field_x, y, self.width, self.height)
        
class Button:
    
    class_id = 1
    
    def __init__(self, width, height, arc_radius, background_color, label_inside, label_inside_color=None):
        self.width = width
        self.height = height
        self.arc_radius = arc_radius
        self.label_inside = label_inside
        self.label_inside_color = label_inside_color
        self.border_color = background_color
        self.background_color = background_color
        
    def draw(self, x, y, img, image_draw):
        """
        :param x: the x position of the element
        :param y: the y position of the element
        :param img: The image element we are drawing on
        :param image_draw: the PIL ImageDraw object
        """
        font_size = int(self.height * 0.8)
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # box containing arc must be twice the size of the radius
        arc_size_for_corner = self.arc_radius * 2 
        text_width = image_draw.textsize(self.label_inside, font)[0]
        
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

        image_draw.text((x + (self.width - text_width) / 2, y + self.height - font_size - 2), self.label_inside, font=font, fill=self.label_inside_color)
        
        return (self.class_id, x, y, self.width, self.height)
    
class Form:
    
    def __init__(self, background_color, width, height, rows, row_height):
        """
        Draw a form with a color and size
        :param background_color: a RGB tuple or string
        :param width: background width
        :param height: background height
        :param rows: number of rows
        """
        
        supersample_factor = 1 # TODO: apply
        self.background_color = background_color
        self.width = width
        self.height = height
        self.rows = rows
        self.row_height = row_height
        self.margin_top = (self.height - self.rows * self.row_height) / 2
        
        self.img = Image.new('RGB', (width * supersample_factor, height * supersample_factor), background_color)
        self.img_draw = ImageDraw.Draw(self.img)
        
    def draw(self, x, element, row):
        y = self.margin_top + row * self.row_height
        class_id, el_x, el_y, el_w, el_h = element.draw(x, y, self.img, self.img_draw)
#         print(class_id, el_x, el_y, el_w, el_h)
        
        # compute bounding box coordinates in yolo format (class_id, center_x, center_y, width, height). All coordinates are computed relative to picture size
        return (class_id,
                (2 * el_x + el_w) / (2 * self.width),
                (2 * el_y + el_h) / (2 * self.height),
                el_w / self.width,
                el_h / self.height
                )
        
    def create_image(self, path, yolo_coordinates):
        """
        creates the image file
        """
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        
        with open(path, 'wb') as output:
            self.img.save(output, format="JPEG", quality=95)
            
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


def generate_dark_color():
    max_sum = 450
    first_channel = random.randint(0, 255)
    second_channel = random.randint(0, min(255, max_sum - first_channel))
    thrid_channel = random.randint(0, min(255, max_sum - first_channel - second_channel))
    color = [first_channel, second_channel, thrid_channel]
    random.shuffle(color)
    return tuple(color)     

if __name__ == '__main__':
    
    
    os.makedirs('out', exist_ok=True)
    
    form_rows = range(3, 6)
    background_colors = [(204, 255, 153), (153, 255, 153), (153, 255, 204), (204, 204, 255)]
    label_colors = [(0, 51, 0), (0, 51, 102), (255, 0, 0), (204, 0, 204), (0, 0, 0)]
    button_colors =  [(0, 255, 153), (255, 102, 255), (51, 153, 255), (255, 153, 102)]
    labels = ['Name', 'Nom', 'Prenom', 'Login', 'Age', 'password', 'Birthdate', 'location', 'information', 'vehicule', 'Chat', 'naissance', 'Address', 'adresse', 'Ville', 'City', 'Rue', 'Street']
    button_labels = ['OK', 'Validate', 'Cancel', 'Save', 'Hello', 'Enregistrer', 'continue', 'Stop', 'Ajouter', 'Add', 'Remove', 'Supprimer']
    
    number_of_images = 1000
    i = 0
    for i in range(number_of_images):
                
        row_spacing = random.randint(5, 30) # spacing between each row
        field_height = random.randint(16, 40)
        button_height = random.randint(16, 40)
        field_has_value = random.choices([True, False])[0]   # does the field has a value inside
        yolo_coordinates = []
        
        rows = random.randint(3, 6)
        button_color = generate_dark_color()
        button__label_color = generate_light_color()
        label_color = generate_dark_color()
        background_color = generate_light_color()
        
        form_height = random.randint((rows - 1) * (row_spacing + field_height) + button_height + row_spacing, rows * 100)
        form_width = random.randint(400, 800)
        
        form = Form(background_color, form_width, form_height, rows, row_spacing + field_height)
        
        for row_id in range(rows - 1):
            field_name = random.choice(labels)
            field_width = random.randint(len(field_name) * 15, form_width - len(field_name) * 15 - 30) # (10 px of left margin + 20 px of space between text and field)
            
            if field_has_value:
                field_value = field_name
            else:
                field_value = ""
            
            text_field = TextField(field_width, # field width 
                                   field_height,              # field height
                                   random.randint(0, 2),                # corners
                                   (background_color[0] - 10, background_color[1] - 10, background_color[2] - 10) , # border color
                                   field_name,                          # name of the text field
                                   label_color, 
                                   field_value)
            yolo_coordinates.append(form.draw(10, text_field, row_id))
    
        # buttons
        button_name = random.choice(button_labels)
        button_width = random.randint(len(button_name) * 15, len(button_name) * 25)
        button_position_x = random.randint(10, form_width - button_width - 20)
        button = Button(button_width, 
                        button_height,
                        random.randint(0, 2),                # corners
                        button_color, 
                        button_name, 
                        button__label_color)
        yolo_coordinates.append(form.draw(button_position_x, button, rows - 1))
        
        form.create_image("out/out-{}.jpg".format(i), yolo_coordinates)
    
  