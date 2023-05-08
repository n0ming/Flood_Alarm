from twilio.rest import Client
def e_msg() :
	account_sid='AC3977e07cea0.....' #Mosaic processing on the back for security
	auth_token ='c67a7584cdb23.....' #Mosaic processing on the back for security
	client = Client(account_sid, auth_token)
	message = client.messages.create(
		body="report the detection of person at high risk of flooding in SBH_PI [ADDRESS: .....]", #need to add resident's address
		from_='+13184963574', #phone number from twilo
		to ='+82119' #emergency number
	)
