# News Cluster Algorithm

#### This project accepts news from crawlers and then process news using cluster service. The results are similar news in given range, ranking from highest to lowest. It serves as the solution to find the hot news in given period. 

#### The main part of the cluster algorith uses tf-idf to get key words, and second clustering after that. 

#### This project is accomplished using python and mongoDB.

---
##### Project layout(Incomplete)
 
 * API
     * article.py -> for receiving news from crawlers
     * cluster.py -> for posting clutersing results 
 * Common -> some utils
     * algorithm.py -> the main function for clustering
 * Model 
     * article.py -> define raw article data structure, indexed by url.
     * cluster.py -> define raw article data structure, indexed by topic.url.
 * Service
     * cluster.py -> saving data into database
 * Tests
