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
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_14 (Conv2D)           (None, 232, 128, 128)     1280      
_________________________________________________________________
average_pooling2d_2 (Average (None, 116, 64, 128)      0         
_________________________________________________________________
dropout_11 (Dropout)         (None, 116, 64, 128)      0         
_________________________________________________________________
conv2d_15 (Conv2D)           (None, 116, 64, 64)       73792     
_________________________________________________________________
average_pooling2d_3 (Average (None, 58, 32, 64)        0         
_________________________________________________________________
dropout_12 (Dropout)         (None, 58, 32, 64)        0         
_________________________________________________________________
flatten_4 (Flatten)          (None, 118784)            0         
_________________________________________________________________
dense_14 (Dense)             (None, 1)                 118785    
=================================================================
Total params: 193,857
Trainable params: 193,857
Non-trainable params: 0
_________________________________________________________________
```

- LSTM MODEL STRUCTURE
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
lstm_4 (LSTM)                (15, 232, 128)            131584    
_________________________________________________________________
lstm_5 (LSTM)                (15, 64)                  49408     
_________________________________________________________________
dense_10 (Dense)             (15, 100)                 6500      
_________________________________________________________________
dense_11 (Dense)             (15, 1)                   101       
=================================================================
Total params: 187,593
Trainable params: 187,593
Non-trainable params: 0
_________________________________________________________________
```

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
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d_18 (Conv2D)           (None, 232, 128, 128)     1280      
_________________________________________________________________
average_pooling2d_6 (Average (None, 116, 64, 128)      0         
_________________________________________________________________
dropout_15 (Dropout)         (None, 116, 64, 128)      0         
_________________________________________________________________
conv2d_19 (Conv2D)           (None, 116, 64, 64)       73792     
_________________________________________________________________
average_pooling2d_7 (Average (None, 58, 32, 64)        0         
_________________________________________________________________
dropout_16 (Dropout)         (None, 58, 32, 64)        0         
_________________________________________________________________
flatten_6 (Flatten)          (None, 118784)            0         
_________________________________________________________________
dense_16 (Dense)             (None, 4)                 475140    
=================================================================
Total params: 550,212
Trainable params: 550,212
Non-trainable params: 0
_________________________________________________________________
```

- LSTM MODEL STRUCTURE
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
lstm_6 (LSTM)                (1, 232, 128)             131584    
_________________________________________________________________
lstm_7 (LSTM)                (1, 64)                   49408     
_________________________________________________________________
dense_17 (Dense)             (1, 100)                  6500      
_________________________________________________________________
dense_18 (Dense)             (1, 4)                    404       
=================================================================
Total params: 187,896
Trainable params: 187,896
Non-trainable params: 0
_________________________________________________________________
```

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
The proposed way of preprocessing multi-feature time series data, while it seems to yield good results, do come with some inherent flaws.

Given that the correlation of columns is determined by a greedy algorithm that only looks at the available data,
the order of features that determine the image's vertical sequence does not adapt with the new incoming data.

This is especially a problem because this could lead to model overfitting due to its columns arrangement advantage during training.

Therefore, this pipeline with the preprocessing included makes it very easy for overfitting problems to arise,
so until the problem with rigid column orders is fixed, this model is not quite useful.

## Next Steps
if images can be dynamically generated based on the correlation incorporating new incoming data, the problem of overfitting may be solved.

However, another problem would arise: the model, whose weights have been trained to expect a certain column order, would produce outlandish results if the column order was changed.

Perhaps the best way of approaching this problem of overfitting would be to completely re-train the model for every interval of time with a new column order that incorporates ALL data, old and new. This would allow the column order to take into account new data while not ruining the input structure of the model.

Or if re-training at set intervals is too resource intensive, you could determine the column order manually through logic. For example, if one column was "rain per day" and another was "seeable distance", you could conclude that these columns would be somewhat correlated given that rain could shorten your seeable distance. This allows the user to be confident in the column order and should allow the machine to essentially get a "head start" of sorts in prediction.

However, please do take all of this with a grain of salt. As you can see from section Classification Results, there was a major difference in accuracy and loss for the training and evaluating results of the CNN classification model. Even with the test data taken into account for when determining the column order, the model still overfitted badly.
