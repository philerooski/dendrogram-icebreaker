import pandas as pd
import getdocs
import binary_dendrogram as bd

BINARY_COLS = ['Researcher: Clinical [y(es) or n(o)]', 'Researcher: Basic [y(es) or n(o)]', 'Researcher: Translational [y(es) or n(o)]', 'Topic: Tumor microenvironment and immune-interactions [y(es) or n(o)]', 'Topic: Tumor migration and metastasis [y(es) or n(o)]', 'Topic: Genomics and gene regulation [y(es) or n(o)]', 'Topic: Drug resistance and combination therapy [y(es) or n(o)]', 'Topic: Signaling networks [y(es) or n(o)]', 'Data: Single cell studies [y(es) or n(o)]', 'Data: Genomics [y(es) or n(o)]', 'Data: Imaging [y(es) or n(o)]', 'Data: Proteomics [y(es) or n(o)]', 'Data: Therapeutics [y(es) or n(o)]', 'Personal: Cat vs Dog [c(at) or d(og)]', 'Personal: Beach vacation vs. Mountain vacation [b(each) or m(ountain)]', 'Personal: Superman vs Batman [s(uperman) or b(atman)]']
COLS = ["Name", "GroupNumber"] + BINARY_COLS[:-3]

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

def draw_metrics(data):
    research_series = pd.Series([
        sum(filter(lambda x : x != 0.5, data['Researcher: Clinical [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Researcher: Basic [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Researcher: Translational [y(es) or n(o)]']))
        ],
            index=['Clinical', 'Basic', 'Translational'],
            name='Research')
    research_series.plot.bar(figsize=(6, 6), colormap='Accent')
    bd.dendro.plt.title(research_series.name)
    bd.dendro.plt.axhline(0, color='k')
    bd.dendro.plt.tight_layout()
    bd.dendro.plt.savefig("research.png", orientation='landscape',
            format='png')
    bd.dendro.plt.clf()
    topic_series = pd.Series([
        sum(filter(lambda x : x != 0.5, data['Topic: Tumor microenvironment and immune-interactions [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Topic: Tumor migration and metastasis [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Topic: Genomics and gene regulation [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Topic: Drug resistance and combination therapy [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Topic: Signaling networks [y(es) or n(o)]'])),
        ],
            index=['T. microenv. & immune-interactions',
                'T. migration & metastasis', 'Genomics & gene regulation',
                'Drug resist. & comb. therapy', 'Signaling networks'],
            name='Topics')
    topic_series.plot.bar(figsize=(6, 6), colormap='Paired')
    bd.dendro.plt.title(topic_series.name)
    bd.dendro.plt.axhline(0, color='k')
    bd.dendro.plt.tight_layout()
    bd.dendro.plt.savefig("topics.png", orientation='landscape', format='png')
    bd.dendro.plt.clf()
    data_series = pd.Series([
        sum(filter(lambda x : x != 0.5, data['Data: Single cell studies [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Data: Genomics [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Data: Imaging [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Data: Proteomics [y(es) or n(o)]'])),
        sum(filter(lambda x : x != 0.5, data['Data: Therapeutics [y(es) or n(o)]'])),
        ],
            index=['Single cell studies', 'Genomics', 'Imaging',
            'Proteomics', 'Therapeutis'],
            name='Data')
    data_series.plot.bar(figsize=(6, 6), colormap='Dark2')
    bd.dendro.plt.title(data_series.name)
    bd.dendro.plt.axhline(0, color='k')
    bd.dendro.plt.tight_layout()
    bd.dendro.plt.savefig("data.png", orientation='landscape', format='png')
    bd.dendro.plt.clf()

def main():
    gson = pd.read_json("groups.json")
    data = agglomerate_groups(gson['groups'])
    data = asterisk_poster_names(data)
    binary_cluster = bd.cluster_by_binary(
            data.drop(["Name", "GroupNumber"], axis=1))
    draw_metrics(binary_cluster)
    bd.dendro.matplotlib.rcParams['lines.linewidth'] = 0.2
    bd.dendro.plot_dendrogram(binary_cluster, labels=list(data['Name']),
            orientation='left', leaf_font_size=2)
    bd.dendro.plt.tight_layout()
    bd.dendro.plt.savefig("omnigram.png", orientation='landscape',
            format='png', dpi=400)
    bd.dendro.plt.clf()

if __name__ == "__main__":
    main()
