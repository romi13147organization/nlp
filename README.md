# NLP - Group 12
## Classifying/Clustering blobs from books

## How to start the project
1. Download Data: https://fiona.uni-hamburg.de/ca89b3cf/blurbgenrecollectionen.zip
2. Unzip the data
3. Create folder "origdata" in the root of the project
4. Copy the unzipped data to the "origdata" folder
5. Make sure you have the required packages installed by running:
`````bash
pip install -r requirements.txt
`````
6. (Optional) If you want to train the DistillBert model yourself the [CUDA-Toolkit](https://developer.nvidia.com/cuda-12-6-0-download-archive) is required in order to utilize the GPU for training.

## Project Structure
The project is divided into 3 main jupyter notebooks
* [data-exploration](./data_exploration.ipynb)
* [data-classification](./data_classification.ipynb)
* [distilBERT](./distllbert-test.ipynb)

### Data Exploration
This [notebook](./data_exploration.ipynb) includes the Exploratory Data Analysis and contains the following topics:
* Basic Statistics
* Exploring the Topics
* Exploring the Blurbs
* SBert & Universal Sentence Encoder Usage to get embeddings
* Clustering Labels -> using KMeans, Agglomerative Clustering 
* Comparing Tokenizers and Stopwords (NLTK vs. Spacy)

### Data Classification
This [notebook](./data_classification.ipynb) contains the following topics:
* Preprocessing Data (Tokenization & StopWord removal)
* Vectorization & Embeddings (TfidfVectorizer & Universal Sentence Encoder & Doc2Vec)
* Using the models (TfidfVectorizer & Universal Sentence Encoder & Doc2Vec)
* Evaluating model performance (classification report + confusion matrix)

### DistillBERT
This [distilBERT](./distllbert-test.ipynb) contains the following topics:
* Tokenization (DistilBertTokenizerFast)
* Setup of Train-Environment (GPU-Usage)
* Training the model (distilbert-base-uncased)
* Evaluating the model (classification report + confusion matrix)
* Test trained model on example blurb