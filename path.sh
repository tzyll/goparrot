export KALDI_ROOT=kaldi
[ ! -f $KALDI_ROOT/src/featbin/compute-fbank-feats ] && echo "Please install kaldi in the dir, or give a softlink 'kaldi' to the dir." && exit 1

[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh
export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh
export LC_ALL=C
