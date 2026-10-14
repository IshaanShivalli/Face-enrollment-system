import pickle

                         
print("[INFO] loading face encodings...")

                                 
with open("output/encodings.pickle", "rb") as f:
    data = pickle.load(f)

                                         
person_id_to_delete = "03"

                                               
if person_id_to_delete in data['names']:
                                                                     
    indices_to_delete = [i for i, name in enumerate(data['names']) if name == person_id_to_delete]
    
                                                                   
    for index in reversed(indices_to_delete):                                                      
        del data['names'][index]
        del data['encodings'][index]
    
    print(f"[INFO] Deleted all occurrences of person ID {person_id_to_delete}")
    
                                                            
    with open("output/encodings.pickle", "wb") as f:
        pickle.dump(data, f)
    
    print("[INFO] Updated encodings.pickle successfully.")
else:
    print(f"[ERROR] Person ID {person_id_to_delete} not found in the encodings data.")
