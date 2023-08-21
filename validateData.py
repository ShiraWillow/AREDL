import os
import sys
import json
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validateData():
    validator = URLValidator()
    current_dir = os.path.join(os.getcwd(), "data")
    list_path = os.path.join(current_dir, "_list.json")
    levels = []
    had_error = False
    with open(list_path, "r") as file:
        levels = json.load(file)
        
    for filename in levels:
        if filename.startswith("_"):
                continue
        file_path = os.path.join(current_dir, f"{filename}.json")
        lines = []
        with open(file_path, "r") as file:
            data = json.load(file)
            records = data["records"]
            names = []
            try:
                validator(data["verification"])
            except ValidationError:
                had_error = True
                print(f"Invalid verification Url: {filename}: {url}")
                    
            for record in records:
                
                name = record["user"].lower()
                if name in names:
                    had_error = True
                    print(f"Duplicate Record: {filename}: {name}")
                    
                names.append(name)
                url = record["link"]
                try:
                    validator(url)
                except ValidationError:
                    had_error = True
                    print(f"Invalid Url: {filename} {name}: {url}")
                    
            creators = []
            for creator in data["creators"]:
                if creator in creators:
                    had_error = True
                    print(f"Duplicate Creator: {filename}: {creator}")
                creators.append(creator)
                
    if had_error:
        sys.exit(1)

if __name__ == "__main__":
    validateData()