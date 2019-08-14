import gepia
import os
import sys

# func
def data_loader(filePath):
    """
    處理 Yubau format
    1. TCGA-XXX 不要
    2. 只拿 \t 的 line   
       空白 line 不要
    #3. gid 開頭 colunms 不要
    """
    fa = open(filePath)
    content = []
    for line in fa:
        if line.startswith("TCGA"):
            pass 
        else:
            if "\t" in line:
                content.append(line)
            else:
                pass
    return content        
    
    
def data_process(content):
    """
    只找出 TCGA-Project 與 ENSGID 
    line[1] == ENSGID
    line[6] == Project_id
    
    {"BRCA": [GENE1, GENE2 ...],
     "LUNC": [GENE1, GENE3 ...],
    }
    
    """
    store_map = {}
    
    for line in content:
        item = line.strip().split("\t")
        ENSGID = item[1]
        Project_id = item[6].replace("TCGA-", "")
        if ENSGID != "ENSGID":
            
            if Project_id not in store_map:
                store_map[Project_id] = [ENSGID]
            else:
                store_map[Project_id].append(ENSGID)
        else:
            pass
            
    return store_map
    
def gepia_plot(cancer, gene):
    """
    """
    su = gepia.survival()
    params = su.params
    #gene
    #cancer
    su.setParam('signature', gene)
    su.setParam('dataset', cancer)
    if os.path.isdir("./"+cancer+"/"):
        pass
    else:
        os.makedirs("./"+cancer+"/")
    su.setOutDir("./"+cancer+"/")
    su.query()
    
    
if __name__ == "__main__":
    fileName = sys.argv[1]
    #print(data_loader(fileName))
    content = data_loader(fileName)
    store_map = data_process(content)
    
    #gepia_plot("BRCA" , "CCR7")
    for cancer in store_map:
        #key: cancer
        #value: [gene, ...]
        for gene in store_map[cancer]:
            gepia_plot(cancer, gene)
            
            
            
        
    