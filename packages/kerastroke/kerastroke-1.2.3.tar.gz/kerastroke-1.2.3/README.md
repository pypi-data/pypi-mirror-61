# Stroke
Stroke implements the concepts of weight pruning and re-initialization. The goal of the Stroke callback is to re-initialize weights that have begun to contribute to overfitting, or weights that are effectively 0.

Keep in mind that using Stroke on larger models may introduce significant slowdown while training.

Parameters of the callback are:

* `stroke` - Implements weight re-initialization, will randomly re-initialize a percentage of weights between the weight bounds. (default_value = True)
* `minweight` - the minimum value of the random weights to be generated. (default value = -.05)
* `maxweight` - the maximum value of the random weights to be generated. (default value = .05)
* `volatility_ratio` - the percentage of weights you would like to re-initialize. (default value = .05)
*  `decay` - volatility_ratio will be multiplied by decay at the end of every epoch, after weights have been stricken. (default value = None)
* `index` - the index of a layer within the model that you'd like to randomize the weights of. This will prevent randomization of all other layers. (default value = None)
* `verbose` - Prints the model/layer name and the percentage of weights that were randomized. (default value = False)
* `pruning` - Implements weight pruning, will set weights between the pruning bounds to 0. (default value = True)
* `pruningmin` - Lower bound for weight pruning. This usually shouldn't be altered. (default value = 0.0)
* `pruningmax` - Upper bound for weight pruning. (default value = .02)

An implementation of the Stroke callback on an MNIST classification model can be seen below:

```python
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from kerastroke import Stroke

model = Sequential()

model.add(Conv2D(32, 3, 3, input_shape = (28,28, 1), activation = 'relu'))
model.add(MaxPool2D(pool_size = (2,2)))

model.add(Conv2D(32,3,3, activation = 'relu'))
model.add(MaxPool2D(pool_size = (2,2)))

model.add(Flatten())

model.add(Dense(output_dim = 128, init = 'uniform', activation = 'relu'))

model.add(Dense(10, init = 'uniform', activation = 'sigmoid'))

model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=64,
                    epochs=1,
                    steps_per_epoch=5,
                    verbose=0,
                    callbacks=[Stroke()])
