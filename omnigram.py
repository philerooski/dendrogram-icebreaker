import pandas as pd
import getdocs
import binary_dendrogram as bd

BINARY_COLS = ['Researcher: Clinical', 'Researcher: Basic', 'Researcher: Translational', 'Topic: Tumor microenvironment and immune-interactions', 'Topic: Tumor migration and metastasis', 'Topic: Translational', 'Topic: Genomics and gene regulation', 'Topic: Drug resistance and combination therapy', 'Topic: Signaling networks', 'Data: Single cell studies', 'Data: Genomics', 'Data: Imaging', 'Data: Proteomics', 'Data: Therapeutics', 'Personal: Cat vs Dog', 'Personal: Beach vacation vs. Mountain vacation', 'Personal: Superman vs Batman']
COLS = ["Name", "GroupNumber"] + BINARY_COLS[:-3]
PARTICIPANT_SHEET_ID = "13YaIbVBifEURdT3lZkotSGmGEoi5xZGrXbmLydtpAv8"

def agglomerate_groups(groups):
    data = pd.DataFrame()
    for g in groups:
        group_number = g['number']
        group_id = g['id']
        d = pd.read_csv(getdocs.get_from_docs(group_id), header=0)
        d['GroupNumber'] = [group_number] * len(d)
        data = data.append(d[COLS])
    return data

def asterisk_poster_names(data):
    csbc_data = pd.read_csv("csbcDay.csv", header=0)
    pson_data = pd.read_csv("psonDay.csv", header=0)
    csbc_data = bd.dendro.clean_data(csbc_data, 'Full Name (First Last)')
    pson_data = bd.dendro.clean_data(pson_data, 'Full Name (First Last)')
    poster_people_csbc = csbc_data[csbc_data['Poster Submission check'] == 'Yes']
    poster_people_pson = pson_data[pson_data['Poster Submission check'] == 'Yes']
    poster_names_csbc = list(poster_people_csbc['Full Name (First Last)'])
    poster_names_pson = list(poster_people_pson['Full Name (First Last)'])
    poster_names = poster_names_csbc + poster_names_pson
    data['Name'] = map(lambda n : n + "*" if n in poster_names else n,
            data['Name'])
    return data

def main():
    gson = pd.read_json("groups.json")
    data = agglomerate_groups(gson['groups'])
    data = asterisk_poster_names(data)
    binary_cluster = bd.cluster_by_binary(
            data.drop(["Name", "GroupNumber"], axis=1))
    bd.dendro.plot_dendrogram(binary_cluster, labels=list(data['Name']),
            orientation='left')
    bd.dendro.plt.show()

if __name__ == "__main__":
    main()
