FROM ubuntu:18.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip python3-setuptools python3-dev git g++ build-essential cmake pkg-config wget vim

WORKDIR /src/jupyter

# Install all Python packages
RUN pip3 install -U pip setuptools wheel
RUN pip3 install setuptools_rust Cython
RUN pip3 install git+https://github.com/Aearsears/Questgen.ai
RUN pip3 install git+https://github.com/Aearsears/pke
RUN pip3 install -Iv spacy==2.3.0  
RUN python3 -m nltk.downloader popular
RUN python3 -m nltk.downloader brown
RUN python3 -m nltk.downloader universal_tagset
RUN python3 -m nltk.downloader stopwords
RUN python3 -m spacy download en_core_web_sm 

# Download and unpack sense2vec model
RUN wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
RUN tar -xvf  s2v_reddit_2015_md.tar.gz

# Execute main.QGen() for the first time because it downloads packages from somewhere
RUN python3 -c "from Questgen import main; qg = main.QGen()"

# Install Jupyter notebook
RUN pip3 install jupyter

# Download and set `tini` as entrypoint (see https://github.com/krallin/tini for reasons)
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# Execute Jupyter notebook
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"] 