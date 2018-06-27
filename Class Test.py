from bs4 import BeautifulSoup
import requests
import pickle

max_pages = 10
outdegree = dict()
indegree = dict()

visited, vtemp = set(), set()
try:

    f2 = open('visited.txt', 'r')
    for line in f2:
        vtemp.add(line.rstrip())
except:

    f2 = open('visited.txt', 'a')


try:
    f5 = open('outdegree.pkl', 'rb')
    f6 = open('indegree.pkl', 'rb')
    f5.seek(0)
    f6.seek(0)
    outdegree = pickle.load(f5)
    f5.close()
    indegree = pickle.load(f6)
    f6.close()
except:
    pass


def gather_links(url):
    print("Extracting links for: ", url)
    try:

        u = requests.get(url)
        visited.add(url)
        b = BeautifulSoup(u.text, 'lxml')
        temp = 0
        k = 0
        base_url = ''
        while temp <= 2 and k < len(url):
            if url[k] == '/':
                temp += 1
            base_url = base_url + url[k]
            k += 1

        for l in b.findAll('a'):
            href = l.get('href')
            flag = 0
            link = ''
            try:
                if 'http://' not in href and 'www.' not in href:
                    link = base_url + href
                elif href[0:4] != 'http':
                    for j in range(0, len(href)):
                        if href[j] == '&':
                            break
                        if flag == 1:
                            link = link + href[j]
                        if href[j] == '=':
                            flag = 1

                if 'http' in link and 'webcache' not in link:
                    if url not in outdegree.keys():
                        outdegree[url] = [link]
                        if link not in indegree.keys():
                            indegree[link] = [url]
                        else:
                            indegree[link].append(url)
                    else:
                        outdegree[url].append(link)
                        if link not in indegree.keys():
                            indegree[link] = [url]
                        else:
                            indegree[link].append(url)



            except:
                print(href, url)
    except:
        print("could not open, ", url)

print("\nFrontier list\n")
page = 0
while len(vtemp) != 0 and page < max_pages:
    url = vtemp.pop()
    gather_links(url)
    page += 1

print(page)

f2.close()
f2 = open('visited.txt', 'a')

for i in visited:
    if i not in vtemp:
        f2.write(i)
        f2.write("\n")

f2.close()

print("\nVisited list: ")
for i in range(0, len(visited)):
    print(visited.pop())


ratio = {}
outd = list(outdegree.keys())
ind = list(indegree.keys())

for i in ind:
    try:
        ratio[len(indegree[i])/len(outdegree[i])] = i
    except:
        pass

for key in sorted(ratio.keys()):
    print(key, ": ", ratio[key])


#print("\nOutdegrees\n")
#for i in outdegree.keys():
#    print(i, ": ", len(outdegree[i]))

#print("\nIndegrees\n")
#for i in indegree.keys():
 #   print(i, ": ", len(indegree[i]))


f5 = open('outdegree.pkl', 'bw')
pickle.dump(outdegree, f5)
f6 = open('indegree.pkl', 'bw')
pickle.dump(indegree, f6)

f5.close()
f6.close()

