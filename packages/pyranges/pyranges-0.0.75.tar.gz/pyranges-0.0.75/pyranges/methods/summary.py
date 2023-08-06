from collections import OrderedDict

import pandas as pd

from tabulate import tabulate


def _summary(self):

    lengths = OrderedDict()
    lengths["pyrange"] = self.lengths(as_dict=True)

    if self.stranded:
        c = self.merge(strand=True)
        lengths["coverage_stranded"] = c.lengths(as_dict=True)

    c = self.merge(strand=False)
    lengths["coverage_unstranded"] = c.lengths(as_dict=True)

    summaries = OrderedDict()

    for summary, d in lengths.items():
        summaries[summary] = pd.concat(d.values()).describe()

    summary = pd.concat(summaries.values(), axis=1)
    summary.columns = list(summaries)

    str_repr = tabulate(summary, headers=summary.columns, tablefmt='psql')
    print(str_repr)
