import glob, os

local_path = os.path.dirname(os.path.abspath(__file__)) + '/'
dataset_path = local_path + 'dataset_extracted'

# Percentage of images to be used for the test set
percentage_test = 10;
max_number_of_files = 2000

# Create and/or truncate train.txt and test.txt
file_train = open('web-generated-train.txt', 'w')  
file_test = open('web-generated-test.txt', 'w')

# Populate train.txt and test.txt
counter = 1  
index_test = round(100 / percentage_test)  
for loop, pathAndFilename in enumerate(glob.iglob(os.path.join(dataset_path, "*.jpg"))):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test+1:
        counter = 1
        file_test.write("dataset_extracted/" + title + '.jpg' + "\n")
    else:
        file_train.write("dataset_extracted/" + title + '.jpg' + "\n")
        counter = counter + 1
        
    if loop > max_number_of_files:
        break
