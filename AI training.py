import tensorflow as tf
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="",
    database="dataset",
    user="postgres",
    password="1234"
)
query = "SELECT input, output FROM trainingdataset;"
data = pd.read_sql(query, conn)
conn.close()

# Предобработка текстовых данных
max_words = 5000
max_sequence_length = 500

tokenizer_input = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer_output = Tokenizer(num_words=max_words, oov_token="<OOV>")

tokenizer_input.fit_on_texts(data['input'])
tokenizer_output.fit_on_texts(data['output'])

input_sequences = tokenizer_input.texts_to_sequences(data['input'])
padded_input_sequences = pad_sequences(input_sequences, padding='post', maxlen=max_sequence_length)

output_sequences = tokenizer_output.texts_to_sequences(data['output'])
padded_output_sequences = pad_sequences(output_sequences, padding='post', maxlen=max_sequence_length)

# Создание модели нейронной сети
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(max_words, 64, input_length=max_sequence_length),
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(max_words, activation='softmax')) 
])

# Компиляция модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Ранняя остановка для предотвращения переобучения
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

# Обучение модели
model.fit(padded_input_sequences, padded_output_sequences, epochs=5, validation_split=0.2, batch_size=64, callbacks=[early_stopping])

# Сохранение весов модели
model.save_weights('model_weights.h5')

print("Исходный текст:")
input_text = input()

# Преобразование входного текста в последовательность
input_sequence = tokenizer_input.texts_to_sequences([input_text])
padded_input_sequence = pad_sequences(input_sequence, padding='post', maxlen=max_sequence_length)

# Получение предсказания от модели
output_sequence = model.predict(padded_input_sequence)

# Декодирование выходной последовательности
predicted_output = []
for token_probs in output_sequence[0]:
    predicted_word_index = np.argmax(token_probs)
    if predicted_word_index != 0:  # Проверка на нулевой индекс
        predicted_word = tokenizer_output.index_word.get(predicted_word_index, "<OOV>")
        predicted_output.append(predicted_word)

output_text = ' '.join(predicted_output)
print("Переcказанный текст:", output_text)
