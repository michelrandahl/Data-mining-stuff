"""
Converts strings to ascii vectors and compares/scores by density.
There are likely better ways to find string outliers, this is just a toy example for finding outliers.
It would probably be interesting to use some of this sample on a real dataset converted to vectors.
"""
from math import sqrt

class link_object:
    def __init__(self,link):
        self.link = link
        self.vector = [ord(c) for c in link]
        self.k_nearest = None

    def distance(self, other):
        vec1 = self.vector
        vec2 = other.vector
        #append the vector which is smallest with zeros
        if len(vec1) > len(vec2):
            vec2 = vec2 + [0]*(len(vec1)-len(vec2))
        else:
            vec1 = vec1 + [0]*(len(vec2)-len(vec1))
        return sqrt(sum([(vec1[i] - vec2[i])**2 for i in range(len(vec1))]))

    def getKNearest(self, k, link_objects):
        if self.k_nearest is None: 
            distances = []
            for obj in link_objects:
                if obj.link == self.link: continue
                distances.append( (self.distance(obj),obj) )
            distances.sort(key = lambda x: x[0])
            self.k_nearest = distances[:k]
        return self.k_nearest

    def density(self, link_objects, k):
        k_nearest = self.getKNearest(k, link_objects)
        return (sum([x for x,_ in k_nearest])/k)**-1

    def avg_relative_density(self, link_objects,k):
        k_nearest = self.getKNearest(k, link_objects)
        return self.density(link_objects, k)/sum([x.density(link_objects, k)/k
                                             for _,x in k_nearest])

    def __str__(self):
        return self.link


# k indicates how many neighbors the algorithm should take into account
# please mess around with it to see the effect
K = 7

links = [
    'https://www.youtube.com/watch?v=OnkCww2ZeVs',
    'https://www.youtube.com/watch?v=5zn8MRKOskw',
    'https://www.youtube.com/watch?v=L777RhL_Fz4',
    'https://www.youtube.com/watch?v=wjmFm8PIz8M',
    'https://www.youtube.com/watch?v=miVmn-JLS1A',
    'https://www.youtube.com/watch?v=J0phq7litTc',
    'https://www.youtube.com/watch?v=JgALlSPlZC8',
    'https://www.youtube.com/watch?v=oRzLcAaihI0',
    'https://www.youtube.com/maybeImAnOutlier',
    'TheresNoDoubtThatImAnOutlierCompared2Others']

link_objects = []
for link in links:
    link_objects.append(link_object(link))

for x in link_objects:
    print x
    print x.avg_relative_density(link_objects, K)
