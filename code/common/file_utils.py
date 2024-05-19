# helper functions for file operations
# In this file, the logic is given to check the type & size of the file uploaded
import os

# mime-types = the type of files which a computer understands
mime_types = {
    # JPEG (.jpg, .jpeg):
    'jpg' : 'image/jpeg',
    'jpeg': 'image/jpeg',

    # PNG (.png):
    'png': 'image/png'
}

def get_mime_type(file_path):
    ext = file_path.split('.')[-1]
    return mime_types.get(ext,'text/plain')

def is_file_allowed(file_path):
    allowed_extensions = list(mime_types.keys())   # check the list of all extensions
    ext = file_path.split('.')[-1]         # if the required file extension exists in the list, choose it
    return ext in allowed_extensions       # return true

def upload_file(file, name):
    upload_path = os.path.join('static','uploads')     # path of file upload; address of folders
    if not os.path.exists(upload_path):   
        os.makedirs(upload_path)
    # The above 2 lines will handle the making of 'static' & 'uploads' folder & will never cause an error 
    
    # Uncomment the below line to restrict file types
    if not is_file_allowed(name):
        return None         
           
    file_path = os.path.join(upload_path, name)  
    file.save(file_path)  
    return file_path