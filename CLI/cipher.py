import os
cls = lambda: os.system("cls" if os.name == "nt" else "clear")
cls()

alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".lower()
def cipher(inputstr: str, offset: int) -> str:
    """Cipher a given string. Maximum offset is 26.

    Args:
        inputstr (str): Given string
        offset (int): Offset

    Returns:
        str: Ciphered string
    """
    if offset > 26:
        raise ValueError("Offset is greater than 26")
    ans = ""
    for i in range(len(inputstr)):
        ch = inputstr[i]
        if ch == " ":
            ans += " "
        elif ch.isupper():
            ans += chr((ord(ch) + offset-65) % 26 + 65)
        else:
            ans += chr((ord(ch) + offset-97) % 26 + 97)
    ans: str

    return ans + alphabet.split()[offset]

def decipher(inputstr: str) -> str:
    """Decipher a given string. Maximum offset is 26.

    Args:
        inputstr (str): Given string
        offset (int): Offset

    Returns:
        str: Deciphered string
    """
    offset = alphabet.split().index([*inputstr][len(inputstr) - 1])
    inputstr = inputstr.replace([*inputstr][len(inputstr) - 1], "")

    if offset > 26:
        raise ValueError("Offset is greater than 26")
    ans = ""
    offset = 26 - offset
    for i in range(len(inputstr)):
        ch = inputstr[i]
        if ch == " ":
            ans += " "
        elif ch.isupper():
            ans += chr((ord(ch) + offset-65) % 26 + 65)
        else:
            ans += chr((ord(ch) + offset-97) % 26 + 97)
    ans: str
    
    return ans

print(cipher(input("Input string to cipher: "), int(input("Offset: "))))
print(decipher(input("Input string to decipher: ")))
