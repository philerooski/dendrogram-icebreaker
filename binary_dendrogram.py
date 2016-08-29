import dendrogram as dendro
import getdocs
import pandas as pd

def cluster_by_binary(data):
    to_binary = {}
    for c in data.columns:
        result = []
        counter = 0
        for v in data[c]:
            try:
                v = v[0]
                v = v.lower()
            except:
                pass
            if v == 'y':
                result.append(1)
            elif v == 'n':
                result.append(0)
            elif v == 1 or v == 0:
                result.append(v)
            elif not v in to_binary:
                if len(to_binary.keys()) < 2 and not pd.isnull(v):
                    to_binary[v] = counter
                    result.append(counter)
                    counter += 1
                else:
                    result.append(0.5)
            else:
                result.append(to_binary[v])
        data[c] = result
        to_binary = {}
    return data

def no_cli_main(group_number, filepath='.'):
    gson = pd.read_json("groups.json")
    group_number = int(group_number)
    google_id = gson['groups'][group_number]['id']
    data = pd.read_csv(getdocs.get_from_docs(google_id), header=0)
    data = dendro.clean_data(data, 'Name')
    names = list(data['Name'])
    binary_cluster = cluster_by_binary(data.drop('Name', axis=1))
    dendro.matplotlib.rcParams['lines.linewidth'] = 3
    dendro.plot_dendrogram(binary_cluster, labels=names)
    dendro.plt.xlim(0, 8)
    dendro.plt.tight_layout()
    dendro.plt.savefig("%s/activity2_group%s.png" % (filepath, group_number),
            orientation='landscape', format='png')
    dendro.plt.clf()

def main():
    if getdocs.parser:
        getdocs.parser.add_argument("--group", \
                help="group number to produce dendrogram for")
        getdocs.flags = getdocs.parser.parse_args()
    no_cli_main(getdocs.flags.group)

if __name__ == "__main__":
    main()
