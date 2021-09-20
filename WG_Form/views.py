import collections
import copy
import itertools
import math

from .forms import FileForm
from django.shortcuts import render


def tf(string):
    tf_text = collections.Counter(string)
    for i in tf_text:
        tf_text[i] = tf_text[i] / float(len(string))
    return dict(tf_text)


def idf(documents):
    length = len(documents)
    td = collections.Counter()
    for d in documents:
        td[d] += 1
    idf_text = []
    for (term, term_frequency) in td.items():
        term_idf = math.log(float(length) / term_frequency)
        idf_text.append((term, term_idf))
    idf_text.sort(reverse=True)
    return dict(idf_text)


def items_to_dict(dict_in: dict, dict_out: dict):
    for key, value in dict_in.items():
        dict_out.setdefault(key, []).append(value)


def delete_values_0(dictionary):
    for i in dictionary.values():
        i.remove(i[0])
    return dictionary


def delete_values_1(dictionary):
    for i in dictionary.values():
        i.remove(i[1])
    return dictionary


def file_processing(request):
    context = {}
    if request.POST:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"].read().decode('utf-8', 'replace').split()
            file_without_symbol = [''.join(filter(str.isalnum, i)) for i in file]
            file_without_numbers = [i for i in file_without_symbol if not i.isdigit()]
            ready_file = list(filter(str.strip, file_without_numbers))
            tf_idf = {}
            items_to_dict(tf(ready_file), tf_idf)
            items_to_dict(idf(ready_file), tf_idf)
            tf_idf_ready = {i: tf_idf[i] for i in sorted(tf_idf, key=tf_idf.get, reverse=False)}
            tf_idf_50 = {k: tf_idf_ready[k] for k in list(tf_idf_ready.keys())[-50:]}
            idf_copy = delete_values_0(copy.deepcopy(tf_idf_50))
            tf_ready = delete_values_1(tf_idf_50)
            idf_copy = {i: str(j[0]) for i, j in idf_copy.items()}
            tf_ready = {i: str(j[0]) for i, j in tf_ready.items()}
            context['tf'] = tf_ready
            context['idf'] = idf_copy
            return render(request, "ready_file.html", context)
    else:
        form = FileForm()
    context['form'] = form
    return render(request, "form.html", context)
