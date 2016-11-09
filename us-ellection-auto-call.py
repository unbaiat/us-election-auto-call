#--------#--------#--------#--------#--------#--------
#US election result - Automated call
#Andre Baptista - https://github.com/ABaptista
#--------#--------#--------#--------#--------#--------

import requests, json, time
from twilio.rest import TwilioRestClient

#--------#--------#--------#--------#--------#--------
#https://twilio.com
#Login or create a new account
#You can find your SID and TOKEN in the dashboard
#Create a twilio number and paste it here
#--------#--------#--------#--------#--------#--------

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_NUMBER = "+123"
MY_NUMBER = "+123"

MIN_E_VOTES = 230 #Minimum number of electoral votes to trigger the call
MIN_DIFF = 10 #Mininum difference of electoral votes to trigger the call

INTERVAL = 60 #seconds

URL = "https://spreadsheets.google.com/feeds/list/1NlQyZ83VAKuXvrI6w4AltpDngnvTlAYGvU8gESiLizg/od6/public/values?alt=json"

CLINTON_WINS_XML_URL = "https://pastebin.com/raw/7bda0WR0"
TRUMP_WINS_XML_URL = "https://pastebin.com/raw/yjD2iiPw"

twilioClient = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def getStatus():
    try:
        r = requests.get(URL);
        s = r.text
        obj = json.loads(s)

        entryA = obj["feed"]["entry"][0]
        entryB = obj["feed"]["entry"][1]
        candidateA = entryA["title"]["$t"]
        candidateB = entryB["title"]["$t"]
        contentA = entryA["content"]["$t"]
        contentB = entryB["content"]["$t"]

        cIndexA = contentA.find("colegio")
        eVotesA = contentA[cIndexA+18:]
        cIndexB = contentB.find("colegio")
        eVotesB = contentB[cIndexB+18:]
        return {candidateA: eVotesA, candidateB: eVotesB}
    except:
        return None

def callMe(number, url):
    call = twilioClient.calls.create(url=url, to=number, from_=TWILIO_NUMBER)
    print("Calling")

def main():
    while True:
        try:
            result = getStatus()
            clintonEVotes = int(result["Clinton"])
            trumpEVotes = int(result["Trump"])
            diff = abs(clintonEVotes-trumpEVotes)

            print("Clinton %s, Trump %s" % (clintonEVotes, trumpEVotes))

            if (clintonEVotes >= MIN_E_VOTES and diff >= MIN_DIFF):
                print("Clinton wins")
                callMe(MY_NUMBER, CLINTON_WINS_XML_URL)
                return
            elif (trumpEVotes >= MIN_E_VOTES and diff >= MIN_DIFF):
                print("Trump wins")
                callMe(MY_NUMBER, TRUMP_WINS_XML_URL)
                return
        except:
            pass

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
