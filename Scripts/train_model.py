import csv
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

with open('sequences.csv', 'r') as f:
    reader = csv.reader(f)
    sequences = list(reader)

loss_tracker = []
best_model = {}

class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 0
        self.curr_lowest_loss = 9999999

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        if loss < self.curr_lowest_loss:
            self.curr_lowest_loss = loss
            print(f"New Lowest Loss: #{loss}")
            best_model[0] = model
            
        # print("Epoch #{} end".format(self.epoch))
        loss_tracker.append(loss)
        model.running_training_loss = 0.0
        self.epoch += 1


    
def run(min_count, epoch_count):
    epoch_logger = EpochLogger()
    
    # model = Word2Vec.load("test_training.model")
    # model.train(corpus_iterable=sequences, epochs=epoch_count,callbacks=[epoch_logger], compute_loss= True, total_examples=model.corpus_count)
    model = Word2Vec(sentences=sequences,     # This is the data that we wish to create notes on. This will take all unique words (stations) and put them in the NN
                    vector_size=100,          # Amount of dimension
                    min_count=min_count,      # If the number of occurences of this station is less than 10, then we are not interested in having it in our embedding. -- THIS NEED TO BE LOOKED AT
                    workers=4,                # Amount of cores used for training and so forth.
                    compute_loss=True,        # Used for logging
                    callbacks=[epoch_logger], # Used for logging
                    alpha=0.05,               # Learning rate. Default is 0.025, but due to the relatively low epochs, a higher lr were decided to give a quicker lowest loss-model
                    window=1,                 # Due to our sequences only being of length two, when using skip-gram, out window only consists of either the next or the prev entry (as there isn't any other elements in the sequence)
                    sg=1,                     # Skip-gram. WHY DO WE CHOOSE THIS OVER CBoW? 
                    batch_words=5000,         # Batching training together for more effeciency
                    epochs=epoch_count
                    )                       

    
    # model.build_vocab(sequences)
    # epochs = epoch_count
    
    # model.train(sequences, total_examples=model.corpus_count, epochs=epoch_count, callbacks=[epoch_logger], compute_loss=True)
    # # for i in range(training_iterations):
    #     loss = model.get_latest_training_loss()
    #     print(f"After {i} iterations with {epochs} epochs the loss is: {loss}")
        
    return model

def main():
    min_count                 = int(input())
    epoch_count               = int(input())

    model = run(min_count, epoch_count)
    best_model[0].save("best_model_100_dim_5e.model")
    model.save("last_model_100_dim_5e.model")
    with open('loss_tracker_4_100_dim.txt', 'w') as f:
        for item in loss_tracker:
            f.write(str(item) + '\n')


main()