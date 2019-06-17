# LINSPECTOR

LINSPECTOR (Language Inspector) is a multilingual inspector to analyze word embeddings in a web based application. Our goal is to provide researchers with an easily accessible tool to gain quick insights into their word embeddings especially outside of the English language. To do this we employ simple classification tasks called probing tasks for a diverse set of languages.

[linspector.ukp.informatik.tu-darmstadt.de](https://linspector.ukp.informatik.tu-darmstadt.de)

## Overview

- `inspector/` is a Django application structured similar to the official documentation.
- `inspector/nn/` contains an AllenNLP based evaluation suite.

## Installation

LINSPECTOR is hosted at [linspector.ukp.informatik.tu-darmstadt.de](https://linspector.ukp.informatik.tu-darmstadt.de) but you can also run a local copy.

1. Clone this repository.

        git clone https://github.com/maexe/linspector-server.git

2. Create a virtual environment using __Python 3.6.x__.

        pip install virtualenv
        cd linspector-server/
        # As of Python 3.7.3 there is a bug using Eventlet with pathlib
        virtualenv linspectorenv -p python3.6
        source linspectorenv/bin/activate

3. Install requirements.

        pip install -r requirements.txt

4. Run migrations and load fixtures.

        ./manage.py migrate
        ./manage.py loaddata languages probing_tasks

5. Download [Bootstrap](https://getbootstrap.com) (4.3) Sass files to `inspector/static/inspector/bootstrap/scss/`.

6. Compile Sass file.

        npm install sass postcss-cli autoprefixer
        sass --no-source-map inspector/static/inspector/scss/custom.scss inspector/static/inspector/custom.css
        npx postcss inspector/static/inspector/custom.css --use autoprefixer --replace

7. Install a Celery supported broker, we use [RabbitMQ](https://www.rabbitmq.com) with Eventlet as an execution pool.

8. Add training data to `media/intrinsic_data/` (see _Intrinsic Data_ below).

9. Start the server (activate virtualenv for Celery and Django).

        rabbitmq-server
        celery -A linspector worker -l info -P eventlet
        ./manage.py runserver

10. Open [localhost:8000](http://localhost:8000) in your browser.

### Notes

When using Celery without Eventlet as an execution pool there can be issues running AllenNLP.

In a production environment you might encounter performance and / or stability issues using SQLite. We recommend using PostgreSQL.

## Probing Tasks

Probing tasks are simple classification tasks aiming to gain insights into information encoded inside embeddings. Our work focuses on word embeddings but should be extendable to other embedding types.

See [Conneau et al. (2018)](https://arxiv.org/abs/1805.01070), or [Şahin et al. (2019)](https://arxiv.org/abs/1903.09442) to learn more.

### Intrinsic Data

For training data each line consists of a token and a label separated by whitespace e.g. `Klammeraffe	Noun`.

We are using intrinsic data provided by [Şahin et al. (2019)](https://github.com/UKPLab/linspector) with a modified folder structure:

- Probing tasks are title cased without spaces
- Use ISO 639-1 codes for languages
- Folder names have to match database entries except for the spaces
- `media/intrinsic_data/CaseMarking/de/ > train.txt, dev.txt, test.txt`

Additionally we renamed some task to be more descriptive:

- _Case_ to _Case Marking_
- _Tag Count_ to _Morphological Feature Count_
- _Odd Feat_ to _Odd Morphological Feature_
- _Pseudo_ to _Pseudoword_
- _Same Feat_ to _Shared Morphological Feature_
- _Character Bin_ to _Word Length_

Also we deleted _Character Count_. It was replaced by _Word Length_.

We have attached our fixtures under `inspector/fixtures/`.

### Contrastive Tasks

Odd Feature and Shared Feature are contrastive tasks trying to predict a single odd or shared feature between two tokens.

For training data each line consists of two tokens and a label all separated by whitespace e.g. `ruckelte	getoastet	Tense`.

A boolean flag `contrastive` has to be set in the database for each contrastive task.

## Commands

There is a command-line script `experiment` to probe static embeddings files which is designed to work with the intrinsic evaluation of [Şahin et al. (2019)](https://github.com/UKPLab/linspector).

To probe a single embeddings file per language run:

    # Folders structured like media/experiment/ar/embeddings.vec
    ./manage.py experiment ar hy cs fr hu

To probe different embedding types run:

    # Folders structured like media/experiment/ar/fasttext/embeddings.vec
    ./manage.py experiment ar hy cs fr hu --types bpe fasttext w2v

To probe different embedding dimensions run:

    # media/experiment/ar/fasttext/100/embeddings.vec
    ./manage.py experiment ar hy cs fr hu --types bpe fasttext w2v --dims 50 100 200 300

The metrics will be written to a CSV file for each language e.g. `media/experiment/ar.csv`.

Run `./manage.py help experiment` for additional arguments.
