import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk


def update_label(value):
    label.config(text=f"当前值: {value}")
    update_image(value)


def update_image(value):
    image_path = f"{value}.jpg"
    try:
        image = Image.open(image_path)
        image = image.resize((340, 219))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
    except Exception as e:
        print(f"无法加载图片: {str(e)}")


# 创建主窗口
root = tk.Tk()
root.title("滑块示例")

# 创建滑块
slider = tk.Scale(root, from_=2, to=50, orient="horizontal", command=update_label)
slider.pack(pady=20)

# 创建显示滑块值的标签
label = tk.Label(root, text="当前值: 1")
label.pack()

# 创建显示图片的标签
image_label = tk.Label(root)
image_label.pack()

root.mainloop()
