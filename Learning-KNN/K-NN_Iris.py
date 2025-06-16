# knn_iris.py

import numpy as np
import pandas as pd
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def load_data(path):
    df = pd.read_csv(path)
    X = df.drop(columns=['variety']).values
    y = preprocessing.LabelEncoder().fit_transform(df['variety'])
    return X, y

def preprocess(X_train, X_test):
    scaler = preprocessing.StandardScaler()
    X_train_norm = scaler.fit_transform(X_train)
    X_test_norm = scaler.transform(X_test)
    return X_train_norm, X_test_norm

def evaluate_kknn(X_train, y_train, X_test, y_test, k):
    neigh = KNeighborsClassifier(n_neighbors=k)
    neigh.fit(X_train, y_train)
    y_pred = neigh.predict(X_test)
    acc_test = metrics.accuracy_score(y_test, y_pred)
    acc_train = metrics.accuracy_score(y_train, neigh.predict(X_train))
    return acc_train, acc_test, neigh

def search_best_k(X_train, y_train, X_test, y_test, max_k=50):
    best = (0, 0, 1)
    for k in range(1, max_k+1):
        _, acc_test, _ = evaluate_kknn(X_train, y_train, X_test, y_test, k)
        if acc_test > best[1]:
            best = (k, acc_test, acc_test)
    print(f"Best k = {best[0]}, Test Accuracy = {best[1]:.4f}")
    return best[0]

def main():
    X, y = load_data('datasets/iris.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                       test_size=0.2, 
                                                       random_state=4)
    X_train_norm, X_test_norm = preprocess(X_train, X_test)
    print("Train/Test split:", X_train.shape, X_test.shape)

    # Coba nilai k default
    k = 4
    acc_train, acc_test, _ = evaluate_kknn(X_train_norm, y_train, X_test_norm, y_test, k)
    print(f"k = {k} -> Train Acc: {acc_train:.4f}, Test Acc: {acc_test:.4f}")

    # Mencari k optimal
    best_k = search_best_k(X_train_norm, y_train, X_test_norm, y_test, max_k=50)

    # Evaluasi lagi dengan k terbaik
    acc_train, acc_test, model = evaluate_kknn(X_train_norm, y_train, X_test_norm, y_test, best_k)
    print(f"Final eval with k={best_k}: Train Acc={acc_train:.4f}, Test Acc={acc_test:.4f}")

    # Contoh prediksi baru
    sample = np.array([[5.9, 3.0, 5.1, 1.8]])
    sample_norm = preprocessing.StandardScaler().fit(X_train).transform(sample)
    print("Sample prediction:", model.predict(sample_norm))

if __name__ == "__main__":
    main()
