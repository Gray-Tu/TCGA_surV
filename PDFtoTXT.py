import os
import sys
import glob
"""
1. 找到某目錄下的所有目錄名與檔案名稱

over1000/BRCA/
        /BLCA/GENE_survivial_XXXX.pdf
             / ....
               ...
        ....

2. 將 pdf 轉出 text 內容

pdftotext [PDF file path] [output file path]

3. 擷取 PDF_txt 欄位並存成 tsv檔案

Cancer \t Gene \t HR 值 \t p 值 ....等等

4. 將 store 內容存放至 txt 檔


"""

path = sys.argv[1]
# Aim 01 找到所有 pdf 檔案路徑
pdf_list = glob.glob(path+"/*/*.pdf")

# Aim 02 轉換 pdf to text

for pdf in pdf_list:
    os.system("pdftotext "+pdf+" "+pdf.replace(".pdf", ".txt"))
    print("Finilshed", pdf)

# Aim 03 txt 內容擷取   
txt_list = glob.glob(path+"/*/*.txt")

store = dict() # key, (cancer, gene)
               # value, {p(HR): 0.01, } 
               
for txt in txt_list:
    #"..\over1000\UCEC\ENSG00000211459_survival_NDMXN.txt"
    #|- path---|\*...\* ----------------------------.txt
    item = txt.split("\\") # 注意 win("\") 與 unix("/") 有所不同
    cancer = item[-2] # CANCER
    gene_filename = item[-1] # txt file name with gene id
    #ENSG00000211459_survival_NDMXN.txt
    gene = gene_filename.split("_")[0] 
    key_tuple = (cancer, gene)
    store[key_tuple] = {} # value is a dictionary
    """
    Logrank p=0.71
    HR(high)=0.95
    p(HR)=0.71
    n(high)=201
    n(low)=201
    """
    #Cancer \t Gene \t HR 值 \t p 值 ....等等
    with open(txt, encoding="UTF-8") as Fa: #== Fa = open(txt); Fa.close()  
        for line in Fa:
            '''
            if "Logrank p" in line:
                ...
            '''
            if "=" in line:
                item = line.strip().split("=")
                sub_key = item[0].strip() # e.g. HR(high)
                sub_val = item[1].strip() # e.g. 0.01
                store[key_tuple][sub_key] = sub_val
 
# Cancer \t Gene \t HR 值 \t p 值 ....等等
# Aim 04 dictionary to txt file in format

order = list(store[list(store.keys())[0]].keys())
#for key in store:
#    value_dict = store[key]
#    order = list(value_dict.keys())

Fw = open("output.txt", "w", encoding="UTF-8")

Fw.write("CANCER\tENSGID\t"+"\t".join(order)+"\n")

for cancer, gene in store:
    value_dict = store[(cancer, gene)]
    Fw.write(cancer+"\t"+gene)
    for sub_key in order:
        sub_value = value_dict[sub_key]
        Fw.write("\t"+sub_value)
    Fw.write("\n")

Fw.close()
 
 
 