import cv2
import numpy as np
from IPython.display import display
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def convert_xyxyxyxy_2_xyxy(points):
    x1,y1=points[0]
    x2,y2=points[2]
    return x1,y1,x2,y2
def inference(ocr,images):
    Results=[]
    for page,image in enumerate(images):
        Flag=False
        pos=None
        text_s=None
        flag_answer=False
        text_p=None
        image=np.array(image)
        h,w=image.shape[:2]
        # print(h,w)
        if page==0:
            image=image[300:h-100,:]
        else:
            image=image[:h-50,:]
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        result = ocr.ocr(image, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                check={"pos":None,"text":None,"page":None,"label":None}
                points=line[0]
                box=list(map(int,convert_xyxyxyxy_2_xyxy(points)))
                check["pos"]=box
                check["text"]=line[1][0]
                check["page"]=page
                if Flag:
                    check["label"]="title"
                    check["text"]=text_s + " " + check["text"]
                    x1,y1,x2,y2=pos
                    x3,y3,x4,y4=check["pos"]
                    check["pos"]=[x1,y1,x2,y4]
                    cv2.putText(image,"Title",(x1-60,y1+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                    cv2.rectangle(image,(x1,y1),(x2,y4),(0,0,255),1)
                    Results.append(check)
                    pos=None
                    Flag=False
                # print("check",check)
                if  "Mark the letter A, B, C, or D".lower() in line[1][0].lower() or "Read the following passage and mark the letter A, B, C" in line[1][0].lower():
                    Flag=True
                    pos=box
                    text_s=line[1][0]
    
                elif "A." in line[1][0] or "B." in line[1][0] or "C." in line[1][0] or "D." in line[1][0] or "A"==line[1][0] or "B"==line[1][0] or "C"==line[1][0] or "D"==line[1][0]:
                    check["label"]="Answer"
                    cv2.putText(image,"Answer",(box[0]-60,box[1]+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                    cv2.rectangle(image,(box[0],box[1]),(box[2],box[3]),(0,0,255),1)
                    Results.append(check)

                else:
                    if "HET" not in line[1][0] and text_s is None:
                        cv2.putText(image,"Content",(box[0]-60,box[1]+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                        cv2.rectangle(image,(box[0],box[1]),(box[2],box[3]),(0,0,255),1)
                        check["label"]="content"
                        Results.append(check)
                    else:
                        text_s=None
    return Results
            
def inference_image(ocr,image):
    Results=[]
    Flag=False
    pos=None
    text_s=None
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    result = ocr.ocr(image, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            check={"pos":None,"text":None,"label":None}
            points=line[0]
            box=list(map(int,convert_xyxyxyxy_2_xyxy(points)))
            check["pos"]=box
            check["text"]=line[1][0]
            if Flag:
                check["label"]="title"
                check["text"]=text_s + " " + check["text"]
                x1,y1,x2,y2=pos
                x3,y3,x4,y4=check["pos"]
                check["pos"]=[x1,y1,x2,y4]
                cv2.putText(image,"Title",(x1-60,y1+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                cv2.rectangle(image,(x1,y1),(x2,y4),(0,0,255),1)
                Results.append(check)
                pos=None
                Flag=False
            # print("check",check)
            if  "Mark the letter A, B, C, or D".lower() in line[1][0].lower() or "Read the following passage and mark the letter A, B, C" in line[1][0].lower():
                Flag=True
                pos=box
                text_s=line[1][0]

            elif "A." in line[1][0] or "B." in line[1][0] or "C." in line[1][0] or "D." in line[1][0] or "A"==line[1][0] or "B"==line[1][0] or "C"==line[1][0] or "D"==line[1][0]:
                check["label"]="Answer"
                cv2.putText(image,"Answer",(box[0]-60,box[1]+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                cv2.rectangle(image,(box[0],box[1]),(box[2],box[3]),(0,0,255),1)
                Results.append(check)

            else:
                if "HET" not in line[1][0] and text_s is None:
                    cv2.putText(image,"Content",(box[0]-60,box[1]+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                    cv2.rectangle(image,(box[0],box[1]),(box[2],box[3]),(0,0,255),1)
                    check["label"]="content"
                    Results.append(check)
                else:
                    text_s=None
    return Results
    


def postprocess(Results:list):
    # Khởi tạo danh sách để chứa nội dung merged
    merged_content_total = []
    merged_check=''
    merge_title=[]
    merged_answer_total = []
    merged_answer_check=''
    count_content=0
    count_answer=0
    # Duyệt qua dữ liệu
    for item in Results:
        label = item['label']
        if label == 'content':
            count_content+=1
            merged_check+=item['text']


        elif label == 'Answer':
            count_answer+=1
            count_content=0
            merged_answer_check+="\n"+item["text"]
            if len(merged_check)>0:
                merged_content_total.append(merged_check)
                merged_check=''
            if merged_answer_check.count("\n")==4:
                    merged_answer_total.append(merged_answer_check)
                    merged_answer_check=''
        elif label =="title":
            count_content=0
            merge_title.append(item["text"])
    if count_answer/4 > len(merged_answer_total):
        merged_answer_total.append(merged_answer_check)
    
    print("*"*20,merged_content_total[-1]) 
    id_save=0
    CHECK=[15,2,2,2,2,2,5,5,8,3,5,5]
    Cluster=[]
    last_index=0
    print("Len answer",len(merged_answer_total))
    print(merge_title)
    for title,size in zip(merge_title,CHECK):
        print(title)
        idx=merge_title.index(title)
        split_list_question = merged_content_total[id_save:size+id_save]
        split_list_answer=merged_answer_total[id_save:size+id_save]
        print("split_list_answer form {} to {}".format(id_save,size+id_save))
        print("split_list_question from {} to {}".format(id_save,size+id_save))
        if last_index<size:
            last_index = size
        else:
            last_index+=size

        id_save=last_index
        passage=''
        for ques,ans in zip(split_list_question,split_list_answer):
            question={"id":None,"title":None,"content":None,"list_answer":None}
            #check idx
            position=ques.find("Question")
            if "Question 50" in ques:
                print("------------------------",ques)
            if position==0:
                index=ques[9:11]
                if is_integer(index):
                    index=int(index)
                    question["id"]=index
                else:
                    print("index",index)
                    index=int(index[0])
                    question["id"]=index
                question["title"]=title
                question["list_answer"]=ans
                question["content"]=passage + "\n" + ques
                print("question: ",question)
                Cluster.append(question)
            elif position>1:
                if len(ques)>250:
                    print("Pos",position)
                    passage=ques[:position]
                    index=ques[position+9:position+11]
                    question["title"]=title
                    question["list_answer"]=ans
                else:
                    
                    question["title"]=title
                    question["list_answer"]=ans
                question["content"]=passage + "\n" + ques[position:]
    
                if is_integer(index):
                    index=int(index)
                    question["id"]=index
                else:
                    print("index",index)
                    index=int(index[0])
                    question["id"]=index
                print("question: ",question)
                Cluster.append(question)
    return Cluster


def postprocess_image(Results: list):
    
    # Khởi tạo danh sách để chứa nội dung merged
    merged_content_total = []
    merged_check=''
    merge_title=[]
    merged_answer_total = []
    merged_answer_check=''
    count_content=0
    count_answer=0
    print("Results-------:",Results)
    # Duyệt qua dữ liệu
    for item in Results:
        label = item['label']
        if label == 'content':
            count_content+=1
            merged_check+=item['text']


        elif label == 'Answer':
            count_content=0
            count_answer+=1
            merged_answer_check+="\n"+item["text"]
            if len(merged_check)>0:
                merged_content_total.append(merged_check)
                merged_check=''
            if merged_answer_check.count("\n")==4:
                merged_answer_total.append(merged_answer_check)
                merged_answer_check=''
        elif label =="title":
            count_content=0
            merge_title.append(item["text"])

    if count_answer/4>len(merged_answer_total):
        print("Đã addd thêm vào !!!!!!")
        merged_answer_total.append(merged_answer_check)
    Cluster=[]
    print("s answers:----------:",merged_answer_total)
    print("s content:-----------------:",merged_content_total)
    for title in merge_title:
        passage=''
        for ques,ans in zip(merged_content_total,merged_answer_total):
            question={"id":None,"title":None,"content":None,"list_answer":None}
            position=ques.find("Question")
            if position==0:
                index=ques[9:11]
                if is_integer(index):
                    index=int(index)
                    question["id"]=index
                else:
                    print("index",index)
                    index=int(index[0])
                    question["id"]=index
                question["title"]=title
                question["list_answer"]=ans
                question["content"]=passage + "\n" + ques
                print("question: ",question)
                Cluster.append(question)
            elif position>1:
                if len(ques)>150:
                    print("Pos",position)
                    passage=ques[:position]
                    index=ques[position+9:position+11]
                    question["title"]=title
                    question["list_answer"]=ans
                else:
                    
                    question["title"]=title
                    question["list_answer"]=ans
                question["content"]=passage + "\n" + ques[position:]
    
                if is_integer(index):
                    index=int(index)
                    question["id"]=index
                else:
                    print("index",index)
                    index=int(index[0])
                    question["id"]=index
                print("question: ",question)
                Cluster.append(question)
    return Cluster
                

        
           
