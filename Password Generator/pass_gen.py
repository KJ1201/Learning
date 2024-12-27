import random
import string

def generate_pass(min_length, numbers=True, special_char=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    # print(letters, digits, special)

    characters = letters
    if numbers:
        characters += digits
    if special_char:
        characters += special
    
    pwd = ""
    meets_criteria = False
    has_number = False
    has_special = False

    while not meets_criteria or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char

        if new_char in digits:
            has_number = True
        elif new_char in special:
            has_special = True

        meets_criteria = True
        if numbers:
            meets_criteria = has_number
        if special_char:
            meets_criteria = meets_criteria and has_special

        
    return pwd
    

min_len = int(input("Enter the minimum length: "))
has_num = input("Do you want to include numbers? (y/n): ").lower() == "y"
has_spec = input("Do you want to include special characters? (y/n): ").lower() == "y"
pwd = generate_pass(min_len, has_num, has_spec)

print("The generated password is", pwd)