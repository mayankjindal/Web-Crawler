from bs4 import BeautifulSoup
import requests
import Tokenizing
import pickle

max_pages = 15
outdegree = dict()
indegree = dict()

frontier = set()
visited = set()
vtemp, ftemp = set(), set()
c = Tokenizing.tokenizing()
try:
    f1 = open('frontier.txt', 'r')
    f2 = open('visited.txt', 'r')
    for line in f1:
        frontier.add(line.rstrip())
        ftemp.add(line.rstrip())

    for line in f2:
        vtemp.add(line.rstrip())
except:
    f2 = open('visited.txt', 'a')
    f1 = open('frontier.txt', 'a')


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
                    if link not in vtemp and link not in visited:
                        frontier.add(link)


            except:
                print(href, url)
    except:
        print("could not open, ", url)


'''
url1 = 'https://www.google.co.in/search?q='
url3 = '&start='
url2 = input("Enter search: ")
i = 1
n = int(input("Enter the number of pages to be searched: "))

while(i<=n):
    url = str(url1 + url2 + url3 + str(i))
    gather_links(url)
    i += 1

gather_links("https://www.tutorialspoint.com")
'''

print("\nFrontier list\n")
page = 0
while len(frontier) != 0 and page < max_pages:
    url = frontier.pop()
    c.create_tokens(url)
    gather_links(url)
    page += 1

print(page)


f1.close()
f2.close()
f1 = open('frontier.txt', 'a')
f2 = open('visited.txt', 'a')

for i in frontier:
    if i not in ftemp:
        f1.write(i)
        f1.write("\n")

for i in visited:
    if i not in vtemp:
        f2.write(i)
        f2.write("\n")

f1.close()
f2.close()

print("\nVisited list: ")
for i in range(0, len(visited)):
    print(visited.pop())


c.save_matrix()

f = open("tokens.txt", 'r')
tokens = list()
for line in f:
    tokens.append(line.rstrip())


ratio = {}
outd = list(outdegree.keys())
ind = list(indegree.keys())

print("\n\n")
for i in ind:
    try:
        ratio[len(indegree[i])/len(outdegree[i])] = i
    except:
        pass

for key in sorted(ratio.keys()):
    print(key, ": ", ratio[key])


'''
print("\nOutdegrees\n")
for i in outdegree.keys():
    print(i, ": ", len(outdegree[i]))

print("\nIndegrees\n")
for i in indegree.keys():
    print(i, ": ", len(indegree[i]))
'''

f5 = open('outdegree.pkl', 'bw')
pickle.dump(outdegree, f5)
f6 = open('indegree.pkl', 'bw')
pickle.dump(indegree, f6)

f5.close()
f6.close()
