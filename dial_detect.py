import requests
from tkinter import *
from bs4 import BeautifulSoup

def get_details():
    access_key = "ea0a56fdfc72a1f2efa107067de1f8a5"
    number = number_entry.get()
    country_code = country_code_entry.get()

    url = f"http://apilayer.net/api/validate?access_key={access_key}&number={number}&country_code={country_code}&format=1"
    response = requests.get(url)
    data = response.json()

    result_text.delete(1.0, END)
    if 'valid' in data and data['valid']:
        result_text.insert(END, "Phone number is valid.\n")
    else:
        result_text.insert(END, "Phone number is invalid.\n")
    
    if 'carrier' in data:
        result_text.insert(END, f"Carrier: {data['carrier']}\n")
    
    if 'line_type' in data:
        result_text.insert(END, f"Line type: {data['line_type']}\n")
    
    if 'location' in data:
        result_text.insert(END, f"Location: {data['location']}\n")

    # Perform Facebook search
    facebook_url = f"https://www.facebook.com/search/people/?q={number}"
    facebook_response = requests.get(facebook_url)
    facebook_soup = BeautifulSoup(facebook_response.content, 'html.parser')
    facebook_results = facebook_soup.find_all("div", class_="_60ri")
    
    if facebook_results:
        result_text.insert(END, "\nFacebook Search Results:\n")
        for result in facebook_results:
            result_text.insert(END, f"- {result.text}\n")
    else:
        result_text.insert(END, "\nNo Facebook results found.\n")
    
    # Perform Instagram search
    instagram_url = f"https://www.instagram.com/explore/tags/{number}/"
    instagram_response = requests.get(instagram_url)
    instagram_soup = BeautifulSoup(instagram_response.content, 'html.parser')
    instagram_results = instagram_soup.find_all("div", class_="v1Nh3")
    
    if instagram_results:
        result_text.insert(END, "\nInstagram Search Results:\n")
        for result in instagram_results:
            result_text.insert(END, "- Instagram post\n")
    else:
        result_text.insert(END, "\nNo Instagram results found.\n")

def exit_program():
    root.destroy()

# Create UI
root = Tk()
root.title("DialDetect")
root.configure(bg="black")  # Set background color to black

# UI Layout
title_frame = Frame(root, bg="black")
title_frame.pack()

title_label = Label(title_frame, text="DialDetect", font=("Courier", 16, "bold"), fg="green", bg="black")
title_label.pack()

line_label = Label(title_frame, text="─" * 50, font=("Courier", 12), fg="green", bg="black")
line_label.pack()

number_label = Label(root, text="Phone Number:", font=("Courier", 12), fg="green", bg="black")
number_label.pack()
number_entry = Entry(root, font=("Courier", 12))
number_entry.pack()

country_code_label = Label(root, text="Country Code:", font=("Courier", 12), fg="green", bg="black")
country_code_label.pack()
country_code_entry = Entry(root, font=("Courier", 12))
country_code_entry.pack()

submit_button = Button(root, text="Get Details", font=("Courier", 12), fg="green", bg="black", bd=0, command=get_details)
submit_button.pack()

exit_button = Button(root, text="Exit", font=("Courier", 12), fg="green", bg="black", bd=0, command=exit_program)
exit_button.pack()

result_text = Text(root, height=10, width=50, font=("Courier", 12), fg="green", bg="black")
result_text.pack()

root.mainloop()
