from __future__ import division
from geopy.geocoders import Nominatim
from scipy.cluster.hierarchy import dendrogram, linkage
import pandas as pd
from matplotlib import rcParams
import matplotlib.pyplot as plt
import getdocs

def get_from_localhost(path):
    data = pd.read_csv(path, header=0)
    return data

def cluster_by_first_letter(data):
    '''
    Does dendrogram actually give distance between first letters?
    '''
    names = data['Full Name (First Last)']
    first_letters = [ord(n.split()[0][0]) for n in names]
    df = pd.DataFrame(columns = ['Letter', 'Dummy'], index = names)
    i = 0
    for index, r in df.iterrows():
        df.loc[index] = [first_letters[i], 0]
        i += 1
    return df

def cluster_by_city_distance(data):
    df = pd.DataFrame({'City':list(data['City']),
        'Province':list(data['State/Province/Region (Non US/Canada)']),
        'Latitude':[0]*len(data), 'Longitude':[0]*len(data)},
        index=data['Full Name (First Last)'])
    geolocator = Nominatim()
    lats = []
    longs = []
    locations = {}
    for i, r in df.iterrows():
        location_name = ' '.join([r['City'], r['Province']])
        try:
            if locations.has_key(location_name):
                lats.append(locations[location_name]['latitude'])
                longs.append(locations[location_name]['longitude'])
            else:
                location = geolocator.geocode(location_name)
                lats.append(location.latitude)
                longs.append(location.longitude)
                locations[location_name] = {'longitude': location.longitude,
                        'latitude': location.latitude}
        except Exception:
            df = df.drop(i)
    df['Latitude'] = lats
    df['Longitude'] = longs
    df = df.drop(labels=["City", "Province"], axis=1)
    return df

def cluster_by_jaccard(data):
    names = data['Full Name (First Last)']
    first_names = [n.split()[0] for n in names]
    df = pd.DataFrame(columns=first_names, index=names)
    i = 0
    for c in df.columns:
        result = []
        for n in df.columns:
            result.append(jaccard(c, n))
        df[c] = result
    return df

def plot_dendrogram(df, **kwargs):
    dendro = linkage(df)
    labels = kwargs.get('labels', None)
    ylabel = kwargs.get("ylabel", 'Names')
    orientation = kwargs.get('orientation', 'left')
    plt.ylabel(ylabel)
    dendrogram(dendro, orientation=orientation, labels=labels)
    plt.plot()

def jaccard(n1, n2):
    n1 = set(map(ord, n1.lower()))
    n2 = set(map(ord, n2.lower()))
    return 1 - (len(n1.intersection(n2)) / len(n1.union(n2)))

def clean_data(data, colname):
    results = []
    for n in list(data[colname]):
        try:
            split_name = n.split()
            fixed_name = ' '.join(list(map(lambda s : s.title(), split_name)))
            results.append(fixed_name)
        except:
            results.append(n)
    data[colname] = results
    return data

def draw_full_plot(df_a, df_b, df_c, group_num):
    rcParams['lines.linewidth'] = 2
    plt.figure(1)
    #ax1 = plt.subplot(311)
    #ax1.set_title("Mystery Plot A (Group %s)" % group_num)
    plot_dendrogram(df_a, labels=df_a.index)
    plt.tight_layout()
    plt.savefig("activity1_figa_group%s.png" % group_num, orientation='landscape',
            format='png')
    plt.clf()
    #ax2 = plt.subplot(312)
    #ax2.set_title("Mystery Plot B (Group %s)" % group_num)
    plot_dendrogram(df_b, labels=df_b.index)
    plt.savefig("activity1_figb_group%s.png" % group_num, orientation='landscape',
            format='png')
    plt.clf()
    #ax3 = plt.subplot(313)
    #ax3.set_title("Mystery Plot C (Group %s)" % group_num)
    plot_dendrogram(df_c, labels=df_c.index)
    plt.savefig("activity1_figc_group%s.png" % group_num, orientation='landscape',
            format='png')
    plt.clf()
    #plt.show()

def no_cli_main(g_id, group_number):
    data = pd.read_csv(getdocs.get_from_docs(g_id), header=0)
    data = clean_data(data, 'Full Name (First Last)')
    if group_number:
        group_number = int(group_number)
        group_data = data[data['Group Number'] == group_number]
        name_cluster = cluster_by_first_letter(group_data)
        distance_cluster = cluster_by_city_distance(group_data)
        jaccard_cluster = cluster_by_jaccard(group_data)
        draw_full_plot(name_cluster, distance_cluster,
                jaccard_cluster, group_number)
    else:
        all_group_numbers = filter(lambda x : not pd.isnull(x), \
                data['Group Number'])
        smallest_number = int(min(all_group_numbers))
        largest_number = int(max(all_group_numbers))
        for i in range(smallest_number, largest_number + 1):
            group_data = data[data['Group Number'] == i]
            name_cluster = cluster_by_first_letter(group_data)
            distance_cluster = cluster_by_city_distance(group_data)
            jaccard_cluster = cluster_by_jaccard(group_data)
            draw_full_plot(name_cluster, distance_cluster, jaccard_cluster, i)

def main():
    if getdocs.parser:
        getdocs.parser.add_argument("fileId", \
                help="ID of a Google sheet", type=str)
        getdocs.parser.add_argument("--group",
                help="Group to generate dendrogram for")
        getdocs.flags = getdocs.parser.parse_args()
    no_cli_main(getdocs.flags.fileId, getdocs.flags.group)

if __name__ == "__main__":
    main()
