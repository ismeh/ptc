# -*- coding: utf-8 -*-
import pickle
from warnings import simplefilter
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.svm import SVC


def main():
    # ignore all future warnings
    simplefilter(action='ignore', category=FutureWarning)
    simplefilter(action='ignore', category=DeprecationWarning)

    #Columnas del dataset
    colnames = ['perimetro', 'profundidad', 'anchura', 'clase']

    #Cargamos el dataset
    data_piernas = pd.read_csv('piernasDataset.csv', names=colnames)

    # Separamos las características de la etiqueta que nos dices a la clase que corresponde
    X = data_piernas.drop('clase', axis=1)
    y = data_piernas['clase']

    # Dividimos el dataset en train y test de forma aleatoria
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=25)

    # Entrenamos el modelo con el algoritmo SVM utilizando diferentes kernels
    # Ejemplo de una sola división de datos (sin validación cruzada)
    print("-------------------- Clasificación con kernel Lineal --------------------")
    svcLineal = SVC(kernel='linear')
    svcLineal.fit(X_train, y_train)

    # Con el clasificador obtenido hacemos la predicción sobre el conjunto de test incial
    y_pred = svcLineal.predict(X_test)
    acc_test = accuracy_score(y_test, y_pred)

    print("Acc_test Lineal: (TP+TN)/(T+P)  %0.4f" % acc_test)
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    print(confusion_matrix(y_test, y_pred))
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred, zero_division=1))

    # Evaluamos de nuevo el kernel lineal con validación cruzada (más riguroso)
    svcLineal2 = SVC(kernel='linear')
    scores = cross_val_score(svcLineal2, X, y, cv=5)

    # exactitud media con intervalo de confianza del 95%
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))

    print("-------------------- Clasificación con kernel POLINOMICO --------------------")
    grado=3
    print("Grado = ", grado)

    svcPol = SVC(kernel='poly', degree=grado)
    svcPol.fit(X_train, y_train)
    y_pred = svcPol.predict(X_test)
    acc_test = accuracy_score(y_test, y_pred)
    print("Acc_test Polinomico: (TP+TN)/(T+P)  %0.4f" % acc_test)
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division=1))

    print("Validación cruzada")
    svcPol2 = SVC(kernel='poly', degree=grado)
    scores = cross_val_score(svcPol2, X, y, cv=5)
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))

    print("-------------------- Clasificación con kernel Radial C=1 y gamma=auto --------------------")
    svcRBF = SVC(kernel='rbf', gamma='auto')
    svcRBF.fit(X_train, y_train)

    y_pred = svcRBF.predict(X_test)
    acc_test = accuracy_score(y_test, y_pred)
    print("Acc_test RBF: (TP+TN)/(T+P)  %0.4f" % acc_test)
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division=1))

    print("Validación cruzada")
    svcRBF2 = SVC(kernel='rbf', gamma='auto')
    scores = cross_val_score(svcRBF2, X, y, cv=5)
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))

    print("-------------------- Búsqueda de parámetros para kernel Gausiano 'rbf' --------------------")
    param_grid = {'C': [1, 10, 100, 1000],
                  'gamma': [0.001, 0.005, 0.01, 0.1, 1, 10, 100]}

    clf = GridSearchCV(SVC(kernel='rbf', class_weight="balanced"), param_grid)
    clf = clf.fit(X_train, y_train)

    print("Mejor estimador encontrado")
    print(clf.best_estimator_)

    mejorSVC = clf.best_estimator_
    y_pred = mejorSVC.predict(X_test)
    acc_test = accuracy_score(y_test, y_pred)
    print("Acc_test_best: (TP+TN)/(T+P)  %0.4f" % acc_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred, zero_division=1))

    print("Validación cruzada")
    svcRBF2 = SVC(kernel='rbf', C=1000, gamma=100)
    scores = cross_val_score(svcRBF2, X, y, cv=5)
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))

    print("------ Salvamos el mejor clasificador en disco ------")

    # Guardamos el clasificador
    with open("clasificador.pkl", "wb") as archivo:
        pickle.dump(mejorSVC, archivo)