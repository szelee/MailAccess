import base64
import json

from django.core.files import File
from GoogleMailAccess import settings


def load_file():
    file = open(settings.PROJECT_DIR + '\GoogleMailAccess\email148a7e33fb7a0a07.txt', 'rb')
    email = json.load(file)
    return email


#identify type of message
def identify_email(email):
    count = 0
    if 'CATEGORY_PROMOTIONS' not in email['labelIds']:
        for item in email['payload']:
            if item == 'parts':
                print ("in payload parts")
                if type(email['payload'][item]) == list:
                    print len(email['payload'][item])
                    i = 0
                    while (i < len(email['payload'][item])):
                        print type(email['payload'][item][i])
                        print email['payload'][item][i].keys()
                        print email['payload'][item][i].get('mimeType')
                        i += 1
                        if email['payload'][item][i].get('mimeType') == 'text/html':

                #print email['payload'][item][1]
                #print (email['payload'][item].keys())
                #for i in email['payload'][item]:
                    #print ("Length of the list : ", len(email['payload'][item][i]))
                    #print type(email['payload'][item][i])
                    #print len(email['payload'][item][i])
                #    print email['payload'][item][i]

                #for data in email['payload'][item][1]:
                #    if data == 'body':
                #        print (email['payload'][item][1][data])
                #        data1 = base64.b64decode(email['payload'][item][1][data]['data'])
                #        print data1

def main():
    email = load_file()
    identify_email(email)

main()
