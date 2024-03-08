import pandas as pd

# https://textfx.withgoogle.com/
dataset_info = [
    ('../data/similes.csv', 'A good simile contains a concrete image that illustrates the concept we want to convey without being too obvious. Good similes are unexpected and evocative. Create a simile that illustrates this concept: '),
    ('../data/fuse.csv', 'Give a connection between the following two things, where the connection is novel and unexpected, rather than an unoriginal technicality: '),
    ('../data/pov.csv', 'A "hot take" is a perspective that is novel and thought-provoking. Give a hot take about '),
    ('../data/scene.csv', 'Sensory details are details that appeal to the five senses: vision, hearing, touch, smell, and taste. Sensory details make our writing more interesting and vivid, and the most effective sensory details are ones that are creative yet concrete and evocative. Provide a list of sensory details that evoke this thing: '),
    ('../data/explode.csv', 'A same-sounding phrase is a phrase that sounds like another word or phrase. Here is a same-sounding phrase for the word ')
]

dataset = pd.DataFrame()

# load all task-specific datasets into main dataset
for filename, task_prefix in dataset_info:
    task_ds = pd.read_csv(filename)
    task_ds['instruction'] = task_prefix + task_ds['input'] + '.'

    task_ds = task_ds[['instruction', 'output']]
    dataset = pd.concat([dataset, task_ds])

# turn our data into instruction format for training
instruction_template = "<s>[INST] {} [/INST] "
dataset['prompt'] = dataset['instruction'].apply(lambda x: instruction_template.format(x))

dataset.rename(columns={'output': 'response'}, inplace=True)
dataset['response'] = dataset['response'] + "</s>"
dataset = dataset[['prompt', 'response']]

dataset['text'] = dataset['prompt'] + dataset['response']
dataset.drop(columns=['prompt', 'response'], inplace=True)

dataset = dataset.sample(frac=1, random_state=42)

TRAIN_SPLIT = 0.8
VAL_SPLIT = 0.1
TEST_SPLIT = 0.1

train_size = int(TRAIN_SPLIT * len(dataset))
val_size = int(VAL_SPLIT * len(dataset))

train_df = dataset[:train_size]
val_df = dataset[train_size:train_size + val_size]
test_df = dataset[train_size + val_size:]

train_df.to_csv('../data/dataset_train.csv')
val_df.to_csv('../data/dataset_val.csv')
test_df.to_csv('../data/dataset_test.csv')