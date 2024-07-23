import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image


def upload_pic():
    file_path = filedialog.askopenfilename()

    if file_path:
        original_image = Image.open(file_path)
        resized_image = original_image.resize((400, 400), Image.ANTIALIAS)
        the_image = ImageTk.PhotoImage(resized_image)

        img_path = file_path
        img = image.load_img(img_path, target_size=(256, 256))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255
        image_label.config(image=the_image)
        image_label.image = the_image
        predictions = loaded_model.predict(img_array)
        if predictions[0, 0] > predictions[0, 1]:
            result_label.config(text="Not a cat", font=('Arial', 15, 'italic'))
        else:
            result_label.config(text="Is a cat!", font=('Arial', 15, 'italic'))


# Load the pre-trained model
loaded_model = load_model('my_new_model_2.0.h5')

# Create the main Tkinter window
TK = tk.Tk()
TK.geometry("600x600")

# Create a button to upload pictures
tk_button = tk.Button(TK, text="Upload picture", width=15, font=('Arial', 15, 'italic'), command=upload_pic)
tk_button.pack(padx=50, pady=10)

# Create a label to display the uploaded image
image_label = tk.Label(TK)
image_label.pack(padx=50, pady=10)

# Create a label to display the result (whether it's a cat or not)
result_label = tk.Label(TK, text="", font=('Arial', 15, 'italic'))
result_label.pack(padx=50, pady=10)

# Start the Tkinter main loop
TK.mainloop()
