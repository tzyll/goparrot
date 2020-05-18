# Copyright 2020 Tsinghua University (Author: Zhiyuan Tang)
# Apache 2.0

import sys
import kaldi_io
import numpy as np

post_path=sys.argv[1]
like_path=sys.argv[2]
pdfali_path=sys.argv[3]
phoneali_path=sys.argv[4]
sil_id_not_bigger_than=int(sys.argv[5])
frame_score_dest=sys.argv[6]
phone_score_dest=sys.argv[7]
score_dest=sys.argv[8]

# read in
posts={key:mat for key,mat in kaldi_io.read_mat_ark(post_path)}
likes={key:mat for key,mat in kaldi_io.read_mat_ark(like_path)}
pdfalis={key:vec for key,vec in kaldi_io.read_ali_ark(pdfali_path)}
phonealis={key:vec for key,vec in kaldi_io.read_ali_ark(phoneali_path)}

f_f = open(frame_score_dest, 'w')
f_p = open(phone_score_dest, 'w')
f = open(score_dest, 'w')
#f.write('wav_id    gop_posterior    gop_likelihood    gop_likelihood_ratio\n')

for key in pdfalis.keys():
    post = posts[key]
    like = likes[key]
    pdfali = pdfalis[key]
    phoneali = phonealis[key]

    # gop based on log phone posterior
    post_best = list(post[np.arange(len(pdfali)), pdfali])

    post_phones = []
    item = 0.0
    start=-1
    num=0
    for v,k in zip(post_best, phoneali):
        if start != k:
            if start > sil_id_not_bigger_than:
                post_phones.append(item/num)
            item = 0.0
            start = k
            num = 0
        item += v
        num += 1
    if start > sil_id_not_bigger_than:
        post_phones.append(item/num)
    gop_post = sum(post_phones)/len(post_phones)

    # gop based on log phone likelihood
    like_best = list(like[np.arange(len(pdfali)), pdfali])

    like_phones = []
    item = 0.0
    start=-1
    num=0
    for v,k in zip(like_best, phoneali):
        if start != k:
            if start > sil_id_not_bigger_than:
                like_phones.append(item/num)
            item = 0.0
            start = k
            num = 0
        item += v
        num += 1
    if start > sil_id_not_bigger_than:
        like_phones.append(item/num)
    gop_like = sum(like_phones)/len(like_phones)

    # gop based on log phone likelihood ratio
    like_max = list(np.amax(like, axis=1))

    like_max_phones = []
    item = 0.0
    start=-1
    num=0
    for v,k in zip(like_max, phoneali):
        if start != k:
            if start > sil_id_not_bigger_than:
                like_max_phones.append(item/num)
            item = 0.0
            start = k
            num = 0
        item += v
        num += 1
    if start > sil_id_not_bigger_than:
        like_max_phones.append(item/num)
    ratio_phones = np.array(like_phones) - np.array(like_max_phones)
    gop_ratio = ratio_phones.mean()

    # write gop scores
    f_f.write(' '.join((str(key), "\n", str(post_best), "\n",
              str(like_best), "\n", str(like_max), "\n")))
    f_p.write(' '.join((str(key), "\n", str(post_phones), "\n",
              str(like_phones), "\n", str(list(ratio_phones)), "\n")))
    f.write(' '.join((str(key), str(gop_post), str(gop_like), str(gop_ratio), "\n")))

print('Write ' + frame_score_dest + ' for frame-level post_best, like_best and like_max.')
print('Write ' + phone_score_dest + ' for phone-level post_phones, like_phones and ratio_phones.')
print('Write ' + score_dest + ' for utt-level gop_post, gop_like and gop_ratio.')
f_f.close()
f_p.close()
f.close()