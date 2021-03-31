# covid_tracking_by_state

## Idea
Create an image joining columns by correlation. The idea is that using a CNN would take into account the similarities between data across columns. I imagine it to be the opposite of naive bayes that assumes independence, instead this assumes correlation.

## Steps
- Get data from TSA and covid tracking project 
* TSA: https://www.tsa.gov/coronavirus/passenger-throughput
* COVID Tracking Project: https://covidtracking.com/data

- Format data into time series

- Create the order of columns to assemble the data into images
* Use greedy algorithm to create a non-repeating circle order of columns and then remove the least correlated
* Use 2 pointers on either end, and use greedy algorithm until no columns are left

- Create Correlation Images (2d numpy arrays) from data
* See samples in correlation_images folder visualized with PIL

- Create 2 models for comparison
* CNN - for processing the correlation images
* LSTM - for processing the time series data before formatted into images

- Do Regression with both models (loss: "mse", optimizer: "adam", metrics: ("mse", "mae"))

- Format y into classes

- Do Classification with both models (loss: "categorical_crossentropy", optimizer: "adam", metrics: ("accuracy"))

- Conclusion



## Regression Model Structures
- CNN MODEL STRUCTURE
<div>
_________________________________________________________________<br>
Layer (type)                 Output Shape              Param #   <br>
=================================================================<br>
conv2d_14 (Conv2D)           (None, 232, 128, 128)     1280      <br>
_________________________________________________________________<br>
average_pooling2d_2 (Average (None, 116, 64, 128)      0         <br>
_________________________________________________________________<br>
dropout_11 (Dropout)         (None, 116, 64, 128)      0         <br>
_________________________________________________________________<br>
conv2d_15 (Conv2D)           (None, 116, 64, 64)       73792     <br>
_________________________________________________________________<br>
average_pooling2d_3 (Average (None, 58, 32, 64)        0         <br>
_________________________________________________________________<br>
dropout_12 (Dropout)         (None, 58, 32, 64)        0         <br>
_________________________________________________________________<br>
flatten_4 (Flatten)          (None, 118784)            0         <br>
_________________________________________________________________<br>
dense_14 (Dense)             (None, 1)                 118785    <br>
=================================================================<br>
Total params: 193,857<br>
Trainable params: 193,857<br>
Non-trainable params: 0<br>
_________________________________________________________________<br>
</div>

- LSTM MODEL STRUCTURE
<div>
_________________________________________________________________<br>
Layer (type)                 Output Shape              Param #   <br>
=================================================================<br>
lstm_4 (LSTM)                (15, 232, 128)            131584    <br>
_________________________________________________________________<br>
lstm_5 (LSTM)                (15, 64)                  49408     <br>
_________________________________________________________________<br>
dense_10 (Dense)             (15, 100)                 6500      <br>
_________________________________________________________________<br>
dense_11 (Dense)             (15, 1)                   101       <br>
=================================================================<br>
Total params: 187,593<br>
Trainable params: 187,593<br>
Non-trainable params: 0<br>
_________________________________________________________________<br>
</div>

## Regression Results (Both trained for 100 epochs)
- CNN results
* Training - loss: 21849.6554 - mse: 21849.6554 - mae: 119.5158
* Evaluation - loss: 25719.7148 - mse: 25719.7148 - mae: 127.7793

- LSTM results
* Training - loss: 93886.5595 - mse: 93886.5595 - mae: 223.5190
* Evaluation - loss: 78718.5234 - mse: 78718.5234 - mae: 205.3980

- Thoughts:
* While this result looks promising, the losses are still absurdly high.
* Next step is to turn this into a classification problem and see if the model still holds up.

## Classification Model Structures
- CNN MODEL STRUCTURE
<div>
_________________________________________________________________<br>
Layer (type)                 Output Shape              Param #   <br>
=================================================================<br>
conv2d_16 (Conv2D)           (None, 232, 128, 128)     1280      <br>
_________________________________________________________________<br>
average_pooling2d_4 (Average (None, 116, 64, 128)      0         <br>
_________________________________________________________________<br>
dropout_13 (Dropout)         (None, 116, 64, 128)      0         <br>
_________________________________________________________________<br>
conv2d_17 (Conv2D)           (None, 116, 64, 64)       73792     <br>
_________________________________________________________________<br>
average_pooling2d_5 (Average (None, 58, 32, 64)        0         <br>
_________________________________________________________________<br>
dropout_14 (Dropout)         (None, 58, 32, 64)        0         <br>
_________________________________________________________________<br>
flatten_5 (Flatten)          (None, 118784)            0         <br>
_________________________________________________________________<br>
dense_15 (Dense)             (None, 4)                 475140    <br>
=================================================================<br>
Total params: 550,212<br>
Trainable params: 550,212<br>
Non-trainable params: 0<br>
_________________________________________________________________<br>
</div>

- LSTM MODEL STRUCTURE
<div>
_________________________________________________________________<br>
Layer (type)                 Output Shape              Param #   <br>
=================================================================<br>
lstm_6 (LSTM)                (1, 232, 128)             131584    <br>
_________________________________________________________________<br>
lstm_7 (LSTM)                (1, 64)                   49408     <br>
_________________________________________________________________<br>
dense_17 (Dense)             (1, 100)                  6500      <br>
_________________________________________________________________<br>
dense_18 (Dense)             (1, 4)                    404       <br>
=================================================================<br>
Total params: 187,896<br>
Trainable params: 187,896<br>
Non-trainable params: 0<br>
_________________________________________________________________<br>
</div

## Classification Results (Both trained for 50 epochs with batch size of 1)
- CNN Results
* Training - loss: 0.0646 - accuracy: 0.9913

![image](https://user-images.githubusercontent.com/46566976/113117706-4d291680-9241-11eb-90ed-dab86c0cf214.png)

* Evaluation - loss: 0.8493 - accuracy: 0.8000

- LSTM Results
* Training: loss: 0.2345 - accuracy: 0.9311

![image](https://user-images.githubusercontent.com/46566976/113117729-531ef780-9241-11eb-8f73-35572977e9c1.png)

* Evaluation - loss: 1.2523 - accuracy: 0.6667

## Conclusion
The proposed way of preprocessing multi-feature time series data, while seem to yield good results, do come with some inherent flaws.

Given that the correlation of columns is determined by a greedy algorithm that only looks at the available data,
the order of features that determine the image's vertical sequence does not adapt with the new incoming data.

This is especially a problem because this could lead to model overfitting due to its columns arrangement advantage during training.

Therefore, this pipeline with the preprocessing included makes it very easy for overfitting problems to arise,
so until the problem with rigid column orders is fixed, this model is not quite useful.

So a very possible next step: 
if images can be dynamically generated based on the correlation incorporating new incoming data, the problem of overfitting may be solved.
However, as seen in the notebook, the testing data was included to generate the correlation order of features.
Even then, as shown above, there was a major difference in accuracy and loss for the training and evaluating results of the CNN classification model.
