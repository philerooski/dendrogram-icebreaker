import dendrogram as dendro
import getdocs
import pandas as pd

def cluster_by_binary(data):
    for c in data.columns:
        to_binary = {}
        result = []
        counter = 0
        for v in data[c]:
            try:
                v = v.lower()
            except:
                pass
            if not v in to_binary:
                to_binary[v] = counter
                result.append(counter)
                counter += 1
            else:
                result.append(to_binary[v])
        data[c] = result
    return data

def no_cli_main(group_number, filepath='.'):
    gson = pd.read_json("groups.json")
    google_id = gson['groups'][group_number-1]['id']
    data = pd.read_csv(getdocs.get_from_docs(google_id), header=0)
    data = dendro.clean_data(data, 'Name')
    names = list(data['Name'])
    binary_cluster = cluster_by_binary(data.drop('Name', axis=1))
    dendro.plot_dendrogram(binary_cluster, labels=names)
    dendro.plt.tight_layout()
    dendro.plt.savefig("%s/activity2_group%s.png" % (filepath, group_number),
            orientation='landscape', format='png')

def main():
    if getdocs.parser:
        getdocs.parser.add_argument("fileId", \
                help="ID of a Google sheet", type=str)
        getdocs.parser.add_argument("--group", \
                help="group number to produce dendrogram for")
        getdocs.flags = getdocs.parser.parse_args()
    no_cli_main(getdocs.flags.fileId, getdocs.flags.group)

if __name__ == "__main__":
    main()
