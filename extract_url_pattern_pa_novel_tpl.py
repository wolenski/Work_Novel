# methods for json format data
import json
import os
import sys

#########################################################################
# extract URL_PATTERN field from pa xpath template file of json format ##
#########################################################################
def extract_url_pattern_pa(file_name):
    # list for pattern
    pattern_list = []
    siteapp_id = [1,376409]  

    #read in url pattern
    file_to_read = open(file_name, 'r')
    count = 0
    for line in file_to_read:
        if len(line) == 0:
            break
        else:
            try:
                count += 1
                s = json.loads(line)
                url_pattern = s["TARGET"]["URL_PATTERN"]
                # remove siteapp_id
                for s_id in siteapp_id:
                    idx = url_pattern.find(str(s_id) + "#")
                    if idx != -1:
                        url_pattern = url_pattern[idx+len(str(s_id))+1:]
                        break
                # append the pattern
                pattern_list.append(url_pattern)
            except Exception, e:
                print "json parsing error!"
                print count
                sys.exit(0)
                break
    file_to_read.close() 
    

    #output the pattern into a file
    out_fname = file_name + ".tpl_pattern.out"
    file_to_write = open(out_fname,"w")
    pattern_list.sort()
    for pat in pattern_list:
        file_to_write.write(str(pat) + "\n")             
    file_to_write.close()

#############################################################################
# extract PATTERN field from a tckernel xpath template file of json format ##
#############################################################################
def extract_url_pattern_tc(file_name):
    # list for pattern
    pattern_list = []

    #read in url pattern
    file_to_read = open(file_name, 'r')
    count = 0
    for line in file_to_read:
        if len(line) == 0:
            break
        idx = line.find("PATTERN")
        if idx == -1:
            continue
        else:            
            count += 1
            # remove PATTERN
            pat = line[idx+7:]
            # remove white space
            url_pattern = pat.strip()            
            # append the pattern
            pattern_list.append(url_pattern)          
    file_to_read.close()     

    #output the url patterns into a file
    out_fname = file_name + ".tpl_pattern.out"
    file_to_write = open(out_fname,"w")
    pattern_list.sort()
    for pat in pattern_list:
        file_to_write.write(str(pat) + "\n")             
    file_to_write.close()

#########################################################################
# extract SAMPLE URL field from pa xpath template file of json format ##
#########################################################################
def extract_novel_cover_sample_url(file_name):
    # dictionary for {generator : url} mapping

    #output the urls into different files based on theis generators
    out_fname = file_name + ".sample_url.out"
    file_to_write = open(out_fname,"a")

    file_to_read = open(file_name, 'r')

    for line in file_to_read:
        if len(line) == 0:
            break
        else:
            s = json.loads(line)
            host = s["TARGET"]
            tpls = s["TPL"]   
            for tpl in tpls:
                page_type = tpl["PAGE_TYPE"]
                if page_type == "PAGE_TYPE_NOVEL_COVER":
                    url =  tpl["SAMPLE URL"]     
                    host_url = host["URL_PATTERN"][7:]
                    file_to_write.write(str(host_url) + "\t" + str(url) + "\n")
                     

    file_to_read.close() 

    file_to_write.close()
                                                                
if __name__ == '__main__':
    # extract_novel_cover_sample_url("novel.dict")
    extract_url_pattern_pa("novel.dict")
