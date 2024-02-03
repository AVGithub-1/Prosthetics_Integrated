import os
import torch
import numpy as np
from tqdm import tqdm
import import_data
from sklearn.model_selection import train_test_split
import features
from sklearn.model_selection import StratifiedShuffleSplit


NUM_EPOCHS = 20000


class ANN(torch.nn.Module):
    def __init__(self):
        super(ANN, self).__init__()
        self.fc1 = torch.nn.Linear(4+650+650, 50)
        self.fc2 = torch.nn.Linear(50, 40)
        self.fc3 = torch.nn.Linear(40, 36)
        self.fc4 = torch.nn.Linear(36, 7)

    def forward(self, x):
        x = torch.sigmoid(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        x = torch.sigmoid(self.fc4(x))
        return x




def get_data(dataset):
    global X_train
    global X_test
    global y_train
    global y_test
    
    np_data = features.get_features(dataset)

    X = np_data[:, 7:]
    y = np_data[:, 0:7]
    y_class_indices = np.argmax(y, axis=1).astype(np.int64)

    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
    for train_index, test_index in sss.split(X, y_class_indices):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y_class_indices[train_index], y_class_indices[test_index]

    # Ensure no more than 25% representation of class 1 in the test set
    class_1_indices = np.where(y_test == 1)[0]
    class_1_count = len(class_1_indices)
    max_class_1_count = int(0.25 * len(y_test))

    if class_1_count > max_class_1_count:
        extra_class_1_count = class_1_count - max_class_1_count
        extra_class_1_indices = class_1_indices[:extra_class_1_count]
        
        y_test = np.delete(y_test, extra_class_1_indices)
        X_test = np.delete(X_test, extra_class_1_indices, axis=0)

    X_test_1 = torch.from_numpy(X_test)
    X_test_1 = X_test_1.to(torch.float32)
    
model = ANN()

def compute_class_weights(y, num_classes=7):
    unique_classes, counts = np.unique(y, return_counts=True)
    weights = np.zeros(num_classes)
    
    for cls, count in zip(unique_classes, counts):
        weights[cls] = 1.0 / count

    class_weights = torch.tensor(weights, dtype=torch.float32)
    return class_weights

def main(dataset):
    
    get_data(dataset)
    class_weights = compute_class_weights(y_train)
    criterion = torch.nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

    X_train_torch = torch.from_numpy(X_train)
    X_train_torch = X_train_torch.to(torch.float32) 
    y_train_torch = torch.from_numpy(y_train)
    y_train_torch = y_train_torch.type(torch.long)

    for epoch in tqdm(range(NUM_EPOCHS)):
        y_pred = model(X_train_torch)

        loss = criterion(y_pred, y_train_torch)
        print(f'Epoch {epoch + 1}/{NUM_EPOCHS} | Loss: {loss.item():.4f}')

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    torch.save(model.state_dict(), 'model.pt')

    # Calculate and print training error
    training_accuracy = calculate_accuracy(model, X_train, y_train)
    print(f'Training accuracy: {training_accuracy * 100:.2f}%')
    
    
    
Fin_Model = ANN()
Fin_Model.load_state_dict(torch.load('model.pt'))
Fin_Model.eval()


def run(dataset):
    dataset = torch.from_numpy(dataset).to(torch.float32)  # Add this line to convert numpy array to tensor
    y_pred = Fin_Model(dataset)
    classifications = []

    for i in y_pred:
        m = torch.nn.Softmax(dim=0)
        i_m = m(i.float())
        value_of_largest = torch.max(i_m)
        onehot_output = []
        for x in i_m:
            if x == value_of_largest:
                onehot_output.append(1)
            else:
                onehot_output.append(0)
        onehot_output = np.asarray(onehot_output)
        classifications.append(np.argmax(onehot_output))

    return classifications

def calculate_accuracy(model, X, y_true):
    X_torch = torch.from_numpy(X).to(torch.float32)
    y_pred = model(X_torch)
    y_pred_class = torch.argmax(y_pred, axis=1).numpy()

    accuracy = np.sum(y_true == y_pred_class) / len(y_true)
    return accuracy


if __name__ == '__main__':
    main(import_data.all_data)
    classifications = run(X_test)
    print("True test classes: ", y_test)
    print("Predicted test classes: ", classifications)

    # Calculate and print test accuracy
    test_accuracy = calculate_accuracy(Fin_Model, X_test, y_test)  # Changed from 'model' to 'Fin_Model'
    print(f'Test accuracy: {test_accuracy * 100:.2f}%')
      
