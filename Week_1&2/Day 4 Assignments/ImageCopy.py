#Write script to copy an image file's contents to another file

with open("img.png", "rb") as img1:

    with open("Copyimg.png", "wb") as img2:
        data = img1.read()
        copy = img2.write(data)

print("picture copied successfully")

