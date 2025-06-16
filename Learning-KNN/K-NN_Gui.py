import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# === Load & train model dulu ===
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = KNeighborsClassifier(n_neighbors=20)
model.fit(X_train, y_train)

# === Mapping label ke nama ===
label_map = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}

# === GUI ===
def predict_species():
    try:
        # Ambil input user
        inputs = [
            float(entry_sepal_length.get()),
            float(entry_sepal_width.get()),
            float(entry_petal_length.get()),
            float(entry_petal_width.get())
        ]
        # Ubah ke array numpy
        sample = np.array([inputs])
        # Prediksi
        result = model.predict(sample)[0]
        species = label_map[result]
        messagebox.showinfo("Hasil Prediksi", f"Bunga tersebut diprediksi sebagai: {species}")
    except:
        messagebox.showerror("Error", "Masukkan semua angka dengan benar!")

# === Layout GUI ===
root = tk.Tk()
root.title("Prediksi Bunga Iris (KNN)")
root.geometry("300x300")

tk.Label(root, text="Sepal Length").pack()
entry_sepal_length = tk.Entry(root)
entry_sepal_length.pack()

tk.Label(root, text="Sepal Width").pack()
entry_sepal_width = tk.Entry(root)
entry_sepal_width.pack()

tk.Label(root, text="Petal Length").pack()
entry_petal_length = tk.Entry(root)
entry_petal_length.pack()

tk.Label(root, text="Petal Width").pack()
entry_petal_width = tk.Entry(root)
entry_petal_width.pack()

tk.Button(root, text="Prediksi", command=predict_species).pack(pady=10)

root.mainloop()
