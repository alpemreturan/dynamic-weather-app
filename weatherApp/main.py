import customtkinter
import weatherapi
from PIL import Image
import os
import sys
import requests
from io import BytesIO

customtkinter.set_appearance_mode("dark")

Height = 800
Width = 1000

default_background_image_path = os.path.join(os.path.dirname(__file__), "background.jpg")
default_background_image = Image.open(default_background_image_path)

search_button_image_path = os.path.join(os.path.dirname(__file__), "search.png")
search_button_image = Image.open(search_button_image_path)

location_label_image_path = os.path.join(os.path.dirname(__file__), "loc.png")
location_label_image = Image.open(location_label_image_path)

error_image_path = os.path.join(os.path.dirname(__file__), "oops.png")
error_label_image = Image.open(error_image_path)

if hasattr(sys, "_MEIPASS"):
    icon_path = os.path.join(sys._MEIPASS, "icon.ico")
else:
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry(f"{Width}x{Height}")
        self.resizable(False, False)
        self.iconbitmap(icon_path)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.default_background = customtkinter.CTkImage(light_image=default_background_image, size=(1980, 1080))
        self.default_background_label = customtkinter.CTkLabel(self, text="", image=self.default_background, width=Width, height=Height)
        self.default_background_label.place(x=0, y=0)

        self.entry = customtkinter.CTkEntry(self,
            width=625,
            height=60,
            font=("Comic Sans MS", 20),
            placeholder_text="Enter Your Location",
            placeholder_text_color="black",
            corner_radius=1,
            fg_color="white",
            text_color="black",
            border_color="black",
            border_width=2,
            justify="center",
        )
        self.entry.place(relx=0.5, rely=0.1, anchor="center")

        self.search_button = customtkinter.CTkButton(self,
            text="",
            width=70,
            height=60,
            fg_color="white",
            text_color="black",
            corner_radius=1,
            hover_color="lightblue",
            border_color="black",
            border_width=2,
            image=customtkinter.CTkImage(light_image=search_button_image, size=(30, 30)),
            command=self.search
        )
        self.search_button.place(relx=0.78, rely=0.1, anchor="center")
        
        self.location_label = customtkinter.CTkLabel(self,
            text="",
            width=60,
            height=50,
            fg_color="white",
            text_color="black",
            corner_radius=1,
            image=customtkinter.CTkImage(light_image=location_label_image, size=(30, 30)),
        )
        self.location_label.place(relx=0.22, rely=0.1, anchor="center")

        self.frame = customtkinter.CTkFrame(self,
            width=620,
            height=600,
            corner_radius=0,
            fg_color="white",
            border_color="black",
            border_width=2,
        )
        self.frame.place(relx=0.5, rely=0.53, anchor="center")
        
        self.city_label = None
        self.country_label = None
        self.icon_label = None
        self.temperature_label = None
        self.description_label = None
        self.error_label = None
        self.error_label_image = None

    def search(self):
        city_name = self.entry.get()
        weather = weatherapi.Weather()
        result = weather.get_weather_data(city_name)

        if self.city_label:
            self.city_label.destroy()
        if self.country_label:
            self.country_label.destroy()
        if self.icon_label:
            self.icon_label.destroy()
        if self.temperature_label:
            self.temperature_label.destroy()
        if self.description_label:
            self.description_label.destroy()
        if self.error_label:
            self.error_label.destroy()
        if self.error_label_image:
            self.error_label_image.destroy()

        if result is True:
            response = requests.get(weatherapi.icon_url.format(weather.icon), stream=True)
            if response.status_code == 200:
                icon_image = Image.open(BytesIO(response.content))
                self.icon_label = customtkinter.CTkLabel(self,
                    text="",
                    fg_color="white",
                    image=customtkinter.CTkImage(light_image=icon_image, size=(300, 300)),
                )
                self.icon_label.place(relx=0.5, rely=0.45, anchor="center")

            self.city_label = customtkinter.CTkLabel(self,
                text=f"{weather.city},",
                font=("Comic Sans MS", 50),
                fg_color="white",
                text_color="black"
            )
            self.city_label.place(relx=0.42, rely=0.25, anchor="center")

            self.country_label = customtkinter.CTkLabel(self,
                text=weather.country,
                font=("Comic Sans MS", 50),
                fg_color="white",
                text_color="black"
            )
            self.country_label.place(relx=0.62, rely=0.25, anchor="center")
        
            self.temperature_label = customtkinter.CTkLabel(self,
                text=weather.temperature,
                font=("Comic Sans MS", 50),
                fg_color="white",
                text_color="black"
            )
            self.temperature_label.place(relx=0.5, rely=0.65, anchor="center")

            self.description_label = customtkinter.CTkLabel(self,
                text=weather.description,
                font=("Comic Sans MS", 50),
                fg_color="white",
                text_color="black"
            )
            self.description_label.place(relx=0.5, rely=0.75, anchor="center")
        else:
            self.error_label = customtkinter.CTkLabel(self,
                text=weatherapi.mistake_message,
                font=("Comic Sans MS", 23),
                fg_color="white",
                text_color="black"
            )
            self.error_label.place(relx=0.5, rely=0.4, anchor="center")

            self.error_label_image = customtkinter.CTkLabel(self,
                text="",
                width=350,
                height=350,
                fg_color="white",
                text_color="black",
                corner_radius=1,
                image=customtkinter.CTkImage(light_image=error_label_image, size=(350, 350)),
            )
            self.error_label_image.place(relx=0.5, rely=0.65, anchor="center")

            

    def on_closing(self):
        self.destroy() 

    def run(self):
        self.mainloop()

app = App()
app.run()