# preptext

Utilities of preparing datasets for deep learning models.
Can easily convert your text-formatted data into a `DataLoader` of `pytorch`.

## Installation

```bash
pip install preptext
```

or build from source code using:

```bash
git clone https://github.com/styxjedi/preptext.git
cd preptext
python setup.py install
```

## Usage

Each dataset consists of many entries, and each entry contains many fields.

This tool is built following the logic above.

For a specific dataset, you just need to follow the steps below.

### 1. Define some fields

Suppose we are working on a translation task that contains two fields, `src` and `trg`, in the dataset.

```python
import preptext
fields = preptext.Fields()
fields.add_field(
    "src", # name
    init_token="<bos>", # bos token
    eos_token="<eos>", # eos token
    # ... ...
)
fields.add_field(
    "trg", # name
    init_token="<bos>", # bos token
    eos_token="<eos>", # eos token
    # ... ...
)
```

You would see more parameters when using.

Basicly, the same field used in different datasets (train, valid, test) would share the same vocab. And vocabs fo different fields are isolated from each other.

### 2. Add each entry to a DataStorage

```python
datastorage = preptext.DataStorage()
for src, trg in dataset:
    entry = preptext.Entry([src, trg], fields)
    datastorage.add_entry(entry)
```

`dataset` here is your own translation dataset.

Or you can collect all entries into a `list`, then convert the list into a DataStorage.

```python
data = []
for src, trg in dataset:
    entry = preptext.Entry([src, trg], fields)
    data.append(entry)
datastorage = preptext.DataStorage(data)
```

### 3. Build Vocabulary

Create a vocab for each field:

```python
fields.src.build_vocab(datastorage.src)
fields.trg.build_vocab(datastorage.trg)
```

Create a shared vocab:

```python
fields.src.build_vocab(
    datastorage.src,
    datastorage.trg
)
fields.trg.vocab = fields.src.vocab
```

Specify pretrained word vectors:

```python
vec = preptext.Vectors('file/path/to/the/word2vec.txt') # need to be txt format
fields.src.build_vocab(datastorage.src, vetors=vec)
fields.trg.build_vocab(datastorage.trg, vectors=vec)
```

**NOTE:** If vectors are specified, this package will cache the vector file into a folder named `.vector_cache` automatically.

Now you're almost ready with your data. The following methods is ready to be used.

```python
# save the prepared data into a binary file
datastorage.dump('data.pkl')
# load from a binary file
datastorage = preptext.DataStorage.load('data.pkl')
# get the i-th data of text format
i = 0
datastorage.get_entry(i)
# get the i-th data of numpy array format
datastorage.get_array(i)
# get vocab matrix
src_matrix = datastorage.fields.src.vocab.vectors
trg_matrix = datastorage.fields.trg.vocab.vectors
# convert into pytorch dataloader
dl = preptext.converter.to_dataloader(
    datastorage,
    bach_size=50,
    shuffle=True,
    num_workers=4
)
# convert into bucketdataloader (minimized padding in each minibatch)
bucketdl = preptext.converter.to_bucketdataloader(
    datastorage,
    key=lambda x: len(x.src),
    batch_size=50,
    shuffle=True,
    num_workers=4
)
# convert into distributed dataloader
distributeddl = preptext.converter.to_distributeddataloader(
    datastorage,
    1, # world_size
    1, # rank
    batch_size=50,
    num_workers=4
)
```

Enjoy!
