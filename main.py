from datetime import datetime
import time

user_name = input("Input WhatsApp username: ")
                  
                  
def formatTime(t):
    hr = t.split(':')[0]
    min = t.split(':')[1]
    if int(hr) >= 12:
        return "{}:{}PM".format(hr, min)
    else:
        return "{}:{}AM".format(hr, min)


def getDay(date_stamp):
    d = date_stamp.split(',')[0].strip()
    #t = date_stamp.split(',')[1].strip()
    str_stamp = d +" "+ "00:00:00"
    #print(str_stamp, type(str_stamp))
    try:
        epoch_value = datetime.strptime(str_stamp.lstrip('â€Ž['), '%d/%m/%Y %H:%M:%S')
        return time.mktime(time.strptime(str(epoch_value), '%Y-%m-%d %H:%M:%S'))
    except ValueError:
        pass


def readDate(date_time_str):
    d = date_time_str.split(',')[0].lstrip('[')
    t = date_time_str.split(',')[1].strip()
    str_stamp = d +" "+ t
    #print(str_stamp, type(str_stamp))
    epoch_value = datetime.strptime(str_stamp, '%d/%m/%Y %H:%M:%S')
    e = time.mktime(time.strptime(str(epoch_value), '%Y-%m-%d %H:%M:%S'))
    return time.strftime("%A, %d %b %Y", time.localtime(e))
    

# file name should be exactly '_chat.txt'
with open ('_chat.txt', 'r', encoding='utf-8') as file:
    content = file.readlines()
    content.remove(content[0]) #deleting the encryption notification line
    content.remove(content[1])

    dates = []
    #obtaining the dates to use in displaying days of chats
    for l in range(len(content)):
        date_time_stamp = content[l].split(']') [0]
        day = date_time_stamp.split(',')[0].lstrip('[')
        dates.append(date_time_stamp.lstrip('['))
 
    # open file to write WhatsApp encryption notification
    with open ('chat.html', 'a', encoding='utf-8') as output:
        output.write("\t\t<span class='enc'>Messages to this chat and calls are now secured with end-to-end encryption. No one outside of this chat, not even WhatsApp, can read or listen to them.</span>\n")
        output.write("\t\t<div class='date'> <b>{}</b> </div>\n\t\t<div class='clear'></div>\n".format(readDate(dates[0])))
        print("\t\t", dates[0].split(',')[0])

    new_day = dates[0]#.split(',')[0]
    for i in range(len(content)):
        date_time = content[i].split(']') [0] # date substring eg [25/04/2019, 19:37:33

        # open file to write the date of chat conversation
        with open ('chat.html', 'a', encoding='utf-8') as output:
            try:
                #print("comparing {} to {}".format(getDay(dates[i]), getDay(new_day)))
                if getDay(dates[i]) > getDay(new_day):
                    print("\t\t", i, dates[i].split(',')[0])
                    try:
                        output.write("\t\t<div class='date'> <b>{}</b> </div>\n\t<div class='clear'></div>\n".format(readDate(dates[i])))
                        new_day = dates[i]
                    except ValueError:
                        pass
                else:
                    pass
            except (IndexError, TypeError):
                print("Error comparing dates")
                pass
                    
        try:
            sender_and_msg = content[i].split(']') [1] # the rest of the line - this caters to overwrapping texts

            sender = str(sender_and_msg.split(':') [0]) # retrieve sender name from the rest of the line

            # check the first sender and proceed
            if user_name in sender_and_msg and sender_and_msg.find(user_name) == 1: 
                my_text = sender_and_msg.split(':') [1] # obtain message by sender
                print("\t\t\t\t", sender)
                print("\t\t\t\t", my_text)

                # open file to write the message by this sender in a chat bubble
                with open ('chat.html', 'a', encoding='utf-8') as output:

                    if "?<attached" in my_text or "<attached" in my_text: # check if message text has an attachment and format appropriately
                        attachment = sender_and_msg.split(":") [2].strip()
                        image = attachment.rstrip('\n')
                        img = image.rstrip(">")
                        output.write("\t\t<div class='me-img'> <img src= 'F:\\Documents\\scripts\\purge - WhatsApp\\img\\{}' alt='file omitted' width={} style='float:right'> </div>\n".format(img, len(sender_and_msg)*2))
                    else:
                        # the text has no attachment escaping characters
                        output.write("\t\t<div class='me bubble bubble-alt green' style='width: {}'>\n \t\t\t{}\n \t\t\t<span class='time'> {} </span>\n\t\t</div>\n".format(len(my_text), my_text, formatTime(date_time.split(',')[1])))

                    output.write("\t\t<div class='clear'></div>\n")

            # check the second sender and proceed
            else:
                your_text = sender_and_msg.split(':') [1]
                print(sender)
                print(your_text)

                # open file to write the message of the other sender in a chat bubble
                with open ('chat.html', 'a', encoding='utf-8') as output:
                    
                    if "?<attached" in your_text or "<attached" in your_text: # check if message text has an attachment and format appropriately
                        attachment = sender_and_msg.split(":") [2].strip()
                        image = attachment.rstrip('\n')
                        img = image.rstrip(">")
                        output.write("\t\t<div class='you-img'> <img src= 'F:\\Documents\\scripts\\purge - WhatsApp\\img\\{}' alt='file omitted' width={}> </div>\n".format(img, len(sender_and_msg)*2))
                    else:
                        # the text has no attachment escaping characters
                        output.write("\t\t<div class='you bubble' style='width: {}'>\n \t\t\t{}\n \t\t\t<span class='time'>{}</span>\n\t\t</div>\n".format(len(your_text), your_text, formatTime(date_time.split(',')[1])))

                    output.write("\t\t<div class='clear'></div>\n")

        except IndexError: # caters to text overlapping to new line
            my_text = content[i]
            print("\t\t\t\t", content[i])
            with open ('chat.html', 'a', encoding='utf-8') as output:
                output.write("\t\t<div class='me bubble bubble-alt green' style='width: {}'> {} </div>\n".format(len(my_text), my_text))

 
with open ('chat.html', 'a', encoding='utf-8') as output:
    output.write('\t</div>\n</body>\n</html>')
       
# final output will be in a chat.html file in the same directory as this file
