# import tensorflow as tf
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# 加载MNIST数据集
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# 对数据进行预处理
train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255
np.random.shuffle(train_images)
train_images = torch.tensor(train_images.reshape((1875, 32, 1, 28, 28)))
plt.figure(figsize=(10, 5))
plt.imshow(train_images[0, 2].reshape(28, 28), cmap='gray')
plt.axis('off')
plt.show()

# test_images = test_images.reshape((10000, 28, 28, 1))
# test_images = test_images.astype('float32') / 255

# # 将标签进行分类编码
# train_labels = tf.keras.utils.to_categorical(train_labels, 10)
# test_labels = tf.keras.utils.to_categorical(test_labels, 10)
print(train_images.shape)
print(train_images[0].shape)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 4, 3, 1)
        self.conv2 = nn.Conv2d(4, 8, 3, 1)
        self.bn1 = nn.BatchNorm2d(32)
        self.fc0 = nn.Linear(1152, 128)
        self.fc1 = nn.Linear(128, 16)
        self.fc2 = nn.Linear(16, 256)
        self.fc3 = nn.Linear(256, 28 * 28)

    # x represents our data
    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)

        x = torch.flatten(x, start_dim=1)
        x = self.fc0(x)
        x = F.relu(x)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        # Apply softmax to x
        output = F.sigmoid(x.resize(x.shape[0], 1, 28, 28))
        return output


net = Net()
criterion = nn.MSELoss(size_average=None, reduce=None, reduction='mean')
optimizer = torch.optim.Adam(net.parameters(), lr=0.001)

for epoch in range(5):  # 5个epochs

    running_loss = 0.0
    for i, data in enumerate(train_images):
        inputs = data
        optimizer.zero_grad()
        outputs = net(inputs)
        loss = criterion(outputs, inputs)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if i % 100 == 99:  # 每100个小批次打印一次平均损失
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 100))
            running_loss = 0.0

print('Finished Training')

plt.imshow(net(train_images[0, 2].reshape(1, 1, 28, 28,)).detach().numpy().reshape(28, 28), cmap='gray')
plt.axis('off')
plt.show()
