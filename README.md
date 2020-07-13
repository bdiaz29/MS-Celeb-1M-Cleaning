# MS-Celeb-1M-Cleaning
Project to clean MS-Celeb-1M dataset
clean list from https://github.com/EB-Dodo/C-MS-Celeb is taken and cleaned ever further 
Face embeddings are pre exracted using Keras implentation of Facenet from https://github.com/nyoki-mtl/keras-facenet . 
These embeddings are then stored in a sql database and are used to train a model.
This new model is then used to compare groups within each identity. Ten random samples are taken from each identity and compared with the entire group 
if the average of the ten samples is less than threshold then the entire group is labeled 'unknown'. After this is done a new model is trained from this cleaned data
and used to repeat the process. 
