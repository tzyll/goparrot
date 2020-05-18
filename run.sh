#!/bin/bash
# Copyright 2020 Tsinghua University (Author: Zhiyuan Tang)
# Apache 2.0

. ./path.sh

stage=1
# num of jobs
nj=2

data=data/test
# split the data for parallel jobs
sdata=$data/split$nj

# models trained with kaldi
lang=data/lang
mdl_dir=exp/nnet3/tdnn
mdl=$mdl_dir/final.mdl

if [ $stage -le 1 ]; then
  # Get feats with same config as training ASR.
  # data has kaldi-style structure, including at least
  # wav.scp, text, utt2spk and spk2utt (utt2spk and spk2utt can be fake,
  # i.e., just wav-id to wav-id).
  steps/make_fbank.sh --nj $nj $data || exit 1;
  steps/compute_cmvn_stats.sh $data || exit 1;
  utils/fix_data_dir.sh $data
  rm -rf $sdata
  split_data.sh $data $nj
fi

if [ $stage -le 2 ]; then
  # Get state level posterior, log(p(s|o_t)) for all states.
  run.pl JOB=1:$nj $data/log/posterior.JOB.log \
    nnet3-compute --use-gpu=no \
      $mdl scp:$sdata/JOB/feats.scp ark:$data/posterior.JOB.ark || exit 1;

  # Get state level likelihood, log(p(s|o_t))-log(p(s)) for all states.
  run.pl JOB=1:$nj $data/log/likelihood.JOB.log \
    nnet3-compute --use-gpu=no --use-priors=true \
      $mdl scp:$sdata/JOB/feats.scp ark:$data/likelihood.JOB.ark || exit 1;
fi

if [ $stage -le 3 ]; then
  # Get pdf and phone level force-aligment.
  steps/nnet3/align.sh --use-gpu false --nj $nj --beam 200 --retry-beam 400 \
    --scale-opts '--transition-scale=1.0 --acoustic-scale=1.0 --self-loop-scale=1.0' \
    $data $lang $mdl_dir $data/force_align || exit 1;

  for i in `seq $nj`; do
    gunzip -c $data/force_align/ali.${i}.gz | \
      ali-to-pdf $mdl ark:- ark:$data/pdfali.${i}.ark || exit 1;
    gunzip -c $data/force_align/ali.${i}.gz | \
      ali-to-phones --per-frame $mdl ark:- ark:$data/phoneali.${i}.ark || exit 1;
  done
fi

if [ $stage -le 4 ]; then
  # compute gop scores posterior, likelihood, likelihood ratio.
  for i in `seq $nj`; do
    # don't consider sil phones whose ids <= 15
    (
      python3 local/compute_gop.py $data/posterior.${i}.ark $data/likelihood.${i}.ark \
                                   $data/pdfali.${i}.ark $data/phoneali.${i}.ark \
                                   15 $data/gop_frame.${i}  $data/gop_phone.${i} \
                                   $data/gop_score.${i} || exit 1;
    ) &
  done
  wait;
  cat $data/gop_frame.* > $data/gop_frame
  cat $data/gop_phone.* > $data/gop_phone
  cat $data/gop_score.* > $data/gop_score
  echo "Done GOP scoring based on posterior, likelihood, likelihood ratio."
  echo "See frame-level $data/gop_frame"
  echo "See phone-level $data/gop_phone"
  echo "See utt-level $data/gop_score"
  python3 local/compute_score_corr.py $data/gop_score $data/human_score
fi

exit 0
