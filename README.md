# GoParrot
GoParrot is a simple tool that computes GOP (Goodness of Pronunciation) scores based on [kaldi](https://github.com/kaldi-asr/kaldi) for oral reading assessment.

Name it parrot as parrot repeats what you say (鹦鹉学舌).

Three kinds of gops can be computed, based on posterior, likelihood and likelihood ratio separately.

- Posterior

  After force-alignment, the log posterior of each phone is the average log posterior of all frames belong to that phone. The GOP score is the average log posterior of all phones. See eq.(7) in this [paper](https://www.isca-speech.org/archive/archive_papers/interspeech_2013/i13_1886.pdf).

- Likelihood

  After force-alignment, the log likelihood of each phone is the average log likelihood of all frames belong to that phone. The GOP score is the average log likelihood of all phones. See eq.(18) in this [paper](https://www.isca-speech.org/archive/Interspeech_2018/pdfs/2138.pdf).

- Likelihood ratio

  After force-alignment, the likelihood of each frame can be scaled by dividing the max likelihood of each frame, then the log likelihood ratio of each phone is the average log likelihood ratio of all frames belong to that phone. The GOP score is the average log likelihood ratio of all phones. See eq.(16) involving eq.(18) and (19) in this [paper](https://www.isca-speech.org/archive/Interspeech_2018/pdfs/2138.pdf).


## How to use it
A Kaldi ASR trained with WSJ dataset is provided, and two samples are given.

```
git clone https://github.com/tzyll/goparrot.git
cd goparrot

# compile kaldi in the dir, or give a softlink 'kaldi' to the dir
# you may just uncomment the following lines to clone a kaldi
# then follow its instruction to install
# git submodule init
# git submodule update

pip3 install kaldi_io

./run.sh
```

## How to test other data
Just prepare test data with kaldi style as in `data/test` which includes at least
wav.scp, text, utt2spk and spk2utt (utt2spk and spk2utt can be fake, i.e., just wav-id to wav-id).

## How to test other ASR or language
Train ASR system with Kaldi with your own dataset, and replace `data/lang` and `exp/nnet3/tdnn` with your own.


## Performance
We scored hundreds of utterances from [ERJ](https://www.gavo.t.u-tokyo.ac.jp/~mine/paper/PDF/2004/ICA_p557-560_t2004-4.pdf), and the Pearson correlation coefficient (PCC) between human scores and the three types of GOP scores were 0.6249, 0.6334 and 0.6361 separately. The PCC between human scores were about 0.57.

The given ASR model was trained with cross-entropy loss.
We also scored with Kaldi Chain (LF-MMI) model, and the PCC between human scores and the three types of GOP scores were 0.1615, 0.1615 (chain model has no prior, so likelihood is actually posterior) and 0.0934 separately.
