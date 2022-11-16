import argparse
import argparse

import fonctions as fn
   


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', action='store', dest="inputfile", required=True)
    parser.add_argument('--output', action='store', dest="outputfile", required=True)
    args = parser.parse_args()

    video_id = fn.json_to_dataframe(args.inputfile)

    dict = {}
    for i in range(len(video_id['videos_id'])):
        id =  video_id.loc[i,"videos_id"]
        r = fn.get_data_video(id)  
        dict[i] = r
        r = 0
    
    fn.dict_to_json(args.outputfile, dict)



    print(fn.get_page("JhWZWXvN_yo"))




    ######



main()