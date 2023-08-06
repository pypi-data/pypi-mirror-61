# TronaldDump API Wrapper

[Tronalddump.io](https://www.tronalddump.io/) is a free API and web archive for the dumbest things Donald Trump has ever said ...

You might want to check out the [documentation](https://docs.tronalddump.io/) for the API before working with it.

## Description

The package consists of two main modules:
- `api`: tools for accessing the API.
- `parse`: tools for parsing retieved data.

## Installation

Ensure you have Python 3 and the package manager `pip` installed.

Install using pip:
```console
$ pip3 install tronalddumpy
```

or, you can build the latest version from source:
```console
$ git clone https://github.com/Gushka/tronalddump-python.git
$ cd tronalddump-python/
$ python3 setup.py install
```

## Basic usage

Import the main modules and create a client:

```python
from tronalddump import api, parse

client = api.TronaldDumpAPI()
```
Now to access any API method we will use this client.

For example, let us get a random quote:

```python
>>> resp = client.random_quote()
>>> resp
<TronaldDumpResponse: 'https://www.tronalddump.io/random/quote'>
# Get the response data:
>>> resp.data
{JSON}
# Get the URL:
>>> resp.url
'https://www.tronalddump.io/random/quote'
```

## Parsing the JSON data

Using the TronaldDump module you also can get specific values from the API response just as easy.

Create a Parser using the JSON file-object we obtained earlier:

```python
>>> parsed = parse.Parser(resp)
```
Now we can extract all kinds of data from the JSON based on what the initial response type was.

```python
# Retrieve value of a quote:
>>> parsed.value()
"Money was never a big motivation for me, except as a way to keep score."
# Retrieve the date it was written online:
>>> parsed.date_appeared()
datetime.date(2014, 9, 14)
```

There's also a function to print into the console formatted JSON response.

__Use it only for the debugging purposes.__

```
>>> parsed.printout()
```

## Documentation

### *TronaldDumpAPI* class:

### Tags

#### **all_tags**
Retrieves all existing tags from the API.
```python
TronaldDumpAPI().all_tags()
```
#### **find_tag**
Finds a tag by its value. Given paramaters will be capitalized for the proper search indexing.
```python
TronaldDumpAPI().find_tag(value)
```
### Quotes

#### **random_quote**
Retrieve a random quote from Troland Dump.
```python
TronaldDumpAPI().random_quote()
```

#### **random_meme**
Retrieve a random meme image with a quote Troland Dump.
```python
TronaldDumpAPI().random_meme(output_dir, filename="randommeme.png", force_write=True)
```
- `output_dir`: The directory where to store the image.
- `filename`: The name for the downloaded file. By default it's *randommeme.png*
- `force_write`: Whether to overwrite already existing file or not. By default is set to _True_

#### **search_quote**
Search for a quote by a query or tag. Returns one-page answer. You must pick either `query` or `tag` parameter.
They are interchangeble and only one may be used at a time.

**TO BE IMPROVED:** For now returns only the first page of a search answer.

```python
TronaldDumpAPI().search_quote(query=None, tag=None, page=0)
```
- `query`: The string which will be searched for. 
- `tag`: The tag which will be searched for. 
- `page`: The number of a page that will be returned.

#### **find_quote**
Find a quote by its ID.
```python
TronaldDumpAPI().find_quote(id)
```
- `id`: The ID of a quote you're looking for.

#### **quote_source**
Retrieve the source of a quote by its ID.
```python
TronaldDumpAPI().quote_source(id)
```
- `id`: The ID of a quote source of which you're looking for.

### Author

#### **find_author**
Find an author by their ID.
```python
TronaldDumpAPI().find_author(id)
```
- `id`: The ID of an author you're looking for.


-----

### *TronaldDumpParser* class:

#### **printout**
Prints the contents of given JSON object in the formatted form.
```python
Parser().printout()
```

### Tags

#### **tag_value**
Retrieve all tags values from the given JSON object in a list.
```python
Parser().tag_value()    
```

### Quotes

#### **value**
Retrieve the "value" value of a given JSON object.
```python
Parser().value()
```

#### **author**
Retrieve the "author" value of a given JSON object.
```python
Parser().author()
```

#### **date_appeared**
Retrieve the date when a given quote was written and published.
```python
Parser().date_appeared()
```

#### **tags**
Retrieve all the tags of a given quote
```python
Parser().tags()
```

#### **quote_id**
Retrieve the "quote-id" value from the JSON object
```python
Parser().quote_id()
```
#### **source**
Retrieve the source of a given quote
```python
Parser().source()
```

For full and more detailed information see `help()` on needed classes and functions.
