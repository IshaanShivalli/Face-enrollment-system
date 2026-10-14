import tkinter as tk
from tkinter import messagebox
from project.utils import Conf
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle

def train_model():
    try:
                                
        conf = Conf("config/config.json")
        encodings_path = conf["encodings_path"]
        recognizer_path = conf["recognizer_path"]
        le_path = conf["le_path"]

                                 
        print("[INFO] loading face encodings...")
        with open(encodings_path, "rb") as f:
            data = pickle.load(f)                                           
            
        names = data.get("names", [])
        encodings = data.get("encodings", [])
        unique_names = set(names)
        if len(names) != len(encodings):
            messagebox.showerror(
                "Invalid Encodings",
                "The number of face labels does not match the number of face encodings. "
                "Run encode_faces.py again."
            )
            return
        if len(unique_names) < 2:
            messagebox.showerror(
                "Not Enough People",
                f"Training needs encodings for at least 2 different people; "
                f"the current file contains {len(unique_names)}. "
                "Enroll another person with a different ID, then run encode_faces.py "
                "again before training."
            )
            return

                           
        print("[INFO] encoding labels...")
        le = LabelEncoder()
        labels = le.fit_transform(names)

                                                                        
        print("[INFO] training model...")
        recognizer = SVC(C=1.0, kernel="linear", probability=True)

                                                     
        recognizer.fit(encodings, labels)

                                 
        print("[INFO] writing the model to disk...")
        with open(recognizer_path, "wb") as f:
            pickle.dump(recognizer, f)

                                         
        with open(le_path, "wb") as f:
            pickle.dump(le, f)

                              
        messagebox.showinfo("Success", "Model training completed successfully!")

                                                      
        exit_program()

    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def exit_program():
                      
    root.quit()

                           
root = tk.Tk()
root.title("Train Face Recognition Model")
root.geometry("500x300")

                      
window_width = 500
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_left = int(screen_width / 2 - window_width / 2)

                                             
root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

                                                                         
root.config(bg="#f4f4f9")

           
title_label = tk.Label(root, text="Train Face Recognition Model", font=("Helvetica", 16, "bold"), bg="#f4f4f9")
title_label.pack(pady=10)

                  
train_button = tk.Button(root, text="Start Training", command=train_model, font=("Helvetica", 14), bg="#007BFF", fg="white")
train_button.pack(pady=20)

             
root.mainloop()
