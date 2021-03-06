# -*- coding: utf-8 -*-
import os
import numpy as np
#Afegim les llibreries de scikit, sklearn.metrics per poder fer tots els càlculs
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt

def plot_confusion_matrix(cm, true_labels,normalize = False,title='Confusion Matrix', cmap=plt.cm.Blues):
    # Normalize matrix rows to sum 1
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        title = 'Normalized ' + title
    plt.imshow(cm, interpolation='nearest',cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(true_labels))
    plt.xticks(tick_marks, true_labels, rotation=90)
    plt.yticks(tick_marks, true_labels)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
    plt.show()


def evaluate_classification(automatic_classification, ground_truth, val_or_test):
    automatic_annotation = open(automatic_classification+'/classification_'+val_or_test+'.txt','r') #obrim el fitxer generat per la funció classify
    groundtruth_annotation = open(ground_truth, 'r') #obrim el fitxer d'annotacio donat
    automatic = []
    id_automatic = []
    next(automatic_annotation) #Saltem la primera linia del fitxer
    for line in automatic_annotation:
        inicio = line.index("\t")
        final = line.index("\n")
        id_automatic.append(line[0:inicio])
        automatic.append(line[inicio+1:final]) #Afegim les categories a cada entrada de l'array
    next(groundtruth_annotation) #Saltem la primera linia del fitxer
    ground_truth = range(0, len(id_automatic))
    for l in groundtruth_annotation:
        id_annot = l[0:l.index("\t")]
        clase_annot = l[l.index("\t")+1:l.index("\n")]
        for i in range(0, len(id_automatic)):
            if id_automatic[i] == id_annot:
               ground_truth[i] = clase_annot

    # CALCULEM LA MATRIU DE CONFUSIO:
    cm = confusion_matrix(ground_truth,automatic)
    labe = np.unique(ground_truth) #ens treu el llistat de les categories en el ground_truth (una categoria només una vegada).
    # CALCULEM L'ACCURACY
    accuracy = accuracy_score(ground_truth,automatic)
    # CALCULEM LA PRECISSION
    precision = precision_score(ground_truth,automatic,average='macro')
    # CALCULEM EL RECALL
    recall = recall_score(ground_truth,automatic,average='macro')
    # CALCULEM EL F1
    f1 = f1_score(ground_truth,automatic,average='macro')
    return cm,labe,accuracy,precision,recall,f1


cm,labe,accuracy,precision,recall,f1 = evaluate_classification('../files','../TerrassaBuildings900/val/annotation.txt',"val")
# CALCULEM LA MATRIU DE CONFUSIO:
print("MATRIU DE CONFUSIO:")
plt.figure(1)
plot_confusion_matrix(cm,labe,normalize=False)
plt.figure(2)
plot_confusion_matrix(cm,labe,normalize=True)
print("\n")

# CALCULEM L'ACCURACY
print("ACCURACY:")
print accuracy
print("\n")

# CALCULEM LA PRECISSION
print("PRECISSION:")
print precision
print("\n")

# CALCULEM EL RECALL
print("RECALL:")
print recall
print("\n")

# CALCULEM EL F1
print("F1:")
print f1
print("\n")